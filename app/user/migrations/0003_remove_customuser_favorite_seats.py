# Generated by Django 5.2 on 2025-05-09 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_favorite_seats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='favorite_seats',
        ),
    ]
