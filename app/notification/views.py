from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer, NotificationListSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """通知视图集，只允许读取操作"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationListSerializer
    
    def get_queryset(self):
        """只返回当前用户的通知"""
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """将所有通知标记为已读"""
        notifications = self.get_queryset().filter(is_read=False)
        count = notifications.count()
        notifications.update(is_read=True)
        return Response({"detail": f"已将{count}条通知标记为已读"})
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """将单条通知标记为已读"""
        notification = self.get_object()
        if notification.is_read:
            return Response({"detail": "该通知已读"})
        
        notification.is_read = True
        notification.save()
        return Response({"detail": "已将通知标记为已读"})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """获取未读通知数量"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({"count": count})
