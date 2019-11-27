from elasticsearch_dsl import Document, InnerDoc, Nested, Long, Text
from anemone.elasticsearch import connections

class AttributeDocument(InnerDoc):
    name = Text()
    value = Text()


class VariantDocument(Document):
    name = Text()
    price = Long()
    product = []
    attributes = Nested(AttributeDocument)
    images = []

    def add_attribute(self, name, value):
        self.attributes.append(AttributeDocument(name=name, value=value))

    class Index:
        name = 'variants'
        settings = {
          "number_of_shards": 1,
          "number_of_replicas": 0
        }

VariantDocument.init()
