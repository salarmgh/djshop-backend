from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from ..models import Product, Image
from .helpers import generate_random_string, generate_random_number, check_file_exists_on_model, check_filename_is_same_on_model

    
class ImageTests(TestCase):
    def setUp(self):
        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)
        self.product = Product.objects.create(title=self.product_title,
                                         description=self.product_description)

        self.image_title = generate_random_string(15, 250)
        self.image_main = True
        self.image_name = generate_random_string(3, 5) + '.jpg'
        self.image_file = SimpleUploadedFile(name=self.image_name, content=open('backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')
        self.image = Image.objects.create(title=self.image_title, product=self.product, main=self.image_main, image=self.image_file)


    def test_can_create_image(self):
        """
        Ensure we can create a new Image object.
        """
        self.assertEqual(self.image.title, self.image_title)
        self.assertEqual(self.image.main, self.image_main)
        
    def test_is_filename_same_on_model(self):
        """
        Ensure filename is same on the model as we want
        """
        self.assertTrue(check_filename_is_same_on_model(self.image, settings.PRODUCT_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))
    
    def test_is_file_exists_on_model(self):
        """
        Ensure file is present on the file system
        """
        self.assertTrue(check_file_exists_on_model(self.image, settings.PRODUCT_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def test_can_delete_image(self):
        """
        Ensure we can delete a image object with the file.
        """
        self.image.delete()
        self.assertFalse(check_file_exists_on_model(self.image, settings.PRODUCT_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))
