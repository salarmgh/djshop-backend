from datetime import datetime
from elasticsearch_dsl import Document, Integer, Text, InnerDoc, Boolean, Nested
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['elasticsearch'])


class AttributeValueIndex(InnerDoc):
    value = Text()

class AttributeIndex(InnerDoc):
    name = Text()
    attribute_value = Nested(AttributeValueIndex)


class ProductIndex(InnerDoc):
    title = Text()
    slug = Text()
    featured = Boolean()
    image = Text()


class VariantIndex(Document):
    name = Text()
    attributes = Nested(AttributeIndex)
    product = Nested(ProductIndex)
    price = Integer()

    class Index:
        name = 'variants'
        settings = {
          "number_of_shards": 1,
          "number_of_replicas": 0,
        }

#    def save(self, **kwargs):
#        self.lines = len(self.body.split())
#        return super(Variant, self).save(**kwargs)


VariantIndex.init()
