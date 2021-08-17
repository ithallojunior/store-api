from datetime import datetime

from django.test import TestCase

from sales.models import Products
from sales.serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):
    """Test cases for the ProductSerializer."""

    def setUp(self):
        self.data = {
            "name": "Bottle",
            "description": "A water bottle.",
            "quantity": 10,
            "price": "2.00"
        }

        Products.objects.create(**self.data)

    def test_valid_fields(self):
        """Asserts valid fields."""

        serializer = ProductSerializer(Products.objects.last())
        fields = [
            'id', 'name', 'description', 'quantity',
            'price', 'created_at', 'updated_at'
        ]
        self.assertEqual(list(serializer.data.keys()), fields)

    def test_missing_fields(self):
        """Passing with missing values."""

        serializer = ProductSerializer(data=self.data)

        self.assertFalse(serializer.is_valid())

    def test_all_fields(self):
        """Passing with all values."""

        data = Products.objects.all().values()[0]
        data['name'] = 'New Bottle'  # A  new product.

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())
