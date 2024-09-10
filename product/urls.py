from django.urls import path,include

from rest_framework.routers import DefaultRouter

from product import views

router = DefaultRouter()
router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'brand', views.BrandViewSet, basename='brand')
urlpatterns = [
    path('api/', include(router.urls)),
]