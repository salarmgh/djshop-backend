from django.test import TestCase
from django.core.exceptions import ValidationError
from ...models import User
from ..helpers import generate_random_number, generate_random_string, generate_random_string_with_numbers

    
class UserTests(TestCase):
    def setUp(self):
        self.username = "sampleuser"
        self.password = "securepassword"
        self.valid_number = "09" + generate_random_number(9, 9)
        self.invalid_number_with_more_length = generate_random_number(10, 20)
        self.invalid_number_with_less_length = "09" + generate_random_number(1, 8)
        self.invalid_number_with_char = "09" + generate_random_string_with_numbers(9, 9)

    def _create_user(self, username, password, number):
        user = User(username=username, number=number)
        user.set_password(password)

        return user

    def test_can_create_account_with_number(self):
        """
        Ensure we can create a new user object.
        """

        user = self._create_user(self.username, self.password, self.valid_number)
        user.save()

        saved_user = User.objects.get(username=self.username)

        self.assertEqual(saved_user.number, self.valid_number)
    
    def test_can_create_account_with_invalid_number_with_more_length(self):
        """
        Ensure we can't create a new user object with more length number.
        """
        user = self._create_user(self.username, self.password, self.invalid_number_with_more_length)
        with self.assertRaises(ValidationError):
            user.save()

    def test_can_create_account_with_invalid_number_with_less_length(self):
        """
        Ensure we can't create a new user object with less length number.
        """
        user = self._create_user(self.username, self.password, self.invalid_number_with_less_length)
        with self.assertRaises(ValidationError):
            user.save()

    def test_can_create_account_with_invalid_number_with_char(self):
        """
        Ensure we can't create a new user object with char inside number.
        """
        user = self._create_user(self.username, self.password, self.invalid_number_with_char)
        with self.assertRaises(ValidationError):
            user.save()
