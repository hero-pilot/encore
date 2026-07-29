from rest_framework import serializers

class EventDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    starts_at = serializers.DateTimeField(read_only=True)
    ends_at = serializers.DateTimeField(read_only=True, allow_null=True)
    performer_name = serializers.CharField(read_only=True)
    venue_location = serializers.CharField(read_only=True)
    venue_id = serializers.IntegerField(read_only=True)