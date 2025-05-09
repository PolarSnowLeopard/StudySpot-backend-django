# 预约应用 (Reservation)

预约应用负责处理用户对自习室座位的预约、签到、取消等操作。

## 数据模型

### Reservation (预约)

```python
class Reservation(models.Model):
    """预约模型"""
    STATUS_CHOICES = (
        ('waiting', '待签到'),
        ('checked_in', '使用中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('expired', '已过期'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reservations', verbose_name='用户')
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, verbose_name='自习室')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name='座位')
    date = models.DateField(verbose_name='日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name='状态')
    check_in_time = models.DateTimeField(null=True, blank=True, verbose_name='签到时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    check_in_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='签到码')
```

## API 接口

### 1. 创建预约

- **URL**: `/api/reservation/reservations/`
- **方法**: `POST`
- **认证**: 需要用户认证
- **请求数据**:
```json
{
    "room": 1,
    "seat": "A12",
    "date": "2023-06-10",
    "start_time": "14:00",
    "end_time": "18:00"
}
```
- **成功响应** (201 Created):
```json
{
    "id": 1,
    "roomId": "1",
    "roomName": "图书馆三楼自习室",
    "seatId": "A12",
    "seatCode": "A12",
    "date": "今天",
    "start_time": "14:00:00",
    "end_time": "18:00:00",
    "status": "waiting"
}
```

### 2. 获取用户预约列表

- **URL**: `/api/reservation/reservations/user_reservations/`
- **方法**: `GET`
- **认证**: 需要用户认证
- **查询参数**:
  - `status`: 筛选特定状态的预约 (waiting, checked_in, completed, cancelled, expired)
  - `date`: 筛选特定日期的预约 (today, future, past)
- **成功响应** (200 OK):
```json
[
    {
        "id": 1,
        "roomId": "1",
        "roomName": "图书馆三楼自习室",
        "seatId": "A12",
        "seatCode": "A12",
        "date": "今天",
        "start_time": "14:00:00",
        "end_time": "18:00:00",
        "status": "waiting"
    },
    {
        "id": 2,
        "roomId": "2",
        "roomName": "计算机学院自习室",
        "seatId": "B05",
        "seatCode": "B05",
        "date": "明天",
        "start_time": "08:00:00",
        "end_time": "12:00:00",
        "status": "waiting"
    }
]
```

### 3. 取消预约

- **URL**: `/api/reservation/reservations/{id}/cancel/`
- **方法**: `POST`
- **认证**: 需要用户认证
- **成功响应** (200 OK):
```json
{
    "detail": "预约已取消"
}
```

### 4. 预约签到

- **URL**: `/api/reservation/reservations/{id}/check_in/`
- **方法**: `POST`
- **认证**: 需要用户认证
- **请求数据**:
```json
{
    "check_in_code": "ABC123"
}
```
- **成功响应** (200 OK):
```json
{
    "detail": "签到成功"
}
```

## 预约规则

1. 预约时间必须是整点开始和结束
2. 单次预约最长时间为4小时
3. 只能预约状态为"可用"的座位
4. 无法预约已被他人预约的时间段
5. 预约签到需要在预定时间前15分钟至后15分钟内完成
6. 未按时签到的预约将在超过预定时间15分钟后自动取消

## 管理命令

### 创建测试预约数据

```bash
python manage.py create_reservations --count 15
```

### 检查并处理过期预约

```bash
python manage.py check_expired_reservations
```

## 信号处理器

预约应用包含以下信号处理器：

1. **reservation_pre_save**: 预约保存前的处理逻辑
2. **reservation_post_save**: 预约保存后的处理逻辑
3. **reservation_post_delete**: 预约删除后的处理逻辑

这些信号处理器负责自动更新座位状态、用户统计数据等。 