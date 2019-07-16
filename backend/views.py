from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import mixins
from pprint import pprint


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ProductAttributeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer

class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer


class ProductCategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = ProductCategorySerializer
    lookup_url_kwarg = "category"

    def get_queryset(self):
        category = self.kwargs.get(self.lookup_url_kwarg)
        category_name = Category.objects.get(slug=category)
        queryset = Product.objects.filter(categories=category_name)
        return queryset

class CarouselViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer

class BannerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class LandingBannerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = LandingBanner.objects.all()
    serializer_class = LandingBannerSerializer

class FeaturedProductViewSet(viewsets.ViewSet, generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = FeaturedProductSerializer

    def get_queryset(self):
        products = Product.objects.filter(featured=True)
        return products
