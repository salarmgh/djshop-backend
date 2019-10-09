from django.test import TestCase
from django.contrib.auth.hashers import make_password
from ...serializers import UserSerializer
from ..helpers import generate_random_string, generate_random_number

    
class UserSerializerTests(TestCase):
    def setUp(self):
        self.user = {"username": "sampleuser", "password": "securepassword", "number": "09124887219", "password": "jkasfhdhjasfd82934nuhfds"}


    def test_can_make_correct_password_with_serializer(self):
        """
        Ensure we make correct password with django hash function
        """
        serialized_user = UserSerializer(data=self.user)
        self.assertTrue(serialized_user.is_valid())
        serialized_user.save()
        self.assertNotEqual(serialized_user.data["password"], self.user["password"])

