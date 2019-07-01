from django.urls import path, include
from rest_framework import routers
from backend import urls


urlpatterns = [
    path('', include(urls.router.urls)),
]
