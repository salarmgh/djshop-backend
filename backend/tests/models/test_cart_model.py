from django.test import TestCase
from utils.user import create_user


class CartTests(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_can_create_order(self):
        """
        Ensure we can create a new order object.
        """
        cart = Cart.objects.create(user=self.user)

        self.assertEqual(user.carts.all()[0].id, cart.id)
