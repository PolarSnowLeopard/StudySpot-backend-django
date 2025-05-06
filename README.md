# StudySpot 自习室预约管理系统后端

## django后端

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