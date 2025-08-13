<!-- Language Switcher -->

<div align="right">

[English](README.md)

</div>

<!-- Header -->

<div align="center">

<img src="frontend/src/assets/logo.png" width="128"/>

# 實驗室網頁框架

現代化、通用的實驗室網站框架，內建內容管理系統

<!-- Shields/Badges -->

<p>
<a href="https://vuejs.org/"><img alt="Vue.js" src="https://img.shields.io/badge/前端-Vue%203-4FC08D?style=for-the-badge&logo=vue.js"></a>
<a href="https://flask.palletsprojects.com/"><img alt="Flask" src="https://img.shields.io/badge/後端-Flask-000000?style=for-the-badge&logo=flask"></a>
<a href="https://www.mysql.com/"><img alt="MySQL" src="https://img.shields.io/badge/數據庫-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white"></a>
<a href="https://www.docker.com/"><img alt="Docker" src="https://img.shields.io/badge/部署-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"></a>
<br/>
<img alt="License" src="https://img.shields.io/badge/許可證-MIT-green?style=for-the-badge">
<img alt="Status" src="https://img.shields.io/badge/狀態-生產就緒-success?style=for-the-badge">
<br/>
<a href="https://github.com/HuangNO1/stellar-lab-web/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/HuangNO1/stellar-lab-web/ci.yml?style=for-the-badge&logo=github&label=持續整合"></a>
<a href="https://github.com/HuangNO1/stellar-lab-web/releases"><img alt="Release" src="https://img.shields.io/github/v/release/HuangNO1/stellar-lab-web?style=for-the-badge&logo=github&label=發布"></a>
<a href="https://github.com/HuangNO1/stellar-lab-web/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/HuangNO1/stellar-lab-web?style=for-the-badge&logo=github&label=版本"></a>
<a href="https://github.com/HuangNO1/stellar-lab-web/pkgs/container/stellar-lab-web-frontend"><img alt="Frontend Image" src="https://img.shields.io/badge/ghcr.io-前端鏡像-blue?style=for-the-badge&logo=docker"></a>
<a href="https://github.com/HuangNO1/stellar-lab-web/pkgs/container/stellar-lab-web-backend"><img alt="Backend Image" src="https://img.shields.io/badge/ghcr.io-後端鏡像-blue?style=for-the-badge&logo=docker"></a>
</p>

</div>

## ✨ 專案簡介

這個實驗室網站框架誕生於對現有解決方案的不滿。許多實驗室依賴靜態的 GitHub Pages，更新繁瑣且缺乏適當的內容管理功能。我們的框架解決了這些痛點，提供現代化、功能豐富的解決方案，任何實驗室都能輕鬆採用和客製化。

基於 Vue 3 和 Flask 構建，本框架提供完整的實驗室網站解決方案，包含對外展示頁面和全面的管理後台。設計理念是通用性 - 允許輕鬆客製化學校 Logo、實驗室資訊和品牌標識，適合不同機構使用。

## 🎯 核心功能

### 🌐 公開網站
- **動態首頁**：可客製化的實驗室介紹，含輪播圖片和最新消息
- **成員展示**：有序展示教師、學生和校友，附詳細個人檔案
- **研究組別**：展示不同研究團隊的專注領域和成員
- **學術發表**：完整論文管理，支援搜尋、篩選和作者連結
- **研究項目**：顯示進行中和已完成的研究項目
- **新聞動態**：最新實驗室成就、獎項和公告
- **🌍 國際化支援**：完整的中英文界面切換，含在地化內容
- **🎨 主題支援**：全頁面明/暗主題切換，提升使用體驗
- **📱 響應式設計**：在桌面、平板和手機設備上完美顯示

### 🛠️ 內容管理系統
- **📊 儀表板**：全面概覽，含統計資料和快速操作（支援主題切換）
- **實驗室管理**：基本資訊、聯絡詳情、Logo 和輪播圖片管理
- **成員管理**：完整 CRUD 操作，含頭像裁切和研究組分配
- **研究組管理**：團隊組織，含組長指派和描述編輯
- **論文管理**：學術發表記錄，含 Markdown 內容編輯和檔案上傳
- **項目管理**：研究項目追蹤，含狀態管理
- **新聞管理**：新聞發布，含分類和內容編輯
- **👥 管理員管理**：多層級管理員帳戶，含權限控制
- **📝 操作日誌**：所有系統變更的完整稽核軌跡，含詳細追蹤
- **📁 媒體管理**：集中式檔案上傳和儲存系統
- **🌐 多語言後台**：管理界面完全支援國際化

### 🔧 技術卓越
- **現代架構**：Vue 3 + TypeScript 前端，Python Flask 後端
- **安全優先**：JWT 認證、bcrypt 加密、XSS 防護、CSRF 預防
- **效能優化**：資料庫索引、分頁、快取和查詢優化
- **Docker 就緒**：完整容器化，一鍵部署
- **開發友好**：全面 API 文件、測試框架和清晰程式碼結構

## 🎨 界面預覽

### 🌟 主要亮點
- **🌐 國際化支援**：完整的中英文界面切換
- **🎨 主題切換**：明/暗主題切換，提升使用體驗
- **📱 響應式設計**：所有設備上的無縫體驗
- **⚡ 現代化 UI**：乾淨專業的設計，直覺式導航

### 🏠 公開網站界面

#### 首頁與核心功能
<div align="center">
<img src="preview/zh/home.png" width="100%" alt="首頁 - 實驗室介紹"/>
<p><em>實驗室首頁，可客製化介紹內容和最新動態</em></p>
</div>

#### 成員與研究展示
<div align="center">
<table>
<tr>
<td width="50%"><img src="preview/zh/member.png" width="100%" alt="成員目錄"/></td>
<td width="50%"><img src="preview/zh/memberDetail.png" width="100%" alt="成員檔案"/></td>
</tr>
<tr>
<td align="center"><em>成員目錄，有序展示</em></td>
<td align="center"><em>詳細成員檔案，含研究資訊</em></td>
</tr>
</table>
</div>

#### 學術發表與研究項目
<div align="center">
<table>
<tr>
<td width="50%"><img src="preview/zh/paper.png" width="100%" alt="論文列表"/></td>
<td width="50%"><img src="preview/zh/project.png" width="100%" alt="研究項目概覽"/></td>
</tr>
<tr>
<td align="center"><em>學術發表管理，支援搜尋和篩選</em></td>
<td align="center"><em>研究項目，含狀態追蹤</em></td>
</tr>
</table>
</div>

#### 新聞動態
<div align="center">
<table>
<tr>
<td width="50%"><img src="preview/zh/news.png" width="100%" alt="新聞列表"/></td>
<td width="50%"><img src="preview/zh/newsDetail.png" width="100%" alt="新聞詳情"/></td>
</tr>
<tr>
<td align="center"><em>實驗室新聞和公告</em></td>
<td align="center"><em>詳細新聞內容，含富文本編輯</em></td>
</tr>
</table>
</div>

### 🛠️ 管理後台界面

#### 儀表板概覽與主題切換
<div align="center">
<table>
<tr>
<td width="50%"><img src="preview/zh/admin_dashboard.png" width="100%" alt="管理儀表板 明亮主題"/></td>
<td width="50%"><img src="preview/zh/admin_dashboard_dark_theme.png" width="100%" alt="管理儀表板 深色主題"/></td>
</tr>
<tr>
<td align="center"><em>管理儀表板 - 明亮主題</em></td>
<td align="center"><em>管理儀表板 - 深色主題</em></td>
</tr>
</table>
</div>

#### 管理界面
<div align="center">
<table>
<tr>
<td width="33%"><img src="preview/zh/admin_memberManage.png" width="100%" alt="成員管理"/></td>
<td width="33%"><img src="preview/zh/admin_labManage.png" width="100%" alt="實驗室管理"/></td>
<td width="33%"><img src="preview/zh/admin_adminManage.png" width="100%" alt="管理員管理"/></td>
</tr>
<tr>
<td align="center"><em>成員管理，含 CRUD 操作</em></td>
<td align="center"><em>實驗室資訊管理</em></td>
<td align="center"><em>管理員帳戶管理</em></td>
</tr>
</table>
</div>

#### 系統監控
<div align="center">
<img src="preview/zh/admin_operationLogs.png" width="70%" alt="操作日誌"/>
<p><em>全面的操作日誌，系統稽核軌跡</em></p>
</div>

## 🚀 快速開始

### 方法一：使用發布的 Docker 鏡像（推薦）

```bash
# 下載配置範例
curl -L https://github.com/your-repo/lab_web/archive/main.tar.gz | tar xz
cd lab_web-main/examples

# 複製並客製化環境文件
cp .env.example .env
# 編輯 .env 文件以配置您的設定

# 使用發布的鏡像部署
docker-compose -f docker-compose.standalone.yml up -d

# 存取應用程式
# 前端：http://localhost:3000
# 後端 API：http://localhost:8000
# 管理面板：http://localhost:3000/admin
```

### 方法二：靈活部署

**僅前端（連接外部後端）：**
```bash
docker run -d -p 3000:80 \
  -e BACKEND_URL=https://your-api.com \
  -e API_BASE_URL=https://your-api.com/api \
  -e APP_TITLE="您的實驗室" \
  ghcr.io/your-repo/frontend:latest
```

**僅後端（獨立 API）：**
```bash
docker run -d -p 8000:8000 \
  -e DATABASE_URL="mysql+pymysql://user:pass@host:3306/db" \
  -e SECRET_KEY="your-secret" \
  -e CORS_ORIGINS="https://your-frontend.com" \
  ghcr.io/your-repo/backend:latest
```

### 方法三：從原始碼建構

```bash
# 複製儲存庫
git clone [your-repo-url]
cd lab_web

# 使用 Docker Compose 啟動所有服務
docker-compose up -d --build

# 存取應用程式
# 前端：http://localhost:3000
# 後端 API：http://localhost:8000
# 管理面板：http://localhost:3000/admin
```

### 方法四：手動設定

```bash
# 後端設定
cd backend
pip install -r requirements.txt
python run.py

# 前端設定（新終端）
cd frontend
npm install
npm run serve
```

## 📊 系統概覽

### 架構
- **前端**：Vue 3 + TypeScript + Naive UI + Vue Router + Pinia
- **後端**：Python + Flask + SQLAlchemy + JWT + MySQL
- **資料庫**：MySQL 完整關聯式設計
- **部署**：Docker + Docker Compose + Nginx
- **儲存**：本地檔案系統，有序媒體管理

### 預設憑證
- **管理員用戶名**：`admin`
- **管理員密碼**：`admin123`
- **資料庫**：自動初始化含範例資料

⚠️ **重要**：生產環境請立即更改預設密碼！

## 💡 使用案例

### 適用於：
- **學術實驗室**：大學和研究所的研究小組
- **企業研發團隊**：公司研究開發部門
- **醫學實驗室**：醫院和臨床研究實驗室
- **政府研究機構**：公部門研究機構
- **新創實驗室**：新興技術公司和孵化器

### 從 GitHub Pages 遷移
本框架專為目前使用 GitHub Pages 的實驗室設計，滿足以下需求：
- **輕鬆內容更新**：不再需要手動編輯 HTML/Markdown
- **動態內容**：即時更新，無需重新建構
- **豐富媒體支援**：圖片上傳、PDF 論文、成員照片
- **搜尋功能**：輕鬆找到論文、成員和項目
- **管理控制**：多位管理員，不同權限等級

## 🌏 本地化配置

### 中文語言支援（繁體 vs 簡體）

系統目前使用**繁體中文**作為預設的中文本地化設定。如果您需要**簡體中文**支援，需要修改以下檔案：

#### 後端本地化
**檔案**：`/backend/app/utils/messages_zh.py`
- **目前狀態**：繁體中文
- **包含內容**：錯誤訊息、成功通知、驗證訊息

**切換至簡體中文：**
```python
# 將繁體中文字符替換為簡體對應字符
# 範例更改：
'LOGIN_SUCCESS': '登录成功',        # 原為：'登錄成功'
'CREATE_SUCCESS': '创建成功',       # 原為：'創建成功' 
'LAB_UPDATE_SUCCESS': '实验室信息更新成功',  # 原為：'實驗室信息更新成功'
'RESEARCH_GROUP_CREATE_SUCCESS': '研究组创建成功',  # 原為：'課題組創建成功'
```

#### 前端本地化  
**檔案**：`/frontend/src/locales/zh.ts`
- **目前狀態**：繁體中文
- **包含內容**：UI 標籤、導航、表單標籤、系統訊息

**切換至簡體中文：**
```typescript
export default {
  nav: {
    home: '首页',        // 原為：'首頁'
    members: '成员',     // 原為：'成員' 
    projects: '项目',    // 原為：'項目'
    papers: '论文',      // 原為：'論文'
    news: '新闻',        // 原為：'新聞'
  },
  common: {
    loading: '加载中...',  // 原為：'載入中...'
    error: '错误',         // 原為：'錯誤'
    confirm: '确认',       // 原為：'確認'
    cancel: '取消',        // 兩者相同
    fetchError: '获取数据失败',  // 原為：'獲取數據失敗'
    // ... 繼續其他翻譯
  }
  // ... 其餘翻譯物件
}
```

#### 轉換工具與建議

1. **自動轉換**：使用線上工具如 [OpenCC](https://github.com/BYVoid/OpenCC) 進行批量轉換
2. **人工審查**：務必審查自動轉換結果，確保語境正確
3. **專業術語**：某些技術術語在兩種變體中可能保持相同
4. **測試**：更改後徹底測試介面

#### 同時支援兩種變體

如果您需要同時支援繁體和簡體中文：

1. **建立獨立的語言檔案：**
   - `zh-TW.ts`（繁體中文）
   - `zh-CN.ts`（簡體中文）

2. **更新前端 i18n 配置：**
```typescript
// 在 src/locales/index.ts 中
import zhTW from './zh-TW'
import zhCN from './zh-CN'

const messages = {
  en,
  'zh-TW': zhTW,
  'zh-CN': zhCN
}
```

3. **在 UI 中添加語言選擇器**，讓使用者選擇偏好的中文變體

#### 注意事項
- 目前 `/preview/zh/` 中的預覽圖片顯示繁體中文介面
- 更改本地化設定後記得重新建構前端
- 選擇中文變體時考慮您的目標使用者群體

## 📁 專案結構

```
lab_web/
├── frontend/          # Vue 3 前端應用程式
│   ├── src/          # 原始碼
│   ├── public/       # 靜態資源
│   └── dist/         # 建構檔案
├── backend/           # Flask 後端應用程式
│   ├── app/          # 應用程式碼
│   ├── docs/         # API 文件
│   ├── scripts/      # 部署與維護腳本
│   └── tests/        # 測試套件
├── docs/             # 專案文件
├── docker-compose.yml # 全端部署
└── deploy/           # 部署腳本
```

詳細技術資訊請參考：
- 前端：[frontend/README.md](frontend/README.md)
- 後端：[backend/README.md](backend/README.md)
- 部署：[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 🔐 安全功能

- **企業級認證**：JWT 令牌，安全過期機制
- **多層授權**：超級管理員和一般管理員角色
- **完整稽核軌跡**：所有操作含時間戳和使用者記錄
- **XSS/CSRF 防護**：現代 Web 安全實作
- **安全檔案上傳**：類型驗證和大小限制
- **軟刪除系統**：資料安全，含恢復功能

## 🌐 多語言支援

完整界面支援：
- **繁體中文**：完整繁體中文界面
- **簡體中文**：完整简体中文界面
- **英文**：完整英文界面
- **可擴展**：輕鬆新增更多語言

內容管理支援所有文字欄位的雙語編輯。

## 📱 設備相容性

- **桌面**：完整功能界面（1024px+）
- **平板**：觸控優化體驗（768-1024px）
- **手機**：行動裝置優先響應式設計（<768px）
- **跨瀏覽器**：相容現代瀏覽器

## 🛠️ 客製化

### 品牌塑造
- 上傳您機構的 Logo
- 客製化色彩方案和主題
- 設定實驗室名稱和聯絡資訊
- 為首頁新增輪播圖片

### 內容結構
- 定義研究組別和專注領域
- 按類別組織成員（教師/學生/校友）
- 按類型和場所分類出版物
- 含時間軸的項目組合管理

## 📚 文件

- **[部署指南](docs/DEPLOYMENT.md)**：完整設定說明
- **[API 文件](backend/docs/api/)**：完整 REST API 參考
- **[使用手冊](docs/USER_MANUAL.md)**：管理面板使用指南
- **[開發指南](docs/DEVELOPMENT.md)**：貢獻和客製化

## 🤝 貢獻

我們歡迎來自研究社群的貢獻：

1. Fork 儲存庫
2. 建立功能分支（`git checkout -b feature/amazing-feature`）
3. 提交變更（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 開啟 Pull Request

## 📧 支援

如有問題、議題或功能請求：
- 在 GitHub 開啟 [issue](../../issues)
- 查看我們的[文件](docs/)
- 聯絡開發團隊

## 📄 許可證

本專案採用 MIT 許可證 - 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**今天就改變您實驗室的線上形象！**

*幾分鐘內從靜態頁面轉換為動態、可管理的內容。*

</div>