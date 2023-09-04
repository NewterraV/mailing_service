from django.db import models


class Blog(models.Model):
    """Модель описывающая Блог"""

    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержание')
    image = models.ImageField(verbose_name='изображение')
    view_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')
    date_publish = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
