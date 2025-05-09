# 系统设置应用 (System Settings)

系统设置应用负责管理全局配置参数，如最大预约时长、提前预约天数、签到宽限期和违规规则等。

## 数据模型

### SystemSettings (系统设置)

```python
class SystemSettings(models.Model):
    """系统设置模型，只有一条记录"""
    max_reservation_hours = models.IntegerField(default=4, verbose_name='最大预约小时数')
    advance_reservation_days = models.IntegerField(default=7, verbose_name='提前预约天数')
    check_in_grace_period = models.IntegerField(default=15, verbose_name='签到宽限期（分钟）')
    violation_rules = models.TextField(default='累计3次限制预约1天', verbose_name='违规规则')
    violation_limit = models.IntegerField(default=3, verbose_name='违规次数限制')
    penalty_days = models.IntegerField(default=1, verbose_name='违规惩罚天数')
```

## API 接口

### 1. 获取系统设置 (需要用户登录)

- **URL**: `/api/system/settings/get_settings/`
- **方法**: `GET`
- **认证**: 需要用户认证
- **说明**: 根据用户权限返回不同级别的系统设置信息。管理员可获取所有设置，普通用户只能获取公开设置。
- **成功响应** (200 OK) - 普通用户:
```json
{
    "max_reservation_hours": 4,
    "advance_reservation_days": 7,
    "check_in_grace_period": 15,
    "violation_rules": "累计3次限制预约1天"
}
```

- **成功响应** (200 OK) - 管理员:
```json
{
    "max_reservation_hours": 4,
    "advance_reservation_days": 7,
    "check_in_grace_period": 15,
    "violation_rules": "累计3次限制预约1天",
    "violation_limit": 3,
    "penalty_days": 1
}
```

### 2. 更新系统设置 (仅管理员)

- **URL**: `/api/system/settings/update_settings/`
- **方法**: `PUT`
- **认证**: 需要管理员权限
- **请求数据**:
```json
{
    "max_reservation_hours": 5,
    "advance_reservation_days": 10,
    "check_in_grace_period": 20,
    "violation_rules": "累计3次限制预约2天",
    "violation_limit": 3,
    "penalty_days": 2
}
```
- **成功响应** (200 OK):
```json
{
    "max_reservation_hours": 5,
    "advance_reservation_days": 10,
    "check_in_grace_period": 20,
    "violation_rules": "累计3次限制预约2天",
    "violation_limit": 3,
    "penalty_days": 2
}
```

### 3. 获取公开系统设置 (无需登录)

- **URL**: `/api/system/settings/public_settings/`
- **方法**: `GET`
- **认证**: 不需要认证
- **成功响应** (200 OK):
```json
{
    "max_reservation_hours": 4,
    "advance_reservation_days": 7,
    "check_in_grace_period": 15,
    "violation_rules": "累计3次限制预约1天"
}
```

## 设置项说明

1. **max_reservation_hours**: 单次预约的最大时长（小时）
2. **advance_reservation_days**: 可提前预约的天数
3. **check_in_grace_period**: 签到宽限期（分钟），超过该时间未签到则自动取消预约
4. **violation_rules**: 违规规则说明文本
5. **violation_limit**: 违规次数限制，达到该次数将受到惩罚
6. **penalty_days**: 违规惩罚天数，禁止预约的天数

## 缓存机制

系统设置使用Django的缓存机制（默认使用内存缓存），以提高性能并减少数据库查询：

1. 每次更新设置时，会自动将设置保存到缓存中
2. 获取设置时，优先从缓存中获取
3. 如果缓存不存在，则从数据库获取并更新缓存
4. 缓存有效期为1天 