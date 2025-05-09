from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Reservation
from .serializers import (
    ReservationSerializer, 
    ReservationDetailSerializer,
    ReservationCreateSerializer,
    ReservationListSerializer
)
from seat.models import Seat

class ReservationViewSet(viewsets.ModelViewSet):
    """预约视图集"""
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'create':
            return ReservationCreateSerializer
        elif self.action == 'list':
            return ReservationListSerializer
        elif self.action in ['retrieve', 'user_reservations']:
            return ReservationDetailSerializer
        return ReservationSerializer
    
    def perform_create(self, serializer):
        """创建预约时自动设置用户为当前用户"""
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """创建预约"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 创建成功后返回完整预约信息
        reservation = Reservation.objects.get(pk=serializer.instance.pk)
        response_serializer = ReservationListSerializer(reservation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def user_reservations(self, request):
        """获取当前用户的所有预约"""
        reservations = Reservation.objects.filter(user=request.user)
        
        # 筛选条件
        status_filter = request.query_params.get('status')
        date_filter = request.query_params.get('date')
        
        if status_filter:
            reservations = reservations.filter(status=status_filter)
        
        if date_filter == 'today':
            reservations = reservations.filter(date=timezone.localdate())
        elif date_filter == 'future':
            reservations = reservations.filter(date__gte=timezone.localdate())
        elif date_filter == 'past':
            reservations = reservations.filter(date__lt=timezone.localdate())
        
        # 默认按日期和开始时间排序
        reservations = reservations.order_by('date', 'start_time')
        
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消预约"""
        reservation = self.get_object()
        
        # 只有待签到状态的预约可以取消
        if reservation.status != 'waiting':
            return Response(
                {"detail": "只能取消待签到状态的预约"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 只能取消自己的预约（除非是管理员）
        if reservation.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "您无权取消此预约"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        reservation.status = 'cancelled'
        reservation.save()
        
        # 释放座位
        seat = reservation.seat
        seat.status = 'available'
        seat.save()
        
        return Response({"detail": "预约已取消"})
    
    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        """预约签到"""
        reservation = self.get_object()
        
        # 验证签到码
        check_in_code = request.data.get('check_in_code')
        if not check_in_code:
            return Response(
                {"detail": "请提供签到码"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证签到码是否正确
        if check_in_code != reservation.room.check_in_code:
            return Response(
                {"detail": "签到码错误"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查是否可以签到
        if not reservation.can_check_in:
            return Response(
                {"detail": "当前不在可签到时间范围内"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新预约状态
        reservation.status = 'checked_in'
        reservation.check_in_time = timezone.now()
        reservation.save()
        
        return Response({"detail": "签到成功"})
