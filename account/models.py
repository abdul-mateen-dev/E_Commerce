from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator,RegexValidator

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\d{11}$',
        message="Phone number must be exactly 11 digits."
    )

    first_name = None
    last_name = None

    email = models.EmailField(unique=True, verbose_name="Email Address", max_length=255,validators=[EmailValidator])
    name = models.CharField(verbose_name="Name", max_length=255)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True, verbose_name="Phone Number")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name", "phone_number","username"]

    def __str__(self):
        return f"Name: {self.name}  , Email: {self.email}"


class Address(models.Model):
    user = (models.ForeignKey(User,on_delete=models.CASCADE))
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} {self.address_line1}"


