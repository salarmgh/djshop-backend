from datetime import datetime
from elasticsearch_dsl import Document, Integer, Text, InnerDoc, Boolean, Nested
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['elasticsearch'])


class AttributeIndex(InnerDoc):
    name = Text()
    value = Text()

    class Index:
        name = 'attributes'


class VariantIndex(Document):
    attributes = Nested(AttributeIndex)
    url = Text()
    featured = Boolean()
    product = Integer()
    price = Integer()
    image = Text()

    class Index:
        name = 'variants'


VariantIndex.init()
