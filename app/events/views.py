from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from core.models import Event
from .serializers import EventSerializer, EventReadSerializer



class IsAdminorReadPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("venue" , "performer").annotate(
        db_available_tickets=Count(
            'tickets', 
            filter=Q(tickets__status="AVAILABLE")
        )
    ).all()
    permission_classes = [IsAdminorReadPermission]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['performer', 'venue', 'starts_at']
    ordering_fields = ['starts_at', 'title']
    ordering = ['starts_at']  

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventSerializer
        return EventReadSerializer


