from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    studentId = models.CharField(max_length=20, unique=True, verbose_name='学号')
    department = models.CharField(max_length=100, verbose_name='学院')
    avatar = models.CharField(max_length=255, default='/assets/icons/default-avatar.png', verbose_name='头像')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    totalReservations = models.IntegerField(default=0)
    totalHours = models.IntegerField(default=0)
    violations = models.IntegerField(default=0)
