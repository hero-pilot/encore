from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from core.models import Event, Performer, Venue, TicketStatus
from .serializers import EventSerializer, EventReadSerializer, PerformerSerializer, VenueSerializer



class IsAdminorReadPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminorReadPermission]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['performer', 'venue', 'starts_at']
    ordering_fields = ['starts_at', 'title']
    ordering = ['starts_at']  

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventSerializer
        return EventReadSerializer

    def get_queryset(self):
        base_queryset = Event.objects.select_related("venue" , "performer")\
                .annotate(
                    available_tickets=Count(
                        'tickets', 
                        filter=Q(tickets__status=TicketStatus.AVAILABLE)
                    )
                )
        #Only staff users see sold out events
        if self.request.user and self.request.user.is_staff:
            return base_queryset
        
        # Regular users only see events with at least 1 available ticket
        return base_queryset.filter(available_tickets__gt=0)

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAdminorReadPermission]


class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    permission_classes = [IsAdminorReadPermission]
