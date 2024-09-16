from django.contrib.sites import requests
from django.core.files import images
from rest_framework import serializers


from .models import Product, Category, Brand, ProductSpecification, Rating, ProductImage

from rest_framework.validators import ValidationError



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name"]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id","name","category"]

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ["product","specification"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id","user","product","rating"]
        read_only_fields = ["user","product"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["product","images"]
        read_only_fields = ["product"]

    def validate_image(self, image):
        if image:
            max_size = 8 * 1024 * 1024  # 8MB
            if image.size > max_size:
                raise serializers.ValidationError('File size too large. Maximum size allowed is 8MB.')
            return image


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'stock', 'price', 'description']






