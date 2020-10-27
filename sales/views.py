from rest_framework import mixins, permissions, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from . import models, serializers, signals
from .permissions import ProductsPermission


class ProductsView(ModelViewSet):
    """View for the products' CRUD."""

    queryset = models.Products.objects.all()
    permission_classes = [ProductsPermission]
    serializer_class = serializers.ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'price']
    ordering = ['name', '-quantity', '-updated_at']
    ordering_fields = '__all__'
    lookup_field = 'name'


class OrdersView(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 GenericViewSet):
    """This view models orders actions."""

    queryset = models.Orders.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'price']
    ordering = ['-created_at', 'name', '-quantity']
    ordering_fields = '__all__'

    def get_queryset(self):

        # queryset just for schema generation metadata to avoid warnings
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user_orders = self.queryset.filter(user=self.request.user)

        if self.action in ['destroy', 'complete_order']:
            return user_orders.filter(status=models.ON_CHART)

        return user_orders

    def get_serializer_class(self):

        if self.action == 'create':
            return serializers.NewOrderSerializer

        if self.action == 'complete_order':
            return serializers.CompleteOrderSerializer

        return serializers.OrdersSerializer

    @action(detail=False, methods=['post'])
    def complete_order(self, request):
        """Groups and completes an order."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset()

        address = serializer.data['address']
        payment_details = serializer.data['payment_details']

        if queryset.exists():
            for order in queryset:
                order.address = address
                order.payment_details = payment_details
                order.status = models.ORDERED
                order.save()

            return Response(None, status=status.HTTP_201_CREATED)

        return Response(None, status=status.HTTP_404_NOT_FOUND)
