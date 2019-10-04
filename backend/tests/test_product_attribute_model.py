from django.test import TestCase
from ..models import Product, ProductAttribute
from .helpers import generate_random_string, generate_random_number

    
class ProductsAttributesTests(TestCase):
    def setUp(self):
        self.product_attribute_name = generate_random_string(15, 50) 

        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)
        self.product_price = generate_random_number(7, 9)


    def test_can_create_products_attribute(self):
        """
        Ensure we can create a new product attribute object.
        """
        products = []
        for i in range(0, 10):
            products.append(Product.objects.create(title=self.product_title, description=self.product_description, price=self.product_price))

        product_attribute = ProductAttribute.objects.create(name=self.product_attribute_name)
        product_attribute.products.set(products)
        product_attribute.save()

        for i in range(0, 10):
            self.assertTrue(products[i].attributes.all()[0].name == self.product_attribute_name)

        self.assertEqual(product_attribute.name, self.product_attribute_name)

