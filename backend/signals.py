import os
from django.dispatch import receiver
from django.db import models
from .models import Image, Category, Carousel, Banner, LandingBanner

@receiver(models.signals.post_delete, sender=Image)
def image_auto_delete_file_on_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(models.signals.post_delete, sender=Category)
def category_auto_delete_file_on_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(models.signals.post_delete, sender=Carousel)
def carousel_auto_delete_file_on_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(models.signals.post_delete, sender=Banner)
def banner_auto_delete_file_on_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(models.signals.post_delete, sender=LandingBanner)
def landing_banner_auto_delete_file_on_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

