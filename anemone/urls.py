from django.urls import path, include
from rest_framework import routers
from backend import urls, views
from django.conf import settings
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    path('', include(urls.router.urls)),
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
]

if settings.DEBUG:
   from django.contrib.staticfiles import views

   urlpatterns += [
       url(r'^static/(?P<path>.*)$', views.serve),
]
