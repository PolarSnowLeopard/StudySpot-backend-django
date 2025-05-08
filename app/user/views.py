from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets
from .models import CustomUser
from user.serializers import GroupSerializer, UserInfoSerializer, AdminInfoSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

# 注册接口，用于新用户注册
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        student_id = request.data.get('studentId')
        department = request.data.get('department')
        name = request.data.get('name')
        phone = request.data.get('phone')
        email = request.data.get('email')
        
        # 验证必填字段
        if not all([username, password, student_id, department, name]):
            return Response({'error': '用户名、密码、学号、学院和姓名为必填项'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查用户名是否已存在
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查学号是否已存在
        if User.objects.filter(studentId=student_id).exists():
            return Response({'error': '学号已存在'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建新用户
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                studentId=student_id,
                department=department,
                first_name=name,
                phone=phone,
                email=email
            )
            # 创建token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': '注册成功',
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'注册失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 登录接口，学生和管理员均使用该接口进行登录。支持用户名/学号登录
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

# 用户信息接口，学生登录后，可使用该接口获取用户信息，需携带token
class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data)

# 管理员信息接口，管理员登录后，可使用该接口获取管理员信息，需携带token
class AdminInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_staff:
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        serializer = AdminInfoSerializer(user)
        return Response(serializer.data)

# 用户视图集，提供增删改查接口
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

# 组视图集，提供增删改查接口
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]