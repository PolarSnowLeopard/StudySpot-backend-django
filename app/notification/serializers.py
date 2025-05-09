from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """通知序列化器"""
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'content', 'time', 'is_read', 'reservation']
        read_only_fields = ['id', 'type', 'title', 'content', 'time', 'reservation']

class NotificationListSerializer(serializers.ModelSerializer):
    """通知列表序列化器，符合前端mock数据格式"""
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    reservationId = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'content', 'time', 'isRead', 'reservationId']
    
    def get_reservationId(self, obj):
        """获取预约ID"""
        if obj.reservation:
            return str(obj.reservation.id)
        return None
    
    def to_representation(self, instance):
        """将字段名转换为前端需要的驼峰命名格式"""
        ret = super().to_representation(instance)
        ret['isRead'] = instance.is_read
        return ret 