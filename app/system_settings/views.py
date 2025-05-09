from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SystemSettings
from .serializers import SystemSettingsPublicSerializer, SystemSettingsAdminSerializer

class IsAdminUser(permissions.BasePermission):
    """只允许管理员访问"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class SystemSettingsViewSet(viewsets.GenericViewSet):
    """系统设置视图集"""
    queryset = SystemSettings.objects.all()
    
    def get_object(self):
        """获取唯一的设置实例"""
        return SystemSettings.get_instance()
    
    def get_serializer_class(self):
        """根据用户权限返回不同的序列化器"""
        if self.request.user.is_staff:
            return SystemSettingsAdminSerializer
        return SystemSettingsPublicSerializer
    
    @action(detail=False, methods=['get'])
    def get_settings(self, request):
        """获取系统设置"""
        settings = self.get_object()
        serializer = self.get_serializer(settings)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], permission_classes=[IsAdminUser])
    def update_settings(self, request):
        """更新系统设置（仅管理员）"""
        settings = self.get_object()
        serializer = self.get_serializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public_settings(self, request):
        """获取公开的系统设置（无需登录）"""
        settings = self.get_object()
        serializer = SystemSettingsPublicSerializer(settings)
        return Response(serializer.data)
