# Generated by Django 5.1.4 on 2024-12-19 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0004_dayforecast_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dayforecast',
            name='day',
        ),
    ]
