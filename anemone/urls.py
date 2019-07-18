from django.urls import path, include
from rest_framework import routers
from backend import urls, views
from django.conf import settings
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('', include(urls.router.urls)),
    url(r'^token/obtain$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    from django.contrib.staticfiles import views

    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
