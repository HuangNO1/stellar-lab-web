# 實驗室通用網頁框架

## 項目簡介

這是一個專為實驗室設計的通用網頁框架，可以自定義學校、實驗室 logo 等資訊，便於不同實驗室使用。系統采用前後端分離架構，具有良好的可擴展性和維護性。

## 技術棧

### 前端
- Vue 3 + TypeScript
- Naive UI 組件庫
- Vue Router 4
- Pinia 狀態管理
- Vite 構建工具

### 後端
- Python + Flask
- SQLAlchemy ORM
- JWT 認證
- MySQL 數據庫
- bcrypt 密碼加密

## 主要功能

### 用戶端功能
- **首頁展示**：實驗室介紹、課題組展示、最新新聞
- **論文管理**：論文列表、搜索、分頁展示
- **成員展示**：按類型（教師、學生、校友）分類展示
- **新聞資訊**：新聞列表展示和搜索
- **項目展示**：項目列表和搜索功能
- **多語言支持**：中英文切換
- **主題切換**：明暗主題切換

### 管理端功能
- **管理員系統**：超級管理員可管理普通管理員
- **實驗室管理**：logo、基本信息設置
- **課題組管理**：課題組信息的增刪改查
- **成員管理**：成員信息的完整管理
- **論文管理**：論文信息和文件上傳管理
- **新聞管理**：新聞內容的發布和管理
- **項目管理**：項目信息的管理
- **編輯記錄**：操作審計和日誌記錄

## 項目結構

```
lab_web/
├── frontend/          # Vue 3 前端應用
│   ├── src/
│   │   ├── components/    # 可複用組件
│   │   ├── views/        # 頁面組件
│   │   ├── router/       # 路由配置
│   │   ├── store/        # 狀態管理
│   │   ├── utils/        # 工具函數
│   │   ├── types/        # TypeScript 類型定義
│   │   └── assets/       # 靜態資源
│   └── public/           # 公共資源
├── backend/           # Flask 後端應用
│   ├── app/
│   │   ├── models/       # 數據模型
│   │   ├── routes/       # API 路由
│   │   └── utils/        # 工具函數
│   ├── config/           # 配置文件
│   ├── migrations/       # 數據庫遷移
│   └── tests/           # 測試文件
└── docs/             # 項目文檔
```

## 快速開始

### 前端設置

```bash
cd frontend
npm install
npm run dev
```

### 後端設置

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 數據庫設置

1. 創建 MySQL 數據庫
2. 配置數據庫連接
3. 運行數據庫初始化腳本
4. 創建超級管理員賬戶

## 數據庫設計

項目包含以下主要數據表：

- `admins` - 管理員表
- `lab` - 實驗室信息表  
- `research_groups` - 課題組表
- `members` - 成員表
- `papers` - 論文表
- `paper_authors` - 論文作者關聯表
- `projects` - 項目表
- `news` - 新聞表
- `edit_records` - 編輯記錄表

詳細的數據庫結構請參考需求文檔。

## API 接口

系統提供完整的 RESTful API，包括：

- 認證鑒權接口
- 實驗室信息管理
- 課題組管理
- 成員管理  
- 論文管理
- 新聞管理
- 項目管理
- 文件上傳接口

所有接口都有完整的權限控制和輸入驗證。

## 開發指南

### 前端開發
- 使用 Composition API
- 遵循 TypeScript 類型規範
- 使用 Naive UI 組件庫
- 響應式設計，支持多設備

### 後端開發
- 遵循 RESTful API 設計原則
- 使用軟刪除（enable 字段）
- 所有操作記錄審計日誌
- 文件存儲使用服務器路徑，不存 BLOB

### 安全考慮
- JWT token 認證
- bcrypt 密碼加密
- 輸入驗證和 XSS 防護
- 文件上傳安全檢查
- HTTPS 強制使用

## 部署說明

### 生產環境部署
1. 構建前端項目：`npm run build`
2. 配置 Web 服務器（Nginx）
3. 設置 HTTPS 證書
4. 配置數據庫連接
5. 設置文件上傳路徑權限
6. 配置日誌和監控

### 環境變量配置
- `DATABASE_URL` - 數據庫連接字符串
- `JWT_SECRET` - JWT 簽名密鑰
- `UPLOAD_FOLDER` - 文件上傳路徑
- `DEBUG` - 調試模式開關

## 貢獻指南

1. Fork 項目
2. 創建功能分支
3. 提交變更
4. 發起 Pull Request

## 許可證

本項目采用 MIT 許可證。

## 技術支持

如有問題或建議，請提交 Issue 或聯繫項目維護者。