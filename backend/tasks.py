from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .documents.variant import VariantDocument
from elasticsearch.helpers import bulk
from anemone.elasticsearch import connections


@shared_task(bind=True, max_retries=600)
def variant_model_indexer(self, model):
    variant = VariantDocument(meta={'id': model["id"]}, name=model["name"], price=model["price"],
                              product=model["product"], images=model["images"], attributes=model["attributes"], category=model["category"])
    try:
        variant.save()
    except Exception as e:
        self.retry(countdown=30, exc=e)
    return model


@shared_task(bind=True, max_retries=600)
def variant_bulk_indexer(self):
    from .models import Variant
    bulk(client=connections.get_connection(), actions=(b.indexing()
                                                       for b in Variant.objects.all().iterator()))


@shared_task(bind=True, max_retries=600)
def product_model_indexer(self, variants):
    for variant in variants:
        document = VariantDocument(meta={'id': variant["id"]}, name=variant["name"], price=variant["price"],
                                   product=variant["product"], images=variant["images"], attributes=variant["attributes"], category=variant["category"])
        try:
            document.save()
        except Exception as e:
            self.retry(countdown=30, exc=e)
    return variants
