from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservation.models import Reservation
from seat.models import Seat
from system_settings.models import SystemSettings

class Command(BaseCommand):
    help = '检查并处理过期的预约'

    def handle(self, *args, **options):
        now = timezone.localtime()
        today = timezone.localdate()
        
        # 获取签到宽限期
        grace_period = SystemSettings.get_check_in_grace_period()
        
        # 处理等待签到但已过期的预约
        waiting_reservations = Reservation.objects.filter(
            status='waiting',
            date=today
        )
        
        expired_count = 0
        
        for reservation in waiting_reservations:
            # 检查是否已过签到截止时间
            reservation_datetime = timezone.make_aware(
                timezone.datetime.combine(reservation.date, reservation.start_time))
            
            # 如果当前时间超过预约开始时间加宽限期，且未签到，则标记为过期
            if now > reservation_datetime + timedelta(minutes=grace_period):
                reservation.status = 'expired'
                reservation.save()
                
                # 释放座位
                seat = reservation.seat
                seat.status = 'available'
                seat.save()
                
                # 记录违约（实际应该由通知系统处理）
                user = reservation.user
                user.violations = getattr(user, 'violations', 0) + 1
                user.save()
                
                expired_count += 1
                self.stdout.write(self.style.WARNING(f'预约已过期: {reservation}'))
        
        # 处理使用中但已结束的预约
        checked_in_reservations = Reservation.objects.filter(
            status='checked_in',
            date__lte=today
        )
        
        completed_count = 0
        
        for reservation in checked_in_reservations:
            # 检查预约是否已结束
            end_datetime = timezone.make_aware(
                timezone.datetime.combine(reservation.date, reservation.end_time))
            
            # 如果当前时间超过预约结束时间，则标记为已完成
            if now > end_datetime:
                reservation.status = 'completed'
                reservation.save()
                
                # 释放座位
                seat = reservation.seat
                seat.status = 'available'
                seat.save()
                
                completed_count += 1
                self.stdout.write(self.style.SUCCESS(f'预约已完成: {reservation}'))
        
        self.stdout.write(self.style.SUCCESS(f'成功处理 {expired_count} 条过期预约和 {completed_count} 条已完成预约')) 