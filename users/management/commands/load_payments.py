
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from materials.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):
    help = 'Создаёт демонстрационные платежи'

    def handle(self, *args, **options):
        user = get_user_model().objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if user is None:
            raise CommandError(
                'Сначала создайте хотя бы одного пользователя.'
            )

        if course is None:
            raise CommandError(
                'Сначала создайте хотя бы один курс.'
            )

        if lesson is None:
            raise CommandError(
                'Сначала создайте хотя бы один урок.'
            )

        payments = [
            Payment(
                user=user,
                course=course,
                amount='5000.00',
                payment_method=Payment.CASH,
            ),
            Payment(
                user=user,
                lesson=lesson,
                amount='1500.00',
                payment_method=Payment.TRANSFER,
            ),
            Payment(
                user=user,
                course=course,
                amount='5000.00',
                payment_method=Payment.TRANSFER,
            ),
        ]

        Payment.objects.bulk_create(payments)

        self.stdout.write(
            self.style.SUCCESS(
                f'Создано платежей: {len(payments)}'
            )
        )
