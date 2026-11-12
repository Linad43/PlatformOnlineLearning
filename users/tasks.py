from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def deactivate_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)

    User = get_user_model()

    users = User.objects.filter(
        last_login__lt=month_ago,
        is_active=True,
    )

    count = users.update(is_active=False)

    return f'Деактивировано пользователей: {count}'