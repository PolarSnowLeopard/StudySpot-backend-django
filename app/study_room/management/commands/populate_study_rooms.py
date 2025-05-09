from django.core.management.base import BaseCommand
from django.utils import timezone
from study_room.models import Department, StudyRoom
import datetime
import random
import string

class Command(BaseCommand):
    help = '填充自习室测试数据'

    def handle(self, *args, **kwargs):
        # 创建院系
        departments = [
            '计算机科学与技术学院',
            '电子工程学院',
            '数学学院',
            '物理学院',
            '经济管理学院',
        ]
        
        for dept_name in departments:
            dept, created = Department.objects.get_or_create(name=dept_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建院系: {dept_name}'))
        
        # 添加"全校开放"选项
        all_dept = None  # 表示全校开放的自习室
        
        # 创建自习室
        study_rooms = [
            {
                'name': '图书馆三楼自习室',
                'open_time': '07:00',
                'close_time': '22:00',
                'total_seats': 50,
                'department': all_dept,
                'is_open': True,
            },
            {
                'name': '计算机学院自习室',
                'open_time': '07:00',
                'close_time': '22:00',
                'total_seats': 40,
                'department': Department.objects.get(name='计算机科学与技术学院'),
                'is_open': True,
            },
            {
                'name': '教学楼A栋301',
                'open_time': '07:00',
                'close_time': '22:00',
                'total_seats': 60,
                'department': all_dept,
                'is_open': True,
            },
            {
                'name': '图书馆二楼自习室',
                'open_time': '07:00',
                'close_time': '22:00',
                'total_seats': 45,
                'department': all_dept,
                'is_open': True,
            },
            {
                'name': '电子学院自习室',
                'open_time': '08:00',
                'close_time': '21:00',
                'total_seats': 35,
                'department': Department.objects.get(name='电子工程学院'),
                'is_open': True,
            },
        ]
        
        for room_data in study_rooms:
            # 转换时间字符串为时间对象
            open_time = datetime.datetime.strptime(room_data['open_time'], '%H:%M').time()
            close_time = datetime.datetime.strptime(room_data['close_time'], '%H:%M').time()
            
            # 生成随机签到码
            check_in_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            room, created = StudyRoom.objects.get_or_create(
                name=room_data['name'],
                defaults={
                    'open_time': open_time,
                    'close_time': close_time,
                    'total_seats': room_data['total_seats'],
                    'department': room_data['department'],
                    'is_open': room_data['is_open'],
                    'check_in_code': check_in_code,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建自习室: {room_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'自习室已存在: {room_data["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('数据填充完成！')) 