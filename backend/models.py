from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE, blank=True, null=True)
    main = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)
    cover = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
   name = models.CharField(max_length=100)
   products = models.ManyToManyField(Product, related_name='attributes')

   def __str__(self):
       return self.name

class ProductAttributeValue(models.Model):
    value = models.CharField(max_length=100)
    price = models.IntegerField()
    attributes = models.ForeignKey(ProductAttribute, related_name='attributes', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='attribute_values')

class Carousel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
