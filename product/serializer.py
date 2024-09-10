from rest_framework import serializers

from.models import Product,Category,Brand


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','category','brand',"stock","price","description"]


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