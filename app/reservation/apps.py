from django.apps import AppConfig


class ReservationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservation'
    verbose_name = '预约管理'
    
    def ready(self):
        """应用启动时导入信号处理器"""
        import reservation.signals
