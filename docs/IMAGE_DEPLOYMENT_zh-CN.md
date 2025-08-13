# 本地構建 + 鏡像部署指南

快速部署方案：在本地構建 Docker 鏡像，上傳到服務器，避免服務器上的耗時構建過程。

## 🚀 優勢

- **⚡ 速度快**: 服務器部署時間從 10-15 分鐘縮短到 2-3 分鐘
- **📦 離線部署**: 支持離線環境，無需服務器聯網構建
- **🔄 版本控制**: 支持多版本鏡像管理
- **🛠️ 靈活性**: 可選擇性更新前端或後端
- **💾 節省資源**: 減少服務器 CPU 和網絡使用

## 📋 部署流程

### 步驟 1: 本地構建鏡像

```bash
# 構建所有服務的鏡像
./build-images.sh

# 構建特定版本
./build-images.sh v1.0.0

# 僅構建後端
./build-images.sh --backend-only

# 僅構建前端  
./build-images.sh --frontend-only

# 無緩存構建
./build-images.sh --no-cache
```

### 步驟 2: 打包並上傳到服務器

```bash
# 打包並上傳到服務器
./package-images.sh --server 192.168.1.100

# 指定用戶和路徑
./package-images.sh --server example.com --user ubuntu --path /home/ubuntu/lab_web

# 僅打包，不上傳
./package-images.sh --package-only

# 僅上傳已打包的鏡像
./package-images.sh --upload-only --server 192.168.1.100
```

### 步驟 3: 服務器上部署

```bash
# SSH 登入服務器
ssh root@192.168.1.100

# 進入項目目錄
cd /opt/lab_web

# 執行快速部署
./server-deploy.sh

# 部署特定版本
./server-deploy.sh v1.0.0
```

## 📝 腳本說明

### build-images.sh - 本地構建腳本

**功能**: 在本地環境構建 Docker 鏡像

**參數**:
- `版本標籤`: 指定鏡像版本 (默認: latest)
- `--no-cache`: 不使用緩存構建
- `--backend-only`: 僅構建後端鏡像
- `--frontend-only`: 僅構建前端鏡像

**示例**:
```bash
./build-images.sh                    # 構建 latest 版本
./build-images.sh v1.0.0            # 構建 v1.0.0 版本
./build-images.sh --no-cache        # 無緩存構建
./build-images.sh latest --backend-only  # 僅構建後端
```

### package-images.sh - 鏡像打包上傳腳本

**功能**: 將構建好的鏡像打包並上傳到服務器

**參數**:
- `版本標籤`: 指定鏡像版本 (默認: latest)
- `--server HOST`: 服務器地址 (必填)
- `--user USER`: SSH 用戶名 (默認: root)
- `--path PATH`: 服務器路徑 (默認: /opt/lab_web)
- `--output-dir DIR`: 本地輸出目錄 (默認: ./docker-images)
- `--package-only`: 僅打包，不上傳
- `--upload-only`: 僅上傳，不重新打包

**示例**:
```bash
./package-images.sh --server 192.168.1.100                    # 基本用法
./package-images.sh v1.0.0 --server example.com --user ubuntu  # 指定版本和用戶
./package-images.sh --package-only                             # 僅打包
./package-images.sh --upload-only --server 192.168.1.100      # 僅上傳
```

### server-deploy.sh - 服務器快速部署腳本

**功能**: 在服務器上載入鏡像並快速部署服務

**參數**:
- `版本標籤`: 指定部署版本 (默認: latest)
- `--no-health-check`: 跳過健康檢查
- `--keep-old`: 保留舊鏡像
- `--force-recreate`: 強制重新創建容器

**示例**:
```bash
./server-deploy.sh                   # 部署 latest 版本
./server-deploy.sh v1.0.0           # 部署 v1.0.0 版本
./server-deploy.sh --no-health-check # 跳過健康檢查
```

## 🕐 時間對比

| 部署方式 | 本地時間 | 服務器時間 | 總時間 | 服務器資源占用 |
|----------|----------|------------|--------|----------------|
| **傳統方式** | 0分鐘 | 10-15分鐘 | 10-15分鐘 | 高 (構建) |
| **鏡像部署** | 8-12分鐘 | 2-3分鐘 | 10-15分鐘 | 低 (載入) |
| **增量更新** | 2-5分鐘 | 1-2分鐘 | 3-7分鐘 | 極低 |

## 💡 使用場景

### 場景 1: 初次部署
```bash
# 本地
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --server YOUR_SERVER

# 服務器
./server-deploy.sh v1.0.0
```

### 場景 2: 代碼更新 (僅後端)
```bash
# 本地 - 僅構建變更的服務
./build-images.sh v1.0.1 --backend-only
./package-images.sh v1.0.1 --server YOUR_SERVER

# 服務器
./server-deploy.sh v1.0.1
```

### 場景 3: 緊急修復
```bash
# 本地 - 快速修復構建
./build-images.sh hotfix-001 --no-cache --backend-only
./package-images.sh hotfix-001 --server YOUR_SERVER

# 服務器 - 快速部署
./server-deploy.sh hotfix-001
```

### 場景 4: 多環境部署
```bash
# 構建一次，部署到多個環境
./build-images.sh v1.0.0

# 部署到測試環境
./package-images.sh v1.0.0 --server test.example.com

# 部署到生產環境
./package-images.sh v1.0.0 --server prod.example.com
```

## 🔧 進階技巧

### 1. 批量部署腳本
```bash
#!/bin/bash
# batch-deploy.sh
VERSION="$1"
SERVERS=("server1.com" "server2.com" "server3.com")

./build-images.sh "$VERSION"

for server in "${SERVERS[@]}"; do
    ./package-images.sh "$VERSION" --server "$server"
done
```

### 2. 自動化 CI/CD 整合
```bash
# .github/workflows/deploy.yml 示例
- name: Build Images
  run: ./build-images.sh ${{ github.sha }}
  
- name: Deploy to Production
  run: ./package-images.sh ${{ github.sha }} --server prod.example.com
```

### 3. 鏡像備份
```bash
# 本地保存鏡像備份
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --package-only
# 打包文件會保存在 ./docker-images/ 目錄
```

## 🛠️ 故障排除

### 1. SSH 連接問題
```bash
# 測試 SSH 連接
ssh -o ConnectTimeout=10 user@server "echo 'Connection OK'"

# 配置 SSH 密鑰
ssh-keygen -t rsa -b 4096
ssh-copy-id user@server
```

### 2. 鏡像載入失敗
```bash
# 檢查鏡像文件
ls -lh *.tar.gz
file backend-image-latest.tar.gz

# 手動載入測試
gunzip -c backend-image-latest.tar.gz | docker load
```

### 3. 服務啟動失敗
```bash
# 查看容器日誌
docker-compose -p lab_web logs backend
docker-compose -p lab_web logs frontend

# 檢查容器狀態
docker-compose -p lab_web ps
```

## 📚 相關文檔

- [主要部署文檔](./DEPLOYMENT_zh-CN.md)
- [ECS 雲服務器部署](./ECS_DEPLOYMENT_zh-CN.md)
- [Docker 參考文檔](./DOCKER_REFERENCE_zh-CN.md)