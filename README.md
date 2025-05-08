# StudySpot 自习室预约管理系统后端

## django后端

> ⚠️ **重要提示**：本项目仅用于前端开发时的接口和数据模拟，并非PJ实际合作开发的后端项目。

首先进入django项目目录

```bash
cd app
```

### 1. 开发环境启动django项目

```bash
python manage.py runserver 0.0.0.0:7778
```

### 2. 生产环境启动django项目

- 生产环境通过github actions自动容器化部署
- 容器启动后先更新数据库结构

```bash
# 创建迁移文件（如果尚未创建）
docker-compose exec studyspot-backend python manage.py makemigrations

# 应用迁移，创建表结构
docker-compose exec studyspot-backend python manage.py migrate

# 创建超级用户(如果还没创建)
docker-compose exec studyspot-backend python manage.py createsuperuser
```

## 开发进度

### 用户相关

- [ ] 用户-微信code登录 `/user/weixin-login`  
  `api.user.login(code)`
- [x] 用户-账号密码登录 `/user/login`  
  `api.user.accountLogin(data)`
- [ ] 用户-微信一键登录 `/user/wx-login`  
  `api.user.wxLogin(data)`
- [x] 用户-获取用户信息 `/user/info`  
  `api.user.getInfo()`
- [ ] 用户-更新用户信息 `/user/info`  
  `api.user.updateInfo(data)`
- [ ] 用户-获取收藏座位 `/user/favoriteSeats`  
  `api.user.getFavoriteSeats()`
- [ ] 用户-添加收藏座位 `/user/favoriteSeats`  
  `api.user.addFavoriteSeat(data)`
- [ ] 用户-删除收藏座位 `/user/favoriteSeats`  
  `api.user.deleteFavoriteSeats(data)`
- [ ] 用户-获取消息通知 `/user/notifications`  
  `api.user.getNotifications(type)`
- [ ] 用户-标记消息为已读 `/user/notifications/{id}/read`  
  `api.user.markNotificationRead(id)`
- [ ] 用户-标记所有消息为已读 `/user/notifications/readAll`  
  `api.user.markAllNotificationsRead()`

---

### 自习室相关
- [ ] 自习室-获取自习室列表 `/studyRoom/list`  
  `api.studyRoom.getList(params)`
- [ ] 自习室-获取自习室详情 `/studyRoom/{id}`  
  `api.studyRoom.getDetail(id)`
- [ ] 自习室-获取附近自习室 `/studyRoom/nearby`  
  `api.studyRoom.getNearby()`
- [ ] 自习室-获取自习室座位 `/studyRoom/{id}/seats`  
  `api.studyRoom.getSeats(id, date)`

---

### 预约相关
- [ ] 预约-创建预约 `/reservation`  
  `api.reservation.create(data)`
- [ ] 预约-获取用户预约 `/reservation/user`  
  `api.reservation.getUserReservations(status)`
- [ ] 预约-取消预约 `/reservation/{id}/cancel`  
  `api.reservation.cancel(id)`
- [ ] 预约-签到 `/reservation/{id}/checkIn`  
  `api.reservation.checkIn(id, checkInCode)`

---

### 管理员相关
- [ ] 管理员-登录 `/admin/login`  
  `api.admin.login(data)`
- [ ] 管理员-获取自习室列表 `/admin/studyRooms`  
  `api.admin.getStudyRooms()`
- [ ] 管理员-获取自习室详情 `/admin/studyRoom/{id}`  
  `api.admin.getStudyRoomDetail(id)`
- [ ] 管理员-添加自习室 `/admin/studyRoom`  
  `api.admin.addStudyRoom(data)`
- [ ] 管理员-更新自习室 `/admin/studyRoom/{id}`  
  `api.admin.updateStudyRoom(id, data)`
- [ ] 管理员-删除自习室 `/admin/studyRoom/{id}`  
  `api.admin.deleteStudyRoom(id)`
- [ ] 管理员-获取座位 `/admin/studyRoom/{roomId}/seats`  
  `api.admin.getSeats(roomId)`
- [ ] 管理员-更新座位 `/admin/studyRoom/{roomId}/seat/{seatId}`  
  `api.admin.updateSeat(roomId, seatId, data)`
- [ ] 管理员-获取预约 `/admin/reservations`  
  `api.admin.getReservations(params)`
- [ ] 管理员-预约签到 `/admin/reservation/{id}/checkIn`  
  `api.admin.checkInReservation(id)`
- [ ] 管理员-取消预约 `/admin/reservation/{id}/cancel`  
  `api.admin.cancelReservation(id)`
- [ ] 管理员-获取统计 `/admin/statistics`  
  `api.admin.getStatistics(timeRange)`
- [ ] 管理员-获取设置 `/admin/settings`  
  `api.admin.getSettings()`
- [ ] 管理员-更新设置 `/admin/settings`  
  `api.admin.updateSettings(data)`
- [ ] 管理员-刷新签到码 `/admin/studyRoom/{roomId}/refreshCheckInCode`  
  `api.admin.refreshCheckInCode(roomId)`