from django.db import models
from mailing.models import NULLABLE
from django.conf import settings


class Client(models.Model):
    """Модель описывающая получателя рассылки"""

    first_name = models.CharField(max_length=50, verbose_name='имя')
    surname = models.CharField(max_length=50, verbose_name='отчество', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    email = models.EmailField(verbose_name='еmail')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
