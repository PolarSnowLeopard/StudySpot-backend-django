from rest_framework import serializers
from .models import Seat, FavoriteSeat
from study_room.models import StudyRoom

class SeatSerializer(serializers.ModelSerializer):
    """基本座位序列化器"""
    class Meta:
        model = Seat
        fields = ['id', 'code', 'status', 'hasSocket', 'room']
    
    hasSocket = serializers.BooleanField(source='has_socket')

class SeatDetailSerializer(serializers.ModelSerializer):
    """座位详情序列化器"""
    roomName = serializers.CharField(source='room.name')
    hasSocket = serializers.BooleanField(source='has_socket')
    features = serializers.SerializerMethodField()
    
    class Meta:
        model = Seat
        fields = ['id', 'code', 'roomId', 'roomName', 'status', 'hasSocket', 'features', 'row', 'column']
    
    def get_features(self, obj):
        """生成座位特点描述"""
        features = []
        if obj.has_socket:
            features.append('有电源')
        if obj.column == 1 or obj.column == 5:  # 假设第一列和最后一列是靠窗的
            features.append('靠窗')
        return '，'.join(features) if features else '无'
    
    def to_representation(self, instance):
        """修改输出格式"""
        ret = super().to_representation(instance)
        ret['roomId'] = str(instance.room.id)
        return ret

class FavoriteSeatSerializer(serializers.ModelSerializer):
    """收藏座位序列化器"""
    roomId = serializers.CharField(source='seat.room.id')
    roomName = serializers.CharField(source='seat.room.name')
    seatCode = serializers.CharField(source='seat.code')
    features = serializers.SerializerMethodField()
    
    class Meta:
        model = FavoriteSeat
        fields = ['id', 'roomId', 'roomName', 'seatCode', 'features']
    
    def get_features(self, obj):
        """生成座位特点描述"""
        features = []
        if obj.seat.has_socket:
            features.append('有电源')
        if obj.seat.column == 1 or obj.seat.column == 5:  # 假设第一列和最后一列是靠窗的
            features.append('靠窗')
        return '，'.join(features) if features else '无'

class RoomSeatLayoutSerializer(serializers.ModelSerializer):
    """自习室座位布局序列化器"""
    columns = serializers.SerializerMethodField()
    rows = serializers.SerializerMethodField()
    seats = serializers.SerializerMethodField()
    
    class Meta:
        model = StudyRoom
        fields = ['columns', 'rows', 'seats']
    
    def get_columns(self, obj):
        """获取房间的列数，默认为5"""
        # 获取当前房间最大列数
        max_column = Seat.objects.filter(room=obj).values_list('column', flat=True).order_by('-column').first()
        return max_column or 5
    
    def get_rows(self, obj):
        """获取房间的行数，默认为4"""
        # 获取当前房间最大行数
        max_row = Seat.objects.filter(room=obj).values_list('row', flat=True).order_by('-row').first()
        return max_row or 4
    
    def get_seats(self, obj):
        """获取房间内所有座位"""
        seats = Seat.objects.filter(room=obj)
        return SeatSerializer(seats, many=True).data 