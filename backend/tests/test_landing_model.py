from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import re
from django.conf import settings
from ..models import LandingBanner
from .helpers import generate_random_string, generate_random_number

    
class LandingBannerTests(TestCase):
    def setUp(self):
        self.image_name = "image.jpg"
        self.title = generate_random_string(15, 50) 
        self.description = generate_random_string(15, 50) 
        self.url = generate_random_string(15, 50) 
        self.image = SimpleUploadedFile(name=self.image_name, content=open('backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')


    def test_can_create_landing(self):
        """
        Ensure we can create a new landing object.
        """
        landing = LandingBanner.objects.create(title=self.title, description=self.description, url=self.url, image=self.image)

        self.assertEqual(landing.title, self.title)
        self.assertEqual(landing.description, self.description)
        self.assertEqual(landing.url, self.url)

        filename, file_extension = os.path.splitext(self.image_name)
        same_name = re.match(settings.LANDING_IMAGES_DIR + filename + ".*" + file_extension, landing.image.name)
        self.assertTrue(same_name)

        file_exists = os.path.isfile(settings.MEDIA_DIR + landing.image.name)
        self.assertTrue(file_exists)


