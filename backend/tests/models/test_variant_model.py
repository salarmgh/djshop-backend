from django.test import TestCase
from django.conf import settings
from ...models import Variant, Product, Attribute, Image
from ..helpers import generate_random_string, generate_random_number
from django.core.files.uploadedfile import SimpleUploadedFile

    
class VariantTests(TestCase):
    def setUp(self):
        self.product_title = generate_random_string(15, 50)
        self.product_description = generate_random_string(15, 500)
        self.product_price = generate_random_number(7, 9)

        self.image_title = generate_random_string(15, 250)
        self.image_name = generate_random_string(3, 5) + '.jpg'
        self.image_file = SimpleUploadedFile(name=self.image_name, content=open('backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')
        self.image = Image.objects.create(title=self.image_title, image=self.image_file)

        self.product_attribute_name = generate_random_string(15, 50) 

        self.variant_name = generate_random_string(15, 50) 

    def test_can_create_variant(self):
        """
        Ensure we can create a new variant object.
        """
        product = Product.objects.create(title=self.product_title,
                                         description=self.product_description,
                                         image=self.image)

        attributes = []
        for i in range(10):
            attributes.append(Attribute.objects.create(name=self.product_attribute_name))

        variant = Variant.objects.create(product=product, name=self.variant_name)
        variant.attributes.set(attributes)

        for i in range(10):
            self.assertEqual(attributes[i].variants.all()[0].name, self.variant_name)

