from django.db import models
from user.models import CustomUser
from reservation.models import Reservation

class Notification(models.Model):
    """通知模型"""
    TYPE_CHOICES = (
        ('system', '系统通知'),
        ('reservation', '预约通知'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications', verbose_name='用户')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='类型')
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='相关预约')
    
    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-time']
    
    def __str__(self):
        return f"{self.user.username}-{self.title}"
    
    @classmethod
    def create_reservation_notification(cls, user, reservation, title, content):
        """创建预约相关通知"""
        return cls.objects.create(
            user=user,
            type='reservation',
            title=title,
            content=content,
            reservation=reservation
        )
    
    @classmethod
    def create_system_notification(cls, user, title, content):
        """创建系统通知"""
        return cls.objects.create(
            user=user,
            type='system',
            title=title,
            content=content
        )
