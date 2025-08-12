# Docker 鏡像靈活部署指南

本指南詳細說明如何使用發布的 Docker 鏡像進行各種部署場景。

## 🎯 支援的部署模式

### 1. 完整部署模式
所有組件（前端、後端、數據庫）在同一環境中部署

### 2. 分離部署模式
前後端可獨立部署，支持不同的服務器或雲平台

### 3. 外部數據庫模式
使用現有的 MySQL 數據庫服務器

### 4. 開發模式
適用於本地開發和測試

## 🔧 環境變量配置

### 前端容器環境變量

| 變量名 | 預設值 | 說明 |
|--------|--------|------|
| `BACKEND_URL` | `http://lab_web_app:8000` | 後端服務地址（內部通信） |
| `API_BASE_URL` | `/api` | API 基礎路徑 |
| `CORS_ORIGIN` | `*` | 跨域設置 |
| `APP_TITLE` | `Lab Website Framework` | 應用標題 |
| `APP_DESCRIPTION` | `Modern laboratory website framework` | 應用描述 |

### 後端容器環境變量

| 變量名 | 預設值 | 說明 |
|--------|--------|------|
| `DATABASE_URL` | `mysql+pymysql://root:lab_web_root_123@db:3306/lab_web` | 完整數據庫連接字符串 |
| `MYSQL_HOST` | `db` | MySQL 主機地址 |
| `MYSQL_PORT` | `3306` | MySQL 端口 |
| `MYSQL_ROOT_PASSWORD` | `lab_web_root_123` | MySQL root 密碼 |
| `MYSQL_DATABASE` | `lab_web` | 數據庫名稱 |
| `SECRET_KEY` | `change_me_in_production` | Flask 密鑰 |
| `JWT_SECRET_KEY` | `change_me_jwt_in_production` | JWT 密鑰 |
| `FLASK_CONFIG` | `production` | Flask 配置模式 |
| `CORS_ORIGINS` | `*` | 跨域白名單 |
| `UPLOAD_FOLDER` | `/app/media` | 檔案上傳目錄 |

## 🚀 部署示例

### 1. 完整部署（推薦新手）

```bash
# 下載配置
mkdir lab_web_deploy && cd lab_web_deploy
curl -O https://raw.githubusercontent.com/your-repo/lab_web/main/examples/docker-compose.standalone.yml
curl -O https://raw.githubusercontent.com/your-repo/lab_web/main/examples/.env.example

# 配置環境
cp .env.example .env
# 編輯 .env 文件設置您的配置

# 啟動服務
docker-compose -f docker-compose.standalone.yml up -d

# 檢查狀態
docker-compose -f docker-compose.standalone.yml ps
```

### 2. 僅前端部署（連接現有 API）

```bash
docker run -d \
  --name lab-frontend \
  -p 3000:80 \
  -e BACKEND_URL=https://api.yourdomain.com \
  -e API_BASE_URL=https://api.yourdomain.com/api \
  -e APP_TITLE="Your Lab Name" \
  -e APP_DESCRIPTION="Your lab description" \
  -e CORS_ORIGIN=https://yourdomain.com \
  ghcr.io/your-repo/frontend:latest
```

### 3. 僅後端部署（提供 API 服務）

```bash
# 先啟動 MySQL（如果需要）
docker run -d \
  --name mysql-db \
  -p 3307:3306 \
  -e MYSQL_ROOT_PASSWORD=secure_password \
  -e MYSQL_DATABASE=lab_web \
  -v mysql_data:/var/lib/mysql \
  mysql:8.0

# 然後啟動後端
docker run -d \
  --name lab-backend \
  -p 8000:8000 \
  --link mysql-db:db \
  -e DATABASE_URL="mysql+pymysql://root:secure_password@db:3306/lab_web" \
  -e SECRET_KEY="your_very_secure_secret_key" \
  -e JWT_SECRET_KEY="your_jwt_secret_key" \
  -e CORS_ORIGINS="https://yourfrontend.com,http://localhost:3000" \
  -v lab_media:/app/media \
  ghcr.io/your-repo/backend:latest
```

### 4. 使用外部數據庫

```bash
docker run -d \
  --name lab-backend-external-db \
  -p 8000:8000 \
  -e DATABASE_URL="mysql+pymysql://username:password@your-db-host.com:3306/lab_web" \
  -e SECRET_KEY="production_secret_key" \
  -e JWT_SECRET_KEY="production_jwt_key" \
  -e CORS_ORIGINS="https://yourdomain.com" \
  -v lab_media:/app/media \
  ghcr.io/your-repo/backend:latest
```

## 🔒 生產環境安全建議

### 必須更改的設置

1. **密鑰設置**：
   ```bash
   export SECRET_KEY=$(openssl rand -hex 32)
   export JWT_SECRET_KEY=$(openssl rand -hex 32)
   ```

2. **數據庫密碼**：
   ```bash
   export MYSQL_ROOT_PASSWORD=$(openssl rand -base64 32)
   ```

3. **跨域設置**：
   ```bash
   export CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

### 推薦的生產環境配置

```yaml
# docker-compose.production.yml
version: '3.8'
services:
  frontend:
    image: ghcr.io/your-repo/frontend:latest
    environment:
      - BACKEND_URL=http://backend:8000
      - API_BASE_URL=/api
      - APP_TITLE=Your Lab Production
      - CORS_ORIGIN=https://yourdomain.com
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(\`yourdomain.com\`)"
      - "traefik.http.routers.frontend.tls.certresolver=letsencrypt"

  backend:
    image: ghcr.io/your-repo/backend:latest
    environment:
      - DATABASE_URL=mysql+pymysql://user:${DB_PASSWORD}@db:3306/lab_web
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - FLASK_CONFIG=production
      - CORS_ORIGINS=https://yourdomain.com
    volumes:
      - media_data:/app/media
      - ./logs:/app/logs
```

## 🔍 故障排除

### 常見問題

1. **前端無法連接後端**
   ```bash
   # 檢查容器日誌
   docker logs lab-frontend
   docker logs lab-backend
   
   # 檢查網絡連接
   docker exec lab-frontend wget -qO- http://backend:8000/health
   ```

2. **數據庫連接失敗**
   ```bash
   # 檢查數據庫狀態
   docker exec backend python -c "
   import pymysql
   conn = pymysql.connect(host='db', user='root', password='your_password')
   print('Database connection successful')
   "
   ```

3. **跨域問題**
   ```bash
   # 確認 CORS 設置
   curl -H "Origin: https://yourdomain.com" \
        -H "Access-Control-Request-Method: POST" \
        -X OPTIONS \
        http://your-backend-url/api/health
   ```

## 📊 性能調優

### 生產環境推薦設置

```bash
# 後端工作進程數（基於 CPU 核心數）
export WORKERS=$(($(nproc) * 2 + 1))

# 內存設置
export GUNICORN_TIMEOUT=120
export GUNICORN_KEEPALIVE=2
export GUNICORN_MAX_REQUESTS=1000

# 前端 nginx 優化
docker run -d \
  --name lab-frontend-optimized \
  -p 80:80 \
  -p 443:443 \
  -v ./nginx-prod.conf:/etc/nginx/nginx.conf \
  -v ./ssl:/etc/ssl/certs \
  ghcr.io/your-repo/frontend:latest
```

## 📝 健康檢查

所有容器都內建健康檢查：

```bash
# 檢查容器健康狀態
docker ps --filter "health=healthy"

# 手動健康檢查
curl http://localhost:3000/health  # 前端
curl http://localhost:8000/health  # 後端
```

## 🔄 更新和維護

### 更新到新版本

```bash
# 拉取新鏡像
docker pull ghcr.io/your-repo/frontend:latest
docker pull ghcr.io/your-repo/backend:latest

# 重新啟動服務
docker-compose -f docker-compose.standalone.yml up -d

# 清理舊鏡像
docker image prune -f
```

### 備份數據

```bash
# 備份數據庫
docker exec mysql-db mysqldump -u root -p lab_web > backup.sql

# 備份媒體文件
docker cp lab-backend:/app/media ./media_backup
```

這個靈活的部署系統讓您可以根據具體需求選擇最適合的部署方式！