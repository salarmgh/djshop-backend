from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import re
from django.conf import settings
from ..models import Carousel
from .helpers import generate_random_string, generate_random_number

    
class CarouselTests(TestCase):
    def setUp(self):
        self.image_name = "image.jpg"
        self.title = generate_random_string(15, 50) 
        self.description = generate_random_string(15, 50) 
        self.url = generate_random_string(15, 50) 
        self.image = SimpleUploadedFile(name=self.image_name, content=open('backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')


    def test_can_create_carousel(self):
        """
        Ensure we can create a new carousel object.
        """
        carousel = Carousel.objects.create(title=self.title, description=self.description, url=self.url, image=self.image)

        self.assertEqual(carousel.title, self.title)
        self.assertEqual(carousel.description, self.description)
        self.assertEqual(carousel.url, self.url)

        filename, file_extension = os.path.splitext(self.image_name)
        same_name = re.match(settings.CAROUSEL_IMAGES_DIR + filename + ".*" + file_extension, carousel.image.name)
        self.assertTrue(same_name)

        file_exists = os.path.isfile(settings.MEDIA_DIR + carousel.image.name)
        self.assertTrue(file_exists)
