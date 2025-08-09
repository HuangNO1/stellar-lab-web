# 實驗室通用網頁框架 - 後端

這是一個專為實驗室設計的通用網頁框架後端，採用Flask + SQLAlchemy + JWT架構，支持自定義學校、實驗室logo等資訊。

## 🚀 快速開始

### 1. 環境要求

- Python 3.8+
- MySQL/MariaDB 5.7+ (推薦) 或 SQLite

### 2. 安裝依賴

```bash
# 創建虛擬環境
python -m venv venv

# 激活虛擬環境
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安裝依賴
pip install -r requirements.txt
```

### 3. 配置數據庫

編輯 `config/config.py` 文件，配置數據庫連接：

```python
# MariaDB/MySQL (推薦)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/lab_web?charset=utf8mb4'

# SQLite (開發環境)
SQLALCHEMY_DATABASE_URI = 'sqlite:///lab_web.db'
```

### 4. 初始化數據庫

**自動創建數據庫和表**（推薦）：
```bash
python scripts/init_db.py
```

**手動創建數據庫**：
```sql
-- 如使用 MariaDB/MySQL，先創建數據庫
CREATE DATABASE lab_web CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 啟動應用

```bash
# 開發模式
python run.py

# 或使用啟動腳本
./start.sh

# 生產模式
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

應用將在 `http://localhost:8000` 啟動

## 📖 完整 API 文檔

### 🔗 在線文檔

啟動應用後，訪問以下地址查看API文檔：

- **主頁**: [http://localhost:8000](http://localhost:8000)
- **API概覽**: [http://localhost:8000/api-info](http://localhost:8000/api-info)  
- **Swagger文檔**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- **健康檢查**: [http://localhost:8000/health](http://localhost:8000/health)

### 📚 離線文檔

詳細的API文檔請參考：**[api.md](./api.md)**

該文檔包含：
- 完整的接口列表和參數說明
- 請求/響應示例
- 錯誤碼說明
- 數據類型定義
- 軟刪除約束說明
- 文件上傳規範

## 🎯 核心功能

### ✨ 功能模塊

| 模塊 | 功能 | CRUD | 搜索 | 批量操作 |
|------|------|------|------|----------|
| 🏢 實驗室管理 | 實驗室基本信息、Logo、輪播圖片 | ✅ | - | - |
| 👥 課題組管理 | 課題組信息、組長關聯 | ✅ | ✅ | - |
| 👨‍💼 成員管理 | 教師、學生信息、頭像 | ✅ | ✅ | ✅ |
| 📄 論文管理 | 論文信息、作者關聯、文件 | ✅ | ✅ | - |
| 📰 新聞管理 | 新聞發布、分類 | ✅ | ✅ | - |
| 🚀 項目管理 | 項目信息、狀態管理 | ✅ | ✅ | - |
| 📁 媒體管理 | 文件上傳、存儲、服務 | ✅ | - | - |
| 🔐 管理員管理 | 權限管理、操作記錄 | ✅ | ✅ | - |
| 📊 操作審計 | 所有操作的詳細記錄 | ✅ | ✅ | - |

### 🔐 權限控制

- **遊客**: 查看公開信息（實驗室、成員、論文、新聞、項目）
- **普通管理員**: 內容管理、文件上傳
- **超級管理員**: 完整權限，包括管理員管理

### 🛡️ 數據安全

- **軟刪除機制**: 所有刪除操作均為軟刪除，保證數據可恢復
- **關聯性約束**: 確保數據完整性
  - 實驗室 → 課題組 → 成員 → 論文
  - 刪除上級前必須處理下級關聯
- **操作審計**: 記錄所有 CRUD 操作和管理員活動

### 📈 性能優化

- **數據庫索引**: 針對搜索和排序字段建立索引
- **分頁查詢**: 所有列表接口支持分頁
- **模糊搜索**: 支持中英文關鍵字搜索
- **文件優化**: 自動文件類型檢測和大小限制

## 🔑 認證方式

1. 使用 `POST /api/admin/login` 獲取JWT Token
2. 在請求頭中添加：`Authorization: Bearer <token>`
3. Token有效期為24小時

### 🔐 默認賬戶

系統初始化後會自動創建超級管理員賬戶：

- **用戶名**：`admin`
- **密碼**：`admin123`

**⚠️ 請在生產環境中立即修改默認密碼！**

## 📊 API 接口概覽

### 認證管理
- `POST /api/admin/login` - 管理員登錄
- `POST /api/admin/logout` - 管理員登出
- `POST /api/admin/change-password` - 修改密碼
- `GET /api/admin/profile` - 獲取個人信息
- `PUT /api/admin/profile` - 更新個人信息

### 實驗室管理
- `GET /api/lab` - 獲取實驗室信息（含輪播圖片）
- `PUT /api/lab` - 更新實驗室信息（支持Logo及輪播圖片上傳）
- `DELETE /api/lab` - 刪除實驗室

### 課題組管理
- `GET /api/research-groups` - 獲取課題組列表
- `GET /api/research-groups/{id}` - 獲取課題組詳情
- `POST /api/research-groups` - 創建課題組
- `PUT /api/research-groups/{id}` - 更新課題組
- `DELETE /api/research-groups/{id}` - 刪除課題組

### 成員管理
- `GET /api/members` - 獲取成員列表
- `GET /api/members/{id}` - 獲取成員詳情
- `POST /api/members` - 創建成員（支持頭像上傳）
- `PUT /api/members/{id}` - 更新成員
- `DELETE /api/members/{id}` - 刪除成員
- `DELETE /api/members/batch` - 批量刪除成員
- `PUT /api/members/batch` - 批量更新成員

### 論文管理
- `GET /api/papers` - 獲取論文列表
- `GET /api/papers/{id}` - 獲取論文詳情
- `POST /api/papers` - 創建論文（支持文件上傳、作者關聯）
- `PUT /api/papers/{id}` - 更新論文
- `DELETE /api/papers/{id}` - 刪除論文

### 新聞管理
- `GET /api/news` - 獲取新聞列表
- `GET /api/news/{id}` - 獲取新聞詳情
- `POST /api/news` - 創建新聞
- `PUT /api/news/{id}` - 更新新聞
- `DELETE /api/news/{id}` - 刪除新聞

### 項目管理
- `GET /api/projects` - 獲取項目列表
- `GET /api/projects/{id}` - 獲取項目詳情
- `POST /api/projects` - 創建項目
- `PUT /api/projects/{id}` - 更新項目
- `DELETE /api/projects/{id}` - 刪除項目

### 媒體文件管理
- `POST /api/media/upload` - 上傳文件
- `GET /api/media/serve/{path}` - 獲取文件
- `GET /api/media/info/{path}` - 獲取文件信息
- `GET /api/media/health` - 媒體服務健康檢查

### 管理員管理
- `GET /api/admins` - 獲取管理員列表
- `POST /api/admins` - 創建管理員
- `PUT /api/admins/{id}` - 更新管理員
- `DELETE /api/admins/{id}` - 刪除管理員

### 操作審計
- `GET /api/edit-records` - 獲取編輯記錄
- `GET /api/edit-records/{id}` - 獲取編輯記錄詳情

### 系統接口
- `GET /api/health` - 健康檢查
- `GET /api/docs` - Swagger文檔
- `GET /api/swagger.json` - API規範

## 📊 響應格式

### 成功響應

```json
{
  "code": 0,
  "message": "OK", 
  "data": { ... }
}
```

### 分頁響應

```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [ ... ],
    "total": 100,
    "page": 1,
    "per_page": 10,
    "pages": 10,
    "has_prev": false,
    "has_next": true
  }
}
```

### 錯誤響應

```json
{
  "code": 錯誤碼,
  "message": "錯誤描述",
  "data": null
}
```

### 錯誤碼說明

| 錯誤碼 | 說明 | HTTP狀態碼 |
|-------|------|-----------|
| 0 | 成功 | 200 |
| 1000 | 認證錯誤（用戶名密碼錯誤） | 401 |
| 1001 | 權限不足 | 403 |
| 2000 | 參數校驗錯誤 | 400 |
| 3000 | 資源不存在 | 404 |
| 4000 | 操作衝突 | 409 |
| 5000 | 服務器內部錯誤 | 500 |

## 📎 文件上傳

### 支持的文件類型

- **圖片**: jpg, jpeg, png, gif (最大5MB)
- **文檔**: pdf (最大50MB，論文文件)

### 文件存儲結構

```
media/
├── lab_logo/          # 實驗室Logo及輪播圖片
├── member_avatar/     # 成員頭像
├── paper/            # 論文文件
└── other/            # 其他文件
```

## 🗂️ 項目結構

```
backend/
├── app/
│   ├── __init__.py          # 應用工廠
│   ├── auth/                # 認證模組
│   │   └── decorators.py    # JWT裝飾器
│   ├── models/              # 數據模型
│   │   ├── admin.py         # 管理員模型
│   │   ├── lab.py           # 實驗室模型
│   │   ├── member.py        # 成員模型
│   │   ├── paper.py         # 論文模型
│   │   ├── project.py       # 項目模型
│   │   ├── news.py          # 新聞模型
│   │   ├── research_group.py # 課題組模型
│   │   └── edit_record.py   # 編輯記錄模型
│   ├── routes/              # API路由
│   │   ├── auth.py          # 認證路由
│   │   ├── admin.py         # 管理員路由
│   │   ├── lab.py           # 實驗室路由
│   │   ├── member.py        # 成員路由
│   │   ├── paper.py         # 論文路由
│   │   ├── news.py          # 新聞路由
│   │   ├── project.py       # 項目路由
│   │   ├── research_group.py # 課題組路由
│   │   ├── media.py         # 媒體文件路由
│   │   ├── edit_record.py   # 編輯記錄路由
│   │   ├── root.py          # 根路由
│   │   └── swagger_docs.py  # Swagger文檔
│   └── utils/               # 工具函數
│       ├── file_handler.py  # 文件處理
│       ├── helpers.py       # 輔助函數
│       └── validators.py    # 數據校驗
├── config/
│   └── config.py           # 配置文件
├── scripts/
│   └── init_db.py          # 數據庫初始化
├── requirements.txt        # Python依賴
├── run.py                 # 應用入口
├── start.sh               # 啟動腳本
├── test_api.py           # API測試
├── api.md                # 完整API文檔
└── README.md             # 項目說明
```

## 🧪 測試

運行測試腳本檢查API是否正常：

```bash
python test_api.py
```

## 🐳 Docker 部署

### 快速部署

使用提供的部署腳本快速部署完整的實驗室網頁框架：

```bash
# 賦予執行權限
chmod +x deploy.sh

# 啟動所有服務
./deploy.sh start

# 查看服務狀態
./deploy.sh status

# 查看服務日誌
./deploy.sh logs

# 重啟服務
./deploy.sh restart

# 停止服務
./deploy.sh stop
```

### 重新部署最新版本

當你對後端代碼進行了修改（如新增功能、修復bug等），需要重新部署到Docker容器：

#### 方法1: 使用部署腳本（推薦）

```bash
# 停止現有服務
./deploy.sh stop

# 重新構建並啟動（會自動構建最新代碼）
./deploy.sh restart
```

#### 方法2: 使用Docker Compose命令

```bash
# 停止並移除現有容器
docker-compose --project-name lab_web down

# 重新構建鏡像並啟動
docker-compose --project-name lab_web up --build -d

# 查看服務狀態
docker-compose --project-name lab_web ps
```

#### 方法3: 強制重新構建

如果遇到緩存問題，可以強制重新構建：

```bash
# 停止服務並移除容器
docker-compose --project-name lab_web down

# 移除舊鏡像
docker rmi lab_web_app 2>/dev/null || true

# 清理構建緩存
docker builder prune -f

# 重新構建並啟動
docker-compose --project-name lab_web up --build -d
```

### 重要提醒

1. **數據持久化**: 數據庫和媒體文件使用Docker volumes存儲，重新部署不會丟失數據
2. **數據庫遷移**: 新版本如果包含數據庫schema變更，會在容器啟動時自動執行遷移
3. **環境變量**: 確保`.env.docker`文件包含所有必要配置

### 服務地址

部署成功後，服務將在以下地址可用：

- **後端API**: http://localhost:8000
- **API文檔**: http://localhost:8000/api/docs
- **數據庫管理**: http://localhost:8081

### Docker 環境要求

- Docker 20.0+
- Docker Compose 1.28+
- 至少2GB可用內存
- 至少5GB可用磁盤空間

### 故障排除

如果部署遇到問題：

```bash
# 查看詳細日誌
./deploy.sh logs

# 檢查服務狀態
docker-compose --project-name lab_web ps

# 檢查容器資源使用
docker stats

# 進入容器調試
docker exec -it lab_web_app bash
```

## 🚦 部署指南

### 開發環境
```bash
python run.py
```

### 生產環境

1. **使用 Gunicorn**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

2. **使用 Docker**:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

3. **配置反向代理** (Nginx):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /media {
        proxy_pass http://localhost:8000;
    }
}
```

## 📝 開發指南

### 數據庫遷移

如果修改了數據模型：

```bash
flask db init      # 第一次使用
flask db migrate   # 生成遷移文件
flask db upgrade   # 應用遷移
```

### 添加新的API模塊

1. **創建數據模型** (`app/models/new_module.py`)
2. **創建API路由** (`app/routes/new_module.py`)
3. **在應用工廠中註冊藍圖** (`app/__init__.py`)
4. **更新Swagger文檔** (`app/routes/swagger_docs.py`)
5. **更新API文檔** (`api.md`)

### 代碼規範

- 使用軟刪除（`enable` 字段）而非硬刪除
- 所有操作記錄到 `EditRecord` 表
- 使用 `@admin_required` 裝飾器保護管理接口
- 實現完整的輸入驗證和錯誤處理
- 遵循 RESTful API 設計原則

## ⚡ 性能優化

- ✅ 數據庫索引優化查詢性能
- ✅ 分頁機制避免大量數據傳輸
- ✅ 文件類型和大小限制
- ✅ JWT Token 認證減少數據庫查詢
- ✅ 軟刪除保持數據完整性
- ✅ CORS 配置支持跨域請求

## 🛡️ 安全特性

- ✅ **JWT Token認證**: 無狀態身份驗證
- ✅ **bcrypt密碼加密**: 安全的密碼存儲
- ✅ **CORS跨域保護**: 配置允許的來源
- ✅ **文件類型校驗**: 防止惡意文件上傳
- ✅ **輸入數據驗證**: 防止注入攻擊
- ✅ **SQL注入防護**: 使用 ORM 查詢
- ✅ **軟刪除機制**: 數據可恢復性
- ✅ **操作審計日誌**: 完整的操作記錄

## 🤝 貢獻指南

1. Fork 本項目
2. 創建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 許可證

MIT License - 詳見 [LICENSE](LICENSE) 文件

---

## 💡 常見問題

### Q: 如何重置管理員密碼？
A: 運行數據庫初始化腳本會重置為默認密碼，或直接在數據庫中更新 `admins` 表。

### Q: 支援哪些數據庫？
A: 支持 MySQL/MariaDB（推薦）和 SQLite。生產環境建議使用 MySQL。

### Q: 如何備份數據？
A: 由於使用軟刪除，可以定期備份整個數據庫。所有數據都保留在表中。

### Q: API 支持版本控制嗎？
A: 當前版本為 v1，所有接口統一使用 `/api` 前綴。

### Q: 如何重新部署Docker容器？
A: 使用 `./deploy.sh restart` 重新部署，或使用 `docker-compose --project-name lab_web up --build -d` 強制重新構建。

### Q: 如何自定義文件存儲路徑？
A: 修改 `config/config.py` 中的 `UPLOAD_FOLDER` 配置。