from django.contrib.auth.models import AbstractUser
from django.db import models
from mailing.models import NULLABLE


class User(AbstractUser):
    username = None
    last_name = models.CharField(max_length=50, verbose_name='имя')
    first_name = models.CharField(max_length=50, verbose_name='фамилия')
    email = models.EmailField(verbose_name='email', unique=True)
    is_active = models.BooleanField(
        default=False, verbose_name='статус верификации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class VerifyCode(models.Model):
    user_code = models.CharField(max_length=5, **NULLABLE, verbose_name='код верификации')
    verify_code = models.CharField(max_length=5, verbose_name='код верификации')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='пользователь')

    class Meta:
        verbose_name = 'код верификации'
        verbose_name_plural = 'коды верификации'

