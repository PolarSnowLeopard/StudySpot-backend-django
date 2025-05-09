from rest_framework import serializers
from .models import SystemSettings

class SystemSettingsSerializer(serializers.ModelSerializer):
    """系统设置序列化器"""
    class Meta:
        model = SystemSettings
        fields = ['max_reservation_hours', 'advance_reservation_days', 'check_in_grace_period', 'violation_rules', 'violation_limit', 'penalty_days']

class SystemSettingsPublicSerializer(serializers.ModelSerializer):
    """面向普通用户的系统设置序列化器，只返回部分字段"""
    class Meta:
        model = SystemSettings
        fields = ['max_reservation_hours', 'advance_reservation_days', 'check_in_grace_period', 'violation_rules']
        read_only_fields = fields  # 所有字段都为只读

class SystemSettingsAdminSerializer(serializers.ModelSerializer):
    """面向管理员的系统设置序列化器，可以更新所有字段"""
    class Meta:
        model = SystemSettings
        fields = ['max_reservation_hours', 'advance_reservation_days', 'check_in_grace_period', 'violation_rules', 'violation_limit', 'penalty_days'] 