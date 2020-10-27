from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework.routers import DefaultRouter

from django.conf.urls import include
from django.urls import path

from . import views


router = DefaultRouter()

router.register(r'user', views.UserView, basename='user')

urlpatterns = [

    # Django JWT urls
    path('', TokenObtainPairView.as_view(), name='login'),
    path('/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('/verify', TokenVerifyView.as_view(), name='token-verify'),

    path('/', include(router.urls)),

    path(r'/user',  views.UserAPIView.as_view(), name='user-detail'),

]
