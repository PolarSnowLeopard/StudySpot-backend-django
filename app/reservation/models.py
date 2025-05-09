from django.db import models
from django.utils import timezone
from user.models import CustomUser
from study_room.models import StudyRoom
from seat.models import Seat

class Reservation(models.Model):
    """预约模型"""
    STATUS_CHOICES = (
        ('waiting', '待签到'),
        ('checked_in', '使用中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('expired', '已过期'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reservations', verbose_name='用户')
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, verbose_name='自习室')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name='座位')
    date = models.DateField(verbose_name='日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name='状态')
    check_in_time = models.DateTimeField(null=True, blank=True, verbose_name='签到时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    check_in_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='签到码')
    
    class Meta:
        verbose_name = '预约'
        verbose_name_plural = '预约'
        ordering = ['-date', '-start_time']
    
    def __str__(self):
        return f"{self.user.username}-{self.room.name}-{self.seat.code}"
    
    @property
    def is_today(self):
        """判断预约是否为今天"""
        return self.date == timezone.localdate()
    
    @property
    def is_expired(self):
        """判断预约是否已过期"""
        if self.status == 'waiting':
            now = timezone.localtime()
            reservation_datetime = timezone.make_aware(
                timezone.datetime.combine(self.date, self.start_time))
            # 超过15分钟未签到视为过期
            return now > reservation_datetime + timezone.timedelta(minutes=15)
        return False
    
    @property
    def can_check_in(self):
        """判断是否可以签到"""
        if self.status != 'waiting':
            return False
        
        now = timezone.localtime()
        reservation_date = self.date
        
        # 检查是否是预约当天
        if reservation_date != now.date():
            return False
        
        # 提前15分钟可以签到
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(reservation_date, self.start_time))
        earliest_check_in = start_datetime - timezone.timedelta(minutes=15)
        
        # 迟到15分钟内可以签到
        latest_check_in = start_datetime + timezone.timedelta(minutes=15)
        
        return earliest_check_in <= now <= latest_check_in
    
    @property
    def formatted_date(self):
        """格式化日期显示"""
        today = timezone.localdate()
        if self.date == today:
            return '今天'
        elif self.date == today + timezone.timedelta(days=1):
            return '明天'
        elif self.date == today - timezone.timedelta(days=1):
            return '昨天'
        elif self.date == today - timezone.timedelta(days=2):
            return '前天'
        else:
            return self.date.strftime('%Y-%m-%d')
