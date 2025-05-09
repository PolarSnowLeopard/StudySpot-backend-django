from rest_framework import serializers
from .models import Reservation
from study_room.serializers import StudyRoomDetailSerializer
from seat.serializers import SeatSerializer
from user.serializers import UserSerializer
from system_settings.models import SystemSettings

class ReservationSerializer(serializers.ModelSerializer):
    """预约序列化器"""
    
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'room', 'seat', 'date', 'start_time', 'end_time', 
                  'status', 'check_in_time', 'created_at', 'formatted_date', 
                  'can_check_in', 'is_today', 'is_expired']
        read_only_fields = ['id', 'created_at', 'check_in_time', 'formatted_date', 
                           'can_check_in', 'is_today', 'is_expired']

class ReservationDetailSerializer(serializers.ModelSerializer):
    """预约详情序列化器，包含关联模型的详细信息"""
    room = StudyRoomDetailSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'room', 'seat', 'date', 'start_time', 'end_time', 
                  'status', 'check_in_time', 'created_at', 'formatted_date', 
                  'can_check_in', 'is_today', 'is_expired']

class ReservationCreateSerializer(serializers.ModelSerializer):
    """预约创建序列化器"""
    
    class Meta:
        model = Reservation
        fields = ['room', 'seat', 'date', 'start_time', 'end_time']
    
    def validate(self, data):
        """验证预约数据"""
        # 验证结束时间是否大于开始时间
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("结束时间必须大于开始时间")
        
        # 验证时间是否为整点
        if data['start_time'].minute != 0 or data['end_time'].minute != 0:
            raise serializers.ValidationError("预约时间必须为整点")
        
        # 验证预约时长是否超过系统设置的最大值
        max_hours = SystemSettings.get_max_reservation_hours()
        hours_diff = (data['end_time'].hour - data['start_time'].hour)
        if hours_diff > max_hours:
            raise serializers.ValidationError(f"单次预约不能超过{max_hours}小时")
        
        # 验证预约日期是否在允许范围内
        from django.utils import timezone
        today = timezone.localdate()
        advance_days = SystemSettings.get_advance_reservation_days()
        max_date = today + timezone.timedelta(days=advance_days)
        
        if data['date'] < today:
            raise serializers.ValidationError("不能预约过去的日期")
        elif data['date'] > max_date:
            raise serializers.ValidationError(f"只能预约{advance_days}天内的座位")
        
        # 验证座位是否可用
        seat = data['seat']
        if seat.status != 'available':
            raise serializers.ValidationError("该座位不可用")
        
        # 验证该座位在所选时间段内是否已被预约
        from django.db.models import Q
        existing_reservation = Reservation.objects.filter(
            Q(seat=seat) & 
            Q(date=data['date']) &
            Q(status__in=['waiting', 'checked_in']) &
            (
                # 开始时间在已有预约的时间范围内
                (Q(start_time__lte=data['start_time']) & Q(end_time__gt=data['start_time'])) |
                # 结束时间在已有预约的时间范围内
                (Q(start_time__lt=data['end_time']) & Q(end_time__gte=data['end_time'])) |
                # 完全包含已有预约
                (Q(start_time__gte=data['start_time']) & Q(end_time__lte=data['end_time']))
            )
        ).exists()
        
        if existing_reservation:
            raise serializers.ValidationError("该座位在所选时间段内已被预约")
        
        # 验证用户是否有违规记录限制
        user = self.context['request'].user
        violation_limit = SystemSettings.get_violation_limit()
        
        if hasattr(user, 'violations') and user.violations >= violation_limit:
            raise serializers.ValidationError(f"您的违规次数已达到{violation_limit}次，暂时无法预约")
        
        return data

class ReservationListSerializer(serializers.ModelSerializer):
    """预约列表序列化器，用于返回前端列表所需数据格式"""
    roomId = serializers.CharField(source='room.id')
    roomName = serializers.CharField(source='room.name')
    seatId = serializers.CharField(source='seat.id')
    seatCode = serializers.CharField(source='seat.code')
    date = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = ['id', 'roomId', 'roomName', 'seatId', 'seatCode', 'date', 
                  'start_time', 'end_time', 'status']
    
    def get_date(self, obj):
        """获取格式化的日期"""
        return obj.formatted_date 