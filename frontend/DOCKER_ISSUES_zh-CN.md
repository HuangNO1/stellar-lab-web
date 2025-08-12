# 前端 Docker 構建已知問題

## TypeScript 兼容性問題

### 問題描述
前端 Docker 構建當前因以下 TypeScript 兼容性問題而失敗：
- TypeScript 版本：~4.5.5（項目使用）
- @types/lodash：使用更新的模板字面量語法
- Node.js 版本：Docker 中的新版本

### 錯誤信息
```
TS1005: '?' expected.
type StringToNumber<T> = T extends `${infer N extends number}` ? N : never;
```

### 臨時解決方案

#### 方案 1：使用預構建分發版
如果 `dist` 目錄可用：

```dockerfile
FROM nginx:stable-alpine
COPY dist/ /usr/share/nginx/html/
COPY docker/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 方案 2：更新依賴
更新 `package.json`：

```bash
npm install typescript@~5.0.0
npm install @types/lodash@^4.14.195
npm audit fix
```

#### 方案 3：降級 Node.js
使用具有更好兼容性的 Node.js 16：

```dockerfile
FROM node:16-alpine as build-stage
```

#### 方案 4：排除類型檢查
添加到 `vue.config.js`：

```javascript
module.exports = {
  chainWebpack: config => {
    config.plugin('fork-ts-checker').tap(args => {
      args[0].typescript.enabled = false
      return args
    })
  }
}
```

### 推薦解決方案
對於生產部署，最佳方法是：

1. 本地構建或在 CI/CD 流水線中構建
2. 在 Docker 中使用構建的 `dist` 目錄
3. 使用 nginx 提供服務

### 構建腳本示例
```bash
#!/bin/bash
# build-frontend.sh
cd frontend
npm install
npm run build
docker build -f Dockerfile.simple -t lab-website-frontend .
```

其中 `Dockerfile.simple`：
```dockerfile
FROM nginx:stable-alpine
COPY dist/ /usr/share/nginx/html/
COPY docker/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

這種方法將構建過程與容器化分離，這在生產環境中通常是更好的選擇。

## 其他常見問題

### 內存不足問題
在資源受限的環境中，Node.js 構建可能會因內存不足而失敗。

**解決方案**：
```dockerfile
# 在 Dockerfile 中增加 Node.js 內存限制
ENV NODE_OPTIONS="--max_old_space_size=4096"
```

### 網絡超時問題
npm 安裝可能會因網絡問題而超時。

**解決方案**：
```bash
# 使用國內鏡像源
npm config set registry https://registry.npmmirror.com/
# 或在 Dockerfile 中
RUN npm config set registry https://registry.npmmirror.com/ && npm install
```

### 權限問題
在某些系統上可能會遇到文件權限問題。

**解決方案**：
```dockerfile
# 設置正確的用戶和權限
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs
```

---

**中文** | **[English](./DOCKER_ISSUES.md)**