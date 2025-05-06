# 使用Python 3.12作为基础镜像
FROM python:3.12-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=StudySpot.settings

# 安装uv和必要依赖
RUN pip install --no-cache-dir uv whitenoise

# 创建并设置工作目录
WORKDIR /project

# 复制整个项目到容器内
COPY . .

# 使用uv根据项目配置安装依赖
RUN uv pip install --system -e .

# 设置工作目录为Django项目目录
WORKDIR /project/app

# 创建静态文件目录
RUN mkdir -p staticfiles

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 7777

# 启动命令
CMD ["python", "-m", "gunicorn", "StudySpot.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:7777"]