from django.test import TestCase
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import re
from django.conf import settings
from ...models import Product, Category, Attribute
from ..helpers import check_file_exists_on_model, check_filename_is_same_on_model
import shutil
from backend.tests.utils.category import create_category


class CategoryTests(TestCase):
    def setUp(self):
        self.image_name = "test.jpg"
        self.category = create_category(self.image_name)

    def test_is_filename_same_on_model(self):
        """
        Ensure filename is same on the model as we want
        """
        self.assertTrue(check_filename_is_same_on_model(
            self.category, settings.CATEGORY_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def test_is_file_exists_on_model(self):
        """
        Ensure file is present on the file system
        """
        self.assertTrue(check_file_exists_on_model(
            self.category, settings.CATEGORY_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def test_can_delete_image(self):
        """
        Ensure we can delete a image object with the file.
        """
        self.category.delete()
        self.assertFalse(check_file_exists_on_model(
            self.category, settings.CATEGORY_IMAGES_DIR, self.image_name, settings.MEDIA_DIR))

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_DIR)
