from django.core.management.base import BaseCommand, CommandError
from backend.models import Variant, Product, Attribute


from backend.tasks import variant_bulk_indexer

class Command(BaseCommand):
    help = 'Index db to elasticsearch'

    def handle(self, *args, **options):
        variant_bulk_indexer.delay()
