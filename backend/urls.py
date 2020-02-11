from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'variants', VariantViewSet)
router.register(r'variants-id', VariantByIdViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'attributes', AttributeViewSet)
router.register(r'attribute-values', AttributeValueViewSet)
router.register(r'category/(?P<category>[^/.]+)',
                ProductCategoryViewSet, basename="product-category")
router.register(r'carousel', CarouselViewSet)
router.register(r'banner', BannerViewSet)
router.register(r'landing-banner', LandingBannerViewSet)
router.register(r'featured-product', FeaturedProductViewSet,
                basename="featured-product")
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'cart', CartViewSet)
router.register(r'create-order', CreateOrderViewSet, basename="create-order")
router.register(r'search', SearchViewSet, basename="search")
router.register(r'variants-by-id/(?P<ids>[^/.]+)',
                CartVarientViewSet, basename="variants-by-id")
router.register(r'addresses', AddressesViewSet, basename="addresses")
