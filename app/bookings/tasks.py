import stripe
from celery import shared_task
from django.utils import timezone
from core.models import Ticket, TicketStatus
from .models import Payment, PaymentStatus


@shared_task
def expire_reserved_tickets():
    timeout_ago = timezone.now() - timezone.timedelta(minutes=15)
    expired_ids = list(
        Ticket.objects.filter(
            status=TicketStatus.RESERVED, reserved_at__lte=timeout_ago
        ).values_list("id", flat=True)
    )

    updated = Ticket.objects.filter(id__in=expired_ids, status=TicketStatus.RESERVED)\
        .update(status=TicketStatus.AVAILABLE, reserved_at=None)

    pending = list(Payment.objects.filter(ticket_id__in=expired_ids, status=PaymentStatus.PENDING))
    for payment in pending:
        try:
            stripe.PaymentIntent.cancel(payment.stripe_payment_intent_id)
            payment.status = PaymentStatus.FAILED
        except stripe.error.InvalidRequestError:
            pass  # already succeeded — the webhook's refund path will catch it
        
    Payment.objects.bulk_update(pending, ["status"])

    return f"Expired {updated} reservations"

