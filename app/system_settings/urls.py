from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemSettingsViewSet

router = DefaultRouter()
router.register(r'settings', SystemSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 