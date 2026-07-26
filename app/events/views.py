from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from core.models import Event, Performer, Venue
from .serializers import EventSerializer, EventReadSerializer, PerformerSerializer, VenueSerializer



class IsAdminorReadPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("venue" , "performer").filter(tickets__status="AVAILABLE")
    permission_classes = [IsAdminorReadPermission]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['performer', 'venue', 'starts_at']
    ordering_fields = ['starts_at', 'title']
    ordering = ['starts_at']  

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventSerializer
        return EventReadSerializer


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAdminorReadPermission]


class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    permission_classes = [IsAdminorReadPermission]
