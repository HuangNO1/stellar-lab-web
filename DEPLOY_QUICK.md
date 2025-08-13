# 快速部署說明

本地構建 + 鏡像部署方案的快速使用指南。

## 📦 新增腳本

- **build-images.sh** - 本地構建 Docker 鏡像
- **package-images.sh** - 打包並上傳鏡像到服務器
- **server-deploy.sh** - 服務器快速部署

## 🚀 3 步驟快速部署

### 1. 本地構建
```bash
./build-images.sh v1.0.0
```

### 2. 打包上傳
```bash
./package-images.sh v1.0.0 --server YOUR_SERVER_IP
```

### 3. 服務器部署
```bash
# SSH 到服務器
ssh root@YOUR_SERVER_IP
cd /opt/lab_web

# 部署
./server-deploy.sh v1.0.0
```

## ⏱️ 時間優勢

- **傳統方式**: 服務器構建 10-15 分鐘
- **鏡像方式**: 服務器部署 2-3 分鐘

## 📚 詳細文檔

查看 [IMAGE_DEPLOYMENT_zh-CN.md](./docs/IMAGE_DEPLOYMENT_zh-CN.md) 獲取完整使用說明。