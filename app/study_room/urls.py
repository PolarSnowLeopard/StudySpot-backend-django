from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudyRoomViewSet, DepartmentViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'studyRooms', StudyRoomViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 