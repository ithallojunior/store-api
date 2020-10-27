from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):
    """Simple serializer to the products."""

    class Meta:
        model = models.Products
        fields = '__all__'
