from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'image', ImageViewSet)
router.register(r'product-attribute', AttributeViewSet)
router.register(r'product-attribute-value', AttributeValueViewSet)
router.register(r'product-category/(?P<category>[^/.]+)', ProductCategoryViewSet, basename="product-category")
router.register(r'carousel', CarouselViewSet)
router.register(r'banner', BannerViewSet)
router.register(r'landing-banner', LandingBannerViewSet)
router.register(r'featured-product', FeaturedProductViewSet, basename="featured-product")
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'cart', CartViewSet)
router.register(r'create-order', CreateOrderViewSet, basename="create-order")
