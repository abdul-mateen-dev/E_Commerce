from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserChangePasswordView,
    SendPasswordResetEmail,
    UserResetPasswordView,
    Login, UserRegister,
)


router = DefaultRouter()


urlpatterns = [
    path("api/", include(router.urls)),
    path ("api/login/", Login.as_view(), name="login"),
    path("api/change/", UserChangePasswordView.as_view(), name="change password"),
    path("api/register/",UserRegister.as_view(), name="registration_api"),
    path(
        "api/email-rest-password/",
        SendPasswordResetEmail.as_view(),
        name="send_password_reset_email",
    ),
    path(
        "api/reset-password/<uid>/<token>/",
        UserResetPasswordView.as_view(),
        name="reset_password",
    ),
]
