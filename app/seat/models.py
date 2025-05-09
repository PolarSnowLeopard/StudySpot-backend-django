from django.db import models
from study_room.models import StudyRoom
from user.models import CustomUser

class Seat(models.Model):
    """座位模型"""
    STATUS_CHOICES = (
        ('available', '可用'),
        ('occupied', '已占用'),
        ('maintenance', '维护中'),
    )
    
    id = models.CharField(primary_key=True, max_length=20, verbose_name='座位ID')
    code = models.CharField(max_length=20, verbose_name='座位编号')
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='seats', verbose_name='所属自习室')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    has_socket = models.BooleanField(default=False, verbose_name='有电源')
    row = models.IntegerField(verbose_name='行号')
    column = models.IntegerField(verbose_name='列号')
    
    def __str__(self):
        return f"{self.room.name}-{self.code}"
    
    class Meta:
        verbose_name = "座位"
        verbose_name_plural = "座位"
        unique_together = ('room', 'code')

class FavoriteSeat(models.Model):
    """收藏座位模型"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorite_seat_records', verbose_name='用户')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name='座位')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = "收藏座位"
        verbose_name_plural = "收藏座位"
        unique_together = ('user', 'seat')
    
    def __str__(self):
        return f"{self.user.username}-{self.seat.code}"
