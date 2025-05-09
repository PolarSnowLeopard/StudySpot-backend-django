from django.contrib import admin
from .models import SystemSettings

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['max_reservation_hours', 'advance_reservation_days', 'check_in_grace_period', 'violation_limit', 'penalty_days']
    fieldsets = (
        ('预约设置', {
            'fields': ('max_reservation_hours', 'advance_reservation_days', 'check_in_grace_period')
        }),
        ('违规规则', {
            'fields': ('violation_rules', 'violation_limit', 'penalty_days')
        }),
    )
    
    def has_add_permission(self, request):
        """限制只能有一条记录"""
        return SystemSettings.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        """禁止删除记录"""
        return False
