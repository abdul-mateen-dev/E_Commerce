from django.db import models
from.category import Category
from .brands import Brand


class Product(models.Model):
    choices = (
        ("In Stock", "In Stock"),
        ("Sold Out", "Sold Out"),
    )
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    availability = models.CharField(max_length=255,null=True, blank=True)
    rating = models.PositiveIntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return f"Name{self.name},Brand{self.brand},Price{self.price}"


    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.availability = "Sold Out"
        return super().save(*args, **kwargs)

