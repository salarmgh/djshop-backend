from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .documents.variant import VariantDocument, AttributeDocument


@shared_task(bind=True, max_retries=600)
def variant_model_indexer(self, model):
    variant = VariantDocument(meta={'id': model["id"]}, name=model["name"], price=model["price"], product=model["product"], images=model["images"])
    for attribute in model["attributes"]:
        variant.add_attribute(attribute["name"], attribute["value"])
    try:
        variant.save()
    except Exception as e:
        self.retry(countdown=30, exc=e)
    return model
