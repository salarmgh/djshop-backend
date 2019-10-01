from django.dispatch import receiver
from django.db.models.signals import post_delete


@receiver(post_delete, sender=Image)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

