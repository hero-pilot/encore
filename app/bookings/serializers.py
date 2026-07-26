from django.conf import settings
from rest_framework import serializers
from core.models import Ticket, TicketStatus


class TicketSerialzier(serializers.Serializer):
    ticket_id = serializers.IntegerField()

    def validate_ticket_id(self, value):
        try:
            ticket = Ticket.objects.get(id =value , status = TicketStatus.AVAILABLE)

        except Ticket.DoesNotExist:
            raise serializers.ValidationError("Ticket Does not exist or is already sold.")
        if settings.REDIS_BOOKING_CLIENT.exists(f"token:{value}"):
            raise serializers.ValidationError("Token is currently reserved by another user.")

        self.context["ticket_id"] = value
        return value
        