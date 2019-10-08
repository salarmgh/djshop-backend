from django.test import TestCase
from ...models import User
from ..helpers import generate_random_string, generate_random_number

    
class AttributesTests(TestCase):
    def setUp(self):
        self.username = "sampleuser"
        self.password = "securepassword"


    def test_can_create__attribute(self):
        """
        Ensure we can create a new attribute object.
        """
        product_attribute = Attribute.objects.create(name=self.product_attribute_name)

        self.assertEqual(product_attribute.name, self.product_attribute_name)


