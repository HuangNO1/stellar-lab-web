# Docker 靈活部署配置示例

<!-- Language Switcher -->

<div align="right">

[English](README.md)

</div>

<!-- Content -->

此文件夾包含各種部署場景的 Docker Compose 配置示例，展示如何使用發布的 Docker 鏡像進行靈活配置。

## 📁 文件說明

### 1. `docker-compose.standalone.yml`
**獨立部署模式** - 使用發布的鏡像進行完整部署
- 包含所有服務（前端、後端、數據庫）
- 適合快速設置和測試
- 使用 GHCR 發布的 Docker 鏡像

### 2. `docker-compose.external-db.yml`
**外部數據庫模式** - 連接現有的 MySQL 數據庫
- 使用您現有的數據庫服務器
- 減少資源使用
- 適合擁有現有數據庫基礎設施的組織

### 3. `docker-compose.separate.yml`
**前後端分離模式** - 前後端獨立部署
- 前端和後端可以獨立部署
- 支援跨域部署
- 適合微服務架構

### 4. `.env.example`
**環境變量模板** - 完整的配置模板
- 包含所有支援的環境變量
- 包括安全建議
- 生產環境就緒的配置示例

## 🚀 使用說明

### 快速開始

```bash
# 下載配置示例
curl -L https://github.com/your-repo/lab_web/archive/main.tar.gz | tar xz
cd lab_web-main/examples

# 複製並客製化環境文件
cp .env.example .env
# 編輯 .env 文件進行配置

# 使用發布的鏡像部署
docker-compose -f docker-compose.standalone.yml up -d
```

### 使用特定配置

```bash
# 獨立部署（推薦新手）
docker-compose -f docker-compose.standalone.yml up -d

# 外部數據庫部署
docker-compose -f docker-compose.external-db.yml up -d

# 前後端分離部署
docker-compose -f docker-compose.separate.yml up -d
```

### 複製到根目錄

```bash
# 將所需配置複製到根目錄
cp examples/docker-compose.standalone.yml docker-compose.yml
cp examples/.env.example .env

# 編輯配置
nano .env

# 部署
docker-compose up -d
```

## 🔧 環境變量

所有示例都支援通過環境變量進行配置。主要變量包括：

### 前端配置
- `BACKEND_URL` - 後端服務地址
- `API_BASE_URL` - API 端點路徑
- `APP_TITLE` - 應用程式標題
- `CORS_ORIGIN` - 跨域設定

### 後端配置
- `DATABASE_URL` - 完整的數據庫連接字符串
- `SECRET_KEY` - Flask 密鑰
- `JWT_SECRET_KEY` - JWT 密鑰
- `CORS_ORIGINS` - 跨域白名單

### 數據庫配置
- `MYSQL_ROOT_PASSWORD` - MySQL root 密碼
- `MYSQL_DATABASE` - 數據庫名稱
- `MYSQL_USER` - 數據庫用戶
- `MYSQL_PASSWORD` - 數據庫用戶密碼

## 📊 部署場景

### 1. 完整實驗室網站設置
使用 `docker-compose.standalone.yml` 適用於：
- 新實驗室網站部署
- 測試和開發
- 自包含環境

### 2. 企業整合
使用 `docker-compose.external-db.yml` 適用於：
- 與現有數據庫基礎設施整合
- 企業安全合規
- 共享數據庫資源

### 3. 可擴展架構
使用 `docker-compose.separate.yml` 適用於：
- 高流量網站
- 負載平衡需求
- 多伺服器部署

## 🔒 安全建議

### 生產環境
1. **更改預設密碼** - 在 `.env` 文件中修改
2. **使用強密鑰** - 使用 `openssl rand -hex 32` 生成
3. **正確配置 CORS** - 指定具體域名
4. **生產環境使用 HTTPS**
5. **定期更新** - 拉取最新鏡像版本

### 生產環境配置示例
```bash
# 生成安全密鑰
export SECRET_KEY=$(openssl rand -hex 32)
export JWT_SECRET_KEY=$(openssl rand -hex 32)
export MYSQL_ROOT_PASSWORD=$(openssl rand -base64 32)

# 設置生產 CORS
export CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 🔍 故障排除

### 常見問題

1. **端口衝突**
   ```bash
   # 檢查端口使用
   netstat -tlnp | grep :3000
   
   # 在 .env 文件中修改端口
   FRONTEND_PORT=3001
   BACKEND_PORT=8001
   ```

2. **容器連接問題**
   ```bash
   # 檢查容器日誌
   docker-compose -f docker-compose.standalone.yml logs frontend
   docker-compose -f docker-compose.standalone.yml logs backend
   ```

3. **數據庫連接**
   ```bash
   # 驗證數據庫狀態
   docker-compose -f docker-compose.standalone.yml exec db mysql -u root -p -e "SHOW DATABASES;"
   ```

## 📚 其他資源

- **[完整部署指南](../docs/FLEXIBLE_DEPLOYMENT.md)** - 詳細部署說明
- **[主要 README](../README.md)** - 專案概覽和功能
- **[後端文檔](../backend/README.md)** - 後端專用配置
- **[前端文檔](../frontend/README.md)** - 前端專用配置

## 🆘 支援

如有問題或疑問：
- 查看 [故障排除指南](../docs/FLEXIBLE_DEPLOYMENT.md#故障排除)
- 檢視容器日誌：`docker-compose logs [service-name]`
- 在 GitHub 開啟 [issue](../../issues)

---

<div align="center">

**準備在幾分鐘內部署您的實驗室網站！**

*選擇最適合您需求的部署模式。*

</div>