from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Department, StudyRoom
from .serializers import (
    DepartmentSerializer, 
    StudyRoomListSerializer,
    StudyRoomDetailSerializer,
    StudyRoomAdminSerializer
)
from seat.serializers import RoomSeatLayoutSerializer
import random
import string

class StudyRoomViewSet(viewsets.ModelViewSet):
    """自习室视图集"""
    queryset = StudyRoom.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return StudyRoomListSerializer
        elif self.action == 'retrieve':
            return StudyRoomDetailSerializer
        else:
            return StudyRoomAdminSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'refresh_check_in_code']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def list(self, request):
        """获取自习室列表"""
        queryset = self.get_queryset()
        
        # 处理查询参数，如按院系筛选
        department = request.query_params.get('department')
        if department:
            queryset = queryset.filter(department__name=department)
        
        # 添加关键词搜索功能
        keyword = request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
        
        # 只返回开放的自习室
        queryset = queryset.filter(is_open=True)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """获取自习室详情"""
        study_room = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(study_room)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def seats(self, request, pk=None):
        """获取自习室座位"""
        study_room = get_object_or_404(self.queryset, pk=pk)
        serializer = RoomSeatLayoutSerializer(study_room)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def refresh_check_in_code(self, request, pk=None):
        """刷新签到码 (管理员)"""
        study_room = get_object_or_404(self.queryset, pk=pk)
        # 生成新的随机签到码
        check_in_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        study_room.check_in_code = check_in_code
        study_room.save()
        return Response({'check_in_code': check_in_code})
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """获取附近自习室 (暂时模拟)"""
        # 这里简单返回所有开放的自习室，真实场景可以基于地理位置筛选
        queryset = self.queryset.filter(is_open=True)
        serializer = StudyRoomListSerializer(queryset, many=True)
        return Response(serializer.data)

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """院系视图集 (只读)"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
