from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DailyStatistics, HourlyStatistics
from .serializers import DailyStatisticsSerializer, HourlyStatisticsSerializer, RoomStatisticsSerializer
from datetime import timedelta
from django.db.models import Avg

class StatisticsViewSet(viewsets.GenericViewSet):
    """统计数据视图集"""
    permission_classes = [permissions.IsAdminUser]  # 只有管理员可以访问统计数据
    
    @action(detail=False, methods=['get'])
    def daily(self, request):
        """获取每日统计数据"""
        room_id = request.query_params.get('room_id')
        days = int(request.query_params.get('days', 7))  # 默认获取7天数据
        
        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=days-1)
        
        # 过滤查询条件
        query_params = {'date__range': [start_date, end_date]}
        if room_id:
            query_params['room_id'] = room_id
            
        statistics = DailyStatistics.objects.filter(**query_params).order_by('date')
        serializer = DailyStatisticsSerializer(statistics, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def hourly(self, request):
        """获取每小时统计数据"""
        room_id = request.query_params.get('room_id')
        date_str = request.query_params.get('date')
        
        # 默认获取今天的数据
        if date_str:
            try:
                from datetime import datetime
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {"detail": "日期格式错误，应为YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            date = timezone.localdate()
        
        # 过滤查询条件
        query_params = {'date': date}
        if room_id:
            query_params['room_id'] = room_id
            
        statistics = HourlyStatistics.objects.filter(**query_params).order_by('hour')
        serializer = HourlyStatisticsSerializer(statistics, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def room_stats(self, request):
        """获取自习室统计汇总数据"""
        days = int(request.query_params.get('days', 7))  # 默认获取7天数据
        
        # 获取日期范围
        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=days-1)
        
        # 获取每个自习室的统计数据
        room_statistics = DailyStatistics.objects.filter(
            date__range=[start_date, end_date]
        ).values('room').annotate(
            usage_rate=Avg('usage_rate'),
            total_reservations=Avg('total_reservations')
        )
        
        serializer = RoomStatisticsSerializer(room_statistics, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def peak_hours(self, request):
        """获取高峰时段"""
        days = int(request.query_params.get('days', 7))  # 默认获取7天数据
        
        # 获取日期范围
        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=days-1)
        
        # 获取每个小时的平均使用率
        hourly_stats = HourlyStatistics.objects.filter(
            date__range=[start_date, end_date]
        ).values('hour').annotate(
            avg_usage_rate=Avg('usage_rate')
        ).order_by('-avg_usage_rate')
        
        # 选择使用率最高的3个小时段
        peak_hours = list(hourly_stats[:3])
        
        # 格式化返回数据
        formatted_peak_hours = []
        for item in peak_hours:
            hour = item['hour']
            next_hour = (hour + 1) % 24
            time_range = f"{hour:02d}:00-{next_hour:02d}:00"
            formatted_peak_hours.append({
                'time_range': time_range,
                'usage_rate': item['avg_usage_rate']
            })
        
        return Response(formatted_peak_hours)
