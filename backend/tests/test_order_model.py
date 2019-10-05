from django.test import TestCase
from django.conf import settings
from ..models import Product, ProductAttribute, ProductAttributeValue, Order
from .helpers import generate_random_string, generate_random_number

    
class OrderTests(TestCase):
    def setUp(self):
        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)
        self.product_price = 1000

        self.product_attribute_value = generate_random_string(15, 50) 
        self.product_attribute_price = 10

        self.product_attribute_name = generate_random_string(15, 50) 

        self.order_count = generate_random_number(1, 3)


    def test_can_create_order(self):
        """
        Ensure we can create a new order object.
        """
        product = Product.objects.create(title=self.product_title, description=self.product_description, price=self.product_price)

        product_attribute = ProductAttribute.objects.create(name=self.product_attribute_name)
        attributes = []
        total_price = int(product.price)
        for i in range(0, 10):
            attributes.append(ProductAttributeValue.objects.create(value=self.product_attribute_value, price=self.product_attribute_price, attribute=product_attribute))
            total_price = total_price + int(self.product_attribute_price)

        order = Order.objects.create(product=product, count=self.order_count)
        order.attributes.set(attributes)
        order.save()
        self.assertEqual(order.price, total_price)
