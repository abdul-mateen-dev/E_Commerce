from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from product.models import Brand
from product.models.product import Product
from product.models.category import Category
from serializer import ProductListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_by_category(request, category):
    category = Category.objects.get(name=category)
    products = Product.objects.filter(brand__category=category)
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_by_brand(request, brand):
    brand = Brand.objects.get(name=brand)
    products = Product.objects.filter(brand=brand)
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)
