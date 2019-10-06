from django.test import TestCase
from django.conf import settings
from ..models import Variant, Product, Attribute
from .helpers import generate_random_string, generate_random_number

    
class VariantTests(TestCase):
    def setUp(self):
        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)
        self.product_price = generate_random_number(7, 9)

        self.product_attribute_name = generate_random_string(15, 50) 

    def test_can_create_variant(self):
        """
        Ensure we can create a new variant object.
        """
        product = Product.objects.create(title=self.product_title,
                                         description=self.product_description)
#
        attributes = []
        for i in range(10):
            attributes.append(Attribute.objects.create())

        variant = Variant.objects.create(product=product)
        variant.attributes.set(attributes)

        for i in range(0, 10):
            self.assertTrue(attributes[i].variants.all()[0].name == self.product_attribute_name)
