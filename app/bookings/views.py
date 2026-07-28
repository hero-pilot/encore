from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .serializers import TicketSerializer
from core.models import Ticket, TicketStatus
from django.conf import settings


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


