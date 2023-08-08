# Generated by Django 4.2.4 on 2023-08-08 18:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время начала рассылки')),
                ('end_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время окончания рассылки')),
                ('period', models.CharField(max_length=5, verbose_name='Периодичность рассылки')),
                ('state', models.CharField(max_length=10, verbose_name='Статус рассылки')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('name', models.CharField(max_length=50, verbose_name='Краткое название рассылки')),
                ('topic', models.CharField(max_length=200, verbose_name='Тема письма')),
                ('content', models.TextField(verbose_name='Содержание письма')),
                ('settings', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mailing.mailing', verbose_name='Настройки')),
            ],
            options={
                'verbose_name': 'содержание рассылки',
                'verbose_name_plural': 'содержание рассылок',
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last', models.DateTimeField(auto_now=True, verbose_name='Время последней отправки')),
                ('status', models.BooleanField(verbose_name='Статус попытки')),
                ('response', models.TextField(verbose_name='Ответ почтового сервиса')),
                ('mailing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='Логи')),
            ],
            options={
                'verbose_name': 'Лог рассылки',
                'verbose_name_plural': 'Логи рассылки',
            },
        ),
    ]
