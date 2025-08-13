# ECS 雲服務器部署指南

完整的 Amazon ECS 或其他雲服務器環境部署指南，適用於從零開始的空服務器環境。

## 📋 目錄

- [項目概覽](#項目概覽)
- [ECS 部署前提條件](#ecs-部署前提條件)
- [需要修改的配置](#需要修改的配置)
- [空環境 ECS 服務器部署步驟](#空環境-ecs-服務器部署步驟)
- [生產環境優化配置](#生產環境優化配置)
- [部署驗證和監控](#部署驗證和監控)
- [ECS 特定優化建議](#ecs-特定優化建議)
- [故障排除](#故障排除)

## 🔍 項目概覽

這是一個完整的實驗室網站框架，包含：

- **前端**: Vue.js + TypeScript，使用 Nginx 提供服務
- **後端**: Flask Python API 服務
- **資料庫**: MySQL 8.0 資料庫
- **管理工具**: phpMyAdmin (可選)
- **容器化**: 完全 Docker 化部署

### 架構圖

```
Internet → [ECS Load Balancer] → [Nginx Frontend] → [Flask Backend] → [MySQL Database]
                                      ↓
                               [Static Files & Media]
```

## 🚀 ECS 部署前提條件

### 1. 硬體需求

| 組件 | 最低需求 | 建議配置 |
|------|----------|----------|
| **CPU** | 2 vCPU | 4+ vCPU |
| **記憶體** | 4GB RAM | 8GB+ RAM |
| **存儲** | 20GB | 50GB+ (SSD) |
| **網路** | 公網 IP | 固定 IP + CDN |

### 2. 系統需求

- **作業系統**: 
  - Ubuntu 20.04+ (推薦)
  - CentOS 8+ / Rocky Linux 8+
  - Amazon Linux 2
- **容器環境**:
  - Docker 20.10+
  - Docker Compose v2.0+
- **版本控制**: Git 最新版本
- **網路工具**: curl, wget

### 3. 端口需求

```bash
# 應用服務端口
3000  # 前端服務 (Vue.js + Nginx)
8000  # 後端 API (Flask)
3307  # MySQL 資料庫 (映射端口)
8081  # phpMyAdmin 管理介面 (可選)

# 生產環境端口
80    # HTTP 服務
443   # HTTPS 服務 (SSL/TLS)
22    # SSH 管理端口
```

### 4. 安全組配置 (AWS ECS)

```bash
# 入站規則
SSH (22)     - 來源: 您的 IP
HTTP (80)    - 來源: 0.0.0.0/0
HTTPS (443)  - 來源: 0.0.0.0/0
Custom (3000) - 來源: 0.0.0.0/0 (臨時，生產環境建議移除)
Custom (8000) - 來源: 0.0.0.0/0 (臨時，生產環境建議移除)

# 出站規則  
All traffic - 來源: 0.0.0.0/0
```

## 📋 需要修改的配置

### 1. 環境變數配置 (.env)

創建並配置 `.env` 檔案：

```env
# ===========================================
# 資料庫安全配置 - 必須修改
# ===========================================
MYSQL_ROOT_PASSWORD=your_very_secure_db_root_password_2024
MYSQL_PASSWORD=your_secure_user_password_2024
MYSQL_DATABASE=lab_web
MYSQL_USER=lab_web_user

# ===========================================
# 應用安全配置 - 必須修改
# ===========================================
SECRET_KEY=your_extremely_secure_secret_key_min_32_chars_2024
JWT_SECRET_KEY=your_jwt_secret_key_for_authentication_2024

# Flask 配置
FLASK_CONFIG=production
FLASK_DEBUG=0

# ===========================================
# 網域和 CORS 配置 - 根據您的域名修改
# ===========================================
CORS_ORIGINS=https://your-domain.com,https://api.your-domain.com,https://www.your-domain.com

# ===========================================
# 端口配置 (可選修改)
# ===========================================
FRONTEND_PORT=3000
BACKEND_PORT=8000
MYSQL_PORT=3307
PHPMYADMIN_PORT=8081

# ===========================================
# 應用配置
# ===========================================
UPLOAD_FOLDER=/app/media
NODE_ENV=production
CHOKIDAR_USEPOLLING=false
```

### 2. 前端環境配置

修改 `frontend/.env.production`:

```env
# 生產環境配置
NODE_ENV=production

# API 配置 - 根據部署方式選擇其一
# 選項 1: 使用相對路徑 (推薦，通過 nginx 代理)
VUE_APP_API_BASE_URL=/api

# 選項 2: 使用絕對路徑 (如果 API 在不同域名)
# VUE_APP_API_BASE_URL=https://api.your-domain.com/api
```

### 3. Docker Compose 網路配置

在主要的 `docker-compose.yml` 中調整 CORS 配置：

```yaml
backend:
  environment:
    # 更新 CORS 設定以匹配您的域名
    CORS_ORIGINS: "https://your-domain.com,https://api.your-domain.com,https://www.your-domain.com"
    
    # 如果需要外部訪問資料庫 (不建議生產環境)
    # 資料庫連接配置
    DATABASE_URL: mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@db:3306/${MYSQL_DATABASE}?charset=utf8mb4
```

### 4. 資料庫安全配置

為生產環境增強資料庫安全性，編輯 `docker-compose.yml`:

```yaml
db:
  environment:
    # 使用強密碼
    MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD}
  # 限制資料庫只能內部訪問 (生產環境推薦)
  # ports:
  #   - "127.0.0.1:3307:3306"  # 只允許本機訪問
  # 或完全移除端口映射，只允許容器間通信
```

## 🛠 空環境 ECS 服務器部署步驟

### 第一步：系統初始化和更新

```bash
# ===== CentOS/Rocky Linux/Amazon Linux 2 =====
sudo yum update -y
sudo yum install -y git curl wget vim unzip

# ===== Ubuntu/Debian =====
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget vim unzip

# 設定系統時區 (可選)
sudo timedatectl set-timezone Asia/Taipei
# 或其他時區，例如: Asia/Shanghai, UTC

# 檢查系統資訊
echo "=== 系統資訊 ==="
cat /etc/os-release
free -h
df -h
```

### 第二步：安裝 Docker 和 Docker Compose

```bash
# ===== 安裝 Docker =====
# 使用官方安裝腳本 (適用所有 Linux 發行版)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 啟動 Docker 服務
sudo systemctl start docker
sudo systemctl enable docker

# 將當前用戶加入 docker 組 (避免每次使用 sudo)
sudo usermod -aG docker $USER

# ===== 安裝 Docker Compose =====
# 獲取最新版本
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 創建符號連結 (可選)
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# ===== 驗證安裝 =====
echo "=== 驗證 Docker 安裝 ==="
docker --version
docker-compose --version

# 重新登錄以應用組權限變更，或執行:
newgrp docker

# 測試 Docker (可選)
docker run hello-world
```

### 第三步：配置系統防火牆

```bash
# ===== CentOS/Rocky Linux (firewalld) =====
sudo systemctl start firewalld
sudo systemctl enable firewalld

# 開放必要端口
sudo firewall-cmd --permanent --add-port=80/tcp    # HTTP
sudo firewall-cmd --permanent --add-port=443/tcp   # HTTPS  
sudo firewall-cmd --permanent --add-port=3000/tcp  # Frontend (臨時)
sudo firewall-cmd --permanent --add-port=8000/tcp  # Backend (臨時)
sudo firewall-cmd --permanent --add-port=22/tcp    # SSH
sudo firewall-cmd --reload

# ===== Ubuntu (ufw) =====
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3000/tcp  # Frontend (臨時)
sudo ufw allow 8000/tcp  # Backend (臨時)
sudo ufw status

echo "=== 防火牆配置完成 ==="
```

### 第四步：部署項目

```bash
# 1. 克隆項目到服務器
cd /opt  # 或您偏好的目錄
sudo git clone <your-repository-url> lab_web
sudo chown -R $USER:$USER lab_web
cd lab_web

# 2. 配置環境變數
cp .env.example .env

# 編輯環境配置文件 (重要!)
nano .env
# 或使用 vim: vim .env

# 請按照上面的 "需要修改的配置" 部分修改以下項目:
# - MYSQL_ROOT_PASSWORD
# - MYSQL_PASSWORD  
# - SECRET_KEY
# - JWT_SECRET_KEY
# - CORS_ORIGINS (設定您的域名)

echo "=== 環境配置完成，請確保已修改所有安全相關設定 ==="
```

### 第五步：執行部署

```bash
# ===== 方式一：使用提供的部署腳本 (推薦) =====

# 讓部署腳本可執行
chmod +x deploy.sh

# 構建所有服務 (首次部署)
echo "=== 開始構建 Docker 映像... ==="
./deploy.sh prod build --no-cache

# 在後台啟動所有服務
echo "=== 啟動服務... ==="
./deploy.sh prod start -d

# 等待服務啟動 (重要!)
echo "=== 等待服務啟動... ==="
sleep 30

# 初始化資料庫和示例資料
echo "=== 初始化資料庫... ==="
./deploy.sh prod db-init

# ===== 方式二：直接使用 Docker Compose =====
# docker-compose up --build -d
# sleep 30
# docker-compose exec backend python scripts/development/init_db.py

echo "=== 部署完成! ==="
```

### 第六步：驗證部署

```bash
# 檢查服務狀態
echo "=== 檢查服務狀態 ==="
./deploy.sh prod status

# 執行健康檢查
echo "=== 執行健康檢查 ==="  
./deploy.sh prod health

# 檢查服務日誌 (如有錯誤)
echo "=== 檢查服務日誌 ==="
./deploy.sh prod logs --service=backend
./deploy.sh prod logs --service=frontend
./deploy.sh prod logs --service=db

# 測試服務訪問
echo "=== 測試服務訪問 ==="
curl -f http://localhost:3000 && echo "前端服務正常" || echo "前端服務異常"
curl -f http://localhost:8000/health && echo "後端服務正常" || echo "後端服務異常"

echo "=== 部署驗證完成 ==="
echo "前端訪問: http://您的服務器IP:3000"
echo "後端 API: http://您的服務器IP:8000"
echo "API 文檔: http://您的服務器IP:8000/api/docs"
echo "資料庫管理: http://您的服務器IP:8081"
echo ""
echo "預設管理員帳號:"
echo "用戶名: admin"
echo "密碼: admin123"
echo "⚠️  請立即修改預設密碼!"
```

## 🔧 生產環境優化配置

### 1. SSL/HTTPS 配置

#### 選項 1: 使用 Let's Encrypt + Nginx (推薦)

```bash
# 安裝 Nginx 作為反向代理
# CentOS/Rocky Linux
sudo yum install -y nginx

# Ubuntu
sudo apt install -y nginx

# 啟動 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 安裝 Certbot 
sudo yum install -y certbot python3-certbot-nginx  # CentOS
# 或
sudo apt install -y certbot python3-certbot-nginx  # Ubuntu

# 獲取 SSL 證書 (替換 your-domain.com)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 設定自動續期
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

#### 選項 2: 使用 Cloudflare SSL (簡單)

如果您使用 Cloudflare，可以直接在 Cloudflare 面板中啟用 SSL。

### 2. Nginx 反向代理配置

創建 `/etc/nginx/sites-available/lab-website` (Ubuntu) 或 `/etc/nginx/conf.d/lab-website.conf` (CentOS):

```nginx
# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS 主配置
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL 配置
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # 安全標頭
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # 前端代理
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持 (如果需要)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # 後端 API 代理  
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # API 特定配置
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    # 靜態文件優化
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        proxy_pass http://localhost:3000;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options nosniff;
    }
}
```

```bash
# 啟用站點 (Ubuntu)
sudo ln -s /etc/nginx/sites-available/lab-website /etc/nginx/sites-enabled/

# 測試 Nginx 配置
sudo nginx -t

# 重啟 Nginx
sudo systemctl restart nginx
```

### 3. 自動化備份設置

創建 `/opt/scripts/backup-lab-website.sh`:

```bash
#!/bin/bash

# 實驗室網站自動備份腳本
# 使用方法: ./backup-lab-website.sh

set -e

# 配置變數
BACKUP_DIR="/opt/backups/lab-website"
PROJECT_DIR="/opt/lab_web"  # 修改為您的項目路徑
DATE=$(date +%Y%m%d_%H%M%S)
RETAIN_DAYS=7  # 保留天數

# 載入環境變數
if [ -f "$PROJECT_DIR/.env" ]; then
    source "$PROJECT_DIR/.env"
else
    echo "錯誤: 找不到 .env 文件"
    exit 1
fi

# 創建備份目錄
mkdir -p "$BACKUP_DIR"

echo "=== 開始備份 $(date) ==="

# 1. 資料庫備份
echo "備份資料庫..."
docker exec lab_web_db mysqldump \
    -u root -p"$MYSQL_ROOT_PASSWORD" \
    --single-transaction \
    --routines \
    --triggers \
    "$MYSQL_DATABASE" > "$BACKUP_DIR/database_$DATE.sql"

# 壓縮資料庫備份
gzip "$BACKUP_DIR/database_$DATE.sql"

# 2. 媒體文件備份
echo "備份媒體文件..."
docker run --rm \
    -v lab_web_media_data:/data \
    -v "$BACKUP_DIR":/backup \
    alpine tar czf "/backup/media_$DATE.tar.gz" -C /data .

# 3. 配置文件備份
echo "備份配置文件..."
tar czf "$BACKUP_DIR/config_$DATE.tar.gz" \
    -C "$PROJECT_DIR" \
    .env \
    docker-compose.yml \
    docker-compose.dev.yml \
    deploy.sh

# 4. 清理舊備份
echo "清理 $RETAIN_DAYS 天前的舊備份..."
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETAIN_DAYS -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETAIN_DAYS -delete

# 5. 備份統計
echo "=== 備份完成 $(date) ==="
echo "備份位置: $BACKUP_DIR"
echo "備份文件:"
ls -lah "$BACKUP_DIR"/*"$DATE"*

# 6. 可選: 上傳到雲端 (AWS S3 示例)
# aws s3 cp "$BACKUP_DIR" s3://your-backup-bucket/lab-website/ --recursive --exclude "*" --include "*$DATE*"
```

```bash
# 設置腳本權限
sudo chmod +x /opt/scripts/backup-lab-website.sh

# 設置定時任務 (每天凌晨 2 點執行)
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/scripts/backup-lab-website.sh >> /var/log/lab-website-backup.log 2>&1") | crontab -

# 測試備份腳本
sudo /opt/scripts/backup-lab-website.sh
```

### 4. 系統服務配置 (Systemd)

創建 systemd 服務 `/etc/systemd/system/lab-website.service`:

```ini
[Unit]
Description=Lab Website Docker Services
Requires=docker.service
After=docker.service
StartLimitIntervalSec=0

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/lab_web
ExecStart=/opt/lab_web/deploy.sh prod start -d
ExecStop=/opt/lab_web/deploy.sh prod stop
ExecReload=/opt/lab_web/deploy.sh prod restart
TimeoutStartSec=300
TimeoutStopSec=120
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# 重載 systemd 配置
sudo systemctl daemon-reload

# 啟用開機自啟
sudo systemctl enable lab-website.service

# 啟動服務
sudo systemctl start lab-website.service

# 檢查服務狀態
sudo systemctl status lab-website.service
```

### 5. 監控和日誌配置

```bash
# 配置 logrotate 
sudo tee /etc/logrotate.d/lab-website << 'EOF'
/opt/lab_web/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 root root
    postrotate
        docker exec lab_web_backend kill -USR1 1 2>/dev/null || true
        docker exec lab_web_frontend nginx -s reopen 2>/dev/null || true
    endscript
}
EOF

# 創建監控腳本
sudo tee /opt/scripts/monitor-lab-website.sh << 'EOF'
#!/bin/bash
# 簡單的服務監控腳本

check_service() {
    local service_name=$1
    local url=$2
    
    if curl -sf "$url" > /dev/null 2>&1; then
        echo "✓ $service_name 運行正常"
        return 0
    else
        echo "✗ $service_name 出現問題"
        return 1
    fi
}

echo "=== Lab Website 服務監控 $(date) ==="
check_service "前端服務" "http://localhost:3000"
check_service "後端服務" "http://localhost:8000/health"
check_service "資料庫服務" "http://localhost:8081" # phpMyAdmin

# 檢查 Docker 容器狀態
echo ""
echo "=== 容器狀態 ==="
docker ps --filter name=lab_web --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
EOF

sudo chmod +x /opt/scripts/monitor-lab-website.sh

# 每 5 分鐘檢查一次
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/scripts/monitor-lab-website.sh >> /var/log/lab-website-monitor.log 2>&1") | crontab -
```

## 🔍 部署驗證和監控

### 全面的部署驗證檢查清單

```bash
# 創建驗證腳本
cat > /tmp/deployment-verification.sh << 'EOF'
#!/bin/bash

echo "=========================================="
echo "    實驗室網站部署驗證檢查"
echo "=========================================="

# 1. Docker 服務檢查
echo ""
echo "1. 檢查 Docker 容器狀態:"
docker ps --filter name=lab_web --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 2. 服務健康檢查  
echo ""
echo "2. 服務健康檢查:"
./deploy.sh prod health 2>/dev/null || echo "使用備用檢查方法"

# 手動健康檢查
echo ""
echo "3. 手動連接測試:"

# 前端測試
if curl -sf http://localhost:3000 > /dev/null 2>&1; then
    echo "✓ 前端服務 (3000) - 正常"
else
    echo "✗ 前端服務 (3000) - 異常"
fi

# 後端測試
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ 後端服務 (8000) - 正常"
else
    echo "✗ 後端服務 (8000) - 異常"
fi

# API 文檔測試
if curl -sf http://localhost:8000/api/docs > /dev/null 2>&1; then
    echo "✓ API 文檔 (8000/api/docs) - 正常"
else
    echo "✗ API 文檔 (8000/api/docs) - 異常"
fi

# phpMyAdmin 測試 (如果啟用)
if curl -sf http://localhost:8081 > /dev/null 2>&1; then
    echo "✓ phpMyAdmin (8081) - 正常"
else
    echo "✗ phpMyAdmin (8081) - 異常或未啟用"
fi

# 4. 資料庫連接測試
echo ""
echo "4. 資料庫連接測試:"
if docker exec lab_web_db mysqladmin ping -h localhost --silent > /dev/null 2>&1; then
    echo "✓ MySQL 資料庫 - 連接正常"
else
    echo "✗ MySQL 資料庫 - 連接異常"
fi

# 5. 存儲卷檢查
echo ""
echo "5. Docker 存儲卷檢查:"
docker volume ls | grep lab_web

# 6. 網路檢查
echo ""
echo "6. Docker 網路檢查:"
docker network ls | grep lab_web

# 7. 日誌檢查 (最近 10 行)
echo ""
echo "7. 最近的錯誤日誌 (如有):"
docker logs lab_web_backend --tail 10 2>/dev/null | grep -i error || echo "後端無錯誤日誌"
docker logs lab_web_frontend --tail 10 2>/dev/null | grep -i error || echo "前端無錯誤日誌"

echo ""
echo "=========================================="
echo "驗證完成！請檢查上述結果。"
echo "如果所有服務都顯示正常，您可以訪問:"
echo "前端: http://$(curl -s ifconfig.me || echo 'YOUR_SERVER_IP'):3000"
echo "後端: http://$(curl -s ifconfig.me || echo 'YOUR_SERVER_IP'):8000"
echo "=========================================="
EOF

chmod +x /tmp/deployment-verification.sh
/tmp/deployment-verification.sh
```

### 預設登入資訊

部署完成後，使用以下預設帳號登入：

- **管理員用戶名**: `admin`
- **管理員密碼**: `admin123`

⚠️ **重要安全提醒**: 
1. 立即登入並修改預設密碼
2. 創建新的管理員帳號
3. 如可能，禁用預設帳號

### 監控設置

```bash
# 創建簡單的監控儀表板腳本
sudo tee /opt/scripts/dashboard.sh << 'EOF'
#!/bin/bash

clear
echo "=========================================="
echo "       實驗室網站服務儀表板"
echo "=========================================="
echo "最後更新: $(date)"
echo ""

# 系統資源
echo "系統資源:"
echo "CPU 使用率: $(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4"%"}')"
echo "記憶體使用: $(free -h | awk 'NR==2{printf "%.1f%% (%s/%s)\n", $3*100/$2, $3, $2}')"
echo "磁碟使用: $(df -h / | awk 'NR==2{print $5 " (" $3 "/" $2 ")"}')"
echo ""

# Docker 容器狀態
echo "容器狀態:"
docker ps --filter name=lab_web --format "table {{.Names}}\t{{.Status}}" | head -4
echo ""

# 服務端點狀態
echo "服務端點:"
curl -sf http://localhost:3000 > /dev/null && echo "✓ 前端 (3000)" || echo "✗ 前端 (3000)"
curl -sf http://localhost:8000/health > /dev/null && echo "✓ 後端 (8000)" || echo "✗ 後端 (8000)"
docker exec lab_web_db mysqladmin ping -h localhost --silent > /dev/null 2>&1 && echo "✓ 資料庫" || echo "✗ 資料庫"
echo ""

echo "按 Ctrl+C 結束監控"
sleep 10
EOF

chmod +x /opt/scripts/dashboard.sh

# 運行儀表板
# watch -n 10 /opt/scripts/dashboard.sh
```

## 🎯 ECS 特定優化建議

### 1. 使用 AWS Application Load Balancer (ALB)

取代 Nginx 反向代理，使用 AWS ALB 提供更好的擴展性:

```yaml
# docker-compose.aws.yml 示例
version: '3.8'
services:
  backend:
    environment:
      # ALB 健康檢查
      HEALTH_CHECK_PATH: /health
      # ALB 目標組配置
      ALB_TARGET_GROUP: lab-website-backend
      
  frontend:
    environment:
      # ALB 配置
      ALB_TARGET_GROUP: lab-website-frontend
```

### 2. 資料庫遷移至 AWS RDS

為提高可靠性和管理性，建議將 MySQL 遷移至 AWS RDS:

```env
# .env 配置 for RDS
DATABASE_URL=mysql+pymysql://username:password@lab-website.cluster-xxxxx.us-west-2.rds.amazonaws.com:3306/lab_web?charset=utf8mb4
MYSQL_HOST=lab-website.cluster-xxxxx.us-west-2.rds.amazonaws.com
MYSQL_PORT=3306

# 移除本地資料庫容器
# 在 docker-compose.yml 中註釋掉 db 服務
```

### 3. 使用 Amazon EFS 進行檔案存儲

```yaml
# docker-compose.aws.yml - 使用 EFS
services:
  backend:
    volumes:
      # 掛載 EFS 檔案系統
      - /mnt/efs/lab_web/media:/app/media
      - /mnt/efs/lab_web/logs:/app/logs
      
  frontend:
    volumes:
      - /mnt/efs/lab_web/static:/usr/share/nginx/html/static
```

### 4. CloudWatch 監控和日誌

```bash
# 安裝 CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
sudo rpm -U ./amazon-cloudwatch-agent.rpm

# 配置 CloudWatch Agent
sudo tee /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << 'EOF'
{
    "logs": {
        "logs_collected": {
            "files": {
                "collect_list": [
                    {
                        "file_path": "/opt/lab_web/logs/*.log",
                        "log_group_name": "/aws/ec2/lab-website",
                        "log_stream_name": "{instance_id}/application"
                    }
                ]
            }
        }
    },
    "metrics": {
        "namespace": "LabWebsite/Application",
        "metrics_collected": {
            "cpu": {
                "measurement": ["cpu_usage_idle", "cpu_usage_iowait"]
            },
            "disk": {
                "measurement": ["used_percent"],
                "resources": ["*"]
            },
            "mem": {
                "measurement": ["mem_used_percent"]
            }
        }
    }
}
EOF

# 啟動 CloudWatch Agent
sudo systemctl start amazon-cloudwatch-agent
sudo systemctl enable amazon-cloudwatch-agent
```

### 5. Auto Scaling Group 配置

```bash
# 創建 AMI 準備腳本
sudo tee /opt/scripts/prepare-ami.sh << 'EOF'
#!/bin/bash
# ECS Auto Scaling AMI 準備腳本

# 確保服務在開機時自動啟動
sudo systemctl enable lab-website.service

# 清理敏感資訊 (創建 AMI 前)
sudo rm -f /opt/lab_web/.env
sudo history -c
sudo rm -f /home/*/.bash_history
sudo rm -f /root/.bash_history

echo "AMI 準備完成"
EOF

chmod +x /opt/scripts/prepare-ami.sh
```

### 6. 使用 ElastiCache Redis 作為快取層

```env
# .env 增加 Redis 配置
REDIS_URL=redis://lab-website.xxxxx.cache.amazonaws.com:6379
CACHE_TYPE=redis
CACHE_DEFAULT_TIMEOUT=3600
```

```python
# 在 backend/config/config.py 中增加 Redis 配置
import os

class Config:
    REDIS_URL = os.environ.get('REDIS_URL')
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
```

## 🔄 ECS 遷移和數據備份方案

當您的 ECS 服務器即將到期或需要遷移到新的服務器時，以下是完整的數據備份和遷移方案。

### 📋 備份清單

需要備份的主要組件：

1. **資料庫數據** - MySQL 資料庫完整備份
2. **媒體文件** - 用戶上傳的圖片、論文等文件
3. **配置文件** - 環境變數和 Docker 配置
4. **程式碼** - 如有自訂修改
5. **SSL 證書** - 如果使用自簽名證書
6. **日誌文件** - 運行日誌和錯誤記錄

### 🚀 快速遷移腳本 (一鍵備份)

創建完整的遷移備份腳本：

```bash
# 創建遷移備份腳本
sudo tee /opt/scripts/full-migration-backup.sh << 'EOF'
#!/bin/bash

# ============================================
# 實驗室網站完整遷移備份腳本
# 用途: ECS 服務器到期前的完整數據遷移備份
# ============================================

set -e

# 配置變數
PROJECT_DIR="/opt/lab_web"
BACKUP_BASE="/opt/migration-backup"
DATE=$(date +%Y%m%d_%H%M%S)
MIGRATION_DIR="$BACKUP_BASE/lab_web_migration_$DATE"
COMPRESS_BACKUP=true

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 檢查必要條件
check_prerequisites() {
    log_info "檢查遷移前提條件..."
    
    if [ ! -d "$PROJECT_DIR" ]; then
        log_error "項目目錄不存在: $PROJECT_DIR"
        exit 1
    fi
    
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        log_error "環境配置文件不存在: $PROJECT_DIR/.env"
        exit 1
    fi
    
    # 檢查 Docker 容器狀態
    if ! docker ps --filter name=lab_web --format "{{.Names}}" | grep -q lab_web; then
        log_warning "部分或所有 Docker 容器未運行，某些備份可能無法完成"
    fi
    
    log_success "前提條件檢查完成"
}

# 載入環境變數
load_environment() {
    log_info "載入環境配置..."
    source "$PROJECT_DIR/.env"
    log_success "環境配置載入完成"
}

# 創建備份目錄
create_backup_structure() {
    log_info "創建備份目錄結構..."
    
    mkdir -p "$MIGRATION_DIR"/{database,media,config,logs,ssl,scripts,docker-images}
    
    log_success "備份目錄創建完成: $MIGRATION_DIR"
}

# 1. 數據庫完整備份
backup_database() {
    log_info "開始數據庫備份..."
    
    local db_backup_file="$MIGRATION_DIR/database/lab_web_complete_$DATE.sql"
    
    # 完整數據庫備份 (包含結構、數據、觸發器、存儲過程等)
    if docker exec lab_web_db mysqldump \
        -u root -p"$MYSQL_ROOT_PASSWORD" \
        --single-transaction \
        --routines \
        --triggers \
        --events \
        --hex-blob \
        --opt \
        --lock-tables=false \
        "$MYSQL_DATABASE" > "$db_backup_file"; then
        
        log_success "數據庫備份完成: $(basename $db_backup_file)"
        
        # 壓縮數據庫備份
        if [ "$COMPRESS_BACKUP" = true ]; then
            gzip "$db_backup_file"
            log_success "數據庫備份已壓縮: $(basename $db_backup_file).gz"
        fi
    else
        log_error "數據庫備份失敗"
        return 1
    fi
    
    # 創建數據庫恢復腳本
    cat > "$MIGRATION_DIR/database/restore-database.sh" << 'RESTORE_EOF'
#!/bin/bash
# 數據庫恢復腳本

echo "=== 數據庫恢復腳本 ==="
echo "使用方法: ./restore-database.sh [備份文件路徑]"

BACKUP_FILE=${1:-"lab_web_complete_*.sql.gz"}

if [ -f "$BACKUP_FILE" ]; then
    echo "正在恢復數據庫: $BACKUP_FILE"
    
    # 如果是壓縮文件
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        zcat "$BACKUP_FILE" | docker exec -i lab_web_db mysql -u root -p lab_web
    else
        cat "$BACKUP_FILE" | docker exec -i lab_web_db mysql -u root -p lab_web
    fi
    
    echo "數據庫恢復完成"
else
    echo "錯誤: 備份文件不存在: $BACKUP_FILE"
    exit 1
fi
RESTORE_EOF
    
    chmod +x "$MIGRATION_DIR/database/restore-database.sh"
}

# 2. 媒體文件備份
backup_media_files() {
    log_info "開始媒體文件備份..."
    
    # 備份 Docker 卷中的媒體文件
    if docker run --rm \
        -v lab_web_media_data:/data \
        -v "$MIGRATION_DIR/media":/backup \
        alpine sh -c "cp -r /data/* /backup/ 2>/dev/null || echo '媒體目錄可能為空'"; then
        
        log_success "媒體文件備份完成"
        
        # 創建媒體文件壓縮包
        if [ "$COMPRESS_BACKUP" = true ] && [ "$(ls -A $MIGRATION_DIR/media)" ]; then
            cd "$MIGRATION_DIR/media" && tar czf "../media_files_$DATE.tar.gz" * && cd - > /dev/null
            rm -rf "$MIGRATION_DIR/media"/*
            log_success "媒體文件已壓縮: media_files_$DATE.tar.gz"
        fi
    else
        log_warning "媒體文件備份可能不完整"
    fi
}

# 3. 配置文件備份
backup_configurations() {
    log_info "開始配置文件備份..."
    
    # 複製主要配置文件
    cp "$PROJECT_DIR/.env" "$MIGRATION_DIR/config/"
    cp "$PROJECT_DIR/docker-compose.yml" "$MIGRATION_DIR/config/" 2>/dev/null || true
    cp "$PROJECT_DIR/docker-compose.dev.yml" "$MIGRATION_DIR/config/" 2>/dev/null || true
    cp "$PROJECT_DIR/deploy.sh" "$MIGRATION_DIR/config/" 2>/dev/null || true
    
    # 備份 Nginx 配置 (如果存在)
    if [ -f "/etc/nginx/sites-available/lab-website" ]; then
        cp "/etc/nginx/sites-available/lab-website" "$MIGRATION_DIR/config/nginx-lab-website.conf"
        log_success "Nginx 配置已備份"
    fi
    
    # 備份系統服務文件
    if [ -f "/etc/systemd/system/lab-website.service" ]; then
        cp "/etc/systemd/system/lab-website.service" "$MIGRATION_DIR/config/"
        log_success "系統服務配置已備份"
    fi
    
    # 創建配置信息文檔
    cat > "$MIGRATION_DIR/config/migration-info.md" << INFO_EOF
# 遷移配置信息

## 備份時間
$(date)

## 原服務器信息
- 主機名: $(hostname)
- IP 地址: $(curl -s ifconfig.me 2>/dev/null || echo "未知")
- 操作系統: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)
- Docker 版本: $(docker --version)
- Docker Compose 版本: $(docker-compose --version)

## 服務配置
- 項目目錄: $PROJECT_DIR
- 前端端口: ${FRONTEND_PORT:-3000}
- 後端端口: ${BACKEND_PORT:-8000}
- 數據庫端口: ${MYSQL_PORT:-3307}

## 數據庫信息
- 數據庫名: ${MYSQL_DATABASE:-lab_web}
- 用戶名: ${MYSQL_USER:-lab_web_user}

## Docker 容器狀態
$(docker ps --filter name=lab_web --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}")

## Docker 卷信息
$(docker volume ls | grep lab_web)

## 重要提醒
1. 恢復前請確保新服務器已安裝 Docker 和 Docker Compose
2. 恢復數據庫前請先創建空的 MySQL 容器
3. 媒體文件需要恢復到正確的 Docker 卷中
4. 記得修改新服務器的環境變數 (.env 文件)
5. 配置新服務器的 SSL 證書和域名
INFO_EOF

    log_success "配置文件備份完成"
}

# 4. 日誌文件備份
backup_logs() {
    log_info "開始日誌文件備份..."
    
    # 備份應用日誌
    if [ -d "$PROJECT_DIR/logs" ]; then
        cp -r "$PROJECT_DIR/logs"/* "$MIGRATION_DIR/logs/" 2>/dev/null || true
        log_success "應用日誌備份完成"
    fi
    
    # 導出 Docker 容器日誌
    for container in lab_web_backend lab_web_frontend lab_web_db; do
        if docker ps --filter name=$container --format "{{.Names}}" | grep -q $container; then
            docker logs $container --details > "$MIGRATION_DIR/logs/${container}_$DATE.log" 2>&1
            log_success "容器日誌已導出: ${container}_$DATE.log"
        fi
    done
}

# 5. SSL 證書備份
backup_ssl_certificates() {
    log_info "開始 SSL 證書備份..."
    
    # Let's Encrypt 證書
    if [ -d "/etc/letsencrypt/live" ]; then
        sudo cp -r /etc/letsencrypt/live/* "$MIGRATION_DIR/ssl/" 2>/dev/null || true
        sudo cp -r /etc/letsencrypt/archive/* "$MIGRATION_DIR/ssl/" 2>/dev/null || true
        sudo chown -R $USER:$USER "$MIGRATION_DIR/ssl/"
        log_success "Let's Encrypt 證書已備份"
    fi
    
    # 自定義證書位置 (根據需要修改)
    # if [ -f "/path/to/custom/certificate.crt" ]; then
    #     cp /path/to/custom/certificate.crt "$MIGRATION_DIR/ssl/"
    #     cp /path/to/custom/private.key "$MIGRATION_DIR/ssl/"
    #     log_success "自定義 SSL 證書已備份"
    # fi
}

# 6. 腳本和自定義文件備份
backup_scripts() {
    log_info "開始腳本備份..."
    
    # 備份自定義腳本
    if [ -d "/opt/scripts" ]; then
        cp -r /opt/scripts/* "$MIGRATION_DIR/scripts/" 2>/dev/null || true
        log_success "自定義腳本已備份"
    fi
    
    # 備份 crontab
    crontab -l > "$MIGRATION_DIR/scripts/crontab_backup.txt" 2>/dev/null || echo "# 無 crontab 配置" > "$MIGRATION_DIR/scripts/crontab_backup.txt"
    log_success "Crontab 配置已備份"
}

# 7. Docker 鏡像備份 (可選)
backup_docker_images() {
    log_info "開始 Docker 鏡像備份..."
    
    # 備份自定義構建的鏡像
    local images=("lab-website-backend:latest" "lab-website-frontend:latest")
    
    for image in "${images[@]}"; do
        if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "$image"; then
            local filename=$(echo "$image" | tr ':/' '_')
            docker save "$image" | gzip > "$MIGRATION_DIR/docker-images/${filename}.tar.gz"
            log_success "Docker 鏡像已備份: $image"
        fi
    done
}

# 創建完整的恢復指南
create_migration_guide() {
    log_info "創建遷移指南..."
    
    cat > "$MIGRATION_DIR/MIGRATION_GUIDE.md" << 'GUIDE_EOF'
# 實驗室網站遷移恢復指南

## 🚀 新服務器準備

### 1. 系統環境準備
```bash
# 更新系統
sudo yum update -y  # CentOS/Rocky Linux
# 或
sudo apt update && sudo apt upgrade -y  # Ubuntu

# 安裝必要工具
sudo yum install -y git curl wget vim  # CentOS/Rocky Linux
# 或
sudo apt install -y git curl wget vim  # Ubuntu
```

### 2. 安裝 Docker 和 Docker Compose
```bash
# 安裝 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 安裝 Docker Compose
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 重新登錄或執行
newgrp docker
```

## 📦 恢復步驟

### 1. 上傳備份文件
```bash
# 將整個備份目錄上傳到新服務器
# 使用 scp, rsync, 或雲存儲下載
scp -r lab_web_migration_* user@new-server:/opt/
```

### 2. 恢復項目代碼
```bash
cd /opt
git clone <your-repository-url> lab_web
cd lab_web

# 恢復配置文件
cp /path/to/migration/config/.env .
cp /path/to/migration/config/docker-compose.yml . 2>/dev/null || true
```

### 3. 恢復數據庫
```bash
# 先啟動數據庫容器
./deploy.sh prod start --service=db -d
sleep 30

# 恢復數據庫數據
cd /path/to/migration/database
./restore-database.sh lab_web_complete_*.sql.gz
```

### 4. 恢復媒體文件
```bash
# 如果媒體文件是壓縮包
cd /path/to/migration/media
tar xzf media_files_*.tar.gz

# 恢復到 Docker 卷
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine sh -c "cp -r /backup/* /data/"
```

### 5. 啟動完整服務
```bash
cd /opt/lab_web
./deploy.sh prod start -d
```

### 6. 恢復 SSL 證書和 Nginx 配置
```bash
# 恢復 Let's Encrypt 證書
sudo cp -r /path/to/migration/ssl/* /etc/letsencrypt/live/

# 恢復 Nginx 配置
sudo cp /path/to/migration/config/nginx-lab-website.conf /etc/nginx/sites-available/lab-website
sudo ln -s /etc/nginx/sites-available/lab-website /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

### 7. 恢復系統服務和腳本
```bash
# 恢復系統服務
sudo cp /path/to/migration/config/lab-website.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lab-website.service

# 恢復自定義腳本
sudo cp -r /path/to/migration/scripts/* /opt/scripts/
sudo chmod +x /opt/scripts/*.sh

# 恢復 crontab
crontab /path/to/migration/scripts/crontab_backup.txt
```

## ✅ 驗證恢復結果

```bash
# 檢查服務狀態
./deploy.sh prod status
./deploy.sh prod health

# 測試網站訪問
curl -f http://localhost:3000
curl -f http://localhost:8000/health

# 檢查數據庫
docker exec lab_web_db mysql -u root -p -e "USE lab_web; SHOW TABLES;"
```

## ⚠️ 重要注意事項

1. **域名和 DNS**: 記得將域名解析指向新服務器 IP
2. **防火牆配置**: 確保新服務器開放了必要端口
3. **環境變數**: 檢查並更新 .env 文件中的配置
4. **SSL 證書**: 如果使用新域名，需要重新申請證書
5. **測試功能**: 完成遷移後務必測試所有功能
6. **備份驗證**: 確保所有數據都已正確恢復

## 🆘 遇到問題？

- 檢查 Docker 容器日誌: `docker logs container_name`
- 檢查網站功能是否正常
- 確認數據庫連接和數據完整性
- 驗證文件上傳和媒體訪問功能
GUIDE_EOF

    log_success "遷移指南創建完成"
}

# 創建快速恢復腳本
create_restore_script() {
    log_info "創建快速恢復腳本..."
    
    cat > "$MIGRATION_DIR/quick-restore.sh" << 'RESTORE_SCRIPT_EOF'
#!/bin/bash
# 快速恢復腳本

echo "=== 實驗室網站快速恢復腳本 ==="
echo "⚠️  請確保新服務器已安裝 Docker 和 Docker Compose"
echo "⚠️  請確保已克隆項目代碼到 /opt/lab_web"
echo ""

read -p "是否已滿足上述條件？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "請先滿足前提條件再運行此腳本"
    exit 1
fi

MIGRATION_DIR=$(dirname $(readlink -f $0))
PROJECT_DIR="/opt/lab_web"

echo "開始快速恢復..."

# 1. 恢復配置文件
echo "恢復配置文件..."
cp "$MIGRATION_DIR/config/.env" "$PROJECT_DIR/"

# 2. 啟動數據庫
echo "啟動數據庫服務..."
cd "$PROJECT_DIR"
./deploy.sh prod start --service=db -d
sleep 30

# 3. 恢復數據庫
echo "恢復數據庫數據..."
cd "$MIGRATION_DIR/database"
if [ -f "lab_web_complete_"*.sql.gz ]; then
    DB_FILE=$(ls lab_web_complete_*.sql.gz | head -1)
    zcat "$DB_FILE" | docker exec -i lab_web_db mysql -u root -p${MYSQL_ROOT_PASSWORD:-lab_web_root_123} lab_web
    echo "數據庫恢復完成"
else
    echo "未找到數據庫備份文件"
fi

# 4. 恢復媒體文件
echo "恢復媒體文件..."
cd "$MIGRATION_DIR"
if [ -f "media/media_files_"*.tar.gz ]; then
    MEDIA_FILE=$(ls media/media_files_*.tar.gz | head -1)
    docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine sh -c "cd /backup && tar xzf $MEDIA_FILE && cp -r media/* /data/ 2>/dev/null || true"
    echo "媒體文件恢復完成"
elif [ -d "media" ] && [ "$(ls -A media)" ]; then
    docker run --rm -v lab_web_media_data:/data -v "$MIGRATION_DIR/media":/backup alpine cp -r /backup/* /data/
    echo "媒體文件恢復完成"
fi

# 5. 啟動完整服務
echo "啟動所有服務..."
cd "$PROJECT_DIR"
./deploy.sh prod start -d

echo ""
echo "=== 快速恢復完成 ==="
echo "前端訪問: http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR_SERVER_IP'):3000"
echo "後端 API: http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR_SERVER_IP'):8000"
echo "請參考 MIGRATION_GUIDE.md 完成其他配置（SSL、Nginx 等）"
RESTORE_SCRIPT_EOF

    chmod +x "$MIGRATION_DIR/quick-restore.sh"
    log_success "快速恢復腳本創建完成"
}

# 生成備份報告
generate_backup_report() {
    log_info "生成備份報告..."
    
    local report_file="$MIGRATION_DIR/BACKUP_REPORT.md"
    
    cat > "$report_file" << REPORT_EOF
# 遷移備份報告

**備份時間**: $(date)  
**備份目錄**: $MIGRATION_DIR  
**原項目路徑**: $PROJECT_DIR  

## 📊 備份統計

| 類型 | 狀態 | 大小 | 說明 |
|------|------|------|------|
| 數據庫 | ✅ 完成 | $(du -sh $MIGRATION_DIR/database 2>/dev/null | cut -f1 || echo "N/A") | 包含完整數據和結構 |
| 媒體文件 | $([ -d "$MIGRATION_DIR/media" ] && echo "✅ 完成" || echo "⚠️ 空") | $(du -sh $MIGRATION_DIR/media 2>/dev/null | cut -f1 || echo "N/A") | 用戶上傳文件 |
| 配置文件 | ✅ 完成 | $(du -sh $MIGRATION_DIR/config 2>/dev/null | cut -f1 || echo "N/A") | 環境配置和系統配置 |
| 日誌文件 | ✅ 完成 | $(du -sh $MIGRATION_DIR/logs 2>/dev/null | cut -f1 || echo "N/A") | 應用和容器日誌 |
| SSL 證書 | $([ -d "$MIGRATION_DIR/ssl" ] && [ "$(ls -A $MIGRATION_DIR/ssl)" ] && echo "✅ 完成" || echo "⚠️ 無") | $(du -sh $MIGRATION_DIR/ssl 2>/dev/null | cut -f1 || echo "N/A") | SSL/TLS 證書 |
| 腳本文件 | ✅ 完成 | $(du -sh $MIGRATION_DIR/scripts 2>/dev/null | cut -f1 || echo "N/A") | 自動化腳本和 cron 配置 |

**總備份大小**: $(du -sh $MIGRATION_DIR 2>/dev/null | cut -f1 || echo "計算中...")

## 📁 目錄結構

\`\`\`
$(tree -L 2 "$MIGRATION_DIR" 2>/dev/null || find "$MIGRATION_DIR" -type d | head -10)
\`\`\`

## ✅ 備份文件清單

### 數據庫文件
$(ls -la "$MIGRATION_DIR/database/" 2>/dev/null || echo "無數據庫備份")

### 配置文件
$(ls -la "$MIGRATION_DIR/config/" 2>/dev/null || echo "無配置文件")

### 重要文件
- ✅ 遷移指南: MIGRATION_GUIDE.md
- ✅ 快速恢復腳本: quick-restore.sh
- ✅ 備份報告: BACKUP_REPORT.md

## 🔄 下一步操作

1. **下載備份**: 將整個 \`$MIGRATION_DIR\` 目錄下載到安全位置
2. **上傳到新服務器**: 使用 scp/rsync 將備份上傳到新服務器
3. **按照遷移指南**: 參考 \`MIGRATION_GUIDE.md\` 進行恢復
4. **快速恢復**: 或使用 \`quick-restore.sh\` 進行自動恢復

## ⚠️ 重要提醒

- 請確保備份文件安全存儲
- 建議創建多個備份副本
- 在新服務器恢復前建議先測試
- 記得更新域名 DNS 解析
- 驗證所有功能正常後再停用舊服務器
REPORT_EOF

    log_success "備份報告生成完成"
}

# 主函數
main() {
    echo "========================================"
    echo "    實驗室網站完整遷移備份工具"
    echo "========================================"
    echo "開始時間: $(date)"
    echo "項目目錄: $PROJECT_DIR"
    echo "備份目錄: $MIGRATION_DIR"
    echo ""
    
    check_prerequisites
    load_environment
    create_backup_structure
    
    echo "開始備份各組件..."
    backup_database
    backup_media_files
    backup_configurations
    backup_logs
    backup_ssl_certificates
    backup_scripts
    backup_docker_images
    
    echo "創建遷移工具..."
    create_migration_guide
    create_restore_script
    generate_backup_report
    
    echo ""
    echo "========================================"
    echo "           遷移備份完成！"
    echo "========================================"
    echo "備份位置: $MIGRATION_DIR"
    echo "總大小: $(du -sh $MIGRATION_DIR | cut -f1)"
    echo ""
    echo "下一步操作:"
    echo "1. 檢查備份內容: ls -la $MIGRATION_DIR"
    echo "2. 查看備份報告: cat $MIGRATION_DIR/BACKUP_REPORT.md"
    echo "3. 下載備份到本地安全位置"
    echo "4. 在新服務器上按照 MIGRATION_GUIDE.md 進行恢復"
    echo "5. 或使用 quick-restore.sh 進行快速恢復"
    echo ""
    echo "完成時間: $(date)"
    echo "========================================"
}

# 執行主函數
main "$@"
EOF

chmod +x /opt/scripts/full-migration-backup.sh
sudo chown $USER:$USER /opt/scripts/full-migration-backup.sh

echo "完整遷移備份腳本創建完成！"
echo "使用方法: sudo /opt/scripts/full-migration-backup.sh"
```

### 🔧 分步驟手動備份方法

如果您不想使用自動腳本，也可以按以下步驟手動備份：

#### 1. 數據庫備份

```bash
# 創建備份目錄
mkdir -p ~/lab_web_backup/{database,media,config,logs}

# 備份數據庫 (替換密碼)
docker exec lab_web_db mysqldump \
  -u root -p你的資料庫密碼 \
  --single-transaction \
  --routines \
  --triggers \
  lab_web > ~/lab_web_backup/database/lab_web_$(date +%Y%m%d).sql

# 壓縮數據庫備份
gzip ~/lab_web_backup/database/lab_web_$(date +%Y%m%d).sql
```

#### 2. 媒體文件備份

```bash
# 備份 Docker 卷中的媒體文件
docker run --rm \
  -v lab_web_media_data:/data \
  -v ~/lab_web_backup/media:/backup \
  alpine tar czf /backup/media_files.tar.gz -C /data .
```

#### 3. 配置文件備份

```bash
# 備份項目配置文件
cp /opt/lab_web/.env ~/lab_web_backup/config/
cp /opt/lab_web/docker-compose.yml ~/lab_web_backup/config/
cp /opt/lab_web/deploy.sh ~/lab_web_backup/config/

# 備份 Nginx 配置 (如果使用)
sudo cp /etc/nginx/sites-available/lab-website ~/lab_web_backup/config/nginx.conf 2>/dev/null || true

# 備份系統服務配置
sudo cp /etc/systemd/system/lab-website.service ~/lab_web_backup/config/ 2>/dev/null || true
```

#### 4. SSL 證書備份

```bash
# Let's Encrypt 證書備份
sudo cp -r /etc/letsencrypt/live/* ~/lab_web_backup/ssl/ 2>/dev/null || true
sudo chown -R $USER:$USER ~/lab_web_backup/ssl/
```

#### 5. 創建完整壓縮包

```bash
# 創建最終備份壓縮包
cd ~/
tar czf lab_web_complete_backup_$(date +%Y%m%d).tar.gz lab_web_backup/

echo "備份完成！文件位置："
echo "~/lab_web_complete_backup_$(date +%Y%m%d).tar.gz"
```

### 📥 新服務器恢復步驟

#### 1. 準備新服務器環境

```bash
# 安裝 Docker 和 Docker Compose (參考上面的安裝步驟)

# 克隆項目代碼
cd /opt
git clone <your-repository-url> lab_web
cd lab_web
```

#### 2. 恢復配置文件

```bash
# 上傳並解壓備份文件
scp lab_web_complete_backup_*.tar.gz user@new-server:~/
ssh user@new-server
cd ~/ && tar xzf lab_web_complete_backup_*.tar.gz

# 恢復配置文件
cp ~/lab_web_backup/config/.env /opt/lab_web/
cp ~/lab_web_backup/config/docker-compose.yml /opt/lab_web/ 2>/dev/null || true
```

#### 3. 恢復數據庫

```bash
cd /opt/lab_web

# 先啟動數據庫容器
./deploy.sh prod start --service=db -d
sleep 30

# 恢復數據庫數據
zcat ~/lab_web_backup/database/lab_web_*.sql.gz | docker exec -i lab_web_db mysql -u root -p lab_web
```

#### 4. 恢復媒體文件

```bash
# 解壓媒體文件到 Docker 卷
docker run --rm \
  -v lab_web_media_data:/data \
  -v ~/lab_web_backup/media:/backup \
  alpine tar xzf /backup/media_files.tar.gz -C /data
```

#### 5. 啟動服務並驗證

```bash
# 啟動所有服務
./deploy.sh prod start -d

# 檢查服務狀態
./deploy.sh prod status
./deploy.sh prod health

# 測試訪問
curl -f http://localhost:3000
curl -f http://localhost:8000/health
```

### 💾 自動化定期備份 (預防性)

為了避免數據丟失，建議設置定期備份：

```bash
# 創建定期備份腳本
sudo tee /opt/scripts/daily-backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/daily"
DATE=$(date +%Y%m%d)
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

# 數據庫備份
docker exec lab_web_db mysqldump -u root -p${MYSQL_ROOT_PASSWORD} lab_web | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# 媒體文件備份
docker run --rm -v lab_web_media_data:/data -v "$BACKUP_DIR":/backup alpine tar czf "/backup/media_$DATE.tar.gz" -C /data .

# 清理舊備份
find "$BACKUP_DIR" -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Daily backup completed: $DATE"
EOF

chmod +x /opt/scripts/daily-backup.sh

# 設置每日自動備份 (凌晨 2 點)
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/scripts/daily-backup.sh >> /var/log/daily-backup.log 2>&1") | crontab -
```

### ⚡ 緊急快速備份

如果 ECS 即將到期，需要緊急備份最重要的數據：

```bash
#!/bin/bash
# 緊急備份腳本 - 只備份最關鍵數據

DATE=$(date +%Y%m%d_%H%M%S)
EMERGENCY_BACKUP="/tmp/emergency_backup_$DATE"
mkdir -p "$EMERGENCY_BACKUP"

echo "開始緊急備份..."

# 1. 最重要：數據庫
docker exec lab_web_db mysqldump -u root -p --all-databases | gzip > "$EMERGENCY_BACKUP/all_databases.sql.gz"

# 2. 媒體文件
docker run --rm -v lab_web_media_data:/data -v "$EMERGENCY_BACKUP":/backup alpine tar czf /backup/media.tar.gz -C /data .

# 3. 配置文件
cp /opt/lab_web/.env "$EMERGENCY_BACKUP/"

# 4. 創建壓縮包
cd /tmp && tar czf "emergency_backup_$DATE.tar.gz" "emergency_backup_$DATE"
echo "緊急備份完成: /tmp/emergency_backup_$DATE.tar.gz"
echo "請立即下載此文件！"
```

### 📱 備份驗證清單

完成備份後，請檢查：

- [ ] 數據庫備份文件存在且不為空
- [ ] 媒體文件備份包含所有上傳的文件  
- [ ] 配置文件 (.env) 已正確備份
- [ ] SSL 證書已備份 (如果使用)
- [ ] 自定義腳本和配置已保存
- [ ] 備份文件已下載到安全位置
- [ ] 在測試環境中驗證恢復流程

這樣您就可以安全地將整個實驗室網站遷移到新的 ECS 服務器了！

## 🚨 故障排除

### 常見問題和解決方案

#### 1. 容器無法啟動

```bash
# 檢查容器日誌
docker logs lab_web_backend
docker logs lab_web_frontend  
docker logs lab_web_db

# 檢查端口衝突
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3307

# 解決端口衝突 - 修改 .env
FRONTEND_PORT=3001
BACKEND_PORT=8001
MYSQL_PORT=3308
```

#### 2. 資料庫連接問題

```bash
# 檢查資料庫容器日誌
docker logs lab_web_db

# 測試資料庫連接
docker exec lab_web_db mysqladmin ping -h localhost -u root -p

# 重置資料庫 (謹慎使用)
./deploy.sh prod stop --service=db
docker volume rm lab_web_mysql_data
./deploy.sh prod start --service=db -d
sleep 30
./deploy.sh prod db-init
```

#### 3. 前端無法載入

```bash
# 檢查前端容器日誌
docker logs lab_web_frontend

# 檢查 Nginx 配置
docker exec lab_web_frontend nginx -t

# 重新構建前端 (如有問題)
./deploy.sh prod build --service=frontend --no-cache --rebuild
./deploy.sh prod restart --service=frontend
```

#### 4. 後端 API 錯誤

```bash
# 檢查後端日誌
docker logs lab_web_backend -f

# 進入後端容器調試
docker exec -it lab_web_backend bash

# 檢查環境變數
docker exec lab_web_backend env | grep FLASK
docker exec lab_web_backend env | grep DATABASE
```

#### 5. 權限問題

```bash
# 修復媒體目錄權限
docker exec lab_web_backend chown -R www-data:www-data /app/media
docker exec lab_web_backend chmod -R 755 /app/media

# 修復日誌目錄權限
sudo chown -R $USER:$USER /opt/lab_web/logs/
sudo chmod -R 644 /opt/lab_web/logs/*.log
```

#### 6. 記憶體不足

```bash
# 檢查系統資源
free -h
df -h

# 增加 swap 空間 (臨時解決)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

#### 7. SSL 證書問題

```bash
# 檢查 SSL 證書狀態
sudo certbot certificates

# 手動續期證書
sudo certbot renew --dry-run
sudo certbot renew

# 檢查 Nginx SSL 配置
sudo nginx -t
```

### 緊急恢復程序

```bash
# 創建緊急恢復腳本
sudo tee /opt/scripts/emergency-recovery.sh << 'EOF'
#!/bin/bash
echo "=== 緊急恢復程序 ==="

# 1. 停止所有服務
echo "停止所有服務..."
cd /opt/lab_web
./deploy.sh prod stop

# 2. 清理問題容器
echo "清理問題容器..."
docker container prune -f

# 3. 重新構建並啟動
echo "重新構建並啟動..."
./deploy.sh prod build --no-cache
./deploy.sh prod start -d

# 4. 等待服務啟動
echo "等待服務啟動..."
sleep 60

# 5. 檢查服務狀態
echo "檢查服務狀態..."
./deploy.sh prod health

echo "=== 恢復程序完成 ==="
EOF

chmod +x /opt/scripts/emergency-recovery.sh
```

### 支援和文檔

如需更多幫助：

- 查看 [主要 README](../README.md) 了解功能概覽
- 查看 [標準部署指南](./DEPLOYMENT_zh-CN.md) 了解基本部署
- 查看 [Docker 參考文檔](./DOCKER_REFERENCE_zh-CN.md) 了解 Docker 配置
- 在專案倉庫中建立 issue 報告問題
- 檢查容器日誌以獲取詳細錯誤資訊

---

## 📝 總結

這份 ECS 部署指南提供了從空環境服務器到完整生產環境的詳細部署流程，包括：

✅ **完整的環境準備**: 從系統更新到 Docker 安裝  
✅ **詳細的配置說明**: 安全性和生產環境配置  
✅ **自動化部署腳本**: 一鍵部署和管理  
✅ **生產環境優化**: SSL、監控、備份、擴展性  
✅ **全面的故障排除**: 常見問題和解決方案  
✅ **AWS 特定優化**: ECS、RDS、EFS、CloudWatch 整合

按照這份指南，您可以成功在任何雲服務器環境中部署實驗室網站框架，並確保其在生產環境中的穩定運行。

*本 ECS 部署指南與實驗室網站框架同步維護。如需最新更新，請查看專案倉庫。*