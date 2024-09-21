from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes,authentication_classes

from product.models import Product
from .models import Order
from .serializers import OrderSerializer
from cart.models import Cart

class CheckOut(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']


    def create(self, request, *args, **kwargs):
        user = request.user
        items = Cart.objects.filter(user=user, is_ordered=False)

        if not items.exists():
            return Response({"detail": "No items in the cart"}, status=status.HTTP_400_BAD_REQUEST)

        order_data = []
        errors = []

        for item in items:
            data = {
                'products': item.product.id,
                'user': user.id,
                'amount': item.price,
                'quantity': item.quantity,
                'status': "Pending"
            }

            serializer = OrderSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                order_data.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if order_data:
            items.update(is_ordered=True)
            items.delete()
            return Response({"orders": order_data}, status=status.HTTP_201_CREATED)

        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)


class CheckOutNowAPI(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')
        product = get_object_or_404(Product, id=pk)

        quantity = request.data.get("quantity")
        if not quantity:
            return Response({"error": "Quantity is required."}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "products": product.id,
            "user": user.id,
            "amount": product.price * quantity,
            "quantity":quantity,
            "status": "Pending",
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


