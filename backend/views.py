from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import ProductSerializer, CategorySerializer, ImageSerializer, ProductAttributeSerializer, ProductAttributeValueSerializer, ProductCategorySerializer
from .models import Product, Category, Image, ProductAttribute, ProductAttributeValue
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.http import JsonResponse
from pprint import pprint


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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



class ProductCategoryViewSet(generics.ListAPIView):
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        category = self.kwargs['category']
        products = Product.objects.filter(categories__in=category)
        return products
