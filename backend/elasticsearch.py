from django.conf import settings
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Boolean
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models



connections.create_connection(
    hosts=settings.ES_CONNECTIONS
)


class ProductIndex(DocType):
    title = Text()
    description = Text()
    created_at = Date()
    features = Boolean()
    image = Text()

    class Meta:
        index = 'products'
#
#
#def product_bulk_indexing():
#    ProductIndex.init()
#    es = Elasticsearch()
#    bulk(client=es, actions=(b.indexing() for b in models.Product.objects.all().iterator()))
