from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Seat, FavoriteSeat
from .serializers import (
    SeatSerializer, 
    SeatDetailSerializer, 
    FavoriteSeatSerializer,
    RoomSeatLayoutSerializer
)
from study_room.models import StudyRoom

class SeatViewSet(viewsets.ModelViewSet):
    """座位视图集"""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SeatDetailSerializer
        return SeatSerializer

class FavoriteSeatViewSet(viewsets.GenericViewSet):
    """收藏座位视图集"""
    queryset = FavoriteSeat.objects.all()
    serializer_class = FavoriteSeatSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def list(self, request):
        """获取用户收藏的座位"""
        favorites = FavoriteSeat.objects.filter(user=request.user)
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """添加收藏座位"""
        seat_id = request.data.get('seatId')
        if not seat_id:
            return Response({"error": "需要提供座位ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        seat = get_object_or_404(Seat, id=seat_id)
        favorite, created = FavoriteSeat.objects.get_or_create(user=request.user, seat=seat)
        
        if created:
            serializer = self.get_serializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "该座位已在收藏中"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def remove(self, request):
        """删除收藏座位"""
        favorite_id = request.data.get('id')
        if not favorite_id:
            return Response({"error": "需要提供收藏ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            favorite = FavoriteSeat.objects.get(id=favorite_id, user=request.user)
            favorite.delete()
            return Response({"message": "已取消收藏"}, status=status.HTTP_200_OK)
        except FavoriteSeat.DoesNotExist:
            return Response({"error": "收藏记录不存在"}, status=status.HTTP_404_NOT_FOUND)

class RoomSeatView(APIView):
    """自习室座位布局视图"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, room_id):
        """获取自习室的座位布局"""
        study_room = get_object_or_404(StudyRoom, id=room_id)
        serializer = RoomSeatLayoutSerializer(study_room)
        return Response(serializer.data)

class AdminSeatViewSet(viewsets.ModelViewSet):
    """管理员座位管理视图集"""
    queryset = Seat.objects.all()
    serializer_class = SeatDetailSerializer
    permission_classes = [IsAdminUser]
    
    def list(self, request):
        """获取指定自习室的所有座位"""
        room_id = request.query_params.get('roomId')
        if not room_id:
            return Response({"error": "需要提供自习室ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        seats = self.queryset.filter(room_id=room_id)
        serializer = self.get_serializer(seats, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """批量创建或更新座位"""
        room_id = request.data.get('roomId')
        if not room_id:
            return Response({"error": "需要提供自习室ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room = StudyRoom.objects.get(id=room_id)
        except StudyRoom.DoesNotExist:
            return Response({"error": "自习室不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        seats_data = request.data.get('seats', [])
        created_count = 0
        updated_count = 0
        
        for seat_data in seats_data:
            seat_id = f"{room_id}_{seat_data.get('code')}"
            seat_data['id'] = seat_id
            seat_data['room'] = room.id
            
            # 处理has_socket字段，将前端的hasSocket映射到has_socket
            if 'hasSocket' in seat_data:
                seat_data['has_socket'] = seat_data.pop('hasSocket')
            
            # 尝试查找现有座位
            try:
                seat = Seat.objects.get(id=seat_id)
                # 更新现有座位
                serializer = self.get_serializer(seat, data=seat_data)
                updated_count += 1
            except Seat.DoesNotExist:
                # 创建新座位
                serializer = self.get_serializer(data=seat_data)
                created_count += 1
            
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": f"成功创建{created_count}个座位, 更新{updated_count}个座位",
            "roomId": room_id
        }, status=status.HTTP_200_OK)
