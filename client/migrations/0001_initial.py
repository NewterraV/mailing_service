# Generated by Django 4.2.4 on 2023-09-04 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='имя')),
                ('surname', models.CharField(blank=True, max_length=50, null=True, verbose_name='отчество')),
                ('last_name', models.CharField(max_length=50, verbose_name='фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='еmail')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
    ]
