from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'image', ImageViewSet)
router.register(r'product-attribute', ProductAttributeViewSet)
router.register(r'product-attribute-value', ProductAttributeValueViewSet)
