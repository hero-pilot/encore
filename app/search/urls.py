from django.urls import path
from .views import EventSearchView

urlpatterns = [
    path("events/", EventSearchView.as_view(), name='event-search'),
]