# 實驗室網站前端

這是一個基於 Vue 3 + TypeScript 的實驗室管理系統前端專案，支持多語言（中文/英文）、響應式設計，並提供完整的管理後台功能。

## 🚀 技術棧

- **框架**: Vue 3 (Composition API)
- **語言**: TypeScript
- **UI 庫**: Naive UI 2.42+
- **路由**: Vue Router 4
- **狀態管理**: Pinia + Vuex
- **國際化**: Vue I18n 9.14+
- **HTTP 客戶端**: Axios 1.11+
- **構建工具**: Vue CLI 5
- **代碼風格**: ESLint + TypeScript ESLint
- **圖片處理**: vue-advanced-cropper 2.8+
- **Markdown 編輯**: md-editor-v3 5.8+
- **工具庫**: js-cookie, highlight.js

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
├── assets/              # 靜態資源
│   ├── engineering.jpg  # 默認輪播圖
│   └── laptop.jpg      # 默認輪播圖
├── components/          # 公共組件
│   ├── HelloWorld.vue  # 示例組件
│   ├── ImageCropperModal.vue  # 圖片裁切模態框
│   ├── MarkdownEditor.vue     # Markdown 編輯器
│   ├── I18nMdEditor.vue       # 國際化 Markdown 編輯器
│   ├── SearchComponent.vue    # 搜索組件
│   ├── ProfileModal.vue       # 個人資料模態框
│   ├── QuickActionModal.vue   # 快速操作模態框
│   └── JsonDetailModal.vue    # JSON 詳情模態框
├── composables/         # Vue 3 組合函數
│   ├── useLab.ts       # 實驗室資訊相關
│   ├── useMembers.ts   # 成員管理相關
│   └── useResearchGroups.ts  # 研究組別相關
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
│   └── api.ts          # API 接口統一管理
├── stores/              # Pinia 狀態管理
├── types/               # TypeScript 類型定義
│   └── api.ts          # API 相關類型
├── utils/               # 工具函數
│   ├── media.ts        # 媒體文件處理
│   └── text.ts         # 文本處理
└── views/               # 頁面組件
    ├── admin/           # 管理後台頁面
    │   ├── DashboardView.vue      # 儀表板
    │   ├── LoginView.vue          # 登錄頁面
    │   ├── ProfileView.vue        # 個人資料
    │   ├── ChangePasswordView.vue # 修改密碼
    │   ├── LabManageView.vue      # 實驗室管理
    │   ├── MemberManageView.vue   # 成員管理
    │   ├── GroupManageView.vue    # 研究組管理
    │   ├── PaperManageView.vue    # 論文管理
    │   ├── ProjectManageView.vue  # 專案管理
    │   ├── NewsManageView.vue     # 新聞管理
    │   ├── AdminManageView.vue    # 管理員管理
    │   ├── SystemManageView.vue   # 系統管理
    │   └── OperationLogsView.vue  # 操作日誌
    ├── HomeView.vue      # 首頁
    ├── MemberView.vue    # 成員列表
    ├── MemberDetailView.vue # 成員詳情
    ├── GroupView.vue     # 研究組詳情
    ├── PaperView.vue     # 論文列表
    ├── PaperDetailView.vue # 論文詳情
    ├── ProjectView.vue   # 專案列表
    ├── ProjectDetailView.vue # 專案詳情
    ├── NewsView.vue      # 新聞列表
    └── NewsDetailView.vue # 新聞詳情
```

## 🔧 核心功能

### 前台用戶功能
- 🏠 **首頁展示**: 實驗室介紹、輪播圖展示、最新動態
- 👥 **成員管理**: 成員列表、成員詳情、研究組分類
- 📚 **研究組展示**: 研究組介紹、組員列表、研究方向
- 📝 **論文發表**: 論文列表、詳細信息、分類篩選
- 🚀 **專案展示**: 專案介紹、技術棧、成果展示
- 📢 **新聞動態**: 最新消息、活動公告、獲獎信息
- 🌍 **多語言支持**: 中英文自由切換
- 📱 **響應式設計**: 支持桌面、平板、手機端

### 後台管理功能
- 🎛️ **儀表板**: 系統概覽、數據統計、快速操作
- 🏢 **實驗室管理**: 基本信息、聯繫方式、Logo 和輪播圖管理
- 👨‍💼 **成員管理**: 成員資料 CRUD、頭像上傳裁切、研究組分配
- 🔬 **研究組管理**: 組別信息、負責人指派、描述編輯
- 📄 **論文管理**: 論文發表記錄、Markdown 內容編輯
- 💼 **專案管理**: 專案信息維護、技術棧管理、成果展示
- 📰 **新聞管理**: 新聞發布、分類管理、內容編輯
- 🔐 **權限管理**: 管理員帳號、密碼修改、操作日誌
- ⚙️ **系統管理**: 系統配置、數據備份、日誌查看

## 🎨 特色功能

### 圖片處理系統
- **智能裁切**: 基於 vue-advanced-cropper 的圖片裁切功能
- **多格式支持**: 支持頭像、Logo、輪播圖等不同尺寸需求
- **預覽功能**: 實時預覽裁切效果
- **錯誤處理**: 圖片載入失敗自動回退

### 動態網站配置
- **動態標題**: 根據實驗室設置自動更新網頁標題
- **動態 Favicon**: 使用實驗室 Logo 作為網站圖標
- **智能回退**: 無設置時使用預設值，確保穩定性

### Markdown 編輯系統
- **雙語編輯**: 支持中英文 Markdown 內容同時編輯
- **實時預覽**: 所見即所得編輯體驗
- **語法高亮**: 代碼塊語法高亮顯示
- **工具欄**: 豐富的格式化工具

### 搜索與篩選
- **全文搜索**: 支持成員、論文、專案等內容搜索
- **智能篩選**: 多條件組合篩選
- **實時結果**: 即時顯示搜索結果

## 🔧 開發指南

### 路由結構
```
用戶端路由:
├── / - 首頁
├── /members - 成員列表
├── /member/:id - 成員詳情
├── /group/:id - 研究組詳情
├── /papers - 論文列表
├── /paper/:id - 論文詳情
├── /projects - 專案列表
├── /project/:id - 專案詳情
├── /news - 新聞列表
└── /news/:id - 新聞詳情

管理後台路由 (需要登錄):
├── /admin - 後台首頁 (重定向到 dashboard)
├── /admin/login - 登錄頁面
├── /admin/dashboard - 儀表板
├── /admin/profile - 個人資料
├── /admin/change-password - 修改密碼
├── /admin/lab - 實驗室管理
├── /admin/members - 成員管理
├── /admin/groups - 研究組管理
├── /admin/papers - 論文管理
├── /admin/projects - 專案管理
├── /admin/news - 新聞管理
├── /admin/admins - 管理員管理
├── /admin/system - 系統管理
└── /admin/logs - 操作日誌
```

### 狀態管理
專案使用 Pinia 進行狀態管理，主要 store 包括：
- `auth.ts` - 身份認證狀態
- 全局狀態通過 provide/inject 機制共享實驗室信息和主題設置

### 國際化
支持中英文切換：
- 語言文件位於 `src/locales/`
- 使用 `useI18n()` 組合函數獲取翻譯方法
- 在模板中使用 `{{ $t('key') }}` 進行翻譯
- 支持動態語言切換，無需重新載入頁面

### 組合函數 (Composables)
- `useLab.ts` - 實驗室資訊相關，提供自動獲取功能
- `useMembers.ts` - 成員管理相關，支持搜索和篩選
- `useResearchGroups.ts` - 研究組別相關，包含自動獲取和管理功能

### API 服務
- API 服務統一在 `src/services/api.ts` 中定義
- 使用 Axios 進行 HTTP 請求
- 支持請求/響應攔截器處理認證和錯誤
- 統一的錯誤處理和消息提示

## 🎨 UI 組件庫

使用 Naive UI 作為主要 UI 庫：
- 已在 `App.vue` 中配置全局 `n-message-provider`
- 可直接使用 `useMessage()` hook 顯示通知
- 支持深色主題切換
- 響應式設計，適配多種設備

### 常用組件
- `n-form` / `n-form-item` - 表單組件
- `n-data-table` - 數據表格，支持分頁、排序、篩選
- `n-button` - 按鈕組件
- `n-input` / `n-select` / `n-upload` - 輸入組件
- `n-modal` / `n-drawer` - 彈窗組件
- `n-message` / `n-notification` - 消息提示
- `n-card` - 卡片容器
- `n-spin` - 加載指示器

## 🔒 身份認證

- 使用 JWT Token 進行身份認證
- Token 存儲在 Cookie 中（使用 js-cookie）
- 路由守衛保護管理後台頁面
- 自動處理 Token 過期和刷新
- 統一的登錄狀態管理

## 📱 響應式設計

專案採用響應式設計，支援多種設備：
- **桌面端**: 1024px 以上，完整功能展示
- **平板端**: 768px - 1024px，適配觸控操作
- **手機端**: 768px 以下，優化移動體驗
- 使用 CSS Grid 和 Flexbox 進行佈局
- 圖片和媒體內容自適應縮放

## 🛠️ 工具函數

### 媒體處理 (`utils/media.ts`)
- `getMediaUrl()` - 獲取媒體文件完整 URL
- `hasCarouselImages()` - 檢查是否有輪播圖片

### 文本處理 (`utils/text.ts`)
- `stripMarkdown()` - 移除 Markdown 標記，獲取純文本

## 🐛 常見問題與解決方案

### Naive UI useMessage 錯誤
**問題**: "No outer <n-message-provider /> founded" 錯誤  
**解決**: 確保在 `App.vue` 中已包裹 `<n-message-provider>`，不要在組件中重複添加

### 圖片上傳和裁切問題
**問題**: 圖片裁切後無法正常顯示  
**解決**: 檢查 `ImageCropperModal` 組件的使用方式，確保正確傳遞裁切類型參數

### 國際化內容不顯示
**問題**: 切換語言後部分內容未更新  
**解決**: 檢查是否使用 `computed` 屬性或 `watch` 監聽語言變化，確保響應式更新

### 路由守衛問題
**問題**: 已登錄用戶無法訪問管理後台  
**解決**: 檢查 Token 是否正確存儲，路由守衛邏輯是否正確

### 開發服務器代理配置
如需配置 API 代理，在 `vue.config.js` 中添加：
```javascript
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  }
}
```

## 📊 性能優化

### 已實施的優化
- **懶加載**: 路由組件按需加載
- **圖片優化**: 輪播圖和頭像圖片壓縮處理
- **緩存策略**: 實驗室信息等公共數據緩存
- **代碼分割**: 管理後台和用戶端代碼分離

### 建議的優化
- 實施 Service Worker 進行離線緩存
- 使用 CDN 加速靜態資源載入
- 實施虛擬滾動處理大量數據列表
- 添加骨架屏提升加載體驗

## 📄 許可證

此專案僅供內部使用。

## 🤝 貢獻指南

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 開發規範
- 遵循 TypeScript 嚴格模式
- 使用 ESLint 進行代碼檢查
- 組件命名使用 PascalCase
- 文件名使用 kebab-case
- 提交訊息使用中文，格式：`類型: 描述`

## 📞 技術支持

如有任何技術問題或建議，請聯繫開發團隊：
- 創建 Issue 描述問題
- 提供詳細的錯誤信息和復現步驟
- 標明使用的瀏覽器和版本信息

## 📈 更新日誌

### v0.1.0 (當前版本)
- ✅ 完成基礎框架搭建
- ✅ 實現用戶端完整功能
- ✅ 完成管理後台所有模塊
- ✅ 實現圖片裁切和動態配置功能
- ✅ 添加多語言支持和響應式設計
- ✅ 完善錯誤處理和用戶體驗