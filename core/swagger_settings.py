from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions


schema_view = get_schema_view(

    openapi.Info(
        title="Store",
        default_version='v1',
        description="Store API",
    ),

    public=True,
    url='http://localhost:8000',
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)
