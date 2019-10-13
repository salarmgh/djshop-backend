from django.core.management.base import BaseCommand, CommandError
from django.core.files.uploadedfile import SimpleUploadedFile
from backend.models import Product, Variant, Attribute, AttributeValue, Image
from ...tests.helpers import generate_random_string, generate_random_number


class Command(BaseCommand):
    help = 'Create dummy data on database'

    def handle(self, *args, **options):
        for i in range(10):
            attributes = []
            for i in range(100):
                attribute =Attribute.objects.create(name=generate_random_string(5, 5))
                for i in range(10):
                    attribute_value = AttributeValue.objects.create(value=generate_random_string(5, 5), attribute=attribute)
                attributes.append(attribute)
            image_file = SimpleUploadedFile(name="test.jpg", content=open('backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')
            image = Image.objects.create(title=generate_random_string(5, 5), image=image_file)
            product = Product.objects.create(title=generate_random_string(5, 5), slug=generate_random_string(5, 5), featured=True, image=image)
            for i in range(10):
                variant = Variant.objects.create(name=generate_random_string(5, 5), product=product, price=generate_random_number(5, 5))
