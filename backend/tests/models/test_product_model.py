from django.test import TestCase
from django.utils.text import slugify
from ...models import Product
from ..helpers import generate_random_string, generate_random_number

    
class ProductTests(TestCase):
    def setUp(self):
        self.title = generate_random_string(15, 50)
        self.description = generate_random_string(15, 500)
        self.featured = True


    def test_can_create_product(self):
        """
        Ensure we can create a new product object.
        """
        product = Product.objects.create(title=self.title, description=self.description, featured=self.featured)

        saved_product = Product.objects.get(pk=product.id)
        self.assertEqual(saved_product.title, self.title)
        self.assertEqual(saved_product.description, self.description)
        self.assertEqual(saved_product.featured, self.featured)
        self.assertEqual(saved_product.slug, slugify(self.title, allow_unicode=True))
