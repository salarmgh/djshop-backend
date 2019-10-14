from datetime import datetime
from elasticsearch_dsl import Document, Integer, Text, InnerDoc, Boolean, Nested
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['elasticsearch'])


class AttributeValueIndex(InnerDoc):
    value = Text()

class AttributeIndex(Document):
    name = Text()
    attribute_value = Nested(AttributeValueIndex)

    class Index:
        name = 'attributes'


class ProductIndex(Document):
    title = Text()
    slug = Text()
    featured = Boolean()
    image = Text()

    class Index:
        name = 'products'


class VariantIndex(Document):
    name = Text()
    attributes = Integer()
    product = Integer()
    price = Integer()

    class Index:
        name = 'variants'


AttributeIndex.init()
ProductIndex.init()
VariantIndex.init()
