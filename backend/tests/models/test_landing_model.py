from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import re
from django.conf import settings
from ...models import LandingBanner
from ..helpers import generate_random_string, generate_random_number, check_file_exists_on_model, check_filename_is_same_on_model 
import shutil

    
class LandingBannerTests(TestCase):
    def setUp(self):
        self.image_name = generate_random_string(3, 5) + '.jpg'
        self.title = generate_random_string(15, 50) 
        self.description = generate_random_string(15, 50) 
        self.url = generate_random_string(15, 50) 
        self.image = SimpleUploadedFile(name=self.image_name, content=open('backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')
        self.landing = LandingBanner.objects.create(title=self.title, description=self.description, url=self.url, image=self.image)


    def test_can_create_landing(self):
        """
        Ensure we can create a new landing object.
        """

        self.assertEqual(self.landing.title, self.title)
        self.assertEqual(self.landing.description, self.description)
        self.assertEqual(self.landing.url, self.url)

    def test_is_filename_same_on_model(self):
        """
        Ensure filename is same on the model as we want
        """
        self.assertTrue(check_filename_is_same_on_model(self.landing, settings.LANDING_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))
    
    def test_is_file_exists_on_model(self):
        """
        Ensure file is present on the file system
        """
        self.assertTrue(check_file_exists_on_model(self.landing, settings.LANDING_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def test_can_delete_image(self):
        """
        Ensure we can delete a image object with the file.
        """
        self.landing.delete()
        self.assertFalse(check_file_exists_on_model(self.landing, settings.LANDING_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_DIR)


