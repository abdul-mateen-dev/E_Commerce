from django.db import models

from account.models import User
from product.models import Product


class Cart(models.Model):
    name = models.CharField(max_length=120,null=True,blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=20,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_checked_out = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.name = self.product.name
        self.price = self.quantity * self.price
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"Name: {self.name} Price: {self.price} Quantity: {self.quantity} "


    def delete(self, *args, **kwargs):
        if self.is_checked_out:
            self.delete()



