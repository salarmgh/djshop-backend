from django.urls import path, include
from rest_framework import routers
from backend import urls, views
from django.conf import settings
from django.conf.urls import url


urlpatterns = [
    path('', include(urls.router.urls)),
]

if settings.DEBUG:
   from django.contrib.staticfiles import views

   urlpatterns += [
       url(r'^static/(?P<path>.*)$', views.serve),
]
