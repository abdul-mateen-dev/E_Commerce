from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializer import *

class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        if not pk:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        successful_uploads = []
        errors = []

        for img in request.data.getlist('image'):
            serializer = ProductImageSerializer(data={'image': img})
            if serializer.is_valid():
                serializer.save(product=product)
                successful_uploads.append(serializer.data)
            else:
                errors.append({"image": img.name, "errors": serializer.errors})

        if errors:
            return Response({
                "uploaded": successful_uploads,
                "errors": errors
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({"uploaded": successful_uploads}, status=status.HTTP_201_CREATED)






class ProductSpecificationViewSet(ModelViewSet):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post','put','delete']



