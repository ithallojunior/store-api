"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, re_path, include
from django.conf.urls import url

from .swagger_settings import schema_view


urlpatterns = [

    re_path(
        '^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='swagger-ui'
    ),

    path('admin/', admin.site.urls),

    # Store auth urls.
    url('auth', include('store_auth.urls')),

    # Sales urls.
    url('', include('sales.urls')),

]

urlpatterns = [
    path('', lambda r: redirect('swagger-ui')),
    path('api/v1/', include(urlpatterns)),
]
