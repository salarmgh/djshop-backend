from django.test import TestCase
from ...models import User, Address
from ..helpers import generate_random_string

    
class AddressTests(TestCase):
    def setUp(self):
        user = User(username="sampleuser", number="09124887219", email="asfdasdf@gmail.com")
        user.set_password("securepassword")
        user.save()
        self.user = user

    def test_can_create_address_with_user(self):
        """
        Ensure we can create multiple new address object.
        """
        addresses = []
        for i in range(0, 10):
            addresses.append(generate_random_string(10, 300))
            Address.objects.create(location=addresses[i], user=self.user)

        for i in range(0, 10):
            user = User.objects.get(pk=self.user.id)
            user_address = user.addresses.all()[i]
            self.assertEqual(user_address.location, addresses[i])
