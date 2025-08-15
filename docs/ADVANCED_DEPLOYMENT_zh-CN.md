# 進階部署指南

進階部署情境完整指南，包括雲服務器、本地構建策略和靈活部署配置。

> 📘 **主要部署指南**: 標準部署情境請先參考 **[DEPLOYMENT_zh-CN.md](./DEPLOYMENT_zh-CN.md)**。

## 📋 目錄

- [雲服務器部署](#雲服務器部署)
- [本地構建 + 鏡像部署](#本地構建--鏡像部署)
- [靈活部署配置](#靈活部署配置)
- [生產環境優化](#生產環境優化)
- [多服務器和擴展](#多服務器和擴展)
- [進階故障排除](#進階故障排除)

---

# 雲服務器部署

Amazon ECS、AWS EC2、阿里雲 ECS、騰訊雲或其他雲服務器環境的完整部署指南。

## 🚀 雲端部署前提條件

### 硬體需求

| 組件 | 最低需求 | 建議配置 |
|------|----------|----------|
| **CPU** | 2 vCPU | 4+ vCPU |
| **記憶體** | 4GB RAM | 8GB+ RAM |
| **存儲** | 20GB | 50GB+ (SSD) |
| **網路** | 公網 IP | 固定 IP + CDN |

### 系統需求

- **作業系統**: 
  - Ubuntu 20.04+ (推薦)
  - CentOS 8+ / Rocky Linux 8+
  - Amazon Linux 2
  - Debian 11+

- **軟體需求**:
  - Docker 20.10+
  - Docker Compose 2.0+
  - Git
  - curl, wget
  - sudo 權限

### 網路需求

- **入站端口**: 80, 443, 22 (SSH)
- **出站**: 完整網路存取用於 Docker 鏡像下載
- **可選**: 開發用自訂端口 (3000, 8000, 8081)

## 📋 雲服務器部署步驟

### 步驟 1: 服務器準備

```bash
# 更新系統套件
sudo apt update && sudo apt upgrade -y

# 安裝必需套件
sudo apt install -y curl wget git unzip

# 安裝 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安裝 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 驗證安裝
docker --version
docker-compose --version
```

### 步驟 2: 複製和配置專案

```bash
# 複製倉庫
git clone <your-repository-url>
cd lab_web

# 配置環境
cp .env.example .env
nano .env  # 編輯生產環境設定
```

### 步驟 3: 雲端部署必需的配置修改

編輯 `.env` 檔案進行雲端部署：

```env
# 安全性 - 生產環境必須修改
SECRET_KEY=your_very_secure_secret_key_here_min_32_chars
JWT_SECRET_KEY=your_jwt_secret_key_here_min_32_chars
MYSQL_ROOT_PASSWORD=your_very_secure_database_password

# 網路配置 (如需要可調整端口)
FRONTEND_PORT=3000
BACKEND_PORT=8000
MYSQL_PORT=3307
PHPMYADMIN_PORT=8081

# CORS 配置 (替換為你的域名)
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com

# Flask 配置
FLASK_CONFIG=production
```

### 步驟 4: 在雲服務器上部署

```bash
# 構建並啟動服務
./deploy.sh prod build
./deploy.sh prod start -d

# 初始化資料庫
./deploy.sh prod db-init

# 驗證部署
./deploy.sh prod status
./deploy.sh prod health
```

### 步驟 5: 雲端特定優化

#### 配置防火牆 (Ubuntu/CentOS)

```bash
# Ubuntu (ufw)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

#### 設定反向代理 (Nginx)

```bash
# 安裝 Nginx
sudo apt install nginx -y

# 配置反向代理
sudo tee /etc/nginx/sites-available/lab-website << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 啟用網站
sudo ln -s /etc/nginx/sites-available/lab-website /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### SSL 證書配置 (Let's Encrypt)

```bash
# 安裝 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 獲取 SSL 證書
sudo certbot --nginx -d your-domain.com

# 自動續期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

# 本地構建 + 鏡像部署

快速部署方案：在本地構建 Docker 鏡像，打包上傳到服務器，避免服務器上的耗時構建過程。

## 🚀 優勢

- **⚡ 速度快**: 服務器部署時間從 10-15 分鐘縮短到 2-3 分鐘
- **📦 離線部署**: 支持離線環境，無需服務器聯網構建
- **🔄 版本控制**: 支持多版本鏡像管理
- **🛠️ 靈活性**: 可選擇性更新前端或後端
- **💾 節省資源**: 減少服務器 CPU 和網絡使用
- **🌏 優化**: 內建鏡像源加速，改善網絡連接

## 📋 本地構建流程

### 步驟 1: 本地鏡像構建

創建構建腳本 `scripts/build-images.sh`：

```bash
#!/bin/bash
set -e

VERSION="${1:-latest}"
BUILD_BACKEND=true
BUILD_FRONTEND=true
NO_CACHE=""

# 解析參數
while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            BUILD_FRONTEND=false
            shift
            ;;
        --frontend-only)
            BUILD_BACKEND=false
            shift
            ;;
        --no-cache)
            NO_CACHE="--no-cache"
            shift
            ;;
        *)
            VERSION="$1"
            shift
            ;;
    esac
done

echo "構建版本為: $VERSION 的鏡像"

if [ "$BUILD_BACKEND" = true ]; then
    echo "構建後端鏡像..."
    docker build $NO_CACHE -t lab-website-backend:$VERSION ./backend
fi

if [ "$BUILD_FRONTEND" = true ]; then
    echo "構建前端鏡像..."
    docker build $NO_CACHE -t lab-website-frontend:$VERSION ./frontend
fi

echo "構建完成！"
docker images | grep lab-website
```

### 步驟 2: 打包和上傳

創建打包腳本 `scripts/package-images.sh`：

```bash
#!/bin/bash
set -e

VERSION="${1:-latest}"
PACKAGE_ONLY=false
SERVER=""
USER="root"
REMOTE_PATH="/opt/lab_web"

# 解析參數
while [[ $# -gt 0 ]]; do
    case $1 in
        --package-only)
            PACKAGE_ONLY=true
            shift
            ;;
        --server)
            SERVER="$2"
            shift 2
            ;;
        --user)
            USER="$2"
            shift 2
            ;;
        --path)
            REMOTE_PATH="$2"
            shift 2
            ;;
        *)
            VERSION="$1"
            shift
            ;;
    esac
done

# 創建部署套件
PACKAGE_DIR="docker-images"
mkdir -p $PACKAGE_DIR

echo "匯出 Docker 鏡像..."
docker save lab-website-backend:$VERSION | gzip > $PACKAGE_DIR/backend-$VERSION.tar.gz
docker save lab-website-frontend:$VERSION | gzip > $PACKAGE_DIR/frontend-$VERSION.tar.gz

# 複製部署檔案
cp docker-compose.yml $PACKAGE_DIR/
cp .env.example $PACKAGE_DIR/.env
cp deploy.sh $PACKAGE_DIR/

# 創建服務器部署腳本
cat > $PACKAGE_DIR/deploy-from-images.sh << 'EOF'
#!/bin/bash
set -e

VERSION="${1:-latest}"

echo "載入 Docker 鏡像..."
docker load < backend-$VERSION.tar.gz
docker load < frontend-$VERSION.tar.gz

echo "啟動服務..."
docker-compose down 2>/dev/null || true
docker-compose up -d

echo "部署完成！"
EOF

chmod +x $PACKAGE_DIR/deploy-from-images.sh

if [ "$PACKAGE_ONLY" = true ]; then
    echo "套件已創建在 $PACKAGE_DIR/"
    echo "上傳到服務器並執行: ./deploy-from-images.sh $VERSION"
    exit 0
fi

if [ -n "$SERVER" ]; then
    echo "上傳到服務器 $SERVER..."
    rsync -av --progress $PACKAGE_DIR/ $USER@$SERVER:$REMOTE_PATH/
    
    echo "在服務器上部署..."
    ssh $USER@$SERVER "cd $REMOTE_PATH && ./deploy-from-images.sh $VERSION"
    
    echo "在 $SERVER 上部署完成！"
fi
```

### 步驟 3: 服務器部署

在服務器上，上傳套件後：

```bash
# 載入並部署鏡像
cd /path/to/uploaded/package
./deploy-from-images.sh latest

# 驗證部署
docker-compose ps
curl http://localhost:3000
```

---

# 靈活部署配置

支援各種部署情境和環境配置。

## 🎯 支援的部署模式

### 1. 完整部署模式
所有組件（前端、後端、資料庫）在同一環境中部署。

### 2. 分離部署模式
前後端可獨立部署，支援不同的服務器或雲平台。

### 3. 外部資料庫模式
使用現有的 MySQL 資料庫服務器。

### 4. 開發模式
適用於本地開發和測試。

## 🔧 環境變數配置

### 前端容器環境變數

| 變數名 | 預設值 | 說明 |
|--------|--------|------|
| `BACKEND_URL` | `http://lab_web_app:8000` | 後端服務地址（內部通信） |
| `API_BASE_URL` | `/api` | API 基礎路徑 |
| `CORS_ORIGIN` | `*` | 跨域設定 |
| `APP_TITLE` | `Lab Website Framework` | 應用標題 |
| `APP_DESCRIPTION` | `Modern laboratory website framework` | 應用描述 |

### 後端容器環境變數

| 變數名 | 預設值 | 說明 |
|--------|--------|------|
| `DATABASE_URL` | `mysql+pymysql://root:lab_web_root_123@db:3306/lab_web` | 完整資料庫連接字符串 |
| `MYSQL_HOST` | `db` | MySQL 主機地址 |
| `MYSQL_PORT` | `3306` | MySQL 端口 |
| `MYSQL_ROOT_PASSWORD` | `lab_web_root_123` | MySQL root 密碼 |
| `MYSQL_DATABASE` | `lab_web` | 資料庫名稱 |
| `SECRET_KEY` | `change_me_in_production` | Flask 密鑰 |
| `JWT_SECRET_KEY` | `change_me_jwt_in_production` | JWT 密鑰 |
| `FLASK_CONFIG` | `production` | Flask 配置模式 |
| `CORS_ORIGINS` | `*` | 跨域白名單 |
| `UPLOAD_FOLDER` | `/app/media` | 檔案上傳目錄 |

## 🚀 部署示例

### 1. 完整部署（推薦新手）

```bash
# 創建 docker-compose.yml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: your_secure_password
      MYSQL_DATABASE: lab_web
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped

  backend:
    image: lab-website-backend:latest
    environment:
      DATABASE_URL: mysql+pymysql://root:your_secure_password@db:3306/lab_web
      SECRET_KEY: your_secret_key
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    image: lab-website-frontend:latest
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  mysql_data:
```

### 2. 分離部署

**後端服務器：**
```bash
# docker-compose.backend.yml
version: '3.8'

services:
  backend:
    image: lab-website-backend:latest
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://user:pass@external-db-server:3306/lab_web
      SECRET_KEY: your_secret_key
      CORS_ORIGINS: https://your-frontend-domain.com
    restart: unless-stopped
```

**前端服務器：**
```bash
# docker-compose.frontend.yml
version: '3.8'

services:
  frontend:
    image: lab-website-frontend:latest
    ports:
      - "80:80"
    environment:
      API_BASE_URL: https://your-backend-domain.com/api
    restart: unless-stopped
```

### 3. 外部資料庫模式

```bash
version: '3.8'

services:
  backend:
    image: lab-website-backend:latest
    environment:
      DATABASE_URL: mysql+pymysql://username:password@external-mysql-server.com:3306/lab_web
      SECRET_KEY: your_secret_key
    restart: unless-stopped

  frontend:
    image: lab-website-frontend:latest
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

---

# 生產環境優化

生產環境的進階優化策略。

## 🚀 效能優化

### 資料庫優化

```yaml
# 增強的 MySQL 配置
services:
  db:
    image: mysql:8.0
    command: >
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --innodb-buffer-pool-size=1G
      --innodb-log-file-size=256M
      --max-connections=500
      --query-cache-size=128M
      --query-cache-type=1
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
        reservations:
          memory: 1G
          cpus: '1.0'
```

### 前端優化

```bash
# 增強的 Nginx 配置
gzip on;
gzip_vary on;
gzip_min_length 10240;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/x-javascript
    application/xml+rss
    application/javascript
    application/json;

# 瀏覽器快取
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# 安全標頭
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
```

### 後端優化

```yaml
services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
    environment:
      WORKERS: 4
      THREADS: 2
      TIMEOUT: 30
```

## 🔒 安全強化

### 容器安全

```yaml
services:
  backend:
    read_only: true
    user: "1000:1000"
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
```

### 網路安全

```yaml
networks:
  frontend:
    driver: bridge
    internal: false
  backend:
    driver: bridge
    internal: true
  database:
    driver: bridge
    internal: true
```

---

# 多服務器和擴展

跨多服務器部署和擴展的策略。

## 🏗️ 負載平衡設定

### Nginx 負載平衡器

```nginx
upstream backend_servers {
    server backend1.example.com:8000;
    server backend2.example.com:8000;
    server backend3.example.com:8000;
}

upstream frontend_servers {
    server frontend1.example.com:3000;
    server frontend2.example.com:3000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://frontend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Swarm 部署

```yaml
version: '3.8'

services:
  frontend:
    image: lab-website-frontend:latest
    deploy:
      replicas: 3
      placement:
        constraints: [node.role == worker]
      restart_policy:
        condition: on-failure
    networks:
      - frontend

  backend:
    image: lab-website-backend:latest
    deploy:
      replicas: 5
      placement:
        constraints: [node.role == worker]
    networks:
      - frontend
      - backend

  db:
    image: mysql:8.0
    deploy:
      replicas: 1
      placement:
        constraints: [node.role == manager]
    networks:
      - backend
```

## 📊 監控和日誌

### Prometheus + Grafana 設定

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### 集中化日誌

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node

  logstash:
    image: docker.elastic.co/logstash/logstash:7.14.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    ports:
      - "5601:5601"
```

---

# 進階故障排除

複雜部署情境的進階故障排除技術。

## 🔍 容器除錯

### 深入容器檢查

```bash
# 檢查容器配置
docker inspect lab_web_backend | jq '.[0].Config'

# 檢查資源使用
docker stats --no-stream

# 查看容器進程
docker exec lab_web_backend ps aux

# 網路連接測試
docker exec lab_web_backend ping db
docker exec lab_web_backend curl -v http://db:3306
```

### 應用程式級除錯

```bash
# 後端除錯
docker exec -it lab_web_backend bash
python -c "from app import create_app; app = create_app(); print(app.config)"

# 資料庫除錯
docker exec -it lab_web_db mysql -u root -p
mysql> SHOW PROCESSLIST;
mysql> SHOW ENGINE INNODB STATUS\G
```

## 📊 效能分析

### 資料庫效能

```sql
-- 慢查詢分析
SELECT * FROM performance_schema.events_statements_summary_by_digest 
ORDER BY avg_timer_wait DESC LIMIT 10;

-- 連接分析
SELECT * FROM performance_schema.hosts;
```

### 應用程式效能

```bash
# 記憶體使用分析
docker exec lab_web_backend python -c "
import psutil
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'CPU: {psutil.cpu_percent()}%')
"

# 請求追蹤
docker logs lab_web_backend | grep -E "(POST|GET|PUT|DELETE)" | tail -50
```

## 🚨 恢復程序

### 資料庫恢復

```bash
# 時間點恢復
docker exec lab_web_db mysqldump --single-transaction \
  --routines --triggers --all-databases > full_backup.sql

# 二進制日誌恢復
docker exec lab_web_db mysqlbinlog /var/lib/mysql/binlog.000001 \
  --start-datetime="2023-12-01 10:00:00" \
  --stop-datetime="2023-12-01 11:00:00" > recovery.sql
```

### 應用程式恢復

```bash
# 回滾到先前版本
docker tag lab-website-backend:latest lab-website-backend:backup
docker pull lab-website-backend:previous
docker tag lab-website-backend:previous lab-website-backend:latest
docker-compose up -d backend

# 資料卷備份和恢復
docker run --rm -v lab_web_mysql_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/mysql_backup.tar.gz -C /data .
```

---

## 支援和延伸閱讀

進階部署的額外協助：

- **主要部署指南**: [DEPLOYMENT_zh-CN.md](./DEPLOYMENT_zh-CN.md)
- **專案文檔**: [../README_zh-CN.md](../README_zh-CN.md)
- **後端 API 參考**: [../backend/README.md](../backend/README.md)
- **前端配置**: [../frontend/README_zh-CN.md](../frontend/README_zh-CN.md)

---

*本進階部署指南與實驗室網站框架一起維護。如需最新更新，請查看專案倉庫。*