# 本地構建 + 鏡像部署指南

快速部署方案：在本地構建 Docker 鏡像，打包上傳到服務器，避免服務器上的耗時構建過程。

## 🚀 優勢

- **⚡ 速度快**: 服務器部署時間從 10-15 分鐘縮短到 2-3 分鐘
- **📦 離線部署**: 支持離線環境，無需服務器聯網構建
- **🔄 版本控制**: 支持多版本鏡像管理
- **🛠️ 靈活性**: 可選擇性更新前端或後端
- **💾 節省資源**: 減少服務器 CPU 和網絡使用
- **🌏 中國優化**: 內建中國鏡像源加速，解決網絡連接問題

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

### 步驟 2: 打包部署文件

```bash
# 打包部署文件（推薦用於手動上傳）
./package-images.sh latest --package-only

# 自動上傳到服務器（需要 SSH 配置）
./package-images.sh --server 192.168.1.100

# 指定用戶和路徑
./package-images.sh --server example.com --user ubuntu --path /home/ubuntu/lab_web
```

打包完成後，你會得到 `docker-images` 目錄，包含所有部署文件：

```
docker-images/
└── deploy/                              # 完整的部署包
    ├── deploy.sh                        # 項目部署腳本
    ├── docker-compose.yml              # Docker Compose 配置
    ├── .env                            # 環境變量配置
    ├── nginx.conf                      # Nginx 配置文件
    ├── server-deploy.sh                # 服務器快速部署腳本
    ├── lab-website-backend-latest.tar.gz   # 後端鏡像文件
    └── lab-website-frontend-latest.tar.gz  # 前端鏡像文件
```

### 步驟 3: 上傳到服務器

**方法 1: 手動上傳（推薦）**
```bash
# 使用 scp 上傳整個部署目錄
scp -r docker-images/deploy/* root@your-server:/opt/lab_web/

# 或使用 rsync（支持增量上傳）
rsync -avz docker-images/deploy/ root@your-server:/opt/lab_web/
```

**方法 2: 自動上傳（需要 SSH 密鑰配置）**
```bash
./package-images.sh latest --server your-server
```

### 步驟 4: 服務器上部署

```bash
# SSH 登入服務器
ssh root@your-server

# 進入項目目錄
cd /opt/lab_web

# 執行快速部署
./server-deploy.sh

# 中國服務器使用鏡像加速
./server-deploy.sh --china

# 部署特定版本
./server-deploy.sh latest --china
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

### package-images.sh - 鏡像打包腳本

**功能**: 將構建好的鏡像打包成部署包，並可選上傳到服務器

**參數**:
- `版本標籤`: 指定鏡像版本 (默認: latest)
- `--package-only`: 僅打包，不上傳（推薦用於手動上傳）
- `--server HOST`: 服務器地址（自動上傳時必填）
- `--user USER`: SSH 用戶名 (默認: root)
- `--path PATH`: 服務器路徑 (默認: /opt/lab_web)
- `--output-dir DIR`: 本地輸出目錄 (默認: ./docker-images)
- `--upload-only`: 僅上傳，不重新打包

**示例**:
```bash
./package-images.sh --package-only                         # 僅打包（推薦）
./package-images.sh --server 192.168.1.100                 # 打包並自動上傳
./package-images.sh v1.0.0 --server example.com --user ubuntu  # 指定版本和用戶
./package-images.sh --upload-only --server 192.168.1.100   # 僅上傳現有包
```

### server-deploy.sh - 服務器快速部署腳本

**功能**: 在服務器上載入鏡像並快速部署服務

**參數**:
- `版本標籤`: 指定部署版本 (默認: latest)
- `--china`: 使用中國鏡像源加速（推薦中國服務器使用）
- `--no-health-check`: 跳過健康檢查
- `--keep-old`: 保留舊鏡像
- `--force-recreate`: 強制重新創建容器

**示例**:
```bash
./server-deploy.sh                   # 部署 latest 版本
./server-deploy.sh --china           # 使用中國鏡像加速部署
./server-deploy.sh v1.0.0 --china    # 部署指定版本並使用加速
./server-deploy.sh --no-health-check # 跳過健康檢查
```

## 🕐 時間對比

| 部署方式 | 本地時間 | 上傳時間 | 服務器時間 | 總時間 | 服務器資源占用 |
|----------|----------|----------|------------|--------|----------------|
| **傳統方式** | 0分鐘 | 0分鐘 | 10-15分鐘 | 10-15分鐘 | 高 (構建) |
| **鏡像部署** | 8-12分鐘 | 2-5分鐘 | 2-3分鐘 | 12-20分鐘 | 低 (載入) |
| **增量更新** | 2-5分鐘 | 1-2分鐘 | 1-2分鐘 | 4-9分鐘 | 極低 |

> 💡 **提示**: 雖然首次總時間可能稍長，但服務器資源占用大幅降低，且支持離線部署

## 💡 使用場景

### 場景 1: 初次部署（推薦流程）
```bash
# 本地
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --package-only

# 手動上傳
scp -r docker-images/deploy/* root@your-server:/opt/lab_web/

# 服務器（中國服務器推薦加 --china）
ssh root@your-server
cd /opt/lab_web
./server-deploy.sh v1.0.0 --china
```

### 場景 2: 代碼更新 (僅後端)
```bash
# 本地 - 僅構建變更的服務
./build-images.sh v1.0.1 --backend-only
./package-images.sh v1.0.1 --package-only

# 手動上傳
scp docker-images/deploy/lab-website-backend-v1.0.1.tar.gz root@your-server:/opt/lab_web/
scp docker-images/deploy/server-deploy.sh root@your-server:/opt/lab_web/

# 服務器
./server-deploy.sh v1.0.1 --china
```

### 場景 3: 緊急修復
```bash
# 本地 - 快速修復構建
./build-images.sh hotfix-001 --no-cache --backend-only
./package-images.sh hotfix-001 --package-only

# 快速上傳關鍵文件
scp docker-images/deploy/lab-website-backend-hotfix-001.tar.gz root@your-server:/opt/lab_web/

# 服務器 - 快速部署
./server-deploy.sh hotfix-001 --china
```

### 場景 4: 多環境部署
```bash
# 構建一次，部署到多個環境
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --package-only

# 上傳到測試環境
scp -r docker-images/deploy/* ubuntu@test.example.com:/home/ubuntu/lab_web/

# 上傳到生產環境  
scp -r docker-images/deploy/* root@prod.example.com:/opt/lab_web/
```

## 🌏 中國服務器優化

### 網絡問題解決
```bash
# 使用中國鏡像加速（推薦）
./server-deploy.sh --china

# 手動配置 Docker 鏡像源（如果需要）
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn", 
    "https://reg-mirror.qiniu.com"
  ]
}
EOF
sudo systemctl restart docker
```

### 上傳加速技巧
```bash
# 使用壓縮傳輸
scp -C -r docker-images/deploy/* root@your-server:/opt/lab_web/

# 使用 rsync 增量同步
rsync -avz --progress docker-images/deploy/ root@your-server:/opt/lab_web/
```

## 🔧 進階技巧

### 1. 批量部署腳本
```bash
#!/bin/bash
# batch-deploy.sh
VERSION="$1"
SERVERS=("server1.com" "server2.com" "server3.com")

./build-images.sh "$VERSION"
./package-images.sh "$VERSION" --package-only

for server in "${SERVERS[@]}"; do
    echo "Deploying to $server..."
    scp -r docker-images/deploy/* "root@$server:/opt/lab_web/"
    ssh "root@$server" "cd /opt/lab_web && ./server-deploy.sh $VERSION --china"
done
```

### 2. 自動化 CI/CD 整合
```yaml
# .github/workflows/deploy.yml 示例
name: Deploy to Production
on:
  push:
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Images
      run: ./build-images.sh ${{ github.ref_name }}
      
    - name: Package Images  
      run: ./package-images.sh ${{ github.ref_name }} --package-only
      
    - name: Deploy to Server
      run: |
        scp -r docker-images/deploy/* ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }}:/opt/lab_web/
        ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} "cd /opt/lab_web && ./server-deploy.sh ${{ github.ref_name }} --china"
```

### 3. 鏡像備份與版本管理
```bash
# 本地保存鏡像備份
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --package-only

# 創建版本備份目錄
mkdir -p backups/v1.0.0
cp -r docker-images/deploy/* backups/v1.0.0/

# 版本回滾
scp -r backups/v1.0.0/* root@your-server:/opt/lab_web/
ssh root@your-server "cd /opt/lab_web && ./server-deploy.sh v1.0.0 --china"
```

## 🛠️ 故障排除

### 1. 鏡像載入失敗
```bash
# 檢查鏡像文件完整性
ls -lh *.tar.gz
file lab-website-backend-latest.tar.gz

# 手動載入測試
gunzip -c lab-website-backend-latest.tar.gz | docker load

# 檢查鏡像是否載入成功
docker images | grep lab-website
```

### 2. 服務啟動失敗
```bash
# 查看容器日誌
docker-compose -p lab_web logs backend
docker-compose -p lab_web logs frontend

# 檢查容器狀態
docker-compose -p lab_web ps

# 檢查端口佔用
netstat -tlnp | grep -E ':3000|:8000|:3307'
```

### 3. 網絡連接問題
```bash
# 測試 Docker Hub 連接
docker pull hello-world

# 使用中國鏡像源
./server-deploy.sh --china

# 檢查 DNS 解析
nslookup registry-1.docker.io
```

### 4. SSH 連接問題
```bash
# 測試 SSH 連接
ssh -o ConnectTimeout=10 user@server "echo 'Connection OK'"

# 配置 SSH 密鑰
ssh-keygen -t rsa -b 4096
ssh-copy-id user@server

# 檢查 SSH 配置
ssh -v user@server
```

### 5. 文件權限問題
```bash
# 檢查文件權限
ls -la server-deploy.sh

# 修復執行權限
chmod +x server-deploy.sh deploy.sh

# 檢查目錄權限
ls -ld /opt/lab_web
```

## 📚 相關文檔

- [主要部署文檔](./DEPLOYMENT_zh-CN.md)
- [ECS 雲服務器部署](./ECS_DEPLOYMENT_zh-CN.md)
- [Docker 參考文檔](./DOCKER_REFERENCE_zh-CN.md)
- [靈活部署指南](./FLEXIBLE_DEPLOYMENT.md)

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