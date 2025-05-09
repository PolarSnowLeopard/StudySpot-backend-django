from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'
    verbose_name = '通知管理'
    
    def ready(self):
        """应用启动时导入信号处理器"""
        import notification.signals
