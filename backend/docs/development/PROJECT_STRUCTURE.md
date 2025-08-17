<!-- Language Switcher -->

<div align="right">

[English](PROJECT_STRUCTURE_EN.md)

</div>

# 項目結構說明

## 📁 整理後的目錄結構

```
backend/
├── app/                          # 主應用目錄
│   ├── __init__.py              # Flask 應用工廠
│   ├── models/                  # 數據模型層（ORM）
│   │   ├── __init__.py
│   │   ├── admin.py            # 管理員模型
│   │   ├── lab.py              # 實驗室模型
│   │   ├── member.py           # 成員模型
│   │   ├── paper.py            # 論文模型
│   │   ├── news.py             # 新聞模型
│   │   ├── project.py          # 項目模型
│   │   ├── research_group.py   # 課題組模型
│   │   ├── resource.py         # 實驗室資源模型 🆕
│   │   ├── uploaded_image.py   # 上傳圖片模型 🆕
│   │   └── edit_record.py      # 編輯記錄模型
│   ├── routes/                  # API 路由層
│   │   ├── admin.py            # 管理員路由
│   │   ├── auth.py             # 認證路由
│   │   ├── lab.py              # 實驗室路由
│   │   ├── member.py           # 成員路由
│   │   ├── paper.py            # 論文路由
│   │   ├── news.py             # 新聞路由
│   │   ├── project.py          # 項目路由
│   │   ├── research_group.py   # 課題組路由
│   │   ├── resource.py         # 實驗室資源路由 🆕
│   │   ├── media.py            # 媒體文件路由
│   │   ├── image_upload.py     # 圖片上傳路由 🆕
│   │   ├── edit_record.py      # 編輯記錄路由
│   │   ├── root.py             # 根路由
│   │   └── swagger_complete.py # 完整版自動化 Swagger 系統 🆕
│   ├── services/                # 業務邏輯層 ⭐
│   │   ├── __init__.py
│   │   ├── base_service.py     # 基礎服務類
│   │   ├── admin_service.py    # 管理員服務
│   │   ├── auth_service.py     # 認證服務
│   │   ├── lab_service.py      # 實驗室服務
│   │   ├── member_service.py   # 成員服務
│   │   ├── paper_service.py    # 論文服務
│   │   ├── news_service.py     # 新聞服務
│   │   ├── project_service.py  # 項目服務
│   │   ├── research_group_service.py # 課題組服務
│   │   ├── resource_service.py # 實驗室資源服務 🆕
│   │   ├── media_service.py    # 媒體服務
│   │   ├── image_upload_service.py # 圖片上傳服務 🆕
│   │   └── audit_service.py    # 審計服務
│   ├── auth/                    # 認證相關
│   │   ├── __init__.py
│   │   └── decorators.py       # 認證裝飾器
│   ├── utils/                   # 工具函數
│   │   ├── __init__.py
│   │   ├── helpers.py          # 通用幫助函數
│   │   ├── validators.py       # 數據驗證器
│   │   └── file_handler.py     # 文件處理工具
│   └── static/                  # 靜態文件
├── config/                      # 配置文件
│   └── config.py               # 應用配置
├── scripts/                     # 腳本目錄
│   ├── deployment/             # 部署腳本
│   │   ├── deploy.sh          # 部署腳本
│   │   ├── start.sh           # 啟動腳本
│   │   └── docker-entrypoint.sh # Docker 入口腳本
│   ├── development/            # 開發腳本
│   │   └── init_db.py         # 數據庫初始化
│   └── maintenance/            # 維護腳本
│       └── diagnose.sh        # 診斷腳本
├── tests/                      # 測試目錄 ⭐
│   ├── conftest.py            # pytest 配置
│   ├── unit/                  # 單元測試
│   │   ├── services/          # 服務層測試 ⭐
│   │   │   └── test_service_template.py # 服務測試模板
│   │   ├── models/            # 模型測試
│   │   └── utils/             # 工具函數測試
│   ├── integration/           # 集成測試
│   │   └── test_api.py       # API 集成測試
│   └── fixtures/              # 測試數據
│       ├── data_fixtures.py  # 業務數據 fixtures
│       └── user_fixtures.py  # 用戶認證 fixtures
├── docs/                      # 文檔目錄
│   ├── api/                   # API 文檔
│   ├── deployment/            # 部署文檔
│   │   └── DOCKER_DEPLOY.md  # Docker 部署指南
│   ├── development/           # 開發文檔
│   └── migration/             # 遷移文檔
│       └── SWAGGER_MIGRATION_GUIDE.md # Swagger 遷移指南
├── migrations/                # 數據庫遷移
├── logs/                      # 日誌目錄
├── media/                     # 媒體文件目錄
├── requirements.txt           # Python 依賴
├── run.py                     # 應用入口點
├── README.md                  # 項目說明
├── .env.example              # 環境變量示例
├── Dockerfile                # Docker 配置
├── docker-compose.yml        # Docker Compose 配置
└── docker-compose-minimal.yml # 最小化 Docker Compose
```

## 🎯 整理成果

### ✅ 已清理的文件
- **臨時演示文件**: `demo_swagger_automation.py`, `test_basic.py`, `test_swagger_automation.py` 等
- **遷移分析文件**: `MIGRATION_ANALYSIS.py`, `MIGRATION_SUCCESS_REPORT.py` 等
- **備份文件**: `app/__init__.py.backup`, `swagger_docs.py.backup`
- **冗余 Swagger 文件**: 升級到完整版 `swagger_complete.py` 系統
- **臨時筆記**: `think/` 目錄

### 🆕 新增功能
- **實驗室資源管理**: 完整的資源CRUD系統，支持設備、軟件、數據庫等資源管理
- **論文預覽圖片**: 為論文添加預覽圖片功能，提升視覺展示效果
- **校友管理增強**: 添加畢業年級和身份字段，支持校友排序功能
- **成員模板系統**: 支持研究領域TAG、個人主頁URL TAG、論文列表TAG等
- **圖片上傳服務**: 專門的Markdown圖片上傳和管理系統
- **404頁面**: 完整的前端錯誤處理頁面
- **菜單智能隱藏**: 根據數據存在性動態隱藏菜單項

### 📁 新增的目錄結構
- **`scripts/`**: 按功能分類的腳本（deployment, maintenance, development）
- **`tests/unit/services/`**: 專門用於服務層單元測試 ⭐
- **`tests/integration/`**: 集成測試
- **`tests/fixtures/`**: 測試數據
- **`docs/`**: 按類別組織的文檔
- **`media/description_image/`**: Markdown描述圖片存儲目錄 🆕

### 🧪 測試環境準備
- **`tests/conftest.py`**: pytest 配置，包含應用、數據庫等 fixtures
- **`tests/unit/services/test_service_template.py`**: 服務層測試模板
- **`tests/fixtures/data_fixtures.py`**: 業務數據測試 fixtures
- **`tests/fixtures/user_fixtures.py`**: 用戶認證測試 fixtures

## 🚀 使用指南

### 運行測試
```bash
# 運行所有測試
pytest

# 運行服務層測試
pytest tests/unit/services/ -v

# 運行特定標記的測試
pytest -m service  # 服務層測試
pytest -m unit     # 單元測試
pytest -m integration  # 集成測試

# 生成覆蓋率報告
pytest --cov=app
```

### 開發新功能
1. **添加模型**: 在 `app/models/` 中添加數據模型
2. **實現服務層**: 在 `app/services/` 中實現業務邏輯
3. **添加路由**: 在 `app/routes/` 中添加 API 端點
4. **編寫測試**: 在 `tests/unit/services/` 中添加服務層測試

### 部署項目
```bash
# 開發環境
./scripts/development/init_db.py

# 生產部署
./scripts/deployment/deploy.sh

# 診斷問題
./scripts/maintenance/diagnose.sh
```

## ✨ 項目優勢

- 🎯 **清晰的分層架構**: Routes → Services → Models
- 🧪 **完整的測試結構**: 專門的服務層測試目錄
- 📚 **規範的文檔組織**: 按類別分類的文檔結構
- 🛠️ **整潔的腳本管理**: 按功能分類的腳本目錄
- ⚡ **零維護 API 文檔**: 完整版自動化 Swagger 系統 (48+ 接口)
- 🚀 **優秀的可維護性**: 每個組件職責清晰
- 📦 **全面的資源管理**: 支援實驗室各類資源的統一管理
- 🎨 **增強的用戶體驗**: 預覽圖片、智能菜單、成員模板系統
- 🔧 **模組化設計**: 新增功能都遵循統一的架構模式