from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Reservation
from seat.models import Seat

@receiver(pre_save, sender=Reservation)
def reservation_pre_save(sender, instance, **kwargs):
    """预约保存前检查并处理"""
    if instance.pk:  # 只处理更新操作
        try:
            old_instance = Reservation.objects.get(pk=instance.pk)
            # 如果状态从waiting更新为checked_in，且尚未设置签到时间
            if old_instance.status == 'waiting' and instance.status == 'checked_in' and not instance.check_in_time:
                instance.check_in_time = timezone.now()
                
            # 如果座位变更，需要更新原座位状态
            if old_instance.seat_id != instance.seat_id:
                # 如果原预约是waiting或checked_in状态，则释放原座位
                if old_instance.status in ['waiting', 'checked_in']:
                    old_seat = old_instance.seat
                    old_seat.status = 'available'
                    old_seat.save()
        except Reservation.DoesNotExist:
            pass

@receiver(post_save, sender=Reservation)
def reservation_post_save(sender, instance, created, **kwargs):
    """预约保存后处理"""
    if created:  # 新建预约
        # 占用座位
        seat = instance.seat
        seat.status = 'occupied'
        seat.save()
        
        # 更新用户预约统计
        user = instance.user
        user.totalReservations += 1
        user.save()
    
    else:  # 更新预约
        # 如果状态变为cancelled或completed或expired，释放座位
        if instance.status in ['cancelled', 'completed', 'expired']:
            seat = instance.seat
            seat.status = 'available'
            seat.save()
        
        # 如果状态变为checked_in，更新座位状态为occupied（虽然可能已经是occupied，但为确保一致性）
        elif instance.status == 'checked_in':
            seat = instance.seat
            seat.status = 'occupied'
            seat.save()
            
            # 计算预约的小时数，并更新用户统计
            user = instance.user
            hour_diff = (timezone.datetime.combine(instance.date, instance.end_time) - 
                         timezone.datetime.combine(instance.date, instance.start_time)).seconds / 3600
            user.totalHours += int(hour_diff)
            user.save()

@receiver(post_delete, sender=Reservation)
def reservation_post_delete(sender, instance, **kwargs):
    """预约删除后处理"""
    # 如果预约状态为waiting或checked_in，则释放座位
    if instance.status in ['waiting', 'checked_in']:
        seat = instance.seat
        seat.status = 'available'
        seat.save() 