from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from ...models import Product, Image
from ..helpers import generate_random_string, generate_random_number, check_file_exists_on_model, check_filename_is_same_on_model
import shutil
from backend.test.utils.category import create_product


class ImageTests(TestCase):
    def setUp(self):
        self.image_title = "image title"
        self.image_name = 'image_test.jpg'
        self.image_file = SimpleUploadedFile(name=self.image_name, content=open(
            'backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')
        self.image = Image.objects.create(
            title=self.image_title, image=self.image_file)

    def test_can_create_image(self):
        """
        Ensure we can create a new Image object.
        """
        self.assertEqual(self.image.title, self.image_title)

    def test_is_filename_same_on_model(self):
        """
        Ensure filename is same on the model as we want
        """
        self.assertTrue(check_filename_is_same_on_model(
            self.image, settings.PRODUCT_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def test_is_file_exists_on_model(self):
        """
        Ensure file is present on the file system
        """
        self.assertTrue(check_file_exists_on_model(
            self.image, settings.PRODUCT_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def test_can_delete_image(self):
        """
        Ensure we can delete a image object with the file.
        """
        self.image.delete()
        self.assertFalse(check_file_exists_on_model(
            self.image, settings.PRODUCT_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_DIR)
