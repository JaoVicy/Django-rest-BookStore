from django.db import models
from .category import Category

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.DecimalField(null = True, decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, blank=True)