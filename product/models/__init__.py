from rest_framework.serializers import ModelSerializer


from.brands import Brand
from.category import Category
from.product import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ''

