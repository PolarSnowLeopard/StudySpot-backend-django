# 使用统计应用 (Study Statistics)

使用统计应用负责收集和分析自习室的使用数据，为管理员提供决策支持。通过这些统计数据，管理员可以了解各自习室的使用情况，调整资源配置，提高座位利用率。

## 数据模型

### DailyStatistics (每日统计)

```python
class DailyStatistics(models.Model):
    """每日统计数据"""
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, verbose_name='自习室')
    date = models.DateField(verbose_name='日期')
    total_reservations = models.IntegerField(default=0, verbose_name='总预约数')
    total_hours = models.IntegerField(default=0, verbose_name='总使用小时数')
    usage_rate = models.FloatField(default=0, verbose_name='使用率')
```

### HourlyStatistics (每小时统计)

```python
class HourlyStatistics(models.Model):
    """每小时统计数据"""
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, verbose_name='自习室')
    date = models.DateField(verbose_name='日期')
    hour = models.IntegerField(verbose_name='小时(0-23)')
    occupied_seats = models.IntegerField(default=0, verbose_name='占用座位数')
    usage_rate = models.FloatField(default=0, verbose_name='使用率')
```

## API 接口

### 1. 获取每日统计数据

- **URL**: `/api/statistics/statistics/daily/`
- **方法**: `GET`
- **认证**: 需要管理员权限
- **查询参数**:
  - `room_id`: (可选) 自习室ID
  - `days`: (可选) 获取最近几天的数据，默认7天
- **成功响应** (200 OK):
```json
[
  {
    "id": 1,
    "room": 1,
    "room_name": "图书馆三楼自习室",
    "room_detail": {
      "id": 1,
      "name": "图书馆三楼自习室",
      "openTime": "07:00",
      "closeTime": "22:00",
      "status": "有空座",
      "availableSeats": 35,
      "totalSeats": 50
    },
    "date": "2023-05-08",
    "total_reservations": 24,
    "total_hours": 72,
    "usage_rate": 65.5
  },
  // 更多日期数据...
]
```

### 2. 获取每小时统计数据

- **URL**: `/api/statistics/statistics/hourly/`
- **方法**: `GET`
- **认证**: 需要管理员权限
- **查询参数**:
  - `room_id`: (可选) 自习室ID
  - `date`: (可选) 日期，格式为YYYY-MM-DD，默认为今天
- **成功响应** (200 OK):
```json
[
  {
    "id": 1,
    "room": 1,
    "room_name": "图书馆三楼自习室",
    "date": "2023-05-09",
    "hour": 8,
    "occupied_seats": 15,
    "usage_rate": 30.0
  },
  {
    "id": 2,
    "room": 1,
    "room_name": "图书馆三楼自习室",
    "date": "2023-05-09",
    "hour": 9,
    "occupied_seats": 25,
    "usage_rate": 50.0
  },
  // 更多小时数据...
]
```

### 3. 获取自习室统计汇总

- **URL**: `/api/statistics/statistics/room_stats/`
- **方法**: `GET`
- **认证**: 需要管理员权限
- **查询参数**:
  - `days`: (可选) 获取最近几天的数据，默认7天
- **成功响应** (200 OK):
```json
[
  {
    "id": 1,
    "name": "图书馆三楼自习室",
    "usage_rate": 70.5,
    "usage_count": 85
  },
  {
    "id": 2,
    "name": "计算机学院自习室",
    "usage_rate": 95.2,
    "usage_count": 76
  },
  // 更多自习室统计...
]
```

### 4. 获取高峰时段

- **URL**: `/api/statistics/statistics/peak_hours/`
- **方法**: `GET`
- **认证**: 需要管理员权限
- **查询参数**:
  - `days`: (可选) 获取最近几天的数据，默认7天
- **成功响应** (200 OK):
```json
[
  {
    "time_range": "10:00-11:00",
    "usage_rate": 85.5
  },
  {
    "time_range": "14:00-15:00",
    "usage_rate": 82.3
  },
  {
    "time_range": "16:00-17:00",
    "usage_rate": 78.9
  }
]
```

## 统计算法

### 每日使用率计算

每日使用率按照以下公式计算：
```
使用率 = (总使用小时数 / (自习室开放小时数 × 座位总数)) × 100%
```

例如，如果自习室开放12小时，有50个座位，当天总使用时长为300小时，则使用率为：
```
使用率 = (300 / (12 × 50)) × 100% = 50%
```

### 每小时使用率计算

每小时使用率按照以下公式计算：
```
使用率 = (占用座位数 / 座位总数) × 100%
```

例如，如果自习室有50个座位，某小时有25个座位被占用，则该小时的使用率为：
```
使用率 = (25 / 50) × 100% = 50%
``` 