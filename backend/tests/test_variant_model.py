from django.test import TestCase
from django.conf import settings
from ..models import Variant, Product, ProductAttribute
from .helpers import generate_random_string, generate_random_number

    
class VariantTests(TestCase):
    def setUp(self):
        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)
        self.product_price = generate_random_number(7, 9)

    def test_can_create_variant(self):
        """
        Ensure we can create a new variant object.
        """

        product = Product.objects.create(title=self.product_title, description=self.product_description, price=self.product_price)

        attributes = []
        for i in range(3):
            attributes.append(ProductAttribute.objects.create())

        variant = Variant.objects.create(product=product)

