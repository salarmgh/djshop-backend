from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .es_models import VariantIndex
from .validators import *
from elasticsearch_dsl import Search


class User(AbstractUser):
    number = models.CharField(max_length=11, validators=[validate_phone_number], blank=False, null=False)
    
    def clean(self, *args, **kwargs):
        validate_phone_number(self.number)
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Address(models.Model):
    location = models.TextField()
    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE, blank=True)


class Image(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to=settings.PRODUCT_IMAGES_DIR)

    def __str__(self):
        return self.title

class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    image = models.ImageField(upload_to=settings.CATEGORY_IMAGES_DIR, blank=True)
    attributes = models.ManyToManyField(Attribute, related_name="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    slug = models.SlugField(allow_unicode=True, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
#    attributes = models.ManyToManyField(Attribute, related_name="products")
 

    def indexing(self):
        obj = ProductIndex(
            meta={'id': self.id},
            title=self.title,
            slug=self.slug,
            featured=self.featured,
            image=self.image.image.url,
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title



class Variant(models.Model):
    name = models.CharField(max_length=200)
    attribute_values = models.ManyToManyField(AttributeValue, related_name="variants", blank=True)
    product = models.ForeignKey(Product, related_name='variants', blank=True, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    images = models.ManyToManyField(Image, related_name="variants", blank=True)

    def indexing(self):
        attrs = []
        values = []
        for attr in self.attributes.all():
            for value in attr.attributes.all():
                values.append(value.value)
            attrs.append({"name": attr.name, "value": values})
        obj = VariantIndex(
            meta={'id': self.id},
            name=self.product.title + " " + self.name,
            attributes=attrs,
            url=self.product.slug + "/apc-" + str(self.id) + "/",
            featured=self.product.featured,
            price=self.price,
            image=self.product.image.image.url,
        )
        obj.save()
        return obj.to_dict(include_meta=True)


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


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    variant = models.ForeignKey(Variant, related_name="orders", on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variant.name
