from django.db import models
from core.models import Ticket


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class Payment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="payments")
    user_id = models.PositiveIntegerField()
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
    amount = models.PositiveBigIntegerField() 
    currency = models.CharField(max_length=3, default="usd")
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ticket"],
                condition=models.Q(status="pending"),
                name="unique_pending_payment_per_ticket",
            )
        ]