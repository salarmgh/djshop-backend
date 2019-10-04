from django.test import TestCase
from ..models import ProductAttribute, ProductAttributeValue
from .helpers import generate_random_string, generate_random_number

    
class ProductsAttributesTests(TestCase):
    def setUp(self):
        self.product_attribute_value = generate_random_string(15, 50) 
        self.product_attribute_price = generate_random_number(6, 8) 

        self.product_attribute_name = generate_random_string(15, 50) 

    def test_can_create_products_attribute(self):
        """
        Ensure we can create a new product attribute value object.
        """
        attribute = ProductAttribute.objects.create(name=self.product_attribute_name)

        product_attribute_value = ProductAttributeValue.objects.create(value=self.product_attribute_value, price=self.product_attribute_price, attribute=attribute)

        self.assertTrue(attribute.attributes.all()[0].value == self.product_attribute_value)

        self.assertEqual(product_attribute_value.value, self.product_attribute_value)


