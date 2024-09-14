from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from product.models.product import Product
from .serializer import ProductListSerializer


@api_view(['GET'])
def list_by_category(request,pk):
    product = Product.objects.filter(brand__category__id=pk)
    serializer = ProductListSerializer(product,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)



@api_view(['GET'])
def list_by_brand(request,pk):
    product = Product.objects.filter(brand__id=pk)
    serializer = ProductListSerializer(product,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)





