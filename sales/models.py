from django.db import models
from django.core.validators import MinValueValidator


class Products(models.Model):
    """Modelates the products to be sold."""

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
