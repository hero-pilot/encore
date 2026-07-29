from django.urls import path
from .views import TicketBookingView, CreatePaymentIntentView, StripeWebhookView

urlpatterns = [
    path("book/" , view= TicketBookingView.as_view() , name="book=ticket"),
    path("tickets/<int:ticket_id>/pay/", CreatePaymentIntentView.as_view()),
    path("webhooks/stripe/", StripeWebhookView.as_view()),
]