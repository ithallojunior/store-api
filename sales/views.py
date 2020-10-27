from rest_framework.viewsets import ModelViewSet

from . import models, serializers, permissions


class ProductsView(ModelViewSet):
    """View for the products' CRUD."""

    queryset = models.Products.objects.all()
    permission_classes = [permissions.ProductsPermission]
    serializer_class = serializers.ProductSerializer
    lookup_field = 'name'
