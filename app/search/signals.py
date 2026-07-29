from django.db.models.signals import post_save, post_delete
from django_elasticsearch_dsl.signals import BaseSignalProcessor
from django_elasticsearch_dsl.registries import registry
from .tasks import update_elasticsearch_document, delete_elasticsearch_document

class CelerySignalProcessor(BaseSignalProcessor):
    """
    Overrides the default synchronous signal processor 
    to dispatch Elasticsearch updates to Celery.
    """
    def setup(self):
        post_save.connect(self.handle_save)
        post_delete.connect(self.handle_delete)

    def teardown(self):
        post_save.disconnect(self.handle_save)
        post_delete.disconnect(self.handle_delete)

    def handle_save(self, sender, instance, **kwargs):
        # Ensure we only trigger tasks for models we track in Elasticsearch
        if sender in registry.get_models():
            update_elasticsearch_document.delay(
                instance._meta.app_label, 
                instance._meta.model_name, 
                instance.pk
            )

    def handle_delete(self, sender, instance, **kwargs):
        if sender in registry.get_models():
            delete_elasticsearch_document.delay(
                instance._meta.app_label, 
                instance._meta.model_name, 
                instance.pk
            )