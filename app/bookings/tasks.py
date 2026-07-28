from celery import shared_task
from django.utils import timezone
from core.models import Ticket, TicketStatus

@shared_task
def expire_reserved_tickets():
    timeout_ago = timezone.now() - timezone.timedelta(minutes=15)
    updated = Ticket.objects.filter(
        status=TicketStatus.RESERVED,
        reserved_at__lte=timeout_ago
    ).update(status= TicketStatus.AVAILABLE, reserved_at=None)
    return f'Expired {updated} reservations'