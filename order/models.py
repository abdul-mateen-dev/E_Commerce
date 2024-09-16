import uuid
from email.headerregistry import Address

from django.contrib.staticfiles.views import serve
from django.db import models

from product.models import Product


class Order(models.Model):
    status_choices = (
        ("D", "Delivered"),
        ("On Way", "On Way"),
    )
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    products = models.ForeignKey(Product, related_name="products",on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=status_choices, default="On Way")
    address = None
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    def save(self, *args, **kwargs):
        return  f"{self.products.name}  Address: {self.address.country,  self.address.state,  self.address.city, self.address.street}"



