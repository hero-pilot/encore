from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from core.models import Event, Performer, Venue

@registry.register_document
class EventDocument(Document):
    performer_name = fields.TextField(attr='performer.name')
    venue_location = fields.TextField(attr='venue.location')
    venue_id = fields.IntegerField(attr='venue.id')
    
    class Index:
        name = 'events'  
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Event 
        fields = [
            'id',
            'title',
            'description',
            'starts_at',
            'ends_at',
        ]

        related_models = [Performer, Venue]

    def get_queryset(self):
        return super().get_queryset().select_related('performer', 'venue')