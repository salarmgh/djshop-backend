from django.test import TestCase
from django.conf import settings
from ...models import Order, Variant, User, Product, Cart, Address
from ..helpers import generate_random_string, generate_random_number
from backend.tests.utils.category import create_product


class OrderTests(TestCase):
    def setUp(self):
        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)
        self.product_price = generate_random_number(7, 9)

        self.variant_name = "Test variant"

        self.count = generate_random_number(1, 2)

        self.username = "sampleuser"
        self.password = "securepassword"
        self.email = "asdfasdf@gmail.com"
        self.number = "09" + generate_random_number(9, 9)

    def test_can_create_order(self):
        """
        Ensure we can create a new order object.
        """
        product = create_product()

        variant = Variant.objects.create(
            product=product, name=self.variant_name, weight=20)

        user = User(username=self.username,
                    number=self.number, email=self.email)
        user.set_password(self.password)
        user.save()

        address = Address.objects.create(
            location="folan bisar bahman - 12", user=user)
        cart = Cart.objects.create(user=user, address=address)

        order = Order.objects.create(
            variant=variant, count=self.count, user=user, cart=cart)

        self.assertEqual(variant.orders.all()[0].id, order.id)
        self.assertEqual(user.orders.all()[0].id, order.id)
        self.assertEqual(order.count, self.count)
