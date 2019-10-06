from django.test import TestCase
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import re
from django.conf import settings
from ..models import Product, Category, Attribute
from .helpers import generate_random_string, generate_random_number

    
class CategoryTests(TestCase):
    def setUp(self):
        self.image_name = "image.jpg"
        self.category_name = generate_random_string(15, 50) 
        self.category_cover = SimpleUploadedFile(name=self.image_name, content=open('backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')

        self.product_attribute_name = generate_random_string(15, 50) 

        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)


    def test_can_create_category(self):
        """
        Ensure we can create a new category object.
        """
        products = []
        for i in range(0, 10):
            products.append(Product.objects.create(title=self.product_title, description=self.product_description))

        attributes = []
        for i in range(0, 10):
            attributes.append(Attribute.objects.create(name=self.product_attribute_name))

        category = Category.objects.create(name=self.category_name, cover=self.category_cover)
        category.products.set(products)
        category.attributes.set(attributes)
        category.save()

        for i in range(0, 10):
            self.assertTrue(products[i].categories.all()[0].name == self.category_name)

        for i in range(0, 10):
            self.assertTrue(attributes[i].categories.all()[0].name == self.category_name)

        self.assertEqual(category.name, self.category_name)
        self.assertEqual(category.slug, slugify(self.category_name, allow_unicode=True))

        filename, file_extension = os.path.splitext(self.image_name)
        same_name = re.match(settings.CATEGORY_IMAGES_DIR + filename + ".*" + file_extension, category.cover.name)
        self.assertTrue(same_name)

        file_exists = os.path.isfile(settings.MEDIA_DIR + category.cover.name)
        self.assertTrue(file_exists)
