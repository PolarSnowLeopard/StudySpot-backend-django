from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'title', 'is_read', 'time']
    list_filter = ['type', 'is_read', 'time']
    search_fields = ['user__username', 'title', 'content']
    date_hierarchy = 'time'
    readonly_fields = ['time']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """标记为已读"""
        queryset.update(is_read=True)
        self.message_user(request, f"已将{queryset.count()}条通知标记为已读")
    mark_as_read.short_description = "标记为已读"
    
    def mark_as_unread(self, request, queryset):
        """标记为未读"""
        queryset.update(is_read=False)
        self.message_user(request, f"已将{queryset.count()}条通知标记为未读")
    mark_as_unread.short_description = "标记为未读"
