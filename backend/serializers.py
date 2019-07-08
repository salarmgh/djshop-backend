from rest_framework import serializers
from .models import Product, Category, Image, ProductAttribute, ProductAttributeValue
from pprint import pprint


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('id', 'name', 'products')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'title', 'url', 'product', 'main')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'cover')


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
        return data

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'images', 'created_at', 'categories', 'attributes')


class ProductCategorySerializer(serializers.ModelSerializer):
    #def to_representation(self, instance):
    #    pprint(instance)
    #    data = super(ProductCategorySerializer, self).to_representation(instance)

        #if len(data["images"]):
        #    main_image = {"title": data["images"][0]["title"], "title": data["images"][0]["url"]}
        #else:
        #    main_image = {}
        #for image in data.pop("images"):
        #    if image["main"]:
        #        main_image = {"title": image["title"], "url": image["url"]}
        #data["main_image"] = main_image

    #    return data

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'created_at')


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ('value', 'price', 'attributes', 'products')
