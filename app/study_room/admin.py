from django.contrib import admin
from .models import Department, StudyRoom

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(StudyRoom)
class StudyRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'open_time', 'close_time', 'total_seats', 'is_open', 'status']
    list_filter = ['is_open', 'department']
    search_fields = ['name']
    readonly_fields = ['code_refresh_time']
