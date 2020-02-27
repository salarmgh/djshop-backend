from backend.models import Category, Attribute, Product
from django.core.files.uploadedfile import SimpleUploadedFile


def create_category(image):
    category_name = "category test"
    image_name = image
    image_file = SimpleUploadedFile(name=image_name, content=open(
        'backend/tests/assets/placeholder.jpg', 'rb').read(), content_type='image/jpeg')
    product_attribute_name = "test attribute"

    attribute = Attribute.objects.create(
        name=product_attribute_name)

    category = Category.objects.create(
        name=category_name, image=image_file)
    category.attributes.set([attribute])
    category.save()

    return category


def create_product():
    product_description = "test description"

    category = create_category("test.jpg")

    product = Product.objects.create(
        title="Product Title", description=product_description, category=category)
    return product
