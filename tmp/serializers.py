from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'content', 'created_at')

class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = ('id', 'name', 'replica', 'image', 'command', 'pool', 'namespace', 'state', 'created_at', 'profile')
