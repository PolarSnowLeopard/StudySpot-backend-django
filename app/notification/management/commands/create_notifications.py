from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from user.models import CustomUser
from notification.models import Notification
from reservation.models import Reservation

class Command(BaseCommand):
    help = '创建测试用通知数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='创建通知的数量'
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
        
        # 获取预约，用于创建预约通知
        reservations = list(Reservation.objects.all())
        
        # 系统通知标题模板
        system_titles = [
            "系统维护通知",
            "新功能上线",
            "使用指南",
            "假期安排",
            "座位调整通知"
        ]
        
        # 系统通知内容模板
        system_contents = [
            "系统将于{date}晚上22:00-24:00进行维护，期间可能无法正常使用。",
            "我们新增了{feature}功能，欢迎体验！",
            "请查看最新的系统使用手册，了解更多功能。",
            "{holiday}期间，自习室开放时间调整为9:00-18:00。",
            "由于设备检修，{room}的座位布局已调整，请注意查看。"
        ]
        
        # 替换内容
        features = ["收藏座位", "历史记录查询", "自习室地图", "座位筛选", "学习统计"]
        holidays = ["国庆节", "元旦", "春节", "五一", "中秋节"]
        rooms = ["图书馆三楼", "教学楼A栋", "计算机学院", "电子学院"]
        
        # 预约通知标题模板
        reservation_titles = [
            "预约成功",
            "预约提醒",
            "签到成功",
            "预约已取消",
            "预约已过期"
        ]
        
        # 创建通知
        created_count = 0
        for _ in range(count):
            user = random.choice(users)
            
            # 随机决定创建系统通知或预约通知
            if random.random() < 0.3 or not reservations:  # 30%概率创建系统通知
                title_index = random.randint(0, len(system_titles) - 1)
                title = system_titles[title_index]
                content_template = system_contents[title_index]
                
                # 根据标题选择适当的内容替换
                if "维护" in title:
                    date = (timezone.now() + timedelta(days=random.randint(1, 10))).strftime('%Y年%m月%d日')
                    content = content_template.format(date=date)
                elif "新功能" in title:
                    content = content_template.format(feature=random.choice(features))
                elif "假期" in title:
                    content = content_template.format(holiday=random.choice(holidays))
                elif "座位" in title:
                    content = content_template.format(room=random.choice(rooms))
                else:
                    content = content_template
                
                notification = Notification.create_system_notification(
                    user=user,
                    title=title,
                    content=content
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'创建系统通知: {notification}'))
            
            else:  # 70%概率创建预约通知
                reservation = random.choice(reservations)
                title = random.choice(reservation_titles)
                
                if title == "预约成功":
                    content = f"您已成功预约{reservation.room.name}的{reservation.seat.code}座位，预约时间为{reservation.date.strftime('%Y-%m-%d')} {reservation.start_time.strftime('%H:%M')}至{reservation.end_time.strftime('%H:%M')}。"
                elif title == "预约提醒":
                    content = f"您预约的{reservation.room.name}{reservation.seat.code}座位将在15分钟后开始，请及时前往签到。"
                elif title == "签到成功":
                    content = f"您已成功签到{reservation.room.name}的{reservation.seat.code}座位，祝您学习愉快！"
                elif title == "预约已取消":
                    content = f"您取消了{reservation.date.strftime('%Y-%m-%d')} {reservation.start_time.strftime('%H:%M')}在{reservation.room.name}的预约。"
                else:  # 预约已过期
                    content = f"您未在规定时间内签到，{reservation.date.strftime('%Y-%m-%d')} {reservation.start_time.strftime('%H:%M')}在{reservation.room.name}的预约已自动取消。"
                
                # 随机设置是否已读
                is_read = random.random() < 0.5
                
                notification = Notification.objects.create(
                    user=user,
                    type='reservation',
                    title=title,
                    content=content,
                    is_read=is_read,
                    reservation=reservation
                )
                
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'创建预约通知: {notification}'))
        
        self.stdout.write(self.style.SUCCESS(f'成功创建 {created_count} 条通知')) 