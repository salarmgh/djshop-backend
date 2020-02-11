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
from elasticsearch_dsl import Q
from rest_framework.decorators import action


class AddressesViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user.id
        queryset = User.objects.get(pk=user).addresses.all()
        return queryset


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
    serializer_class = FeaturedProductsSerializer

    def get_queryset(self):
        products = Variant.objects.filter(featured=True)
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
    lookup_field = 'slug'


class VariantByIdViewSet(viewsets.ViewSet, generics.ListAPIView, mixins.RetrieveModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class TokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


class SearchViewSet(viewsets.ViewSet):
    def attributes_query_builder(self, search, query):
        attributes_query = []
        query_keys = set()
        query_values = set()
        for match in query:
            key = match.split(':')[0]
            value = match.split(':')[1]
            query_keys.add(key)
            query_values.add(value)

        query_keys = list(query_keys)
        query_values = list(query_values)

        attributes_query.append(
            Q('terms', attributes__name__keyword=query_keys))
        attributes_query.append(
            Q('terms', attributes__value__keyword=query_values))

        return Q('bool', must=attributes_query)

    def category_query_builder(self, search, categories):
        category = search.filter('term', product__category__keyword=categories)
        return category

    def search(self, query, fields):
        query = Q('multi_match', query=query, fields=fields)

        return query

    def price_filter(self, price):
        search_price = {}
        if price["min"]:
            search_price['gte'] = price["min"]
        if price["max"]:
            search_price['lte'] = price["max"]

        query = Q('range', price=search_price)
        return query

    def list(self, request):
        from anemone.elasticsearch import connections

        categories = self.request.query_params.get('categories')
        search_text = self.request.query_params.get('q')

        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        attributes_filter = self.request.query_params.getlist('attribute')

        client = connections.get_connection()
        context = Search(using=connections.get_connection(), index="variants")

        if categories:
            context = self.category_query_builder(context, categories)

        if attributes_filter:
            attributes = self.attributes_query_builder(
                context, attributes_filter)
            context = context.query(attributes)

        if search_text:
            query = self.search(
                search_text, ['name', 'product.title', 'product.description'])
            context = context.query(query)

        if min_price or max_price:
            query = self.price_filter({"max": max_price, "min": min_price})
            context = context.query(query)

        result = context.execute()

        price_max = Search(using=connections.get_connection(), index="variants")
        price_max = price_max.sort('-price')
        price_max = price_max.execute()
        price_max = price_max[0]["price"]

        price_min = Search(using=connections.get_connection(), index="variants")
        price_min = price_min.sort('price')
        price_min = price_min.execute()
        price_min = price_min[0]["price"]

        result = result.to_dict()["hits"]["hits"]

        response = {'price_max': int(price_max),
                    'price_min': int(price_min), 'results': result}
        return Response(response)


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


class CartVarientViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = VariantSerializer
    lookup_url_kwarg = "ids"

    def get_queryset(self):
        ids = self.kwargs.get(self.lookup_url_kwarg).split(",")
        queryset = Variant.objects.filter(pk__in=ids)
        return queryset
