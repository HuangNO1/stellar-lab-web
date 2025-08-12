# Docker 快速參考

實驗室網站框架 Docker 命令和故障排除快速參考指南。

## 🚀 常用命令

### 使用部署腳本（推薦）

```bash
# 生產環境
./deploy.sh prod start -d          # 啟動所有服務
./deploy.sh prod stop              # 停止所有服務  
./deploy.sh prod restart           # 重啟所有服務
./deploy.sh prod logs -f           # 追蹤所有日誌
./deploy.sh prod status            # 顯示狀態
./deploy.sh prod health            # 健康檢查

# 開發環境
./deploy.sh dev start -d           # 啟動開發環境
./deploy.sh dev logs -f            # 追蹤開發日誌

# 資料庫
./deploy.sh prod db-init           # 初始化資料庫
./deploy.sh prod db-backup         # 備份資料庫
./deploy.sh prod shell --service=db  # MySQL shell
```

### 使用 Make（更簡單）

```bash
make deploy        # 完整部署
make start         # 啟動服務
make stop          # 停止服務
make logs          # 追蹤日誌
make status        # 顯示狀態
make dev          # 啟動開發環境
make db-init      # 初始化資料庫
make urls         # 顯示服務 URLs
```

## 📊 服務 URLs

| 服務 | URL | 用途 |
|---------|-----|---------|
| 前端 | http://localhost:3000 | 主要網站 |
| 後端 API | http://localhost:8000 | REST API |
| API 文檔 | http://localhost:8000/api/docs | Swagger 文檔 |
| phpMyAdmin | http://localhost:8081 | 資料庫管理 |

**預設登入**: admin / admin123

## 🔧 直接 Docker 命令

### 容器管理

```bash
# 列出運行中的容器
docker ps

# 列出所有容器
docker ps -a

# 檢視容器日誌
docker logs lab_web_frontend -f
docker logs lab_web_backend -f
docker logs lab_web_db -f

# 在容器中執行命令
docker exec -it lab_web_backend /bin/bash
docker exec -it lab_web_frontend /bin/sh
docker exec -it lab_web_db mysql -u root -plab_web_root_123 lab_web

# 重啟個別容器
docker restart lab_web_frontend
docker restart lab_web_backend
docker restart lab_web_db
```

### Docker Compose 命令

```bash
# 啟動服務
docker-compose up -d

# 啟動特定服務
docker-compose up -d frontend

# 停止服務
docker-compose down

# 檢視日誌
docker-compose logs -f
docker-compose logs -f backend

# 建構並啟動
docker-compose up --build -d

# 擴展服務
docker-compose up --scale frontend=2 -d
```

## 🛠️ 故障排除命令

### 健康檢查

```bash
# 檢查服務是否回應
curl http://localhost:3000/health    # 前端
curl http://localhost:8000/health    # 後端

# 檢查資料庫連接
docker exec lab_web_db mysqladmin ping -h localhost

# 檢查容器健康狀態
docker inspect lab_web_frontend --format='{{.State.Health.Status}}'
```

### 資源使用

```bash
# 容器資源使用
docker stats

# 磁碟使用
docker system df

# 資料卷使用
docker volume ls
docker volume inspect lab_web_mysql_data
```

### 清理

```bash
# 移除已停止的容器
docker container prune

# 移除未使用的映像
docker image prune

# 移除未使用的資料卷
docker volume prune

# 移除未使用的網路
docker network prune

# 完整清理（小心！）
docker system prune -a --volumes
```

## 📂 資料卷管理

### 資料卷位置

```bash
# 列出資料卷
docker volume ls | grep lab_web

# 檢查資料卷位置
docker volume inspect lab_web_mysql_data
docker volume inspect lab_web_media_data

# 備份資料卷
docker run --rm -v lab_web_mysql_data:/data -v $(pwd):/backup alpine tar czf /backup/mysql_backup.tar.gz -C /data .
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar czf /backup/media_backup.tar.gz -C /data .

# 恢復資料卷
docker run --rm -v lab_web_mysql_data:/data -v $(pwd):/backup alpine tar xzf /backup/mysql_backup.tar.gz -C /data
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar xzf /backup/media_backup.tar.gz -C /data
```

## 🔍 除錯

### 容器問題

```bash
# 檢查容器啟動失敗的原因
docker logs lab_web_backend

# 檢查容器配置
docker inspect lab_web_backend

# 檢查網路連接
docker network ls
docker network inspect lab_web_default

# 測試容器間連接
docker exec lab_web_backend ping db
docker exec lab_web_frontend ping backend
```

### 資料庫問題

```bash
# 檢查 MySQL 日誌
docker logs lab_web_db

# 連接到 MySQL
docker exec -it lab_web_db mysql -u root -plab_web_root_123

# 檢查資料庫狀態
docker exec lab_web_db mysqladmin status -u root -plab_web_root_123

# 檢查資料庫大小
docker exec lab_web_db mysql -u root -plab_web_root_123 -e "SELECT table_schema 'Database', SUM(data_length + index_length) / 1024 / 1024 'Size (MB)' FROM information_schema.tables WHERE table_schema='lab_web' GROUP BY table_schema;"
```

### 效能問題

```bash
# 監控資源使用
docker stats --no-stream

# 檢查容器程序
docker exec lab_web_backend ps aux
docker exec lab_web_frontend ps aux

# 檢查容器內磁碟空間
docker exec lab_web_backend df -h
docker exec lab_web_db df -h
```

## 🚨 緊急程序

### 完全重設

```bash
# 停止所有服務
./deploy.sh prod stop

# 移除所有容器和資料卷（破壞性！）
./deploy.sh prod clean

# 重新開始
./deploy.sh prod start -d
./deploy.sh prod db-init
```

### 資料庫緊急重設

```bash
# 停止後端以防止連接
./deploy.sh prod stop --service=backend

# 重設資料庫資料卷
docker volume rm lab_web_mysql_data

# 啟動資料庫並重新初始化
./deploy.sh prod start --service=db -d
./deploy.sh prod db-init

# 啟動後端
./deploy.sh prod start --service=backend -d
```

### 緊急操作前的備份

```bash
# 在破壞性操作前總是備份
./deploy.sh prod db-backup

# 備份媒體檔案
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar czf /backup/media_emergency_backup.tar.gz -C /data .
```

## 📋 維護腳本

### 更新所有內容

```bash
#!/bin/bash
# update-lab-website.sh

echo "停止服務..."
./deploy.sh prod stop

echo "備份資料庫..."
./deploy.sh prod db-backup

echo "拉取最新程式碼..."
git pull origin main

echo "重新建構服務..."
./deploy.sh prod build --no-cache --rebuild

echo "啟動服務..."
./deploy.sh prod start -d

echo "檢查健康狀態..."
sleep 30
./deploy.sh prod health

echo "更新完成！"
```

### 每日健康檢查

```bash
#!/bin/bash
# health-check.sh

DATE=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/var/log/lab-website-health.log"

echo "[$DATE] 開始健康檢查..." >> "$LOG_FILE"

# 檢查服務
if curl -sf http://localhost:3000/health > /dev/null; then
    echo "[$DATE] 前端: 正常" >> "$LOG_FILE"
else
    echo "[$DATE] 前端: 失敗" >> "$LOG_FILE"
fi

if curl -sf http://localhost:8000/health > /dev/null; then
    echo "[$DATE] 後端: 正常" >> "$LOG_FILE"
else
    echo "[$DATE] 後端: 失敗" >> "$LOG_FILE"
fi

# 檢查磁碟空間
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "[$DATE] 磁碟使用: 警告 - ${DISK_USAGE}%" >> "$LOG_FILE"
else
    echo "[$DATE] 磁碟使用: 正常 - ${DISK_USAGE}%" >> "$LOG_FILE"
fi

echo "[$DATE] 健康檢查完成" >> "$LOG_FILE"
```

## 🔗 實用 Docker 命令

### 映像管理

```bash
# 列出映像
docker images

# 移除未使用的映像
docker image prune

# 不使用快取建構
docker build --no-cache -t lab-website-frontend ./frontend

# 標記映像
docker tag lab-website-frontend:latest lab-website-frontend:v1.0.0
```

### 網路除錯

```bash
# 列出網路
docker network ls

# 檢查網路
docker network inspect lab_web_default

# 測試 DNS 解析
docker exec lab_web_backend nslookup db
docker exec lab_web_frontend nslookup backend
```

### 環境變數

```bash
# 顯示容器環境
docker exec lab_web_backend env
docker exec lab_web_frontend env

# 檢查特定變數
docker exec lab_web_backend printenv DATABASE_URL
```

---

💡 **專業提示:**
- 在進行變更前總是備份
- 使用 `./deploy.sh prod health` 檢查所有服務
- 使用 `./deploy.sh prod logs -f` 監控日誌
- 使用 `make` 命令進行常見操作
- 保持 `.env` 檔案的安全和備份