from django.test import TestCase
from django.conf import settings
from ...models import Order, Variant, User, Product, Cart
from ..helpers import generate_random_string, generate_random_number

    
class OrderTests(TestCase):
    def setUp(self):
        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)
        self.product_price = generate_random_number(7, 9)

        self.variant_name = generate_random_string(15, 50) 

        self.count = generate_random_number(1, 2)

        self.username = "sampleuser"
        self.password = "securepassword"
        self.number = "09" + generate_random_number(9, 9)
               

    def test_can_create_order(self):
        """
        Ensure we can create a new order object.
        """
        product = Product.objects.create(title=self.product_title,
                                         description=self.product_description)

        variant = Variant.objects.create(product=product, name=self.variant_name)

        user = User(username=self.username, number=self.number)
        user.set_password(self.password)
        user.save()

        cart = Cart.objects.create(user=user)

        order = Order.objects.create(variant=variant, count=self.count, user=user, cart=cart)

        self.assertEqual(variant.orders.all()[0].id, order.id)
        self.assertEqual(user.orders.all()[0].id, order.id)
        self.assertEqual(order.count, self.count)
