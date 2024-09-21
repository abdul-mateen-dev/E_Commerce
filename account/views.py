
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken



from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings


from.backends import UserAuthBackend as auth
from account.serializer import *

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = AccessToken.for_user(user)

    return {"access": str(access_token), "refresh": str(refresh)}

class UserRegister(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            user = serializer.save()
            user.set_password(password)
            user.save()
            token = get_tokens_for_user(user)
            response_data = {
                "message":"User Registered",
                "token":token
            }
            return Response(response_data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            username = serializer.validated_data['username']

            user = auth.authenticate(request,username=username,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                response_data = {
                    "token": token
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

        return Response("User is not authenticated", status=status.HTTP_401_UNAUTHORIZED)




class UserChangePasswordView(APIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            user = request.user
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response({"msg": "Password has been changed "}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmail(APIView):
    serializer_class = SendPasswordResetEmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            try:
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                    uid = urlsafe_base64_encode(force_bytes(user.id))
                    token = PasswordResetTokenGenerator().make_token(user)
                    link = f"http://localhost:8000/api/reset-password/{uid}/{token}/"
                    subject = "Reset Your Password"
                    message = f"Click the link below to reset your password:\n{link}"
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.email]

                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=from_email,
                        recipient_list=recipient_list,
                        fail_silently=False,
                    )
                    return Response(
                        {"msg": "Password reset email has been sent"}, status=status.HTTP_200_OK
                    )
                else:
                    return Response({"error": "Email does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except DjangoUnicodeDecodeError:
                return Response(
                    {"error": "There was an error processing your request. Please try again."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(APIView):




    serializer_class = UserResetPasswordSerializer
    def post(self, request, uid, token):
        serializer = self.serializer_class(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid(raise_exception=True):
            try:
                pk = smart_str(urlsafe_base64_decode(uid))
                user = User.objects.get(id=pk)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(serializer.validated_data["password"])
                user.save()
                return Response(
                    {"msg": "Password Reset Successfully"}, status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
