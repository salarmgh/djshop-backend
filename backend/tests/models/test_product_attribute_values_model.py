from django.test import TestCase
from ...models import Attribute, AttributeValue
from ..helpers import generate_random_string, generate_random_number

    
class ProductsAttributeValuesTests(TestCase):
    def setUp(self):
        self.product_attribute_value = generate_random_string(15, 50) 

        self.product_attribute_name = generate_random_string(15, 50) 

    def test_can_create_products_attribute_value(self):
        """
        Ensure we can create a new product attribute value object.
        """
        attribute = Attribute.objects.create(name=self.product_attribute_name)

        product_attribute_value = AttributeValue.objects.create(value=self.product_attribute_value, attribute=attribute)

        self.assertEqual(attribute.attributes.all()[0].value, self.product_attribute_value)

        self.assertEqual(product_attribute_value.value, self.product_attribute_value)


