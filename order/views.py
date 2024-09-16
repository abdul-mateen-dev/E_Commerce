from rest_framework import viewsets,status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order
from.serializers import OrderSerializer

from cart.models import Cart

class CheckOut(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        items = Cart.objects.filter(user=user,is_ordered=False)
        for item in items:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(product=item,user=user,quantity=item.quantity,amount=item.price)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

