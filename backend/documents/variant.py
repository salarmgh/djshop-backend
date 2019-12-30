from elasticsearch_dsl import Document, Long, Text, Keyword, Nested, InnerDoc
from anemone.elasticsearch import connections


class VariantDocument(Document):
    name = Text()
    category = Text(fields={'keyword': Keyword()})
    price = Long()
    product = []
    attributes = []
    images = []


    class Index:
        name = 'variants'
        settings = {
          "number_of_shards": 1,
          "number_of_replicas": 0
        }

