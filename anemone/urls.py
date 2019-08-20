from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from backend import urls, views
from django.conf import settings
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from backend.admin import admin_site
from django.conf.urls.static import static


urlpatterns = [
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^jet/', include('jet.urls', 'jet')),
    path('admin/', admin_site.urls),
    path('', include(urls.router.urls)),
    url(r'^token/obtain/$', views.TokenObtainView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.contrib.staticfiles import views

    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
