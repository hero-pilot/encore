from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TicketSerializer
from django.conf import settings

r = settings.REDIS_BOOKING_CLIENT
TICKET_TTL = 600

class TicketBookingView(APIView):
    def post(self, request):
        serializer = TicketSerializer(data = request.data)

        serializer.is_valid(raise_exception=True)

        ticket_id = serializer.validated_data["ticket_id"]
        user_id = request.user.id

        was_set = r.setnx(f"ticket:{ticket_id}",  user_id)
        if was_set:
            r.expire(f'ticket:{ticket_id}', TICKET_TTL)
            return Response({"status": "reserved"}, status=200)
        return Response({"status": "Already reserved"}, status=409)


