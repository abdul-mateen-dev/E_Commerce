from rest_framework import serializers

from product.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name","price","brand","rating"]

