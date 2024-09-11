from django.db import models




class ProductSpecification(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class GeneralFeatures(models.Model):
    sim_choices = (
        ("Dual_Sim", "Dual_Sim"),
        ("Single_Sim", "Single_Sim"),
    )
    product = models.ForeignKey("ProductSpecification", on_delete=models.CASCADE)
    release_date = models.DateField(null=True, blank=True)
    sim_support = models.CharField(max_length=10, choices=sim_choices, null=True, blank=True)
    dimensions = models.CharField(max_length=55, default=0, null=True, blank=True)
    weight = models.FloatField(default=0, null=True, blank=True)
    operating_system = models.CharField(max_length=55, null=True, blank=True)
    battery_mah = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Display(models.Model):
    product = models.ForeignKey("ProductSpecification", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    size = models.IntegerField(null=True, blank=True)
    resolution = models.CharField(max_length=55, null=True, blank=True)
    type = models.CharField(max_length=55, null=True, blank=True)
    protection = models.CharField(max_length=55, null=True, blank=True)

class Camera(models.Model):
    pass