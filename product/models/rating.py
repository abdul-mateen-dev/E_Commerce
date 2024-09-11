from django.db import models

from account.models import User
from .product import Product


class Rating(models.Model):
    Choices = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )

    rating = models.PositiveSmallIntegerField(choices=Choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE,related_name="product_ratings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"Name: {self.product.name}Rating: {self.rating}"
