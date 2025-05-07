from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets
from .models import CustomUser
from user.serializers import GroupSerializer, UserInfoSerializer, AdminInfoSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

class LoginView(APIView):
    def post(self, request):
        identifier = request.data.get('identifier')  # 可以是用户名或学号
        password = request.data.get('password')
        user = None
        User = get_user_model()
        # 先尝试用用户名查找
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            # 再尝试用学号查找
            try:
                user = User.objects.get(studentId=identifier)
            except User.DoesNotExist:
                return Response({'error': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '用户名/学号或密码错误'}, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data)
    
class AdminInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_staff:
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        serializer = AdminInfoSerializer(user)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]