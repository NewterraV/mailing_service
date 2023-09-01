from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Команда для создания администратора"""

    def handle(self, *args, **options):
        email = input('Введите email: ')
        user = User.objects.create(email=email, is_superuser=True, is_staff=True, )

        while True:
            password = input('Введите пароль: ')
            password_2 = input('Повторите пароль: ')

            if password == password_2:
                user.set_password(password)
                user.is_active = True
                user.save()
                return

            print('Пароли не совпали, попробуйте еще раз')
