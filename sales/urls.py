from rest_framework.routers import DefaultRouter

from django.conf.urls import include
from django.urls import path

from . import views


router = DefaultRouter()

router.register(r'products', views.ProductsView, basename='products')
router.register(r'orders', views.OrdersView, basename='orders')
router.register(
    r'staff-order-control',
    views.StaffOrdersView,
    basename='staff-order-control'
)


urlpatterns = [
    path('', include(router.urls)),
]
