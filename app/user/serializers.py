from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import CustomUser


class UserInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')
    stats = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'studentId', 'department', 'avatar', 'phone', 'email', 'stats']

    def get_stats(self, obj):
        return {
            'totalReservations': obj.totalReservations,
            'totalHours': obj.totalHours,
            'violations': obj.violations
        }
    
class AdminInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')
    role = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'avatar', 'role']

    def get_role(self, obj):
        return 'admin' if obj.is_staff else 'user'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']