from django.urls import path,include

from rest_framework.routers import DefaultRouter

from product.product_list_views.products_view import list_by_brand,list_by_category
from product.product_list_views.product_detail import ProductDetailsView
from product import views

router = DefaultRouter()
router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'brand', views.BrandViewSet, basename='brand')
router.register(r'product-specs', views.ProductSpecificationViewSet, basename='product-specification')
router.register(r'product-detail', ProductDetailsView, basename='product-detail')

urlpatterns = [
    path('api/', include(router.urls)),
    path("api/products/brand/<int:pk>/",list_by_brand,name="list_by_brand"),
    path("api/products/category/<int:pk>/",list_by_category,name="list_by_category"),
]