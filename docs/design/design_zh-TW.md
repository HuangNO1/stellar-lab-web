實驗室網頁框架設計需求
===

## 一、前言

因為我目前想要針對我們所在的實驗室進行網頁設計，但是因為網頁應該更具備一個抽象框架的功能，我覺得我有必要做成通用的，換句話說就是可以自己去設置學校、實驗室logo等資訊

## 二、技術選型

考慮到框架必須是開源且容易上手，後人方便維護，我以我熟練的框架：

1. 前端：Vue3 + Typescript + [Naive UI](https://www.naiveui.com/zh-CN/os-theme/docs/introduction)
2. 後端：Python + Flask
3. 資料庫：mysql（原本是考慮使用sqlite，但是考慮到如果有多個管理員並發編輯，sqlite會將整個資料庫文件鎖住）

在設計的時候要思考擴展性，不能寫死

## 三、數據結構

- 資料庫一定要注意中文編碼、日期格式問題。
- 所有的主鍵都要加索引，寫sql查詢的條件如果太多，可能影響性能，不過實驗室網站本身能增量的數據量不至於在幾年內到十萬級別，否則需要進行排查與調優
- enable是刪除的時候，設為0不展示（軟刪除），不能硬刪除
- 要編寫資料庫初始化腳本，並且寫一些基本數據進去，e.g.超級管理員、實驗室資訊
- 圖片和文件不建議直接用 blob 存，會拖慢整個尋找過程，要使用在伺服器上的路徑
- 因為目前我們很明顯沒有對象儲存的服務，所以儲存論文pdf和圖片只能存在伺服器上，或是不儲存論文pdf，需要看伺服器空間大小
- 注意：當我想要刪除整個課題組的時候，當課題組下有有效的成員時候要禁止刪除，直到所有成員都被遷移或刪除才能軟刪除整個課題組

### 3.1 管理員（進入管理端用）

管理員可以進行研究所的內容進行修改，只有超級管理員可以編輯新增或減少，管理員與成員不相關

| key name   | 主鍵 | 含義             | 類型   | 範圍    | 非空        | 備註                                   |
| ---------- | ---- | ---------------- | ------ | ------- | ----------- | -------------------------------------- |
| admin_id   | 是   | 管理員id         | int    | /       | 是          | 遞增                                   |
| is_super   |      | 是否是超級管理員 | int    | (0, 1)  | 是（默認0） |                                        |
| admin_name |      | 管理員使用者名稱     | string | (0, 50) |             | 一定要約束是英文與數字組合，不能是中文 |
| admin_pass |      | 管理員密碼       | string | (0, 50) |             | 必須經過bcrypt等加密                   |
| enable     |      | 是               |        |         |             |                                        |

### 3.2 實驗室數據

這裡一定要清楚需求，只會有一個實驗室，不會有多個實驗室，如果要設計研究所，會把設計變得更複雜，雖然有這個表格，但我這裡默認這張表只會有一條數據，未來需要做擴展就有用，這個設計結構就有用（e.g.加表加鍵位）

| key name       | 主鍵 | 含義                         | 類型   | 範圍      | 非空        | 備註                |
| -------------- | ---- | ---------------------------- | ------ | --------- | ----------- | ------------------- |
| lab_id         | 是   | 實驗室id                     | int    | /         | 是          | 遞增                |
| lab_logo_path  |      | 實驗室logo在伺服器的儲存路徑 | string | (0, 500)  |             | 圖片限制5M          |
| carousel_img_1 |      | 輪播圖1路徑                  | string | (0, 500)  |             | 首頁輪播圖片        |
| carousel_img_2 |      | 輪播圖2路徑                  | string | (0, 500)  |             | 首頁輪播圖片        |
| carousel_img_3 |      | 輪播圖3路徑                  | string | (0, 500)  |             | 首頁輪播圖片        |
| carousel_img_4 |      | 輪播圖4路徑                  | string | (0, 500)  |             | 首頁輪播圖片        |
| lab_zh         |      | 實驗室名稱中文               | string | (0, 500)  |             |                     |
| lab_en         |      | 實驗室名稱英文               | string | (0, 500)  |             |                     |
| lab_desc_zh    |      | 實驗室介紹中文               | text   | /         |             | 支持Markdown格式    |
| lab_desc_en    |      | 實驗室介紹英文               | text   | /         |             | 支持Markdown格式    |
| lab_address_zh |      | 實驗室地址中文               | string | (0, 500)  |             |                     |
| lab_address_en |      | 實驗室地址英文               | string | (0, 500)  |             |                     |
| lab_email      |      | 實驗室Email                  | string | (0, 500)  |             |                     |
| lab_phone      |      | 實驗室電話                   | string | (0, 500)  |             |                     |
| enable         |      | 數據是否有效                 | int    | (0, 1)    | 是（默認1） | 0->無效;<br>1->有效 |
| created_at     |      | 創建時間                     | datetime | /        | 是          | 自動生成            |
| updated_at     |      | 更新時間                     | datetime | /        | 是          | 自動更新            |

### 3.3 課題組

| key name                    | 主鍵     | 含義           | 類型   | 範圍      | 非空        | 備註                |
| --------------------------- | -------- | -------------- | ------ | --------- | ----------- | ------------------- |
| research_group_id           | 是       | 課題組id       | int    | /         | 是          | 遞增                |
| lab_id                      | 外部主鍵 | 實驗室id       | int    | /         | 是          |                     |
| research_group_name_zh      |          | 課題組中文     | string | (0, 500)  |             |                     |
| research_group_name_en      |          | 課題組英文     | string | (0, 500)  |             |                     |
| research_group_desc_zh      |          | 課題組中文介紹 | string | (0, 1000) |             | 支持Markdown格式    |
| research_group_desc_en      |          | 課題組英文介紹 | string | (0, 1000) |             | 支持Markdown格式    |
| mem_id                      | 外部主鍵 | 課題組組長     | int    | /         |             | 可為空              |
| enable                      |          | 數據是否有效   | int    | (0, 1)    | 是（默認1） | 0->無效;<br>1->有效 |
| created_at                  |          | 創建時間       | datetime | /       | 是          | 自動生成            |
| updated_at                  |          | 更新時間       | datetime | /       | 是          | 自動更新            |

### 3.4 成員

| key name          | 主鍵     | 含義             | 類型   | 範圍      | 非空        | 備註                                                         |
| ----------------- | -------- | ---------------- | ------ | --------- | ----------- | ------------------------------------------------------------ |
| mem_id            | 是       | 成員id           | int    | /         | 是          | 遞增                                                         |
| mem_avatar_path   |          | 成員頭像路徑     | string | (0, 500)  |             | 圖片限制5M，存儲路徑而非blob                                 |
| mem_name_zh       |          | 成員中文名       | string | (0, 500)  |             |                                                              |
| mem_name_en       |          | 成員英文名       | string | (0, 500)  |             |                                                              |
| mem_desc_zh       |          | 成員中文介紹     | text   | /         |             | 支持Markdown格式，預設內容：個人簡介、教育與工作經歷、發表論文、獲獎情況、教學工作 |
| mem_desc_en       |          | 成員英文介紹     | text   | /         |             | 支持Markdown格式                                             |
| mem_email         |          | 成員email        | string | (0, 500)  |             |                                                              |
| mem_type          |          | 成員類型         | int    | /         | 是（默認0） | 0->教師;<br>1->學生; <br>2->校友                             |
| job_type          |          | 職稱類型         | int    | /         |             | 只有選擇教師才會有職稱<br>0->教授<br>1->副教授<br>2->講師<br>3->助理研究員<br>4->博士後 |
| student_type      |          | 學生類型         | int    | /         |             | 0 -> 博士生<br>1 -> 碩士生<br>2 -> 大學生<br>                |
| student_grade     |          | 學生幾年級       | int    | /         |             |                                                              |
| destination_zh    |          | 去向中文         | string | (0, 500)  |             | 用於校友畢業去向                                             |
| destination_en    |          | 去向英文         | string | (0, 500)  |             |                                                              |
| research_group_id | 外部主鍵 | 成員所在課題組id | int    | /         | 是          |                                                              |
| lab_id            | 外部主鍵 | 成員所在實驗室   | int    | /         | 是          |                                                              |
| enable            |          | 數據是否有效     | int    | (0, 1)    | 是（默認1） | 0->無效;<br>1->有效                                          |
| created_at        |          | 創建時間         | datetime | /       | 是          | 自動生成                                                     |
| updated_at        |          | 更新時間         | datetime | /       | 是          | 自動更新                                                     |

### 3.5 論文

#### 3.5.1 論文列表

| key name          | 主鍵     | 含義               | 類型   | 範圍      | 非空        | 備註                                                         |
| ----------------- | -------- | ------------------ | ------ | --------- | ----------- | ------------------------------------------------------------ |
| paper_id          | 是       | 論文id             | int    | /         | 是          | 遞增                                                         |
| research_group_id | 外部主鍵 | 論文成員所在課題組 | int    | /         |             | 需要考慮如果此篇論文作者已畢業或是課題組被刪除               |
| lab_id            | 外部主鍵 | 論文成員所在實驗室 | int    | /         |             | 需要考慮如果此篇論文作者已畢業或是實驗室被刪除               |
| paper_date        |          | 論文發表日期       | date   | /         | 是          |                                                              |
| paper_title_zh    |          | 論文中文標題       | string | (0, 500)  |             |                                                              |
| paper_title_en    |          | 論文英文標題       | string | (0, 500)  |             |                                                              |
| paper_desc_zh     |          | 論文簡述中文       | text   | /         |             |                                                              |
| paper_desc_en     |          | 論文簡述英文       | text   | /         |             |                                                              |
| paper_type        |          | 論文類型           | int    | /         | 是（默認0） | 0->期刊論文<br>1->會議論文<br>2->學位論文<br>3->專題著作<br>4->其它 |
| paper_venue       |          | 論文在哪發表       | string | (0, 500)  |             | e,g. AAAI, ICCV, CVPR                                        |
| paper_accept      |          | 論文是否被接收     | int    | (0, 1)    | 是（默認0） | 0->未接收<br>1->已接收                                       |
| paper_file_path   |          | 論文pdf路徑        | string | (0, 500)  |             | 存儲路徑而非blob                                             |
| paper_url         |          | 論文外部連結       | string | (0, 1000) |             |                                                              |
| all_authors_zh    |          | 全部作者中文       | text   | /         |             | 包含非實驗室成員作者                                         |
| all_authors_en    |          | 全部作者英文       | text   | /         |             | 包含非實驗室成員作者                                         |
| enable            |          | 數據是否有效       | int    | (0, 1)    | 是（默認1） | 0->無效;<br>1->有效                                          |
| created_at        |          | 創建時間           | datetime | /       | 是          | 自動生成                                                     |
| updated_at        |          | 更新時間           | datetime | /       | 是          | 自動更新                                                     |

#### 3.5.2 論文作者

| key name   | 類型   | 備註                                  |
|------------|--------|---------------------------------------|
| paper_id | int  | 論文ID (外鍵, 聯合主鍵)              |
| mem_id   | int  | 成員ID (外鍵, 聯合主鍵)              |
| author_order | int  | 作者順序 (例如: 1, 2, 3...)         |
| is_corresponding | int | 是否是通訊作者 (0/1)              |



### 3.6 項目

不過多去細化項目是否結束日期，因為有些項目是需要持續疊代，所以不加此鍵位

| key name           | 主鍵 | 含義           | 類型   | 範圍      | 非空        | 備註                   |
| ------------------ | ---- | -------------- | ------ | --------- | ----------- | ---------------------- |
| project_id         | 是   | 項目id         | int    | /         | 是          | 遞增                   |
| project_url        |      | 項目url        | string | (0, 500)  |             |                        |
| project_name_zh    |      | 項目中文名     | string | (0, 500)  |             |                        |
| project_name_en    |      | 項目英文名     | string | (0, 500)  |             |                        |
| project_desc_zh    |      | 項目中文描述   | text   | /         |             |                        |
| project_desc_en    |      | 項目英文描述   | text   | /         |             |                        |
| project_date_start |      | 項目開始日期   | date   | /         |             |                        |
| is_end             |      | 項目是否已結項 | int    | /         | 是（默認0） | 0->未結項<br>1->已結項 |
| enable             |      | 數據是否有效   | int    | (0, 1)    | 是（默認1） | 0->無效;<br>1->有效    |
| created_at         |      | 創建時間       | datetime | /       | 是          | 自動生成               |
| updated_at         |      | 更新時間       | datetime | /       | 是          | 自動更新               |

### 3.7 新聞

| key name        | 主鍵 | 含義         | 類型   | 範圍      | 非空        | 備註                                        |
| --------------- | ---- | ------------ | ------ | --------- | ----------- | ------------------------------------------- |
| news_id         | 是   | 新聞id       | int    | /         | 是          | 遞增                                        |
| news_type       |      | 新聞類型     | int    | /         | 是          | 0->論文;<br>1->獎項;<br>2->報告;<br>3->其它 |
| news_title_zh   |      | 新聞標題中文 | string | (0, 500)  |             |                                             |
| news_title_en   |      | 新聞標題英文 | string | (0, 500)  |             |                                             |
| news_content_zh |      | 新聞內容中文 | text   | /         |             |                                             |
| news_content_en |      | 新聞內容英文 | text   | /         |             |                                             |
| news_date       |      | 新聞發表日期 | date   | /         |             |                                             |
| enable          |      | 數據是否有效 | int    | (0, 1)    | 是（默認1） | 0->無效;<br>1->有效                         |
| created_at      |      | 創建時間     | datetime | /       | 是          | 自動生成                                    |
| updated_at      |      | 更新時間     | datetime | /       | 是          | 自動更新                                    |

### 3.8 編輯記錄

編輯記錄是絕對不可刪的，但是因為只是簡單的實驗室網站，不需要記錄的太細

| key name     | 主鍵     | 含義         | 類型   | 範圍    | 非空 | 備註                                             |
| ------------ | -------- | ------------ | ------ | ------- | ---- | ------------------------------------------------ |
| edit_id      | 是       | 編輯資訊id   | int    | /       | 是   | 遞增                                             |
| admin_id     | 外部主鍵 | 編輯的管理員 | int    | /       | 是   |                                                  |
| edit_type    |          | 操作類型     | string | (0, 50) | 是   | CREATE,UPDATE, DELETE                            |
| edit_module  |          | 編輯模組     | int    | /       | 是   | 0->實驗室<br>1->課題組<br>2->成員<br>3->論文<br> |
| edit_content |          | 編輯內容     | JSON   |         |      | 將post請求內容塞入                               |
| edit_date    |          | 編輯日期     | date   | /       | 是   |                                                  |

## 四、後端介面

> [!TIP]
> 
> 本章包含：通用約定、認證鑒權、統一響應、每個資源的 RESTful API 規範（URL / 方法 / 入參 / 出參 / 範例）、輸入校驗、文件上傳策略、批次導入/導出、審計/編輯記錄、事務約束、錯誤碼、運維與安全建議。實現參考棧：Flask + SQLAlchemy + JWT，但介面規範與其它後端框架相容。


### 4.0 總則（跨介面約定）

#### 4.0.1 鑒權與會話

* 推薦方案：**JWT（JSON Web Token）**。登錄成功後返回 `{ "access_token": "Bearer <token>", "expires_in": 3600 }`。
* 用戶端儲存建議：SPA 可存 `localStorage`（注意 XSS 風險）或更安全地使用 HttpOnly Cookie + CSRF token。
* 所有受保護介面須在 HTTP Header 中攜帶 `Authorization: Bearer <token>`。
* 後端需實現 middleware/裝飾器解析 token、驗證過期並注入 `current_admin`（含 `admin_id`, `is_super` 等）。
* 可選：使用 RBAC（角色/權限）實現精細權限控制。

#### 4.0.2 統一響應格式

所有介面統一響應結構：

```json
{
  "code": 0,          // 0 表示成功，非 0 為錯誤碼
  "message": "OK",
  "data": { ... }     // 成功時返回的數據；錯誤時可為空或返回錯誤詳情
}
```

#### 4.0.3 分頁、排序、過濾

* 分頁參數：`page`（>=1），`per_page`（默認 10，上限 100）。
* 排序參數：`sort_by`（欄位名），`order`（`asc|desc`）。
* 常用過濾參數：`q`（全文/標題關鍵字），`start_date`/`end_date`（時間區間），其他資源特定欄位。

#### 4.0.4 軟刪除

* 所有可刪除資源使用 `enable` 欄位（1=有效，0=已刪除）。刪除行為為將 `enable` 置為 0。
* 列表默認 `WHERE enable = 1`；管理端可傳 `show_all=true` 查看已刪除項。

#### 4.0.5 文件儲存

* 圖片上限建議：**5 MB**；論文/pdf 建議上限：**50 MB**（可根據磁碟/需求調整）。
* 儲存路徑策略：`/media/{resource}/{YYYYMM}/{uuid}.{ext}`。
* 只在 DB 中保存文件路徑/元數據，不以 BLOB 存入 DB。
* 僅允許白名單後綴與 MIME 類型（圖片：jpg/jpeg/png/gif；pdf：application/pdf）。

#### 4.0.6 輸入校驗與 XSS

* 後端嚴格校驗所有輸入（類型、長度、正則、枚舉值）。
* 對渲染 HTML/markdown 的內容做 XSS 過濾（如使用 bleach、DOMPurify 等）。
* 常見欄位範例校驗：

  * `admin_name`: `^[A-Za-z0-9_\-]{3,50}$`
  * `email`: 標準 email 校驗
  * 日期格式：`YYYY-MM-DD`

#### 4.0.7 事務、約束與審計

* 對涉及多表寫入/修改的操作使用事務保證一致性。
* 刪除資源前做約束檢查（例如：刪除課題組前需無有效成員）。
* 每次 CRUD 操作應寫入審計表 `edit_records`（記錄 admin\_id、模組、變更內容、時間）。

#### 4.0.8 錯誤碼規範（範例）

* `0` 成功
* `1000` 未認證或 token 無效
* `1001` 權限不足
* `2000` 參數校驗錯誤
* `3000` 資源未找到
* `4000` 操作衝突（例如：刪除被阻止）
* `5000` 伺服器內部錯誤

---

### 4.1 認證與管理員（Auth & Admin）

#### 4.1.1 登錄

* **URL**：`POST /api/admin/login`
* **權限**：公開
* **請求（JSON）**

  ```json
  {
    "admin_name": "string",
    "admin_pass": "string"
  }
  ```
* **成功響應**

  ```json
  {
    "code": 0,
    "message": "OK",
    "data": {
      "access_token": "Bearer xxx",
      "expires_in": 3600,
      "admin": { "admin_id": 1, "admin_name": "root", "is_super": 1 }
    }
  }
  ```
* **錯誤**：`code=1000`（使用者名稱或密碼錯誤）

#### 4.1.2 修改密碼

* **URL**：`POST /api/admin/change-password`
* **權限**：登錄
* **請求**

  ```json
  { "old_password": "xxx", "new_password": "yyy" }
  ```
* **規則**：`new_password` >= 8 字元，建議包含字母與數字。後端保存使用 bcrypt（或更強）+ salt。

#### 4.1.3 管理員管理（僅超級管理員）

* 列表：`GET /api/admins`（分頁/過濾）
* 創建：`POST /api/admins`（`admin_name`, `admin_pass`, `is_super`）
* 修改：`PUT /api/admins/{admin_id}`
* 刪除（軟刪除）：`DELETE /api/admins/{admin_id}`
* 僅 `is_super=1` 能創建/刪除管理員。

---

### 4.2 實驗室資訊（Lab）

#### 4.2.1 獲取實驗室資訊

* **URL**：`GET /api/lab`
* **權限**：公開
* **響應範例**

  ```json
  {
    "code": 0,
    "data": {
      "lab_id": 1,
      "lab_logo_path": "/media/lab/202508/uuid.png",
      "lab_zh": "實驗室中文名",
      "lab_en": "Lab English",
      "lab_desc_zh": "介紹",
      "lab_desc_en": "desc",
      "lab_address_zh": "...",
      "lab_email": "...",
      "lab_phone": "...",
      "enable": 1
    }
  }
  ```

#### 4.2.2 更新實驗室資訊

* **URL**：`PUT /api/lab` 或 `POST /api/lab`
* **權限**：管理員
* **Content-Type**：`multipart/form-data`（支持 `lab_logo` 文件）
* **入參（multipart）**

  * 文本：`lab_zh`, `lab_en`, `lab_desc_zh`, `lab_desc_en`, `lab_address_zh`, `lab_email`, `lab_phone`
  * 文件：`lab_logo`（image，max 5MB）
* **操作**：上傳先存臨時，再校驗、移動到正式路徑；記錄 `edit_record`。

---

### 4.3 課題組（Research Group）

#### 4.3.1 列表

* **URL**：`GET /api/research-groups`
* **權限**：公開
* **Query**：`page`, `per_page`, `q`（名稱模糊）, `lab_id`, `show_all`
* **響應**：分頁 `total/page/per_page/items`。

#### 4.3.2 創建

* **URL**：`POST /api/research-groups`
* **權限**：管理員
* **請求**

  ```json
  {
    "research_group_name_zh": "名稱",
    "research_group_name_en": "Name",
    "research_group_desc_zh": "...",
    "research_group_desc_en": "...",
    "mem_id": 2   // 可選：組長 mem_id
  }
  ```
* **校驗**：若 `mem_id` 填寫，必須存在且 enable=1。

#### 4.3.3 修改

* **URL**：`PUT /api/research-groups/{id}`
* **權限**：管理員
* **操作**：修改欄位並寫入 `edit_record`。

#### 4.3.4 刪除（軟刪除）

* **URL**：`DELETE /api/research-groups/{id}`
* **權限**：管理員
* **規則**：刪除前必須檢查組內是否存在 enable=1 的成員；若有，返回 `code=4000` 與提示資訊（“該課題組下仍有有效成員，無法刪除”）。

---

### 4.4 成員（Member）

#### 4.4.1 列表（前端展示）

* **URL**：`GET /api/members`
* **權限**：公開
* **Query**：`type`（教師/學生/校友）、`research_group_id`、`q`（姓名/職稱）、`page`, `per_page`, `sort_by`

#### 4.4.2 成員詳情

* **URL**：`GET /api/members/{mem_id}`
* **權限**：公開
* **返回**：完整資訊（頭像 URL、簡介、教育/工作經歷、論文列表引用等）。

#### 4.4.3 創建（管理員）

* **URL**：`POST /api/members`
* **權限**：管理員
* **Content-Type**：`multipart/form-data`
* **入參（範例）**

  * 文本欄位：`mem_name_zh`, `mem_name_en`, `mem_desc_zh`, `mem_email`, `mem_type`（0 教師、1 學生、2 校友）, `job_type`, `student_grade`, `research_group_id`, `lab_id` 等。
  * 文件：`mem_avatar`（image）
* **校驗**

  * `mem_email` 合法；`mem_type` 枚舉限制；若 `job_type` 填寫必須與 `mem_type` 邏輯一致。
* **事務**：創建成員同時寫入與論文/項目的關聯必須在事務中處理。
* **審計**：記錄 `edit_record`。

#### 4.4.4 修改

* **URL**：`PUT /api/members/{mem_id}`
* **權限**：管理員
* **注意**：更改 `research_group_id` 要保證目標組存在且 enable=1。

#### 4.4.5 刪除（軟刪除）

* **URL**：`DELETE /api/members/{mem_id}`
* **權限**：管理員
* **注意**：刪除後保留論文作者歷史（避免破壞論文記錄），可把成員標記為已離隊並在 `paper_author` 中保留 `mem_id` 或用 `external_author` 欄位記錄歷史。

---

### 4.5 論文（Paper）

#### 4.5.1 列表

* **URL**：`GET /api/papers`
* **權限**：公開
* **Query**：`q`（標題/作者/venue）、`paper_type`、`paper_accept`、`start_date`、`end_date`、`page`、`per_page`、`sort_by=paper_date`。

#### 4.5.2 論文詳情

* **URL**：`GET /api/papers/{paper_id}`
* **權限**：公開
* **返回欄位**：論文基本資訊、作者列表（每位作者包含 `mem_id`、`author_order`、`is_corresponding`）、`paper_url`、`paper_file_url`（若有，建議短期簽名 URL 或通過後端流式下載）。

#### 4.5.3 上傳 / 新增（含文件）

* **URL**：`POST /api/papers`
* **權限**：管理員
* **Content-Type**：`multipart/form-data`
* **入參**

  * 文本：`paper_date`（YYYY-MM-DD）, `paper_title_zh`, `paper_title_en`, `paper_desc`, `paper_type`, `paper_venue`, `paper_accept`（0/1）, `paper_url`
  * 文件：`paper_file`（pdf，max 50MB）
  * 作者：`authors`（JSON 字串數組）範例：`[{"mem_id":1,"author_order":1,"is_corresponding":1}, ...]`
* **校驗**

  * `paper_date` 合法，`authors` 中 `mem_id` 必須存在；作者順序不得重複。
* **事務**：寫 `papers` 與 `paper_author` 聯合表在同一事務中。
* **響應**：創建的 `paper_id` 與作者資訊。

#### 4.5.4 修改

* **URL**：`PUT /api/papers/{paper_id}`
* **權限**：管理員
* **注意**：更新文件要處理舊文件（刪除或版本化）；修改作者列表應差分並記錄修改歷史。

#### 4.5.5 刪除（軟刪除）

* **URL**：`DELETE /api/papers/{paper_id}`

---

### 4.6 新聞（News）

#### 4.6.1 列表（首頁用）

* **URL**：`GET /api/news`
* **權限**：公開
* **Query**：`page`, `per_page`（首頁默認 `per_page=5`）, `q`, `news_type`
* **前端規則**：首頁拉取最新 5 條（`sort_by=news_date, order=desc`）

#### 4.6.2 創建 / 修改 / 刪除（管理員）

* `POST /api/news`、`PUT /api/news/{news_id}`、`DELETE /api/news/{news_id}`
* 欄位：`news_type`, `news_content_zh`, `news_content_en`, `news_date`, `thumbnail_path`（可選）

---

### 4.7 項目（Project）

#### 4.7.1 列表 / 詳情 / 創建 / 修改 / 刪除

* **URL**：`GET /api/projects`, `GET /api/projects/{project_id}`, `POST /api/projects`, `PUT /api/projects/{project_id}`, `DELETE /api/projects/{project_id}`
* **欄位**：`project_name_zh/en`, `project_desc_zh/en`, `project_date_start`, `project_date_end`, `is_end`, `project_url`
* **成員關係**：`project_member`（`project_id`, `mem_id`, `role`）

---

### 4.8 編輯記錄（Audit / Edit Record）

#### 4.8.1 列表

* **URL**：`GET /api/edit-records`
* **權限**：管理員（建議僅超級管理員可見完整內容）
* **Query**：`admin_id`, `edit_module`, `start_date`, `end_date`, `page`, `per_page`
* **記錄欄位**：`edit_id`, `admin_id`, `edit_type`（create/update/delete）、`edit_module`（members/papers/...），`edit_content`（建議存差分或請求 body），`edit_date`

#### 4.8.2 實現建議

* `edit_content` 建議存最小差異（patch）或原始請求 body；若內容過大，限制長度並記錄摘要與儲存位置。

---

### 4.9 文件上傳與媒體服務（Media）

#### 4.9.1 通用上傳

* **URL**：`POST /api/media/upload`
* **權限**：管理員或公開但受限制
* **Content-Type**：`multipart/form-data`
* **入參**：`file`，`type`（lab\_logo|member\_avatar|paper|other）
* **返回**

  ```json
  { "code":0, "data": { "path": "/media/lab/202508/uuid.png", "url": "/api/media/serve/uuid" } }
  ```
* **校驗**

  * 文件後綴與 MIME 雙重校驗；大小限制；病毒/惡意文件掃描（可選）。

#### 4.9.2 媒體下載 / 訪問

* **URL**：`GET /api/media/serve/{file_id}`
* **權限**：公開或受限（敏感文件可要求管理員 token）
* **實現要點**：支持 HTTP Range；推薦生成短期簽名 URL（用於 CDN 或前端直接下載），避免暴露文件系統路徑。

#### 4.9.3 縮圖與元數據

* 對圖片生成縮圖（多尺寸），並在 DB 中記錄原始尺寸、縮圖路徑。

---

### 4.10 批次導入 / 導出（Bulk）

#### 4.10.1 批次導入（CSV/Excel）

* **URL**：`POST /api/bulk/import/{resource}`（`resource`：members|papers|projects）
* **權限**：管理員
* **Content-Type**：`multipart/form-data`
* **入參**：`file`（CSV/Excel），`mode`（`insert|upsert|dry_run`）
* **行為**

  * `dry_run=true`：僅校驗返回錯誤行
  * `mode=upsert`：需指定唯一鍵（如 `mem_email` 或 `paper_title+paper_date`）
* **長任務處理**

  * 建議非同步（隊列/任務 id），返回 `task_id` 供前端查詢進度；若不實現非同步，需保證事務回滾與超時保護。
* **響應**：分行級錯誤報告，成功/失敗統計。

#### 4.10.2 導出

* **URL**：`GET /api/bulk/export/{resource}`
* **權限**：管理員
* **Query**：支持過濾欄位，返回文件（CSV/Excel）或短期簽名下載 URL。

---

### 4.11 權限模型建議（RBAC）

* 推薦引入角色表 `roles`、權限表 `permissions`、角色-權限關聯與管理員-角色關聯，便於未來擴展。
* 對敏感操作（如管理員管理、刪除資源）做額外審計與二次確認（2FA 可選）。

---

### 4.12 常見錯誤響應與 HTTP 狀態碼範例

* **未認證**

  ```http
  HTTP/1.1 401 Unauthorized
  {
    "code": 1000,
    "message": "未認證或 token 無效"
  }
  ```
* **權限不足**

  ```http
  HTTP/1.1 403 Forbidden
  {
    "code": 1001,
    "message": "權限不足"
  }
  ```
* **參數錯誤**

  ```http
  HTTP/1.1 400 Bad Request
  {
    "code": 2000,
    "message": "參數錯誤：mem_email 格式不正確"
  }
  ```
* **資源不存在**

  ```http
  HTTP/1.1 404 Not Found
  {
    "code": 3000,
    "message": "資源未找到"
  }
  ```
* **操作衝突**

  ```http
  HTTP/1.1 409 Conflict
  {
    "code": 4000,
    "message": "該課題組下仍有有效成員，無法刪除。"
  }
  ```
* **伺服器內部錯誤**

  ```http
  HTTP/1.1 500 Internal Server Error
  {
    "code": 5000,
    "message": "伺服器內部錯誤"
  }
  ```

---

### 4.13 後端實現片段（參考偽碼）

> 下列偽碼僅作實現參考，非完整代碼。

**JWT 驗證裝飾器（範例）**

```python
from functools import wraps
import jwt
from flask import request, jsonify, g

SECRET = "your-secret-key"

def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"code":1000,"message":"缺少 token"}), 401
        token = auth.split(" ",1)[1]
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"code":1000,"message":"token 已過期"}), 401
        except Exception:
            return jsonify({"code":1000,"message":"token 無效"}), 401
        g.current_admin = {"admin_id": payload["admin_id"], "is_super": payload.get("is_super",0)}
        return func(*args, **kwargs)
    return wrapper
```

**創建課題組範例路由（偽碼）**

```python
@app.route("/api/research-groups", methods=["POST"])
@jwt_required
def create_research_group():
    data = request.get_json()
    if not data.get("research_group_name_zh"):
        return jsonify({"code":2000,"message":"名稱不能為空"}), 400
    # 檢查 mem_id（如有）存在且 enable=1
    # 在事務中插入 research_group，寫 edit_record
    return jsonify({"code":0,"data":new_group}), 201
```

---

### 4.14 驗證規則匯總（欄位限制）

* 字串長度上限按需求表設置（常見：標題 200，描述 2000）。
* 日期：`YYYY-MM-DD`，使用庫校驗（`dateutil` / `datetime.strptime`）。
* 枚舉欄位校驗（如 `mem_type` ∈ {0,1,2}）。
* 文件：

  * 圖片 MIME：`image/jpeg`, `image/png`, `image/gif`；大小 ≤ 5MB。
  * PDF MIME：`application/pdf`；大小 ≤ 50MB。

---

### 4.15 運維與安全（介面相關建議）

* 強制 HTTPS（生產環境）。
* 介面訪問日誌（IP、時間、user-agent、admin\_id 若存在）。
* 速率限制（登錄、上傳、批次導入等）：例如登錄每分鐘最多 10 次。
* 備份策略：資料庫每日備份，media 定期同步/備份。
* 上傳文件安全：MIME 與後綴雙檢、殺毒/沙盒掃描（如有需要）。
* 敏感資訊不在 API 返回中洩露（不返回密碼、金鑰等）。

---

### 4.16 交付與後續建議

1. **生成 OpenAPI / Swagger 文件**：把本章轉為 OpenAPI v3 描述，可用於前後端契約與自動化測試。
2. **生成骨架代碼**：可基於 Flask + SQLAlchemy 自動生成模型與 CRUD 路由（含 JWT 中間件、文件處理、審計中間件）。
3. **Postman / curl 範例集**：提供便於前端除錯的 collection。
4. **非同步任務**：對耗時批次導入或文件處理建議用任務隊列（Celery / RQ），並提供任務狀態查詢介面 `GET /api/tasks/{task_id}`。

## 五、頁面

- 一定要注意怎麼去利用token去判斷是否是管理員，對應去載入頁面，前端取token、後端加校驗
- 如果當前沒有數據要有對應的組件展示

### 5.1 用戶端

#### 5.1.1 首頁

**頂部NAV導覽**

導覽列需要置頂：

- 左側：實驗室Logo與名稱
- 右側：論文、項目、成員（如果是一整個研究所，就需要展示下拉框）、新聞
- 最右側：主題切換（light、Night）、國際化默認中文（中英）

**中間介紹篇幅**

- 簡略說明我們實驗室的理念和風格，展示課題組卡片列表


**新聞欄位**

- 只展示最新的五條新聞
- 新聞下有點擊"查看更多"，點擊可以跳轉新聞頁

**底部**

- 有聯繫我們的TAG
- 實驗室地址
- 實驗室email

#### 5.1.2 論文

- 有展示論文列表
- 上方有搜索框，可以條件搜索
- 論文列表展示論文資訊
- 點擊論文作者可跳轉到成員詳情頁面
- 最新的論文在上面
- 分頁管理

#### 5.1.3 成員

- 分類（教師、學生、校友）展示所有成員（頭像、姓名、職稱）
- 如果是校友就展示去向（如果是離開的教師也適用）
- 點擊成員能跳轉到成員詳情頁面

#### 5.1.4 新聞

為了避免後端存過多新聞圖片與資訊壟餘等，這裡推薦只需要簡短的祝賀內容等描述，不做詳情頁

- 展示新聞列表
- 上方有搜索框，可以條件搜索
- 新聞列表展示新聞資訊
- 新聞列表最新的在上面
- 分頁管理

#### 5.1.5 成員詳情頁面

展示成員頭像、email、簡介等


#### 5.1.6 項目

為了避免後端存過多項目與資訊壟餘等，不做詳情頁

- 展示項目列表
- 上方有搜索框，可以條件搜索
- 項目列表展示項目資訊
- 項目啟動日期最新的在上面
- 分頁管理

### 5.2 管理端

注意有些內容編輯要使用 md-editor-v3 組件，前端顯示markdown

- 如果是超級管理員：有管理員增減頁面、改密碼界面
- 首頁設置
- 實驗室管理
- 課題組管理
- 論文管理
- 成員管理
- 新聞管理
- 項目管理
