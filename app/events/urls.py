from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, PerformerViewSet, VenueViewSet

router = DefaultRouter()
router.register("events", EventViewSet, basename="event")
router.register("performers", PerformerViewSet, basename="performer")
router.register("venues", VenueViewSet, basename="venue")

urlpatterns = [
    path("", include(router.urls)),  
]