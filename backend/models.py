from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid


def get_filename(self, instance, filename):
    filename, ext = os.path.splitext(filename)
    filename = '{0}{1}'.format(uuid.uuid4().hex, ext)
    return os.path.join('upload/images/{0}'.format(filename))


class User(AbstractUser):
    number = models.CharField(max_length=15)


class Address(models.Model):
    location = models.TextField()
    addresses = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE, blank=True, null=True)


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    slug = models.SlugField(allow_unicode=True)
    created_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField()

    def __str__(self):
        return self.title


class Image(models.Model):
    title = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE, blank=True, null=True)
    main = models.BooleanField(default=False)
    image = models.FileField(upload_to=get_filename)


    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)
    cover = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(allow_unicode=True)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
   name = models.CharField(max_length=100)
   products = models.ManyToManyField(Product, related_name='attributes', null=True, blank=True)

   def __str__(self):
       return self.name


class ProductAttributeValue(models.Model):
    value = models.CharField(max_length=100)
    price = models.IntegerField()
    attributes = models.ForeignKey(ProductAttribute, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class Carousel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LandingBanner(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    product = models.ForeignKey(Product, related_name="order_products", on_delete=models.CASCADE)
    attribute = models.ManyToManyField(ProductAttributeValue, related_name="order_attributes")
    price = models.IntegerField(blank=True)
    count = models.IntegerField()

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    price = models.IntegerField()
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, related_name="cart")
    created_at = models.DateTimeField(auto_now=True)
