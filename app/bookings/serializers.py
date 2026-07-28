from rest_framework import serializers
from core.models import Ticket, TicketStatus


class TicketSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()

    def validate_ticket_id(self, value):
        if not Ticket.objects.filter(id=value).exists():
            raise serializers.ValidationError("Ticket does not exist.")
        return value