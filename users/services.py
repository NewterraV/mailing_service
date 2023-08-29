from random import randint
from django.core.mail import send_mail
from django.conf import settings


def generate_code():
    """Метод генерирует случайное пятизначное число"""
    return str(randint(00000, 99999))


def send_verification_mail(user, code):
    """Метод отправляет на email нового пользователя код для активации аккаунта"""

    send_mail(
        'Подтвердите ваш Email',
        f'Код верификации {code} \n Ссылка для ввода кода верификации: '
        f'http://127.0.0.1:8000/auth/verify/{user.pk}',
        settings.EMAIL_HOST_USER,
        [user.email]
    )


def send_reset_password_mail(email, password):
    """Метод отправляет на email нового пользователя код для активации аккаунта"""

    send_mail(
        'Подтвердите ваш Email',
        f'ваш новый пароль {password} \n Ссылка для входа: '
        f'http://127.0.0.1:8000/auth/login',
        settings.EMAIL_HOST_USER,
        [email]
    )
