from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from .models import Payment, Subscription
from .permissions import UserAccessPermission
from .serializers import (
    PaymentSerializer,
    RegistrationSerializer,
    UserSerializer,
)
from .services.stripe import create_product, create_price, create_checkout_session

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


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'Необходимо указать course_id.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course = get_object_or_404(
            Course,
            pk=course_id,
        )

        subscription = Subscription.objects.filter(
            user=request.user,
            course=course,
        )

        if subscription.exists():
            subscription.delete()

            return Response({
                'message': 'Подписка удалена.',
                'is_subscribed': False,
            })

        Subscription.objects.create(
            user=request.user,
            course=course,
        )

        return Response({
            'message': 'Подписка добавлена.',
            'is_subscribed': True,
        })
class PaymentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'Необходимо указать course_id.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course = get_object_or_404(
            Course,
            pk=course_id,
        )

        product = create_product(course)

        price = create_price(
            product_id=product['id'],
            amount=course.price,
        )

        session = create_checkout_session(
            price_id=price['id'],
        )

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method='transfer',
            stripe_product_id=product['id'],
            stripe_price_id=price['id'],
            stripe_session_id=session['id'],
            payment_url=session['url'],
        )

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )