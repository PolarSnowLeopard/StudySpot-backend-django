from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from reservation.models import Reservation
from .models import Notification

@receiver(post_save, sender=Reservation)
def reservation_notification(sender, instance, created, **kwargs):
    """处理预约相关通知"""
    # 预约成功通知
    if created:
        title = "预约成功"
        content = f"您已成功预约{instance.room.name}的{instance.seat.code}座位，预约时间为{instance.date.strftime('%Y-%m-%d')} {instance.start_time.strftime('%H:%M')}至{instance.end_time.strftime('%H:%M')}。请记得提前15分钟前往签到。"
        Notification.create_reservation_notification(
            user=instance.user,
            reservation=instance,
            title=title,
            content=content
        )
        
        # 创建一个定时任务，在预约时间前15分钟发送提醒
        # 这里我们只是创建通知记录，实际环境中应该使用Celery等任务队列
        # 创建提前15分钟的提醒
        reservation_datetime = timezone.make_aware(
            timezone.datetime.combine(instance.date, instance.start_time))
        reminder_time = reservation_datetime - timedelta(minutes=15)
        
        # 如果当前时间已经超过提醒时间，则不创建提醒（例如预约后马上就要去）
        if timezone.now() < reminder_time:
            title = "预约即将开始"
            content = f"您预约的{instance.room.name}{instance.seat.code}座位将在15分钟后开始，请及时前往签到。"
            Notification.create_reservation_notification(
                user=instance.user,
                reservation=instance,
                title=title,
                content=content
            )
    
    # 处理预约状态变更通知
    else:
        # 签到成功通知
        if instance.status == 'checked_in':
            title = "签到成功"
            content = f"您已成功签到{instance.room.name}的{instance.seat.code}座位，祝您学习愉快！"
            Notification.create_reservation_notification(
                user=instance.user,
                reservation=instance,
                title=title,
                content=content
            )
        
        # 预约取消通知
        elif instance.status == 'cancelled':
            title = "预约已取消"
            content = f"您取消了{instance.date.strftime('%Y-%m-%d')} {instance.start_time.strftime('%H:%M')}在{instance.room.name}的预约。"
            Notification.create_reservation_notification(
                user=instance.user,
                reservation=instance,
                title=title,
                content=content
            )
        
        # 预约过期通知
        elif instance.status == 'expired':
            title = "预约已过期"
            content = f"您未在规定时间内签到，{instance.date.strftime('%Y-%m-%d')} {instance.start_time.strftime('%H:%M')}在{instance.room.name}的预约已自动取消。"
            Notification.create_reservation_notification(
                user=instance.user,
                reservation=instance,
                title=title,
                content=content
            )
        
        # 预约完成通知
        elif instance.status == 'completed':
            title = "预约已完成"
            content = f"您在{instance.room.name}的学习已结束，感谢您使用自习室预约系统。"
            Notification.create_reservation_notification(
                user=instance.user,
                reservation=instance,
                title=title,
                content=content
            ) 