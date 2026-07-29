import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Payment, PaymentStatus
from .serializers import TicketSerializer
from core.models import Ticket, TicketStatus


stripe.api_key = settings.STRIPE_SECRET_KEY



class TicketBookingView(APIView):
    def post(self, request):
        serializer = TicketSerializer(data = request.data)

        serializer.is_valid(raise_exception=True)

        ticket_id = serializer.validated_data["ticket_id"]
        user_id = request.user.id
        updated_rows = Ticket.objects.filter(
            id=ticket_id,
            status=TicketStatus.AVAILABLE  
        ).update(
            user=user_id,
            status=TicketStatus.RESERVED,
            reserved_at=timezone.now()
        )

        
        if updated_rows == 0:
            return Response(
                {"error": "Ticket is no longer available."},
                status=409  
            )

        return Response({"status": "reserved"}, status=200)




class CreatePaymentIntentView(APIView):
    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found."}, status=404)

        if ticket.status != TicketStatus.RESERVED or ticket.user_id != request.user.id:
            return Response({"error": "Ticket is not reserved by you."}, status=409)

        # belt-and-suspenders: the sweep task runs every 5 min, so there's a gap
        # where a reservation is technically stale but hasn't been flipped back yet
        if ticket.reserved_at < timezone.now() - timezone.timedelta(minutes=15):
            return Response({"error": "Reservation expired."}, status=409)

        existing = Payment.objects.filter(ticket=ticket, status=PaymentStatus.PENDING).first()

        if existing:
            intent = stripe.PaymentIntent.retrieve(existing.stripe_payment_intent_id)
        else:
            intent = stripe.PaymentIntent.create(
                amount=ticket.price,     
                currency="usd",
                metadata={"ticket_id": str(ticket.id), "user_id": str(request.user.id)},
            )
            Payment.objects.create(
                ticket=ticket,
                user_id=request.user.id,
                stripe_payment_intent_id=intent.id,
                amount=ticket.price,
                status=PaymentStatus.PENDING,
            )

        return Response({"client_secret": intent.client_secret})




@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except (ValueError, stripe.error.SignatureVerificationError):
            return HttpResponse(status=400)

        intent = event["data"]["object"]

        if event["type"] == "payment_intent.succeeded":
            self._handle_success(intent)
        elif event["type"] == "payment_intent.payment_failed":
            Payment.objects.filter(stripe_payment_intent_id=intent["id"]).update(status=PaymentStatus.FAILED)

        return HttpResponse(status=200)

    def _handle_success(self, intent):
        try:
            payment = Payment.objects.select_related("ticket").get(stripe_payment_intent_id=intent["id"])
        except Payment.DoesNotExist:
            return

        updated = Ticket.objects.filter(
            id=payment.ticket_id,
            status=TicketStatus.RESERVED,
            user=payment.user_id,
        ).update(status=TicketStatus.SOLD)

        if updated:
            payment.status = PaymentStatus.SUCCEEDED
        else:
            # reservation was already released before the webhook arrived — refund
            stripe.Refund.create(payment_intent=intent["id"])
            payment.status = PaymentStatus.REFUNDED
        payment.save(update_fields=["status", "updated_at"])