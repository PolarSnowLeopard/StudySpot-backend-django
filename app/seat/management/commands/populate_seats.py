from django.core.management.base import BaseCommand
from study_room.models import StudyRoom
from seat.models import Seat
import random

class Command(BaseCommand):
    help = '填充座位测试数据'

    def handle(self, *args, **kwargs):
        # 获取所有自习室
        study_rooms = StudyRoom.objects.all()
        
        if not study_rooms:
            self.stdout.write(self.style.WARNING('没有找到自习室，请先运行 python manage.py populate_study_rooms'))
            return
        
        for room in study_rooms:
            # 根据mock数据生成图书馆三楼自习室的座位
            if room.name == '图书馆三楼自习室':
                self.stdout.write(self.style.SUCCESS(f'为 {room.name} 生成座位...'))
                
                # 创建4行5列的座位
                rows = 4
                columns = 5
                
                # 使用字母表示行
                row_letters = ['A', 'B', 'C', 'D']
                
                # 有电源的座位位置，从mock数据中获取
                has_socket_positions = [
                    (0, 1),  # A2
                    (1, 1),  # B2
                    (2, 3),  # C4
                    (3, 3),  # D4
                ]
                
                # 已占用的座位位置，从mock数据中获取
                occupied_positions = [
                    (0, 2),  # A3
                    (1, 0),  # B1
                    (1, 4),  # B5
                    (2, 2),  # C3
                    (3, 1),  # D2
                ]
                
                for r in range(rows):
                    for c in range(columns):
                        # 生成座位编码，如 A1, B2, C3 等
                        code = f"{row_letters[r]}{c+1}"
                        seat_id = f"{room.id}_{code}"
                        
                        # 确定座位状态
                        if (r, c) in occupied_positions:
                            status = 'occupied'
                        else:
                            status = 'available'
                        
                        # 确定是否有电源
                        has_socket = (r, c) in has_socket_positions
                        
                        # 创建或更新座位
                        seat, created = Seat.objects.update_or_create(
                            id=seat_id,
                            defaults={
                                'code': code,
                                'room': room,
                                'status': status,
                                'has_socket': has_socket,
                                'row': r + 1,
                                'column': c + 1
                            }
                        )
                        
                        action = '创建' if created else '更新'
                        self.stdout.write(self.style.SUCCESS(f'{action}座位: {code} (状态: {status}, 电源: {has_socket})'))
            else:
                # 为其他自习室生成随机座位布局
                self.stdout.write(self.style.SUCCESS(f'为 {room.name} 生成随机座位...'))
                
                # 随机确定行列数
                rows = random.randint(3, 5)
                columns = random.randint(4, 6)
                
                # 使用字母表示行
                row_letters = ['A', 'B', 'C', 'D', 'E']
                
                # 随机生成一些有电源的座位和已占用的座位
                total_seats = rows * columns
                socket_count = total_seats // 4  # 约1/4的座位有电源
                occupied_count = total_seats // 5  # 约1/5的座位已占用
                
                # 随机选择座位位置
                all_positions = [(r, c) for r in range(rows) for c in range(columns)]
                socket_positions = random.sample(all_positions, socket_count)
                remaining_positions = [pos for pos in all_positions if pos not in socket_positions]
                occupied_positions = random.sample(remaining_positions, min(occupied_count, len(remaining_positions)))
                
                for r in range(rows):
                    for c in range(columns):
                        # 生成座位编码，如 A1, B2, C3 等
                        code = f"{row_letters[r]}{c+1}"
                        seat_id = f"{room.id}_{code}"
                        
                        # 确定座位状态
                        if (r, c) in occupied_positions:
                            status = 'occupied'
                        else:
                            status = 'available'
                        
                        # 确定是否有电源
                        has_socket = (r, c) in socket_positions
                        
                        # 创建或更新座位
                        seat, created = Seat.objects.update_or_create(
                            id=seat_id,
                            defaults={
                                'code': code,
                                'room': room,
                                'status': status,
                                'has_socket': has_socket,
                                'row': r + 1,
                                'column': c + 1
                            }
                        )
                        
                        action = '创建' if created else '更新'
                        self.stdout.write(self.style.SUCCESS(f'{action}座位: {code} (状态: {status}, 电源: {has_socket})'))
        
        self.stdout.write(self.style.SUCCESS('所有自习室座位数据填充完成!')) 