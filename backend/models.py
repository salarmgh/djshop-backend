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
    product = models.ManyToManyField(Product)

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
    value = models.CharField(max_length=100)
    price = models.IntegerField()
    product = models.ManyToManyField(Product)
