# Generated by Django 4.2.4 on 2023-09-04 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date_publish',
            field=models.DateField(auto_now=True),
        ),
    ]
