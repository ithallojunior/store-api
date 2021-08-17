from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db import models

ON_CHART = 'chart'
ORDERED = 'ordered'
UNDEFINED = 'undefined'  # When something unexpected happens.
SHIPPED = 'shipped'
FINISHED = 'finished'

ORDER_STATUS_CHOICES = (
    (ON_CHART, 'On chart'),
    (ORDERED, 'Ordered'),
    (UNDEFINED, 'Undefined'),
    (SHIPPED, 'Shipped'),
    (FINISHED, 'Finished'),
)


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


class Orders(models.Model):
    """
    Simple order model. For the sake of simplicity,
    every order needs to set an address and credit card info.
    It somewhat copies info from the product, as those can change.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=9,
        default=ON_CHART,
        choices=ORDER_STATUS_CHOICES
    )
    address = models.CharField(max_length=200, null=True)
    payment_details = models.CharField(max_length=300, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
