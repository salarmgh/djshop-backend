from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='categories')

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


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

