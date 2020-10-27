from django.db.models import Sum

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models


class ProductSerializer(serializers.ModelSerializer):
    """Simple serializer to the products."""

    class Meta:
        model = models.Products
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    """Shows orders."""

    url = serializers.HyperlinkedIdentityField(
        view_name='products-detail',
        lookup_field='name',
        read_only=True,
        default=None
    )
    unity_price = serializers.SerializerMethodField()

    def get_unity_price(self, order):
        return order.total_price/order.quantity

    class Meta:
        model = models.Orders
        fields = '__all__'


class NewOrderSerializer(serializers.ModelSerializer):
    """Makes an order possible."""

    def validate(self, data):
        """Making sure there is enough product."""

        quantity = data['quantity']
        product = data['product']

        available = product.quantity
        on_chart = models.Orders.objects.filter(
            product=product,
            status=models.ON_CHART
        ).aggregate(Sum('quantity')).get('quantity__sum') or 0

        if quantity > (available - on_chart):
            raise ValidationError({
                'quantity': [
                    f'The requested quantity of {product.name} cannot be provided.'
                ]
            })

        return data

    def create(self, validated_data):

        product = validated_data['product']
        quantity = validated_data['quantity']

        validated_data['name'] = product.name
        validated_data['description'] = product.description
        validated_data['total_price'] = quantity * product.price

        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    class Meta:
        model = models.Orders
        fields = ['product', 'quantity']


class CompleteOrderSerializer(serializers.ModelSerializer):
    """Receives the last details and finishes a order """

    class Meta:
        model = models.Orders
        fields = ['address', 'payment_details']
        extra_kwarg = {
            'address': {'required': True},
            'payment_details': {'required': True}
        }


class OrdersStaffSerializer(serializers.ModelSerializer):
    """A serializer for the staff to update product status."""

    def validate_status(self, status):
        """Limiting status movimentation."""

        previous = self.instance.status

        if previous == models.ON_CHART or status == models.ON_CHART:

            raise ValidationError({
                'status': ['Staff cannot alter from/to this status.']
            })

        return status

    class Meta:
        model = models.Orders
        fields = ['status']
