from django.db import models

# Create your models here.

class Department(models.Model):
    """院系模型"""
    name = models.CharField(max_length=100, verbose_name='院系名称')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "院系"
        verbose_name_plural = "院系"

class StudyRoom(models.Model):
    """自习室模型"""
    name = models.CharField(max_length=100, verbose_name='自习室名称')
    open_time = models.TimeField(verbose_name='开放时间')
    close_time = models.TimeField(verbose_name='关闭时间')
    total_seats = models.IntegerField(verbose_name='总座位数')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属院系')
    is_open = models.BooleanField(default=True, verbose_name='是否开放')
    check_in_code = models.CharField(max_length=20, blank=True, verbose_name='签到码')
    code_refresh_time = models.DateTimeField(auto_now=True, verbose_name='签到码刷新时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "自习室"
        verbose_name_plural = "自习室"
    
    @property
    def available_seats(self):
        """计算可用座位数"""
        # 这里需要导入Seat模型，但由于循环导入问题，我们将在方法内部导入
        from seat.models import Seat
        return Seat.objects.filter(room=self, status='available').count()

    @property
    def status(self):
        """计算自习室状态"""
        available = self.available_seats
        if available == 0:
            return '已满'
        elif available <= 5:  # 假设少于5个座位为"剩余少"
            return '剩余少'
        else:
            return '有空座'
