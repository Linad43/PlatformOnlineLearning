from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Payment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'phone',
            'city',
            'avatar',
            'password',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        if not password:
            raise serializers.ValidationError({
                'password': 'Это поле обязательно.'
            })

        return User.objects.create_user(
            password=password,
            **validated_data,
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            validate_password(password, user=instance)
            instance.set_password(password)

        instance.save()
        return instance


class RegistrationSerializer(UserSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', 'payment_date')
