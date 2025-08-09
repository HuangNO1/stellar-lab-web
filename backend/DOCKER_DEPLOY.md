# 🐳 Docker 部署指南

本指南将帮助您在本地 Docker 容器中部署實驗室網頁框架後端服務。

## 🚀 快速開始

### 前置要求
- Docker Desktop 或 Docker Engine (20.10+)
- Docker Compose (2.0+)
- 至少 2GB 可用磁盘空間

### 一鍵部署
```bash
# 1. 克隆項目到本地
cd /home/rem/Documents/Study/Code/lab_web/backend

# 2. 構建並啟動所有服務（包含 phpMyAdmin）
docker-compose up --build -d

# 或者啟動最小配置（僅後端+數據庫，不包含 phpMyAdmin）
docker-compose -f docker-compose-minimal.yml up --build -d

# 3. 查看服務狀態
docker-compose ps
```

## 📋 服務說明

### 服務端口映射
- **Flask 後端**: [http://localhost:8000](http://localhost:8000)
- **MySQL 數據庫**: `localhost:3307` (避免與本地 MySQL 衝突)
- **phpMyAdmin** (可選): [http://localhost:8081](http://localhost:8081)

### 默認賬戶信息
- **管理員賬戶**: `admin` / `admin123`
- **MySQL Root**: `root` / `lab_web_root_123`
- **MySQL 用戶**: `lab_web_user` / `lab_web_pass_123`

## 🛠️ 詳細部署步驟

### 第一步：準備文件
確保以下文件存在於項目根目錄：
```
backend/
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── .env.docker
└── .dockerignore
```

### 第二步：構建鏡像
```bash
# 僅構建後端應用鏡像
docker-compose build app

# 或者構建所有服務
docker-compose build
```

### 第三步：啟動服務
```bash
# 前台啟動（查看實時日誌）
docker-compose up

# 後台啟動
docker-compose up -d

# 指定服務啟動順序
docker-compose up -d db    # 先啟動數據庫
docker-compose up -d app   # 再啟動應用
```

### 第四步：驗證部署
```bash
# 查看服務狀態
docker-compose ps

# 查看應用日誌
docker-compose logs app

# 查看數據庫日誌
docker-compose logs db

# 測試API健康狀態
curl http://localhost:8000/health
```

## 🔧 常用操作命令

### 服務管理
```bash
# 停止所有服務
docker-compose down

# 停止並刪除數據卷
docker-compose down -v

# 重啟特定服務
docker-compose restart app

# 查看實時日誌
docker-compose logs -f app
```

### 數據管理
```bash
# 進入數據庫容器
docker-compose exec db mysql -u root -p

# 從外部連接數據庫（如需要）
mysql -h localhost -P 3307 -u root -p

# 備份數據庫
docker-compose exec db mysqldump -u root -plab_web_root_123 lab_web > backup.sql

# 還原數據庫
docker-compose exec -T db mysql -u root -plab_web_root_123 lab_web < backup.sql
```

### 應用容器操作
```bash
# 進入應用容器
docker-compose exec app bash

# 手動初始化數據庫
docker-compose exec app python scripts/init_db.py

# 查看媒體文件
docker-compose exec app ls -la /app/media/
```

## 📊 API 測試

### 基礎測試
```bash
# 健康檢查
curl http://localhost:8000/health

# API信息
curl http://localhost:8000/api-info

# 獲取實驗室信息
curl http://localhost:8000/api/lab
```

### 管理員登錄測試
```bash
# 登錄獲取Token
curl -X POST http://localhost:8000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"admin_name":"admin","admin_pass":"admin123"}'

# 使用Token訪問管理接口（需要替換實際token）
curl -X GET http://localhost:8000/api/admin/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🗄️ 數據初始化

### 自動初始化流程
系統使用項目原有的 `scripts/init_db.py` 腳本進行數據庫初始化：

**啟動順序**:
```
MySQL 容器啟動 → 等待數據庫服務就緒 → 運行 init_db.py → 啟動 Flask 應用
```

**自動創建的示例數據**:
- ✅ **管理員賬戶**: `admin/admin123`
- ✅ **實驗室信息**: 智能計算實驗室
- ✅ **課題組**: 計算機視覺、自然語言處理
- ✅ **成員**: 張教授、李副教授、王博士
- ✅ **論文**: 2篇（CVPR 2024、AAAI 2024）
- ✅ **新聞**: 3條（論文錄用、獲獎、學術報告）
- ✅ **項目**: 2個（監控系統、對話機器人）

## 📁 數據持久化

### 數據卷說明
- `mysql_data`: MySQL 數據持久化
- `media_data`: 上傳文件持久化
- `./logs`: 應用日誌文件

### 數據目錄結構
```
media_data/
├── lab_logo/          # 實驗室Logo
├── member_avatar/     # 成員頭像
├── paper/            # 論文文件
└── other/            # 其他文件
```

## 🔒 安全配置

### 生產環境配置
在生產環境中，請修改以下敏感信息：
1. 編輯 `.env.docker` 文件：
```bash
# 修改密鑰
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret

# 修改數據庫密碼
MYSQL_PASSWORD=your-secure-password
```

2. 更新 `docker-compose.yml` 中的數據庫密碼

### 網絡安全
- 移除不必要的端口映射
- 使用自定義網絡
- 配置防火牆規則

## 🐛 故障排除

### 常見問題

**1. 數據庫連接失敗**
```bash
# 檢查數據庫服務狀態
docker-compose ps db
docker-compose logs db

# 重啟數據庫服務
docker-compose restart db
```

**2. 應用啟動失敗**
```bash
# 查看應用啟動日誌
docker-compose logs app

# 檢查依賴服務
docker-compose ps
```

**3. 文件上傳失敗**
```bash
# 檢查媒體目錄權限
docker-compose exec app ls -la /app/media/

# 重新設置權限
docker-compose exec app chmod -R 755 /app/media/
```

**4. 端口衝突**
```bash
# 如果 3307 端口也被佔用，可以修改為其他端口
# 編輯 docker-compose.yml
ports:
  - "3308:3306"  # 改為其他可用端口

# 檢查端口使用情況
netstat -tlnp | grep :3306
lsof -i :3306
```

**5. 本地 MySQL 服務衝突**
```bash
# 停止本地 MySQL 服務（如果不需要）
sudo systemctl stop mysql        # Linux
brew services stop mysql         # macOS
net stop mysql                  # Windows

# 或者使用不同端口（已在配置中修改為 3307）
```

### 清理環境
```bash
# 停止並刪除所有容器
docker-compose down

# 刪除所有相關鏡像
docker rmi $(docker images "*lab_web*" -q)

# 清理未使用的數據卷
docker volume prune

# 完全重置（謹慎使用）
docker-compose down -v --rmi all
```

## 🔧 開發模式

如需開發模式部署：
```bash
# 修改 docker-compose.yml
environment:
  FLASK_ENV: development

# 添加代碼卷掛載
volumes:
  - .:/app
  - media_data:/app/media
```

## 📝 日誌管理

```bash
# 查看所有服務日誌
docker-compose logs

# 實時跟踪應用日誌
docker-compose logs -f app

# 導出日誌到文件
docker-compose logs app > app.log
```

---

## 🎉 部署完成

部署成功後，您可以：
- 訪問 [http://localhost:8000](http://localhost:8000) 查看 API 文檔
- 使用 [http://localhost:8080](http://localhost:8080) 管理數據庫
- 通過 API 接口管理實驗室數據

如有問題，請參考故障排除部分或查看容器日誌進行診斷。