from celery import shared_task
from django.core.mail import send_mail

from users.models import Subscription


@shared_task
def send_course_update_email(course_id):
    subscriptions = Subscription.objects.filter(
        course_id=course_id
    ).select_related('user', 'course')

    for subscription in subscriptions:
        send_mail(
            subject=f'Обновление курса: {subscription.course.title}',
            message=(
                f'Курс "{subscription.course.title}" был обновлён.\n'
                f'Зайдите на платформу, чтобы посмотреть изменения.'
            ),
            from_email=None,
            recipient_list=[subscription.user.email],
        )
