from rest_framework import status
from rest_framework.decorators import action, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Avg
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Product, Rating, ProductImage, ProductSpecification
from .serializer import ProductListSerializer
from product.serializer import RatingSerializer


class ProductDetailsView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

        # authentication_classes = [JWTAuthentication]
        # permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        item = self.get_object()
        rating = Rating.objects.filter(product__id=item.id).values('rating').aggregate(Rating=Avg('rating'))[
                     "Rating"] or None
        specifications = ProductSpecification.objects.values("specification").get(product=item.id) or None
        images = ProductImage.objects.values("image").filter(product__id=item.id) or None

        data = {
            "product": self.serializer_class(item).data,
            "rating": rating,
            "specifications": specifications,
            "images": images,
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='rating', permission_classes=[IsAuthenticated],
            authentication_classes=[JWTAuthentication])
    def rating_product(self, request, pk=None):
        item = Product.objects.get(pk=pk)
        user = request.user
        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            existing_rating = Rating.objects.filter(user=user, product=item).first()

            if existing_rating:
                serializer = RatingSerializer(existing_rating, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    avg_rating = Rating.objects.filter(product=item).aggregate(rating=Avg("rating"))["rating"]
                    Product.objects.filter(id=item.id).update(rating=avg_rating)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user=user, product=item)
            avg_rating = Rating.objects.filter(product=item).aggregate(rating=Avg("rating"))["rating"]
            Product.objects.filter(id=item.id).update(rating=avg_rating)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
