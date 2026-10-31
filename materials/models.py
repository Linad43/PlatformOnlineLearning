from django.conf import settings
from django.db import models


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

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        null=True,
        blank=True,
        verbose_name='Владелец',
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

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True,
        blank=True,
        verbose_name='Владелец',
    )

    def __str__(self):
        return self.title
