from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'seat', 'date', 'start_time', 'end_time', 'status', 'check_in_time']
    list_filter = ['status', 'date', 'room']
    search_fields = ['user__username', 'user__studentId', 'room__name', 'seat__code']
    date_hierarchy = 'date'
    list_per_page = 20
    readonly_fields = ['created_at']
    
    actions = ['mark_as_checked_in', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_checked_in(self, request, queryset):
        """标记为已签到"""
        queryset.filter(status='waiting').update(status='checked_in')
        self.message_user(request, f"已将{queryset.filter(status='waiting').count()}个预约标记为已签到")
    mark_as_checked_in.short_description = "标记为已签到"
    
    def mark_as_completed(self, request, queryset):
        """标记为已完成"""
        queryset.filter(status__in=['waiting', 'checked_in']).update(status='completed')
        self.message_user(request, f"已将{queryset.filter(status__in=['waiting', 'checked_in']).count()}个预约标记为已完成")
    mark_as_completed.short_description = "标记为已完成"
    
    def mark_as_cancelled(self, request, queryset):
        """标记为已取消"""
        queryset.filter(status__in=['waiting']).update(status='cancelled')
        self.message_user(request, f"已将{queryset.filter(status__in=['waiting']).count()}个预约标记为已取消")
    mark_as_cancelled.short_description = "标记为已取消"
