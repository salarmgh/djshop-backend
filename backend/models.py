from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    price = models.IntegerField()

