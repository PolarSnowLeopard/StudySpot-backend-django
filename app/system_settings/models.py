from django.db import models
from django.core.cache import cache

class SystemSettings(models.Model):
    """系统设置模型，只有一条记录"""
    max_reservation_hours = models.IntegerField(default=4, verbose_name='最大预约小时数')
    advance_reservation_days = models.IntegerField(default=7, verbose_name='提前预约天数')
    check_in_grace_period = models.IntegerField(default=15, verbose_name='签到宽限期（分钟）')
    violation_rules = models.TextField(default='累计3次限制预约1天', verbose_name='违规规则')
    violation_limit = models.IntegerField(default=3, verbose_name='违规次数限制')
    penalty_days = models.IntegerField(default=1, verbose_name='违规惩罚天数')
    
    class Meta:
        verbose_name = '系统设置'
        verbose_name_plural = '系统设置'
    
    def __str__(self):
        return "系统设置"
    
    def save(self, *args, **kwargs):
        """保存时更新缓存"""
        super().save(*args, **kwargs)
        # 将设置保存到缓存
        self.update_cache()
    
    def update_cache(self):
        """更新缓存中的设置"""
        cache.set('system_settings', {
            'max_reservation_hours': self.max_reservation_hours,
            'advance_reservation_days': self.advance_reservation_days,
            'check_in_grace_period': self.check_in_grace_period,
            'violation_rules': self.violation_rules,
            'violation_limit': self.violation_limit,
            'penalty_days': self.penalty_days
        }, timeout=86400)  # 缓存一天
    
    @classmethod
    def get_settings(cls):
        """获取系统设置，优先从缓存获取"""
        settings = cache.get('system_settings')
        if not settings:
            # 缓存不存在，从数据库获取
            instance = cls.get_instance()
            instance.update_cache()
            settings = cache.get('system_settings')
        return settings
    
    @classmethod
    def get_instance(cls):
        """获取设置实例，如果不存在则创建"""
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls.objects.create()
    
    @classmethod
    def get_max_reservation_hours(cls):
        """获取最大预约小时数"""
        settings = cls.get_settings()
        return settings.get('max_reservation_hours', 4)
    
    @classmethod
    def get_advance_reservation_days(cls):
        """获取提前预约天数"""
        settings = cls.get_settings()
        return settings.get('advance_reservation_days', 7)
    
    @classmethod
    def get_check_in_grace_period(cls):
        """获取签到宽限期（分钟）"""
        settings = cls.get_settings()
        return settings.get('check_in_grace_period', 15)
    
    @classmethod
    def get_violation_limit(cls):
        """获取违规次数限制"""
        settings = cls.get_settings()
        return settings.get('violation_limit', 3)
    
    @classmethod
    def get_penalty_days(cls):
        """获取违规惩罚天数"""
        settings = cls.get_settings()
        return settings.get('penalty_days', 1)
