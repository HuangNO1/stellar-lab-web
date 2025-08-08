# 實驗室通用網頁框架 - 後端

這是一個專為實驗室設計的通用網頁框架後端，採用Flask + SQLAlchemy + JWT架構，支持自定義學校、實驗室logo等資訊。

## 🚀 快速開始

### 1. 環境要求

- Python 3.8+
- MySQL 5.7+ (可選，默認使用SQLite)

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
# SQLite (默認)
SQLALCHEMY_DATABASE_URI = 'sqlite:///lab_web.db'

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/lab_web?charset=utf8mb4'
```

### 4. 初始化數據庫

```bash
python scripts/init_db.py
```

### 5. 啟動應用

```bash
# 開發模式
python run.py

# 或使用啟動腳本
./start.sh
```

應用將在 `http://localhost:8000` 啟動

## 📖 API 文檔

### 🔗 在線文檔

啟動應用後，訪問以下地址查看API文檔：

- **主頁**: [http://localhost:8000](http://localhost:8000)
- **API概覽**: [http://localhost:8000/api-info](http://localhost:8000/api-info)  
- **Swagger文檔**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- **健康檢查**: [http://localhost:8000/health](http://localhost:8000/health)

### 認證相關

- `POST /api/admin/login` - 管理員登錄
- `POST /api/admin/change-password` - 修改密碼

### 實驗室資訊

- `GET /api/lab` - 獲取實驗室資訊
- `PUT /api/lab` - 更新實驗室資訊 (需要管理員權限)

### 課題組管理

- `GET /api/research-groups` - 獲取課題組列表
- `POST /api/research-groups` - 創建課題組 (需要管理員權限)
- `PUT /api/research-groups/{id}` - 更新課題組 (需要管理員權限)
- `DELETE /api/research-groups/{id}` - 刪除課題組 (需要管理員權限)

### 成員管理

- `GET /api/members` - 獲取成員列表
- `GET /api/members/{id}` - 獲取成員詳情
- `POST /api/members` - 創建成員 (需要管理員權限)
- `PUT /api/members/{id}` - 更新成員 (需要管理員權限)  
- `DELETE /api/members/{id}` - 刪除成員 (需要管理員權限)

### 論文管理

- `GET /api/papers` - 獲取論文列表
- `GET /api/papers/{id}` - 獲取論文詳情
- `POST /api/papers` - 創建論文 (需要管理員權限)
- `DELETE /api/papers/{id}` - 刪除論文 (需要管理員權限)

### 新聞管理

- `GET /api/news` - 獲取新聞列表
- `GET /api/news/{id}` - 獲取新聞詳情
- `POST /api/news` - 創建新聞 (需要管理員權限)
- `PUT /api/news/{id}` - 更新新聞 (需要管理員權限)
- `DELETE /api/news/{id}` - 刪除新聞 (需要管理員權限)

### 項目管理

- `GET /api/projects` - 獲取項目列表
- `GET /api/projects/{id}` - 獲取項目詳情
- `POST /api/projects` - 創建項目 (需要管理員權限)
- `PUT /api/projects/{id}` - 更新項目 (需要管理員權限)
- `DELETE /api/projects/{id}` - 刪除項目 (需要管理員權限)

### 文件管理

- `POST /api/media/upload` - 上傳文件 (需要管理員權限)
- `GET /api/media/serve/{path}` - 獲取文件
- `GET /api/media/health` - 媒體服務健康檢查

### 管理員管理

- `GET /api/admins` - 獲取管理員列表 (需要超級管理員權限)
- `POST /api/admins` - 創建管理員 (需要超級管理員權限)
- `PUT /api/admins/{id}` - 更新管理員 (需要超級管理員權限)
- `DELETE /api/admins/{id}` - 刪除管理員 (需要超級管理員權限)

### 編輯記錄

- `GET /api/edit-records` - 獲取編輯記錄 (需要管理員權限)
- `GET /api/edit-records/{id}` - 獲取編輯記錄詳情 (需要管理員權限)

## 🔐 默認賬戶

系統初始化後會自動創建超級管理員賬戶：

- 用戶名：`admin`
- 密碼：`admin123`

**⚠️ 請在生產環境中立即修改默認密碼！**

## 🔑 認證方式

1. 使用 `POST /api/admin/login` 獲取JWT Token
2. 在請求頭中添加：`Authorization: Bearer <token>`
3. Token有效期為24小時

## 📊 響應格式

### 成功響應

```json
{
  "code": 0,
  "message": "OK", 
  "data": { ... }
}
```

### 錯誤響應

```json
{
  "code": 2000,
  "message": "參數錯誤",
  "data": null
}
```

### 錯誤碼說明

- `0` - 成功
- `1000` - 未認證或token無效
- `1001` - 權限不足
- `2000` - 參數校驗錯誤
- `3000` - 資源未找到
- `4000` - 操作衝突
- `5000` - 服務器內部錯誤

## 📁 分頁參數

所有列表API支持以下分頁參數：

- `page` - 頁碼 (從1開始)
- `per_page` - 每頁數量 (默認10，最大100)
- `q` - 搜索關鍵字
- `sort_by` - 排序字段
- `order` - 排序方向 (asc/desc)

## 📎 文件上傳

### 支持的文件類型

- **圖片**: jpg, jpeg, png, gif (最大5MB)
- **文檔**: pdf (最大50MB)

### 文件存儲

文件存儲路徑：`/media/{type}/{YYYYMM}/{uuid}.{ext}`

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
│   │   └── ...
│   ├── routes/              # API路由
│   │   ├── auth.py          # 認證路由
│   │   ├── lab.py           # 實驗室路由
│   │   ├── member.py        # 成員路由
│   │   ├── swagger_docs.py  # API文檔
│   │   └── ...
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
└── test_api.py           # API測試
```

## 🧪 測試

運行測試腳本檢查API是否正常：

```bash
python test_api.py
```

## 📝 開發說明

### 數據庫遷移

如果修改了數據模型，需要創建遷移：

```bash
flask db init      # 第一次使用
flask db migrate   # 生成遷移文件
flask db upgrade   # 應用遷移
```

### 添加新的API端點

1. 在 `app/models/` 中定義數據模型
2. 在 `app/routes/` 中創建API路由
3. 在 `app/__init__.py` 中註冊藍圖
4. 更新API文檔

## ⚡ 性能優化

- 使用數據庫索引優化查詢
- 實現分頁避免大量數據傳輸
- 圖片自動壓縮和調整尺寸
- 軟刪除保持數據完整性

## 🛡️ 安全特性

- JWT Token認證
- bcrypt密碼加密
- CORS跨域保護
- 文件類型校驗
- 輸入數據驗證
- SQL注入防護

## 📄 許可證

MIT License - 詳見LICENSE文件