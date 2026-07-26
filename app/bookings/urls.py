from django.urls import path
from .views import TicketBookingView

urlpatterns = [
    path("book/" , view= TicketBookingView.as_view() , name="book=ticket"),
]