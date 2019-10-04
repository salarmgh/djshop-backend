from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import re
import os
from ..models import Product, Image
from .helpers import generate_random_string, generate_random_number

    
class ImageTests(TestCase):
    def setUp(self):
        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)
        self.product_price = generate_random_number(6, 8)
        self.image_title = generate_random_string(15, 250)
        self.image_main = True
        self.image_name='image.jpg'
        self.image = SimpleUploadedFile(name=self.image_name, content=open('backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')


    def test_can_create_Image(self):
        """
        Ensure we can create a new Image object.
        """
        product = Product.objects.create(title=self.product_title, description=self.product_description, price=self.product_price)

        image = Image.objects.create(title=self.image_title, product=product, main=self.image_main, image=self.image)

        saved_product = Product.objects.get(pk=product.id)
        saved_image = Image.objects.get(pk=image.id)

        self.assertEqual(saved_image.title, self.image_title)
        self.assertEqual(saved_image.main, self.image_main)

        filename, file_extension = os.path.splitext(self.image_name)
        same_name = re.match(settings.PRODUCT_IMAGES_DIR + filename + ".*" + file_extension, saved_image.image.name)
        self.assertTrue(same_name)

        file_exists = os.path.isfile(settings.MEDIA_DIR + saved_image.image.name)
        self.assertTrue(file_exists)
