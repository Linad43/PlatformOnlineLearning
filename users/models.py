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
