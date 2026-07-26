from rest_framework import serializers
from core.models import Event, Performer, Venue, Ticket


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = ["id", "name", "description"]
        #read_only_fields =["id"] modelserializer automatically makes primary keys readonly

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name", "location", "capacity"]

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ["id", "title", "venue", "performer","description", "starts_at", "ends_at"]


class EventReadSerializer(EventSerializer):
    performer = PerformerSerializer(read_only = True)
    venue = VenueSerializer(read_only = True)
    available_tickets = serializers.SerializerMethodField()

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + ["available_tickets"]

    def get_available_tickets(self, obj):
        db_available = getattr(obj, 'tickets')
        return db_available



