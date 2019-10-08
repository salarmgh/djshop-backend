from django.test import TestCase
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import re
from django.conf import settings
from ...models import Product, Category, Attribute
from ..helpers import generate_random_string, generate_random_number, check_file_exists_on_model, check_filename_is_same_on_model
import shutil

    
class CategoryTests(TestCase):
    def setUp(self):
        self.category_name = generate_random_string(15, 50) 
        self.image_name = generate_random_string(3, 5) + '.jpg'
        self.image_file = SimpleUploadedFile(name=self.image_name, content=open('backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')

        self.product_attribute_name = generate_random_string(15, 50) 

        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)

        self.products = []
        for i in range(0, 10):
            self.products.append(Product.objects.create(title=self.product_title, description=self.product_description))

        self.attributes = []
        for i in range(0, 10):
            self.attributes.append(Attribute.objects.create(name=self.product_attribute_name))

        self.category = Category.objects.create(name=self.category_name, image=self.image_file)
        self.category.products.set(self.products)
        self.category.attributes.set(self.attributes)
        self.category.save()


    def test_can_create_category(self):
        """
        Ensure we can create a new category object.
        """
        for i in range(0, 10):
            self.assertEqual(self.products[i].categories.all()[0].name, self.category_name)

        for i in range(0, 10):
            self.assertEqual(self.attributes[i].categories.all()[0].name, self.category_name)

        self.assertEqual(self.category.name, self.category_name)
        self.assertEqual(self.category.slug, slugify(self.category_name, allow_unicode=True))

    def test_is_filename_same_on_model(self):
        """
        Ensure filename is same on the model as we want
        """
        self.assertTrue(check_filename_is_same_on_model(self.category, settings.CATEGORY_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))
    
    def test_is_file_exists_on_model(self):
        """
        Ensure file is present on the file system
        """
        self.assertTrue(check_file_exists_on_model(self.category, settings.CATEGORY_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def test_can_delete_image(self):
        """
        Ensure we can delete a image object with the file.
        """
        self.category.delete()
        self.assertFalse(check_file_exists_on_model(self.category, settings.CATEGORY_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_DIR)
