from django.db import models
from django.utils.timezone import now

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    """
    Модель описывающая настройки рассылки
    """

    start_time = models.DateTimeField(default=now, verbose_name='Время начала рассылки')
    end_time = models.DateTimeField(default=now, verbose_name='Время окончания рассылки')
    period = models.CharField(max_length=5, verbose_name='Периодичность рассылки')  # day, week, month
    state = models.CharField(max_length=10, verbose_name='Статус рассылки')  # completed, created, launched

    def __str__(self):
        return f'{self.start_time} - {self.end_time}:{self.state}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Content(models.Model):
    """
    Модель описывающая содержание рассылки
    """

    name = models.CharField(max_length=50, verbose_name='Краткое название рассылки')
    topic = models.CharField(max_length=200, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Содержание письма')
    settings = models.OneToOneField(Mailing, on_delete=models.CASCADE,  primary_key=True, verbose_name='Настройки')

    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = 'содержание рассылки'
        verbose_name_plural = 'содержание рассылок'


class Logs(models.Model):
    """

    Модель описывающая логи рассылок
    """

    mailing = models.ForeignKey(Mailing, **NULLABLE, on_delete=models.CASCADE, verbose_name='Логи')
    last = models.DateTimeField(auto_now=True, verbose_name='Время последней отправки')
    status = models.BooleanField(verbose_name='Статус попытки')
    response = models.TextField(verbose_name='Ответ почтового сервиса')

    def __str__(self):
        return f'{self.last} - {self.status}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
