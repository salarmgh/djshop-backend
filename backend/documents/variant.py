from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from backend.models import Variant


VARIANT_INDEX = Index('variants')
VARIANT_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@VARIANT_INDEX.doc_type
class VariantDocument(Document):
    """Variant Elasticsearch document."""

    id = fields.IntegerField(attr='id')

    name = fields.TextField(fields={
        'raw': fields.KeywordField()
    }, fielddata=False)

    price = fields.IntegerField(attr='price')

    class Django(object):
        model = Variant
