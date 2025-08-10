# 實驗室網站前端

這是一個基於 Vue 3 + TypeScript 的實驗室管理系統前端專案，支持多語言（中文/英文）並提供完整的管理後台功能。

## 🚀 技術棧

- **框架**: Vue 3 (Composition API)
- **語言**: TypeScript
- **UI 庫**: Naive UI
- **路由**: Vue Router 4
- **狀態管理**: Pinia + Vuex
- **國際化**: Vue I18n
- **HTTP 客戶端**: Axios
- **構建工具**: Vue CLI 5
- **代碼風格**: ESLint + TypeScript ESLint

## 📦 快速開始

### 環境要求
- Node.js >= 16
- Yarn 或 npm

### 安裝依賴
```bash
yarn install
# 或
npm install
```

### 開發模式
```bash
yarn serve
# 或
npm run serve
```
啟動後訪問 http://localhost:8080

### 構建生產版本
```bash
yarn build
# 或
npm run build
```

### 代碼檢查和修復
```bash
yarn lint
# 或
npm run lint
```

## 📁 專案結構

```
src/
├── api/                 # API 接口定義
├── assets/              # 靜態資源
├── components/          # 公共組件
├── composables/         # Vue 3 組合函數
├── guards/              # 路由守衛
├── layouts/             # 佈局組件
│   ├── AdminLayout.vue  # 管理後台佈局
│   └── UserLayout.vue   # 用戶端佈局
├── locales/             # 國際化文件
│   ├── zh.ts           # 中文
│   └── en.ts           # 英文
├── Model/               # 數據模型
├── router/              # 路由配置
├── services/            # 服務層
├── stores/              # Pinia 狀態管理
├── types/               # TypeScript 類型定義
├── utils/               # 工具函數
└── views/               # 頁面組件
    ├── admin/          # 管理後台頁面
    └── ...             # 用戶端頁面
```

## 🔧 開發指南

### 路由結構
- `/` - 首頁
- `/members` - 成員列表
- `/groups` - 研究組別
- `/papers` - 論文發表
- `/projects` - 專案展示
- `/news` - 最新消息
- `/about` - 關於實驗室
- `/admin/*` - 管理後台（需要登錄）

### 管理後台功能
- 實驗室基本資訊管理
- 成員資料管理
- 研究組別管理
- 論文發表管理
- 專案展示管理
- 最新消息管理
- 管理員帳戶管理

### 狀態管理
專案使用 Pinia 進行狀態管理，主要 store 包括：
- `auth.ts` - 身份認證狀態

### 國際化
支持中英文切換：
- 語言文件位於 `src/locales/`
- 使用 `$t()` 函數進行翻譯
- 在 Vue 文件中使用 `{{ $t('key') }}`

### 組合函數 (Composables)
- `useLab.ts` - 實驗室資訊相關
- `useMembers.ts` - 成員管理相關
- `useResearchGroups.ts` - 研究組別相關

### API 服務
- API 服務統一在 `src/services/api.ts` 中定義
- 使用 Axios 進行 HTTP 請求
- 支持請求攔截器處理認證

## 🎨 UI 組件庫

使用 Naive UI 作為主要 UI 庫：
- 已在 `App.vue` 中配置全局 `n-message-provider`
- 可直接使用 `useMessage()` hook 顯示通知
- 支持深色主題切換

### 常用組件
- `n-form` - 表單
- `n-table` - 表格
- `n-button` - 按鈕
- `n-input` - 輸入框
- `n-select` - 選擇器
- `n-modal` - 模態框
- `n-message` - 消息提示

## 🔒 身份認證

- 使用 JWT Token 進行身份認證
- Token 存儲在 Cookie 中（js-cookie）
- 路由守衛保護管理後台頁面

## 📱 響應式設計

專案採用響應式設計，支持：
- 桌面端
- 平板端
- 移動端

## 🐛 常見問題

### Naive UI useMessage 錯誤
如果遇到 "No outer <n-message-provider /> founded" 錯誤：
- 確保在 `App.vue` 中已包裹 `<n-message-provider>`
- 不要在組件中重複添加 `<n-message-provider>`

### 開發服務器代理
如需配置 API 代理，在 `vue.config.js` 中添加：
```javascript
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    }
  }
}
```

## 📄 許可證

此專案僅供內部使用。

## 🤝 貢獻指南

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📞 聯繫方式

如有任何問題，請聯繫開發團隊。