from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import mixins
from pprint import pprint
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView


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


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class TokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


class CreateOrderViewSet(viewsets.ViewSet):
    def create(self, request):
        products = request.data["products"]
        orders = []
        cart_price = 0
        orders_price = 0
        for product in products:
            product["product"] = Product.objects.get(pk=product["product"])
            product["price"] = product["product"].price

            attribute = product.pop("attribute")
            for attr in attribute:
                attribute_value = ProductAttributeValue.objects.get(pk=attr)
                product["price"] = product["price"] + attribute_value.price
            order = Order(**product)
            order.save()
            order.attribute.set(attribute)
            orders.append(order)
            cart_price = cart_price + product["price"]

        user = User.objects.get(pk=1)
        cart = Cart(user=user, price=cart_price)
        cart.save()
        cart.orders.set(orders)
        return Response()
