from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PaymentListAPIView,
    RegistrationAPIView,
    UserViewSet,
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
]
