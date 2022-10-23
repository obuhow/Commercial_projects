from datetime import datetime

from django.db import models


class ScheduledPosts(models.Model):
    sending_datetime = models.CharField(
        max_length=20,
        verbose_name='Дата отправки',
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    )
    channel_id = models.IntegerField(
        verbose_name='ID канала',
        default=-1001516084523,
    )
    url = models.CharField(
        max_length=256,
        verbose_name='URL статьи',
        default='https://sweetspeak.ru/',
    )
    post = models.TextField(
        verbose_name='Пост',
        default = 'Этот пост еще не написан',
    )

    def __str__(self):
        return f'Пост'

    class Meta:
        verbose_name = 'Расписание постов'
        verbose_name_plural = 'Расписание постов'


class PublishedPosts(ScheduledPosts):

    class Meta:
        verbose_name = 'Опубликованные посты'
        verbose_name_plural = 'Опубликованные посты'
