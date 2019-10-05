from django.test import TestCase
from django.conf import settings
from ..models import Order
from .helpers import generate_random_string, generate_random_number

    
class OrderTests(TestCase):
    def test_can_create_order(self):
        """
        Ensure we can create a new order object.
        """
        pass
