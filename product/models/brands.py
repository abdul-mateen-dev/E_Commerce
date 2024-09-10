from django.db import models
from .category import Category


class Brand(models.Model):
    name = models.CharField(max_length=255)
    category  = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name