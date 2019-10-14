from rest_framework import serializers
from .models import *
from django.utils.text import slugify
from pprint import pprint
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.fields import empty


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
        fields = ("id", "username", "first_name", "last_name", "email", "number", "addresses")


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ('value', 'attribute')


class AttributeSerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(many=True, read_only=True)
    class Meta:
        model = Attribute
        fields = ('id', 'name', 'attributes')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'title', 'image')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'attributes')


class VariantSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, read_only=True)
    images = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Variant
        fields = ('id', 'name', 'attributes', 'product', 'price', 'images')


class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'image', 'created_at', 'categories', 'featured', 'variants', 'slug')


class ESProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'featured', 'image')


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ('id', 'title', 'description', 'image', 'url', 'created_at')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'description', 'image', 'url', 'created_at')


class LandingBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingBanner
        fields = ('id', 'title', 'description' 'image', 'url', 'created_at')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'variant', 'count', 'user', 'cart', 'created_at')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'orders', 'created_at')


class TokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email
        token["number"] = user.number

        return token
