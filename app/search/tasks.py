from celery import shared_task
from django.apps import apps
from django_elasticsearch_dsl.registries import registry

@shared_task
def update_elasticsearch_document(app_label, model_name, pk):
    """Background task to update or create a document in Elasticsearch"""
    model = apps.get_model(app_label, model_name)
    try:
        instance = model.objects.get(pk=pk)
        registry.update(instance)
    except model.DoesNotExist:
        pass

@shared_task
def delete_elasticsearch_document(app_label, model_name, pk):
    """Background task to remove a document from Elasticsearch"""
    model = apps.get_model(app_label, model_name)
    # We create a dummy instance because the real one is already deleted from the DB
    instance = model(pk=pk)
    registry.delete(instance)