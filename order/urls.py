from django.urls import path,include

from rest_framework.routers import DefaultRouter


from.views import CheckOut,CheckOutNowAPI

router = DefaultRouter()

router.register('check-out',CheckOut,basename='checkout')
urlpatterns = [
    path('api/',include(router.urls)),
    path('api/checkout/<int:pk>/', CheckOutNowAPI.as_view(), name='check-out-now'),]