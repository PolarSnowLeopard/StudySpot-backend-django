from django.urls import path
from .views import LoginView, UserInfoView, AdminInfoView, RegisterView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('info', UserInfoView.as_view(), name='user-info'),
    path('admin-info', AdminInfoView.as_view(), name='admin-info'),
    path('register', RegisterView.as_view(), name='register'),
]