from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .validators import *
from .tasks import variant_model_indexer, product_model_indexer


class User(AbstractUser):
    number = models.CharField(max_length=11, validators=[
                              validate_phone_number], blank=False, null=False)

    def clean(self, *args, **kwargs):
        validate_phone_number(self.number)
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Address(models.Model):
    location = models.TextField()
    user = models.ForeignKey(
        User, related_name="addresses", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.location


class Image(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to=settings.PRODUCT_IMAGES_DIR)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     variants = self.variants.all()
    #     if variants:
    #         documents = []
    #         for variant in self.variants.all():
    #             documents.append(variant.document())

    #         product_model_indexer.delay(documents)


class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return self.value

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     documents = []
    #     for variant in self.variants.all():
    #         documents.append(variant.document())

    #     product_model_indexer.delay(documents)


class Size(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        documents = []
        for variant in self.variants.all():
            documents.append(variant.document())

        product_model_indexer.delay(documents)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    image = models.ImageField(
        upload_to=settings.CATEGORY_IMAGES_DIR, blank=True)
    attributes = models.ManyToManyField(Attribute, related_name="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     documents = []
    #     for variant in self.variants.all():
    #         documents.append(variant.document())

    #     product_model_indexer.delay(documents)


class Variant(models.Model):
    name = models.CharField(max_length=200)
    attribute_values = models.ManyToManyField(
        AttributeValue, related_name="variants", blank=True)
    size = models.ManyToManyField(
        Size, related_name="variants", blank=True)
    product = models.ForeignKey(
        Product, related_name='variants', blank=True, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    images = models.ManyToManyField(Image, related_name="variants", blank=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(allow_unicode=True, unique=True)
    weight = models.FloatField()

    def document(self):
        product = {"title": self.product.title, "description": self.product.description, "slug": self.slug,
                   "created_at": self.product.created_at, "featured": self.featured, "category": self.product.category.name}

        images = []
        for image in self.images.all():
            images.append(image.image.url)

        attributes = []
        for attribute in self.attribute_values.all():
            attributes.append(
                {"name": attribute.attribute.name, "value": attribute.value})

        variant = {"id": self.id, "name": self.name, "price": self.price, "product": product,
                   "attributes": attributes, "images": images, "category": self.product.category.name}
        return variant

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product.title + "-" +
                            self.name, allow_unicode=True)
        super().save(*args, **kwargs)
        variant = self.document()
        variant_model_indexer.delay(variant)

    def indexing(self):
        from .documents.variant import VariantDocument
        variant = self.document()
        document = VariantDocument(
            meta={'id': variant["id"]},
            name=variant["name"],
            price=variant["price"],
            product=variant["product"],
            attributes=variant["attributes"],
            category=variant["category"],
            images=variant["images"]
        )

        return document.to_dict(include_meta=True)

    def __str__(self):
        return self.name


class Carousel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=settings.CAROUSEL_IMAGES_DIR)
    url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=settings.BANNER_IMAGES_DIR)
    url = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LandingBanner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=settings.LANDING_IMAGES_DIR)
    description = models.CharField(max_length=300)
    url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ShippingMethod(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="carts",
                             on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, related_name="carts", on_delete=models.CASCADE)
    shipping_method = models.ForeignKey(
        ShippingMethod, related_name="carts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    variant = models.ForeignKey(
        Variant, related_name="orders", on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    user = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE)
    cart = models.ForeignKey(
        Cart, related_name="orders", on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variant.product.title + " " + self.variant.name
