from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон',
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Город',
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название курса',
    )
    preview = models.ImageField(
        upload_to='courses/',
        blank=True,
        null=True,
        verbose_name='Превью',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название урока',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    preview = models.ImageField(
        upload_to='lessons/',
        blank=True,
        null=True,
        verbose_name='Превью',
    )
    video_url = models.URLField(
        blank=True,
        verbose_name='Ссылка на видео',
    )

    def __str__(self):
        return self.title


class Payment(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'

    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь',
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Оплаченный курс',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Оплаченный урок',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты',
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты',
    )

    def __str__(self):
        return f'Платёж №{self.pk} — {self.amount}'
