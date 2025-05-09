from django.contrib import admin
from .models import DailyStatistics, HourlyStatistics

@admin.register(DailyStatistics)
class DailyStatisticsAdmin(admin.ModelAdmin):
    list_display = ['room', 'date', 'total_reservations', 'total_hours', 'usage_rate']
    list_filter = ['room', 'date']
    date_hierarchy = 'date'
    search_fields = ['room__name']
    readonly_fields = ['total_reservations', 'total_hours', 'usage_rate']

@admin.register(HourlyStatistics)
class HourlyStatisticsAdmin(admin.ModelAdmin):
    list_display = ['room', 'date', 'hour', 'occupied_seats', 'usage_rate']
    list_filter = ['room', 'date', 'hour']
    date_hierarchy = 'date'
    search_fields = ['room__name']
    readonly_fields = ['occupied_seats', 'usage_rate']
