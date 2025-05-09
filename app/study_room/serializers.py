from rest_framework import serializers
from .models import Department, StudyRoom

class DepartmentSerializer(serializers.ModelSerializer):
    """院系序列化器"""
    class Meta:
        model = Department
        fields = ['id', 'name']

class StudyRoomListSerializer(serializers.ModelSerializer):
    """自习室列表序列化器"""
    department = serializers.StringRelatedField(read_only=True)
    status = serializers.ReadOnlyField()
    availableSeats = serializers.SerializerMethodField()
    
    class Meta:
        model = StudyRoom
        fields = ['id', 'name', 'openTime', 'closeTime', 'status', 'availableSeats', 'totalSeats', 'department']
    
    def get_availableSeats(self, obj):
        return obj.available_seats
    
    def to_representation(self, instance):
        # 将字段名称转换为前端需要的驼峰命名格式
        ret = super().to_representation(instance)
        ret['openTime'] = instance.open_time.strftime('%H:%M')
        ret['closeTime'] = instance.close_time.strftime('%H:%M')
        if isinstance(instance.department, Department):
            ret['department'] = instance.department.name
        else:
            ret['department'] = '全校开放'
        return ret

class StudyRoomDetailSerializer(serializers.ModelSerializer):
    """自习室详情序列化器"""
    department = serializers.StringRelatedField(read_only=True)
    status = serializers.ReadOnlyField()
    availableSeats = serializers.SerializerMethodField()
    
    class Meta:
        model = StudyRoom
        fields = ['id', 'name', 'openTime', 'closeTime', 'status', 'availableSeats', 'totalSeats', 'department', 'is_open']
    
    def get_availableSeats(self, obj):
        return obj.available_seats
    
    def to_representation(self, instance):
        # 将字段名称转换为前端需要的驼峰命名格式
        ret = super().to_representation(instance)
        ret['openTime'] = instance.open_time.strftime('%H:%M')
        ret['closeTime'] = instance.close_time.strftime('%H:%M')
        if isinstance(instance.department, Department):
            ret['department'] = instance.department.name
        else:
            ret['department'] = '全校开放'
        return ret

class StudyRoomAdminSerializer(serializers.ModelSerializer):
    """管理员使用的自习室序列化器"""
    class Meta:
        model = StudyRoom
        fields = ['id', 'name', 'open_time', 'close_time', 'total_seats', 'department', 'is_open', 'check_in_code']
        read_only_fields = ['code_refresh_time'] 