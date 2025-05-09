from rest_framework import serializers
from .models import DailyStatistics, HourlyStatistics
from study_room.serializers import StudyRoomListSerializer

class DailyStatisticsSerializer(serializers.ModelSerializer):
    """每日统计序列化器"""
    room_detail = StudyRoomListSerializer(source='room', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = DailyStatistics
        fields = ['id', 'room', 'room_name', 'room_detail', 'date', 'total_reservations', 'total_hours', 'usage_rate']
        read_only_fields = fields

class HourlyStatisticsSerializer(serializers.ModelSerializer):
    """每小时统计序列化器"""
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = HourlyStatistics
        fields = ['id', 'room', 'room_name', 'date', 'hour', 'occupied_seats', 'usage_rate']
        read_only_fields = fields

class RoomStatisticsSerializer(serializers.Serializer):
    """自习室统计汇总序列化器"""
    id = serializers.IntegerField(source='room.id')
    name = serializers.CharField(source='room.name')
    usage_rate = serializers.FloatField()
    usage_count = serializers.IntegerField(source='total_reservations') 