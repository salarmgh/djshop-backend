from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.views import APIView
from .serializers import *
from .models import *
from .helpers.deployment import *
import json

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class DeploymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class DeploymentActionViewSet(viewsets.ViewSet):
    def list(self, request):
        pass

    def create(self, request):
        data = json.loads(request.body)
        deployment = Deployment.objects.get(pk=data["id"])
        deployment_data = DeploymentSerializer(deployment)
        deployment_dict = deployment_data.data
        profile_id = deployment_dict.pop("profile")
        profile = Profile.objects.get(pk=profile_id)
        deployment_dict["profile"] = profile.content
        deploy(deployment_dict)
        return JsonResponse(deployment_dict)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        deployment = Deployment.objects.get(pk=pk)
        deployment_data = DeploymentSerializer(deployment)
        deployment_dict = deployment_data.data
        delete(deployment_dict)
        deployment.state = "Deleted"
        deployment.save()
        return JsonResponse(deployment_dict)
