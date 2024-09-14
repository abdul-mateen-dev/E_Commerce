from rest_framework import serializers

from product.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    specification = serializers.JSONField(read_only=True)
    class Meta:
        model = Product
        fields = ["name","price","brand","specification"]


