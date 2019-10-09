from rest_framework import serializers
from .models import *
from django.utils.text import slugify
from pprint import pprint
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.fields import empty


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'location')


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = User(**validated_data)
        user.save()
        return validated_data

    def update(self, instance, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = User
        validators = []
        fields = ("id", "username", "first_name", "last_name", "email", "number")


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'title', 'image', 'main')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'products', 'attributes')


class ProductSerializer(serializers.ModelSerializer):
#    attributes = AttributeSerializer(many=True, read_only=True)
#    categories = CategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)

        if len(data["images"]):
            main_image = {"title": data["images"][0]["title"], "title": data["images"][0]["url"]}
        else:
            main_image = {}
        images = []
        for image in data.pop("images"):
            print(image)
            if not image["main"]:
                images.append({"title": image["title"], "url": image["image"]})
            else:
                main_image = {"title": image["title"], "url": image["image"]}
        data["images"] = images
        data["main_image"] = main_image

#        categories = []
#        for category in data.pop("categories"):
#            categories.append(category["name"])
#        data["categories"] = categories
#
#        attributes = []
#        for attribute in data.pop("attributes"):
#            product_attributes = AttributeValue.objects.filter(attributes=attribute["id"])
#            attrs = []
#            for attr in product_attributes:
#                attrs.append({"id": attr.id, "value": attr.value, "price": attr.price})
#            attributes.append({"id": attribute["id"], "name": attribute["name"], "value": attrs})
#
#        data["attributes"] = attributes
#        data["slug"] = instance.slug
        return data

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'images', 'created_at', 'categories', 'featured', 'variants')


class ProductCategorySerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    def to_representation(self, instance):
        data = super(ProductCategorySerializer, self).to_representation(instance)

        if len(data["images"]):
            main_image = {"title": data["images"][0]["title"], "title": data["images"][0]["url"]}
        else:
            main_image = {}
        for image in data.pop("images"):
            if image["main"]:
                main_image = {"title": image["title"], "url": image["url"]}
        data["main_image"] = main_image

        return data

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'created_at', 'images', 'slug')


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ('value', 'price', 'attributes')


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ('id', 'title', 'description', 'image', 'url', 'created_at')

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'image', 'url', 'created_at')

class LandingBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingBanner
        fields = ('id', 'title', 'image', 'url', 'created_at')

class FeaturedProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    def to_representation(self, instance):
        data = super(FeaturedProductSerializer, self).to_representation(instance)

        if len(data["images"]):
            main_image = {"title": data["images"][0]["title"], "title": data["images"][0]["url"]}
        else:
            main_image = {}
        for image in data.pop("images"):
            if image["main"]:
                main_image = {"title": image["title"], "url": image["url"]}
        data["main_image"] = main_image

        return data

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'created_at', 'images', 'slug')


class TokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email
        token["number"] = user.number

        return token

class OrderSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)

        product_data = data.pop("product")
        product_data = Product.objects.get(pk=product_data)
        data["product_id"] = product_data.id
        data["title"] = product_data.title
        data["product_price"] = product_data.price
        data["slug"] = product_data.slug

        attributes = []
        for attribute in data.pop("attribute"):
            attribute_data = AttributeValue.objects.get(pk=attribute)
            attribute_name = Attribute.objects.get(attributes=attribute)
            attributes.append(
                {
                    "name": attribute_name.name,
                    "value": attribute_data.value,
                    "price": attribute_data.price
                }
            )
        data["attributes"] = attributes

        return data

    def create(self, validated_data):
        product = validated_data["product"]
        price = product.price
        for attribute in validated_data["attribute"]:
            price = price + attribute.price

        validated_data["price"] = price
        attributes = validated_data.pop('attribute')
        order = Order.objects.create(**validated_data)
        order.attribute.set(attributes)
        validated_data['attribute'] = attributes
        return validated_data

    def update(self, instance, validated_data):
        price = 0
        product = validated_data["product"]
        price = price + product.price
        for attribute in validated_data["attribute"]:
            price = price + attribute.price
        validated_data["price"] = price

        attribute = validated_data.pop("attribute")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.attribute.set(attribute)

        return instance

    class Meta:
        model = Order
        fields = ('id', 'product', 'attribute', 'price', 'count')


class CartSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(CartSerializer, self).to_representation(instance)

        orders = data.pop("orders")
        cart_orders = []
        for order_id in orders:
            order = Order.objects.get(pk=order_id)
            serialized_order = OrderSerializer().to_representation(order)
            cart_orders.append(serialized_order)

        data["orders"] = cart_orders
        data["price"] = instance.price


        return data

    def create(self, validated_data):
        price = 0
        orders = validated_data.pop("orders_cart")
        for order in orders:
            price = price + order.price

        validated_data["price"] = price
        cart = Cart.objects.create(**validated_data)
        cart.orders_cart.set(orders)
        return validated_data

    #def update(self, instance, validated_data):
    #    price = 0
    #    product = validated_data["product"]
    #    price = price + product.price
    #    for attribute in validated_data["attribute"]:
    #        price = price + attribute.price

    #    instance.price = price
    #    return instance

    class Meta:
        model = Cart
        fields = ('id', 'user', 'orders', 'created_at')

class CreateOrderSerializer(serializers.Serializer):

    orders = OrderSerializer
    carts = CartSerializer

