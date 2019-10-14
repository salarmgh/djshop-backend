from django.core.management.base import BaseCommand, CommandError
from backend.models import Variant, Product, Attribute
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from ...tests.helpers import generate_random_string, generate_random_number


class Command(BaseCommand):
    help = 'Index db to elasticsearch'

    def handle(self, *args, **options):
        es = Elasticsearch(["elasticsearch"])
        bulk(client=es, actions=(b.indexing() for b in Variant.objects.all().iterator()))
