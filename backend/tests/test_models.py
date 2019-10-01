from django.test import TestCase
from django.contrib.auth.hashers import check_password
from ..models import User


class UserTests(TestCase):
    def setUp(self):
        self.username = "sample_user"
        self.password = "secure_Password"
        self.number = "+989124887218"

    def test_can_create_account_with_number(self):
        """
        Ensure we can create a new account object.
        """

        user = User(username=self.username, number=self.number)
        user.set_password(self.password)
        user.save()

        saved_user = User.objects.get(username=self.username)

        self.assertEqual(saved_user.username, self.username)
        self.assertTrue(check_password(self.password, saved_user.password))
        self.assertEqual(saved_user.number, self.number)

class AddressTests(TestCase):
    def setUp(self):
        self.location = "Tehran, Iran, Folan ja, Bahman kooche, 24 Pelak, 224 Vahed"
        self.addresses = 
