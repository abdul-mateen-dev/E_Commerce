from django.contrib import admin

from .models import ProductSpecification,Category,Product,Brand,ProductImage,Rating

admin.site.register(ProductSpecification)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Rating)
admin.site.register(ProductImage)
