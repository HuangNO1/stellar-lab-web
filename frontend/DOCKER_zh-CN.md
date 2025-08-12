# 前端 Docker 部署

此目錄包含了用於部署前端應用程式的 Docker 配置文件。

## 文件概覽

- `Dockerfile` - 生產環境多階段構建
- `Dockerfile.dev` - 開發環境構建（支持熱重載）
- `docker-compose.yml` - 生產部署配置
- `docker-compose.dev.yml` - 開發環境
- `deploy.sh` - 部署自動化腳本
- `docker/nginx.conf` - 生產環境 Nginx 配置
- `.dockerignore` - Docker 構建排除文件

## 快速開始

### 生產環境部署

```bash
# 構建並啟動前端
./deploy.sh start

# 檢查狀態
./deploy.sh status

# 查看日誌
./deploy.sh logs -f

# 停止前端
./deploy.sh stop
```

### 開發模式

```bash
# 啟動開發服務器（支持熱重載）
docker-compose -f docker-compose.dev.yml up --build

# 應用程式將在 http://localhost:8080 可用
```

## 部署腳本用法

```bash
./deploy.sh [動作] [選項]

動作:
  build       構建前端 Docker 鏡像
  start       啟動前端容器
  stop        停止前端容器
  restart     重啟前端容器
  logs        顯示前端日誌
  status      顯示容器狀態
  clean       刪除容器和鏡像
  health      檢查容器健康狀態
  shell       在前端容器中打開 shell

選項:
  --port PORT     指定端口（默認：3000）
  --detach, -d    在後台運行
  --follow, -f    跟隨日誌
  --help, -h      顯示幫助信息
```

## 網絡配置

前端容器連接到 `lab_web_default` 網絡以與後端通信。Nginx 配置將 API 請求代理到後端服務。

## 環境變量

- `NODE_ENV` - 設置為 'production' 或 'development'
- `CHOKIDAR_USEPOLLING` - 為開發環境啟用文件監聽

## 健康檢查

生產環境容器包含健康檢查，用於驗證：
- Nginx 正在響應
- `/health` 端點返回 200 OK

## 自定義配置

### Nginx 配置

編輯 `docker/nginx.conf` 來自定義：
- 服務器設置
- 代理配置
- 安全頭
- 緩存設置

### 構建參數

您可以傳遞構建參數來自定義構建：

```bash
docker build --build-arg NODE_ENV=production -t lab-website-frontend .
```

## 故障排除

1. **容器無法啟動**：檢查 Docker 守護程序和網絡
2. **端口衝突**：更改 docker-compose.yml 中的端口映射
3. **構建失敗**：檢查 .dockerignore 和構建上下文
4. **API 代理問題**：驗證後端正在運行且網絡連接正常

## 生產環境考量

1. 在容器前使用反向代理（如 Traefik 或 nginx）
2. 配置 SSL/TLS 證書
3. 設置日誌輪換
4. 配置監控和警報
5. 使用 Docker Swarm 或 Kubernetes 進行編排

---

**中文** | **[English](./DOCKER.md)**