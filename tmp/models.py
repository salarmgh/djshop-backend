from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Deployment(models.Model):
    name = models.CharField(max_length=100)
    namespace = models.CharField(max_length=20)
    replica = models.IntegerField()
    image = models.CharField(max_length=100)
    command = models.CharField(max_length=100)
    pool = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    machine = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, related_name="deployments", on_delete=models.CASCADE)

