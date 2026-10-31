from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny

from .models import Payment
from .permissions import UserAccessPermission
from .serializers import (
    PaymentSerializer,
    RegistrationSerializer,
    UserSerializer,
)

User = get_user_model()


class RegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [UserAccessPermission]
    http_method_names = [
        'get', 'put', 'patch', 'delete', 'head', 'options'
    ]

    def get_queryset(self) -> QuerySet:
        user = self.request.user

        if not user.is_authenticated:
            return User.objects.none()

        is_moderator = user.groups.filter(
            name='Модераторы'
        ).exists()

        if user.is_superuser or is_moderator:
            return User.objects.all()

        return User.objects.filter(pk=user.pk)

    def perform_update(self, serializer):
        serializer.save()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        'course',
        'lesson',
        'payment_method',
    ]
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.groups.filter(
                name='Модераторы'
        ).exists():
            return Payment.objects.all()

        return Payment.objects.filter(user=user)
