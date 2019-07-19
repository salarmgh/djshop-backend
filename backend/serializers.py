from rest_framework import serializers
from .models import *
from django.utils.text import slugify
from pprint import pprint
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address')

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = User(**validated_data)
        user.save()
        return validated_data

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "number", "password")

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('id', 'name', 'products')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'title', 'url', 'product', 'main')

class CategorySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(CategorySerializer, self).to_representation(instance)
        data["slug"] = instance.slug
        return data

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["name"], allow_unicode=True)
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        instance.slug = slugify(validated_data["name"], allow_unicode=True)
        instance.products.set(validated_data["products"])

        return instance

    class Meta:
        model = Category
        fields = ('id', 'name', 'cover', 'products')


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)

        if len(data["images"]):
            main_image = {"title": data["images"][0]["title"], "title": data["images"][0]["url"]}
        else:
            main_image = {}
        images = []
        for image in data.pop("images"):
            if not image["main"]:
                images.append({"title": image["title"], "url": image["url"]})
            else:
                main_image = {"title": image["title"], "url": image["url"]}
        data["images"] = images
        data["main_image"] = main_image

        categories = []
        for category in data.pop("categories"):
            categories.append(category["name"])
        data["categories"] = categories

        attributes = []
        for attribute in data.pop("attributes"):
            product_attributes = ProductAttributeValue.objects.filter(attributes=attribute["id"])
            attrs = []
            for attr in product_attributes:
                attrs.append(attr.value)
            attributes.append({attribute["name"]: attrs})

        data["attributes"] = attributes
        data["slug"] = instance.slug
        return data

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["title"], allow_unicode=True)
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        instance.slug = slugify(validated_data["title"], allow_unicode=True)

        return instance

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'images', 'created_at', 'categories', 'attributes', 'featured')


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


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ('value', 'price', 'attributes', 'products')


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
