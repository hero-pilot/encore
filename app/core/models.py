from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required!")
        if not username:
            raise ValueError("Username is required!")
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """Create and return a super user"""
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(unique=True, max_length=250)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

class TicketStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    PURCHASED = "PURCHASED"

class Venue(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    capacity = models.PositiveBigIntegerField()

class Performer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Event(models.Model):
    title = models.CharField(max_length=255)
    venue = models.ForeignKey(Venue, related_name="events", on_delete=models.CASCADE)
    performer = models.ForeignKey(Performer, related_name="events", on_delete=models.CASCADE)
    description = models.TextField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)

class Seat(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="seats")
    row = models.CharField(max_length=10)
    number = models.CharField(max_length=10)
    section = models.CharField(max_length=50, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["venue", "row", "number"], 
                name="unique_seat_placement",                
                violation_error_message="This seat already exists in the venue."
            )
        ]

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="tickets", null=True, blank=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="tickets")
    status = models.CharField(max_length=20, choices=TicketStatus.choices, default=TicketStatus.AVAILABLE)
    price = models.PositiveBigIntegerField()
    purchased_at = models.DateTimeField(null=True, blank=True)
    reserved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "seat"], 
                name="each_seat_one_unique_event",                
                violation_error_message="This seat and event already exist."
            )
        ]
        indexes = [models.Index(fields=['status', 'reserved_at'])]