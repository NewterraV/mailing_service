from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Settings(models.Model):
    """
    Модель описывающая настройки рассылки
    """

    time = models.DurationField(verbose_name='Время рассылки')
    period = models.CharField(max_length=5, verbose_name='Периодичность рассылки')  # day, week, month
    state = models.CharField(max_length=10, verbose_name='Статус рассылки')  # completed, created, launched

    def __str__(self):
        return f'{self.time} - {self.period}:{self.state}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылок'


class Content(models.Model):
    """
    Модель описывающая содержание рассылки
    """

    name = models.CharField(max_length=50, verbose_name='Краткое название рассылки')
    topic = models.CharField(max_length=200, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Содержание письма')
    settings = models.ForeignKey(Settings, **NULLABLE, on_delete=models.CASCADE, verbose_name='Настройки')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Logs(models.Model):
    """

    Модель описывающая логи рассылок
    """

    mailing = models.ForeignKey(Content, **NULLABLE, on_delete=models.CASCADE, verbose_name='Логи')
    last = models.DateTimeField(auto_now=True, verbose_name='Время последней отправки')
    status = models.BooleanField(verbose_name='Статус попытки')
    response = models.TextField(verbose_name='Ответ почтового сервиса')

    def __str__(self):
        return f'{self.last} - {self.status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
