from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
import uuid
from .validators import *


class User(AbstractUser):
    number = models.CharField(max_length=11, validators=[validate_phone_number])

    def clean(self, *args, **kwargs):
        validate_phone_number(self.number)
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Address(models.Model):
    location = models.TextField()
    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE, blank=True)


class Product(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    slug = models.SlugField(allow_unicode=True)
    created_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Image(models.Model):
    title = models.CharField(max_length=300)
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    main = models.BooleanField(default=False)
    image = models.ImageField(upload_to=settings.PRODUCT_IMAGES_DIR)

    def __str__(self):
        return self.title


class Attribute(models.Model):
   name = models.CharField(max_length=100)
   products = models.ManyToManyField(Product, related_name='attributes', blank=True)

   def __str__(self):
       return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return self.value

class Variant(models.Model):
    name = models.CharField(max_length=200)
    attributes = models.ManyToManyField(Attribute, related_name="variants")
    product = models.ForeignKey(Product, related_name='variants', blank=True, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()


class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)
    slug = models.SlugField(allow_unicode=True)
    cover = models.ImageField(upload_to=settings.CATEGORY_IMAGES_DIR, blank=True)
    attributes = models.ManyToManyField(Attribute, related_name="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

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


class Order(models.Model):
    product = models.ForeignKey(Product, related_name="order_products", on_delete=models.CASCADE)
    price = models.IntegerField(null=True, default=None)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, related_name="cart")
    created_at = models.DateTimeField(auto_now=True)
