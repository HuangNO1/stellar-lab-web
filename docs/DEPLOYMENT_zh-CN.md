# 實驗室網站部署指南

使用 Docker 容器化的實驗室網站框架完整部署指南。

## 📋 目錄

- [系統需求](#系統需求)
- [快速開始](#快速開始)
- [環境配置](#環境配置)
- [生產環境部署](#生產環境部署)
- [開發環境](#開發環境)
- [配置說明](#配置說明)
- [資料庫管理](#資料庫管理)
- [SSL/HTTPS 設定](#sslhttps-設定)
- [備份與恢復](#備份與恢復)
- [監控與日誌](#監控與日誌)
- [故障排除](#故障排除)
- [維護](#維護)

## 系統需求

### 硬體要求
- **作業系統**: Linux (Ubuntu 20.04+, CentOS 8+, 等), macOS, 或 Windows with WSL2
- **記憶體**: 最低 2GB, 建議 4GB+
- **儲存空間**: 最低 10GB 可用空間
- **CPU**: 建議 2+ 核心

### 軟體要求
- **Docker**: 版本 20.10+
- **Docker Compose**: 版本 2.0+
- **Git**: 用於複製倉庫
- **Make**: 可選，用於便捷命令

### 網路要求
- **端口**: 3000 (前端), 8000 (後端), 3307 (MySQL), 8081 (phpMyAdmin)
- **網路存取**: 需要網路連接以下載 Docker 映像和依賴項

## 快速開始

### 1. 複製與設定

```bash
# 複製倉庫
git clone <your-repository-url>
cd lab_web

# 使用 Make 快速部署（推薦）
make deploy

# 或手動部署
cp .env.example .env
./deploy.sh prod build
./deploy.sh prod start -d
./deploy.sh prod db-init
```

### 2. 存取應用程式

- **前端**: http://localhost:3000
- **後端 API**: http://localhost:8000
- **API 文檔**: http://localhost:8000/api/docs
- **資料庫管理**: http://localhost:8081

### 3. 預設登入

- **使用者名稱**: `admin`
- **密碼**: `admin123`

⚠️ **重要**: 在生產環境中立即更改預設密碼！

## 環境配置

### 前端環境配置

前端支援不同部署場景的環境配置：

#### 開發環境
- **檔案**: `frontend/.env.development`
- **API 基底 URL**: `http://127.0.0.1:8000/api`
- **使用場景**: 本地開發，直接連接後端

```env
NODE_ENV=development
VUE_APP_API_BASE_URL=http://127.0.0.1:8000/api
```

#### 生產/Docker 環境
- **檔案**: `frontend/.env.production` (生產), `frontend/.env.docker` (Docker 構建)
- **API 基底 URL**: `/api` (通過 nginx 代理的相對路徑)
- **使用場景**: Docker 容器、生產部署

```env
NODE_ENV=production
VUE_APP_API_BASE_URL=/api
```

#### 自訂環境
建立 `frontend/.env.local` 用於自訂配置（此檔案被 Docker 和 git 忽略）：

```env
NODE_ENV=development
VUE_APP_API_BASE_URL=https://your-custom-api-domain.com/api
```

### 後端環境變數

複製 `.env.example` 到 `.env` 並自訂：

```bash
cp .env.example .env
```

生產環境需要修改的關鍵變數：

```env
# 安全性 - 必須更改
SECRET_KEY=your_very_secure_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
MYSQL_ROOT_PASSWORD=your_secure_db_password

# 端口（如需要）
FRONTEND_PORT=3000
BACKEND_PORT=8000
MYSQL_PORT=3307
PHPMYADMIN_PORT=8081

# CORS（調整為你的域名）
CORS_ORIGINS=https://your-domain.com,https://api.your-domain.com
```

## 生產環境部署

### 標準部署

```bash
# 建構所有服務
./deploy.sh prod build

# 以生產模式啟動
./deploy.sh prod start -d

# 使用範例資料初始化資料庫
./deploy.sh prod db-init

# 檢查服務狀態
./deploy.sh prod status
```

### 進階生產環境設定

#### 1. 自訂網路配置

```bash
# 建立自訂網路（可選）
docker network create --driver bridge lab_web_network
```

#### 2. 資源限制

建立 `docker-compose.override.yml` 用於資源限制：

```yaml
version: '3.8'

services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
  
  frontend:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
  
  db:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

#### 3. 持久化資料卷

資料會自動持久化在 Docker 資料卷中：
- `mysql_data`: 資料庫檔案
- `media_data`: 上傳的檔案（圖片、論文等）

## 開發環境

### 啟動開發模式

```bash
# 使用熱重載啟動
./deploy.sh dev start -d

# 或使用 Make
make dev

# 檢視日誌
./deploy.sh dev logs -f
```

### 開發環境 URLs

- **前端開發伺服器**: http://localhost:8080 (熱重載)
- **後端**: http://localhost:8000
- **資料庫**: localhost:3307

### 開發環境功能

- **熱重載**: 前端在檔案更改時自動重載
- **除錯模式**: 後端以除錯模式執行，提供詳細錯誤訊息
- **資料卷掛載**: 原始程式碼被掛載以供即時編輯

## 配置說明

### 前端配置

編輯 `frontend/docker/nginx.conf` 進行以下設定：
- 伺服器設定
- 代理配置  
- 安全標頭
- 快取策略

### 後端配置

後端配置透過環境變數和 `backend/config/config.py` 處理。

### 資料庫配置

MySQL 配置包含：
- UTF8MB4 字元集，支援完整 Unicode
- 針對中小型工作負載優化的設定
- 健康檢查和自動重啟

## 資料庫管理

### 初始化資料庫

```bash
# 建立資料表和範例資料
./deploy.sh prod db-init

# 或使用 Make
make db-init
```

### 資料庫操作

```bash
# 備份資料庫
./deploy.sh prod db-backup

# 存取 MySQL shell
./deploy.sh prod shell --service=db
# 或: make db-shell

# 自訂 SQL 執行
docker exec -it lab_web_db mysql -u root -plab_web_root_123 lab_web -e "SELECT COUNT(*) FROM admins;"
```

### 資料庫遷移

```bash
# 存取後端容器
./deploy.sh prod shell --service=backend

# 在容器內執行遷移
flask db upgrade
```

## SSL/HTTPS 設定

### 使用反向代理（推薦）

#### 選項 1: Nginx 反向代理

建立 `/etc/nginx/sites-available/lab-website`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    # 前端
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 後端 API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 選項 2: Traefik (基於 Docker)

加入到 `docker-compose.yml`:

```yaml
services:
  traefik:
    image: traefik:v2.9
    command:
      - --api.insecure=true
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.myresolver.acme.httpchallenge=true
      - --certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web
      - --certificatesresolvers.myresolver.acme.email=your-email@example.com
      - --certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt
    labels:
      - "traefik.http.routers.http-catchall.rule=hostregexp(`{host:.+}`)"
      - "traefik.http.routers.http-catchall.entrypoints=web"
      - "traefik.http.routers.http-catchall.middlewares=redirect-to-https"
      - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"

  frontend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`your-domain.com`)"
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=myresolver"

volumes:
  letsencrypt:
```

## 備份與恢復

### 自動備份

建立備份腳本 `/etc/cron.daily/lab-website-backup`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/lab-website"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# 資料庫備份
docker exec lab_web_db mysqldump -u root -plab_web_root_123 lab_web > "$BACKUP_DIR/db_$DATE.sql"

# 媒體檔案備份
docker run --rm -v lab_web_media_data:/data -v "$BACKUP_DIR":/backup alpine tar czf "/backup/media_$DATE.tar.gz" -C /data .

# 只保留最近 7 天
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "備份完成: $DATE"
```

### 手動備份/恢復

```bash
# 建立備份
./deploy.sh prod db-backup

# 從備份恢復
./deploy.sh prod db-restore --backup-file=backup_20231201_120000.sql

# 備份媒體檔案
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar czf /backup/media_backup.tar.gz -C /data .

# 恢復媒體檔案
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar xzf /backup/media_backup.tar.gz -C /data
```

## 監控與日誌

### 檢視日誌

```bash
# 所有服務
./deploy.sh prod logs -f

# 特定服務
./deploy.sh prod logs --service=backend -f
./deploy.sh prod logs --service=frontend -f

# 或使用 Make
make logs
make backend-logs
make frontend-logs
```

### 健康監控

```bash
# 檢查所有服務健康狀態
./deploy.sh prod health

# 個別服務狀態
./deploy.sh prod status

# 或使用 Make
make health
make status
```

### 日誌管理

在 `/etc/logrotate.d/lab-website` 配置日誌輪轉：

```
/path/to/lab_web/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 root root
    postrotate
        docker exec lab_web_backend kill -USR1 1 2>/dev/null || true
    endscript
}
```

## 故障排除

### 常見問題

#### 1. 端口衝突

```bash
# 檢查端口使用情況
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000

# 在 .env 檔案中更改端口
FRONTEND_PORT=3001
BACKEND_PORT=8001
```

#### 2. 資料庫連接問題

```bash
# 檢查資料庫容器
docker logs lab_web_db

# 測試資料庫連接
docker exec lab_web_db mysqladmin ping -h localhost

# 重設資料庫
./deploy.sh prod stop --service=db
docker volume rm lab_web_mysql_data
./deploy.sh prod start --service=db
./deploy.sh prod db-init
```

#### 3. 權限問題

```bash
# 修復媒體目錄權限
docker exec lab_web_backend chown -R www-data:www-data /app/media

# 修復日誌目錄權限
sudo chown -R $USER:$USER logs/
```

#### 4. 建構失敗

```bash
# 清除建構快取
./deploy.sh prod build --no-cache --rebuild

# 移除所有容器並重新建構
./deploy.sh prod clean
./deploy.sh prod build
```

#### 5. 前端無法載入

```bash
# 檢查 nginx 日誌
docker logs lab_web_frontend

# 使用新模組重新建構前端
cd frontend
docker build --no-cache -t lab-website-frontend .
```

### 除錯模式

在開發環境中啟用除錯模式：

```bash
# 以開發模式啟動
./deploy.sh dev start -d

# 檢視詳細後端日誌
./deploy.sh dev logs --service=backend-dev -f
```

### 容器 Shell 存取

```bash
# 後端 shell
./deploy.sh prod shell --service=backend
# 或: make backend-shell

# 前端 shell  
./deploy.sh prod shell --service=frontend
# 或: make frontend-shell

# 資料庫 shell
./deploy.sh prod shell --service=db
# 或: make db-shell
```

## 維護

### 更新

#### 更新應用程式

```bash
# 拉取最新程式碼
git pull origin main

# 重新建構並重啟
./deploy.sh prod stop
./deploy.sh prod build --rebuild
./deploy.sh prod start -d

# 執行新的遷移
./deploy.sh prod shell --service=backend
flask db upgrade
```

#### 更新 Docker 映像

```bash
# 拉取最新基礎映像
docker pull node:18-alpine
docker pull python:3.9-slim
docker pull mysql:8.0
docker pull nginx:stable-alpine

# 使用更新的映像重新建構
./deploy.sh prod build --no-cache --rebuild
./deploy.sh prod restart
```

### 安全更新

1. **定期更新基礎 Docker 映像**
2. **監控依賴項安全建議**
3. **更新密碼和金鑰**
4. **檢查和更新 CORS 設定**
5. **保持 SSL 憑證為最新**

### 效能調優

#### 資料庫優化

編輯 MySQL 配置：

```yaml
# 在 docker-compose.yml 中，添加命令參數
command: >
  --character-set-server=utf8mb4
  --collation-server=utf8mb4_unicode_ci
  --innodb-buffer-pool-size=512M
  --innodb-log-file-size=128M
  --max-connections=200
```

#### 前端優化

更新 `frontend/docker/nginx.conf`:

```nginx
# 啟用 gzip 壓縮
gzip on;
gzip_vary on;
gzip_min_length 10240;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

# 瀏覽器快取
location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 擴展

對於高流量部署：

1. **使用多個前端副本**
2. **實施 Redis 快取**  
3. **設定資料庫讀取副本**
4. **對靜態資源使用 CDN**
5. **實施負載平衡**

擴展配置範例：

```yaml
services:
  frontend:
    deploy:
      replicas: 3
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
      
  nginx-lb:
    image: nginx:alpine
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
      - "443:443"
```

## 生產環境檢查清單

上線前：

- [ ] 更改所有預設密碼
- [ ] 更新生產環境的環境變數
- [ ] 配置 SSL/HTTPS
- [ ] 設定自動備份
- [ ] 配置日誌輪轉
- [ ] 設定監控
- [ ] 測試備份和恢復程序
- [ ] 配置防火牆規則
- [ ] 設定域名和 DNS
- [ ] 測試所有功能
- [ ] 更新 CORS 設定
- [ ] 檢查安全標頭
- [ ] 設定錯誤追蹤
- [ ] 配置電子郵件通知（如已實現）
- [ ] 記錄自訂配置

## 支援

如需更多幫助：

- 查看[主要 README](../README.md) 了解功能概覽
- 查看[後端文檔](../backend/README.md) 了解 API 詳情
- 查看[前端文檔](../frontend/README.md) 了解 UI 資訊
- 在專案倉庫中建立 issue
- 檢查 Docker 和容器日誌以獲取錯誤詳情

---

*本部署指南與實驗室網站框架一起維護。如需最新更新，請查看專案倉庫。*