from rest_framework import serializers
from account.models import User


def normalize_email( email):

    email = email or ""
    try:
        email_name, domain_part = email.strip().rsplit("@", 1)
    except ValueError:
        pass
    else:
        email = email_name + "@" + domain_part.lower()
    return email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name","email","password","phone_number","username"]

    def validate_email(self, email):
        return normalize_email(email)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["email","password"]

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        max_length=255, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["password", "confirm_password"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match")
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)

    class Meta:
        fields = ["email"]


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        max_length=255, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["password", "confirm_password"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match")
        return attrs




