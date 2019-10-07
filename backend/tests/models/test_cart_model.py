from django.test import TestCase
from ...models import User, Cart
from ..helpers import generate_random_string, generate_random_number

    
class CartTests(TestCase):
    def setUp(self):
        self.count = generate_random_number(1, 2)

        self.username = "sampleuser"
        self.password = "securepassword"
        self.number = "09" + generate_random_number(9, 9)
               

    def test_can_create_order(self):
        """
        Ensure we can create a new order object.
        """
        user = User(username=self.username, number=self.number)
        user.set_password(self.password)
        user.save()

        cart = Cart.objects.create(user=user)

        self.assertEqual(user.carts.all()[0].id, cart.id)

