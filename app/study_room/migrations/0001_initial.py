# Generated by Django 5.2 on 2025-05-08 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='院系名称')),
            ],
        ),
        migrations.CreateModel(
            name='StudyRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='自习室名称')),
                ('open_time', models.TimeField(verbose_name='开放时间')),
                ('close_time', models.TimeField(verbose_name='关闭时间')),
                ('total_seats', models.IntegerField(verbose_name='总座位数')),
                ('is_open', models.BooleanField(default=True, verbose_name='是否开放')),
                ('check_in_code', models.CharField(blank=True, max_length=20, verbose_name='签到码')),
                ('code_refresh_time', models.DateTimeField(auto_now=True, verbose_name='签到码刷新时间')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='study_room.department', verbose_name='所属院系')),
            ],
        ),
    ]
