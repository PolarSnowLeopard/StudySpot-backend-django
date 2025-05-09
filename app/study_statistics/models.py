from django.db import models
from django.utils import timezone
import datetime
from study_room.models import StudyRoom

class DailyStatistics(models.Model):
    """每日统计数据"""
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, verbose_name='自习室')
    date = models.DateField(verbose_name='日期')
    total_reservations = models.IntegerField(default=0, verbose_name='总预约数')
    total_hours = models.IntegerField(default=0, verbose_name='总使用小时数')
    usage_rate = models.FloatField(default=0, verbose_name='使用率')
    
    class Meta:
        verbose_name = '每日统计'
        verbose_name_plural = '每日统计'
        unique_together = ('room', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.room.name}-{self.date}"
    
    @classmethod
    def calculate_statistics(cls, room, date):
        """计算某自习室某日的统计数据"""
        from reservation.models import Reservation
        
        # 获取该自习室在特定日期的所有完成和使用中的预约
        reservations = Reservation.objects.filter(
            room=room,
            date=date, 
            status__in=['completed', 'checked_in']
        )
        
        # 计算总预约数
        total_reservations = reservations.count()
        
        # 计算总使用小时数
        total_hours = 0
        for reservation in reservations:
            start_hour = reservation.start_time.hour
            end_hour = reservation.end_time.hour
            hours = end_hour - start_hour
            total_hours += hours
        
        # 计算使用率
        # 假设自习室开放12小时 (从7点到19点), 有50个座位
        open_hours = (room.close_time.hour - room.open_time.hour)
        max_usage = open_hours * room.total_seats
        
        usage_rate = 0
        if max_usage > 0:
            usage_rate = (total_hours / max_usage) * 100
        
        # 创建或更新统计记录
        stats, created = cls.objects.update_or_create(
            room=room,
            date=date,
            defaults={
                'total_reservations': total_reservations,
                'total_hours': total_hours,
                'usage_rate': usage_rate
            }
        )
        
        return stats

class HourlyStatistics(models.Model):
    """每小时统计数据"""
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, verbose_name='自习室')
    date = models.DateField(verbose_name='日期')
    hour = models.IntegerField(verbose_name='小时(0-23)')
    occupied_seats = models.IntegerField(default=0, verbose_name='占用座位数')
    usage_rate = models.FloatField(default=0, verbose_name='使用率')
    
    class Meta:
        verbose_name = '每小时统计'
        verbose_name_plural = '每小时统计'
        unique_together = ('room', 'date', 'hour')
        ordering = ['-date', 'hour']
    
    def __str__(self):
        return f"{self.room.name}-{self.date}-{self.hour}点"
    
    @classmethod
    def calculate_statistics(cls, room, date, hour):
        """计算某自习室某日某小时的统计数据"""
        from reservation.models import Reservation
        
        # 获取该小时内的所有预约
        reservations = Reservation.objects.filter(
            room=room,
            date=date,
            status__in=['completed', 'checked_in'],
            start_time__lte=datetime.time(hour, 59),
            end_time__gte=datetime.time(hour, 0)
        )
        
        # 计算占用座位数
        occupied_seats = reservations.count()
        
        # 计算使用率
        usage_rate = 0
        if room.total_seats > 0:
            usage_rate = (occupied_seats / room.total_seats) * 100
        
        # 创建或更新统计记录
        stats, created = cls.objects.update_or_create(
            room=room,
            date=date,
            hour=hour,
            defaults={
                'occupied_seats': occupied_seats,
                'usage_rate': usage_rate
            }
        )
        
        return stats
