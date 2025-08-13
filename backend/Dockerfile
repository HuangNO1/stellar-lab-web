FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建媒体上传目录
RUN mkdir -p /app/media/lab_logo \
    && mkdir -p /app/media/member_avatar \
    && mkdir -p /app/media/paper \
    && mkdir -p /app/media/other

# 设置媒体目录权限
RUN chmod -R 755 /app/media

# 创建启动脚本
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# 设置默认后端端口环境变量
ENV BACKEND_PORT=8000

# 暴露默认端口 8000 (运行时可通过环境变量动态配置)
# 注意：EXPOSE 指令仅用于文档目的，实际端口由环境变量决定
EXPOSE 8000

# 创建健康检查脚本
RUN echo '#!/bin/bash\ncurl -f http://localhost:${BACKEND_PORT:-8000}/health || exit 1' > /healthcheck.sh && chmod +x /healthcheck.sh

# 健康检查 - 使用脚本以支持环境变量
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD /healthcheck.sh

# 启动应用
ENTRYPOINT ["/app/docker-entrypoint.sh"]