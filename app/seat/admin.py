from django.contrib import admin
from .models import Seat, FavoriteSeat

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'room', 'status', 'has_socket', 'row', 'column']
    list_filter = ['room', 'status', 'has_socket']
    search_fields = ['code', 'room__name']
    list_editable = ['status', 'has_socket']
    
@admin.register(FavoriteSeat)
class FavoriteSeatAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'created_at']
    list_filter = ['user', 'seat__room']
    search_fields = ['user__username', 'seat__code']
    date_hierarchy = 'created_at'
