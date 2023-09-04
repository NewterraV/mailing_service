# Generated by Django 4.2.4 on 2023-09-04 19:50

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('last_name', models.CharField(max_length=50, verbose_name='фамилия')),
                ('first_name', models.CharField(max_length=50, verbose_name='имя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('is_active', models.BooleanField(default=False, verbose_name='статус верификации')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'permissions': [('list_users', 'Просмотр списка пользователей'), ('block_users', 'Блокировка пользователя')],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('user_code', models.CharField(blank=True, max_length=5, null=True, verbose_name='код верификации')),
                ('verify_code', models.CharField(max_length=5, verbose_name='код верификации')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'код верификации',
                'verbose_name_plural': 'коды верификации',
            },
        ),
    ]
