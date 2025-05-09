from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from user.models import CustomUser
from study_room.models import StudyRoom
from seat.models import Seat
from reservation.models import Reservation

class Command(BaseCommand):
    help = '创建测试用预约数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='创建预约的数量'
        )
        
        parser.add_argument(
            '--user',
            type=str,
            help='指定用户ID'
        )

    def handle(self, *args, **options):
        count = options['count']
        user_id = options.get('user')
        
        # 获取用户，如果指定了用户ID，则使用该用户，否则随机选择
        if user_id:
            try:
                users = [CustomUser.objects.get(id=user_id)]
            except CustomUser.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'用户ID {user_id} 不存在'))
                return
        else:
            users = list(CustomUser.objects.all())
            if not users:
                self.stdout.write(self.style.ERROR('没有可用用户'))
                return
        
        # 获取自习室和座位
        rooms = list(StudyRoom.objects.all())
        if not rooms:
            self.stdout.write(self.style.ERROR('没有可用自习室'))
            return
            
        seats = list(Seat.objects.all())
        if not seats:
            self.stdout.write(self.style.ERROR('没有可用座位'))
            return
        
        # 创建预约
        created_count = 0
        status_choices = ['waiting', 'checked_in', 'completed', 'cancelled', 'expired']
        status_weights = [0.4, 0.2, 0.2, 0.1, 0.1]  # 各状态的权重
        
        # 日期范围：前7天到后7天
        today = timezone.localdate()
        date_range = [(today + timedelta(days=i)) for i in range(-7, 8)]
        
        for _ in range(count):
            user = random.choice(users)
            room = random.choice(rooms)
            seat = random.choice([s for s in seats if s.room == room])
            date = random.choice(date_range)
            
            # 根据自习室的开放时间设置预约时间
            open_hour = room.open_time.hour
            close_hour = room.close_time.hour
            
            # 确保开始时间小于结束时间且时间间隔不超过4小时
            start_hour = random.randint(open_hour, close_hour - 1)
            max_end_hour = min(start_hour + 4, close_hour)
            end_hour = random.randint(start_hour + 1, max_end_hour)
            
            start_time = datetime.strptime(f"{start_hour}:00", "%H:%M").time()
            end_time = datetime.strptime(f"{end_hour}:00", "%H:%M").time()
            
            # 根据权重随机选择状态
            status = random.choices(status_choices, weights=status_weights)[0]
            
            # 对于历史数据，根据状态设置合理的签到时间
            check_in_time = None
            if status in ['checked_in', 'completed'] and date <= today:
                check_in_datetime = timezone.datetime.combine(date, start_time)
                # 随机在预约开始前15分钟到开始后10分钟之间签到
                random_minutes = random.randint(-15, 10) 
                check_in_time = timezone.make_aware(check_in_datetime + timedelta(minutes=random_minutes))
            
            try:
                # 创建预约记录
                reservation = Reservation.objects.create(
                    user=user,
                    room=room,
                    seat=seat,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    status=status,
                    check_in_time=check_in_time
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'创建预约: {reservation}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'创建预约失败: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'成功创建 {created_count} 条预约记录')) 