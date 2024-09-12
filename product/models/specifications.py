from django.db import models




class ProductSpecification(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    specification = models.JSONField()
