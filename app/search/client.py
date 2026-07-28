from elasticsearch import Elasticsearch
from django.conf import settings

client = Elasticsearch(settings.ELASTICSEARCH_HOST)