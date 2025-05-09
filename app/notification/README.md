# 通知应用 (Notification)

通知应用负责处理系统通知和预约相关通知的创建、查询和管理。

## 数据模型

### Notification (通知)

```python
class Notification(models.Model):
    """通知模型"""
    TYPE_CHOICES = (
        ('system', '系统通知'),
        ('reservation', '预约通知'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications', verbose_name='用户')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='类型')
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='相关预约')
```

## API 接口

### 1. 获取用户通知列表

- **URL**: `/api/notification/notifications/`
- **方法**: `GET`
- **认证**: 需要用户认证
- **成功响应** (200 OK):
```json
[
    {
        "id": 1,
        "type": "system",
        "title": "系统维护通知",
        "content": "系统将于2023年6月10日晚上22:00-24:00进行维护，期间可能无法正常使用。",
        "time": "2023-06-08 15:30:00",
        "isRead": false,
        "reservationId": null
    },
    {
        "id": 2,
        "type": "reservation",
        "title": "预约提醒",
        "content": "您有一个预约将在15分钟后开始，请及时前往自习室签到。",
        "time": "2023-06-08 13:45:00",
        "isRead": true,
        "reservationId": "1"
    }
]
```

### 2. 获取通知详情

- **URL**: `/api/notification/notifications/{id}/`
- **方法**: `GET`
- **认证**: 需要用户认证
- **成功响应** (200 OK):
```json
{
    "id": 1,
    "type": "system",
    "title": "系统维护通知",
    "content": "系统将于2023年6月10日晚上22:00-24:00进行维护，期间可能无法正常使用。",
    "time": "2023-06-08 15:30:00",
    "isRead": false,
    "reservationId": null
}
```

### 3. 标记通知为已读

- **URL**: `/api/notification/notifications/{id}/mark_as_read/`
- **方法**: `POST`
- **认证**: 需要用户认证
- **成功响应** (200 OK):
```json
{
    "detail": "已将通知标记为已读"
}
```

### 4. 标记所有通知为已读

- **URL**: `/api/notification/notifications/mark_all_as_read/`
- **方法**: `POST`
- **认证**: 需要用户认证
- **成功响应** (200 OK):
```json
{
    "detail": "已将10条通知标记为已读"
}
```

### 5. 获取未读通知数量

- **URL**: `/api/notification/notifications/unread_count/`
- **方法**: `GET`
- **认证**: 需要用户认证
- **成功响应** (200 OK):
```json
{
    "count": 5
}
```

## 通知类型

1. **系统通知**：由管理员或系统自动发送的通知，如系统维护、功能更新、使用指南等。
2. **预约通知**：与预约相关的通知，如预约成功、预约提醒、签到成功、预约取消、预约过期等。

## 管理命令

### 创建测试通知数据

```bash
python manage.py create_notifications --count 20
```

## 信号处理器

通知应用包含以下信号处理器：

1. **reservation_notification**: 监听预约状态变更，自动生成相应通知
   - 预约创建时：生成"预约成功"通知和"预约提醒"通知
   - 预约签到时：生成"签到成功"通知
   - 预约取消时：生成"预约已取消"通知
   - 预约过期时：生成"预约已过期"通知
   - 预约完成时：生成"预约已完成"通知 