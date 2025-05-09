from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeatViewSet, FavoriteSeatViewSet, RoomSeatView, AdminSeatViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'seats', SeatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('favorites', FavoriteSeatViewSet.as_view({'get': 'list'}), name='favorite-seats-list'),
    path('favorites/add', FavoriteSeatViewSet.as_view({'post': 'add'}), name='favorite-seats-add'),
    path('favorites/remove', FavoriteSeatViewSet.as_view({'post': 'remove'}), name='favorite-seats-remove'),
    path('room/<int:room_id>/seats', RoomSeatView.as_view(), name='room-seats'),
    path('admin/seats', AdminSeatViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-seats'),
    path('admin/seats/<str:pk>', AdminSeatViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-seat-detail'),
] 