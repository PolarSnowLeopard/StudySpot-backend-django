from django.urls import path
from .views import LoginView, UserInfoView, AdminInfoView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('info', UserInfoView.as_view(), name='user-info'),
    path('admin-info', AdminInfoView.as_view(), name='admin-info'),
]