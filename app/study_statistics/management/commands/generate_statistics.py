from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from study_room.models import StudyRoom
from study_statistics.models import DailyStatistics, HourlyStatistics

class Command(BaseCommand):
    help = '生成自习室使用统计数据'

    def add_arguments(self, parser):
        """添加命令行参数"""
        parser.add_argument(
            '--daily',
            action='store_true',
            help='生成每日统计数据',
        )
        parser.add_argument(
            '--hourly',
            action='store_true',
            help='生成每小时统计数据',
        )
        parser.add_argument(
            '--date',
            type=str,
            help='指定日期 (YYYY-MM-DD), 默认为昨天',
        )
        parser.add_argument(
            '--hour',
            type=int,
            help='指定小时 (0-23), 默认为上一小时',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制重新生成数据（覆盖已有数据）',
        )

    def handle(self, *args, **options):
        """命令处理函数"""
        daily = options.get('daily')
        hourly = options.get('hourly')
        date_str = options.get('date')
        hour = options.get('hour')
        force = options.get('force')

        # 如果没有指定类型，则默认全部生成
        if not daily and not hourly:
            daily = True
            hourly = True

        # 处理日期参数
        if date_str:
            try:
                from datetime import datetime
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                self.stderr.write(self.style.ERROR('日期格式错误，应为YYYY-MM-DD'))
                return
        else:
            # 默认为昨天
            date = timezone.localdate() - timedelta(days=1)
        
        # 如果是每小时统计，但没有指定小时，则默认为上一小时
        if hourly and hour is None:
            hour = (timezone.localtime() - timedelta(hours=1)).hour
        
        # 获取所有自习室
        study_rooms = StudyRoom.objects.all()
        if not study_rooms.exists():
            self.stderr.write(self.style.WARNING('没有找到自习室数据'))
            return
        
        # 生成每日统计
        if daily:
            self.stdout.write(f'开始生成 {date} 的每日统计数据...')
            daily_count = 0
            
            for room in study_rooms:
                # 检查是否已有数据
                if not force and DailyStatistics.objects.filter(room=room, date=date).exists():
                    self.stdout.write(f'已跳过 {room.name} {date} 的统计数据 (已存在)')
                    continue
                
                stats = DailyStatistics.calculate_statistics(room, date)
                self.stdout.write(f'已生成 {room.name} {date} 的统计数据:')
                self.stdout.write(f'  总预约数: {stats.total_reservations}')
                self.stdout.write(f'  总使用小时数: {stats.total_hours}')
                self.stdout.write(f'  使用率: {stats.usage_rate:.2f}%')
                daily_count += 1
            
            self.stdout.write(self.style.SUCCESS(f'成功生成 {daily_count} 条每日统计数据'))
        
        # 生成每小时统计
        if hourly:
            self.stdout.write(f'开始生成 {date} {hour}点 的每小时统计数据...')
            hourly_count = 0
            
            for room in study_rooms:
                # 检查是否已有数据
                if not force and HourlyStatistics.objects.filter(room=room, date=date, hour=hour).exists():
                    self.stdout.write(f'已跳过 {room.name} {date} {hour}点 的统计数据 (已存在)')
                    continue
                
                stats = HourlyStatistics.calculate_statistics(room, date, hour)
                self.stdout.write(f'已生成 {room.name} {date} {hour}点 的统计数据:')
                self.stdout.write(f'  占用座位数: {stats.occupied_seats}')
                self.stdout.write(f'  使用率: {stats.usage_rate:.2f}%')
                hourly_count += 1
            
            self.stdout.write(self.style.SUCCESS(f'成功生成 {hourly_count} 条每小时统计数据')) 