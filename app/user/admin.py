from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # 展示哪些字段
    list_display = ('username', 'studentId', 'department', 'email', 'is_staff')
    # 编辑页面分组
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('studentId', 'department', 'avatar', 'phone', 'totalReservations', 'totalHours', 'violations')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('扩展信息', {'fields': ('studentId', 'department', 'avatar', 'phone', 'totalReservations', 'totalHours', 'violations')}),
    )
