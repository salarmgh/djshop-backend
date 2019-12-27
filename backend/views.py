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
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView, mixins.RetrieveModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView, mixins.RetrieveModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class AttributeViewSet(viewsets.ViewSet, generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AttributeValueViewSet(viewsets.ViewSet, generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


class ProductCategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = ProductSerializer
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
    serializer_class = ProductSerializer

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


class VariantViewSet(viewsets.ViewSet, generics.ListAPIView, mixins.RetrieveModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class TokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


class SearchViewSet(viewsets.ViewSet):
    def list(self, request):
        from anemone.elasticsearch import connections
        client = connections.get_connection()
        search = Search(using=connections.get_connection(), index="variants")
        multi_match = MultiMatch(query='gold', fields=['name', 'product.title', 'product.description'])
        filter = search.filter('term', product__category__keyword='Necklace')
        query = filter.query(multi_match)

        result = query.execute()
        return Response(result.to_dict()["hits"]["hits"])

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
                attribute_value = AttributeValue.objects.get(pk=attr)
                product["price"] = product["price"] + attribute_value.price
            product["price"] = float(product["price"]) * int(product["count"])
            pprint(product)
            order = Order(**product)
            order.save()
            order.attribute.set(attribute)
            orders.append(order)
            cart_price = cart_price + product["price"]

        user = User.objects.get(pk=int(request.data["user"]))
        cart = Cart(user=user, price=cart_price)
        cart.save()
        cart.orders.set(orders)
        return Response()

