from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from django.contrib.auth.models import User

from . import serializers, permissions


class UserView(mixins.CreateModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               GenericViewSet):
    """Deals with user data manipulation."""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.UserPermission]
    lookup_field = 'username'


class UserAPIView(APIView):
    """Simply returns basic user info."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Gathers and returns user info."""

        fields = ['first_name', 'last_name', 'email']
        info = {field: getattr(request.user, field, '') for field in fields}
        return Response(info)
