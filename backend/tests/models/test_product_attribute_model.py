from django.test import TestCase
from ...models import Product, Attribute
from ..helpers import generate_random_string, generate_random_number

    
class AttributesTests(TestCase):
    def setUp(self):
        self.product_attribute_name = generate_random_string(15, 50) 

        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)


    def test_can_create__attribute(self):
        """
        Ensure we can create a new attribute object.
        """
        product_attribute = Attribute.objects.create(name=self.product_attribute_name)

        self.assertEqual(product_attribute.name, self.product_attribute_name)

