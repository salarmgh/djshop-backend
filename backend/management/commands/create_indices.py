from backend.documents.variant import VariantDocument
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Create indices'

    def handle(self, *args, **options):
        VariantDocument.init()

