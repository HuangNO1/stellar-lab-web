# 實驗室網頁框架 API 文件

## 目錄
- [概述](#概述)
- [認證](#認證)
- [通用響應格式](#通用響應格式)
- [錯誤碼說明](#錯誤碼說明)
- [API 介面](#api-介面)
  - [認證管理](#認證管理)
  - [管理員管理](#管理員管理)
  - [實驗室管理](#實驗室管理)
  - [課題組管理](#課題組管理)
  - [成員管理](#成員管理)
  - [論文管理](#論文管理)
  - [新聞管理](#新聞管理)
  - [項目管理](#項目管理)
  - [媒體檔案管理](#媒體檔案管理)
  - [編輯記錄管理](#編輯記錄管理)
  - [系統介面](#系統介面)

## 概述

實驗室網頁框架後端 API，基於 Flask 框架開發，提供實驗室資訊管理的完整功能。

- **基礎URL**: `http://localhost:8000/api`
- **內容類型**: `application/json` (除文件上傳外)
- **字元編碼**: UTF-8

## 認證

需要認證的介面使用 JWT (JSON Web Token) 進行身份驗證。

### 請求頭設置
```
Authorization: Bearer <token>
Content-Type: application/json
```

### 權限級別
- **普通管理員**: `@admin_required`
- **超級管理員**: `@super_admin_required`

## 通用響應格式

### 成功響應
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    // 實際數據
  }
}
```

### 錯誤響應
```json
{
  "code": 2000,
  "message": "參數錯誤",
  "data": null
}
```

### 分頁響應格式
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      // 數據列表
    ],
    "total": 100,
    "page": 1,
    "per_page": 10,
    "pages": 10,
    "has_prev": false,
    "has_next": true
  }
}
```

## 錯誤碼說明

| 錯誤碼 | 說明 | HTTP狀態碼 |
|-------|------|-----------|
| 0 | 成功 | 200 |
| 1000 | 認證錯誤（使用者名稱密碼錯誤） | 401 |
| 1001 | 權限不足 | 403 |
| 2000 | 參數校驗錯誤 | 400 |
| 3000 | 資源不存在 | 404 |
| 4000 | 操作衝突 | 409 |
| 5000 | 伺服器內部錯誤 | 500 |

## API 介面

## 認證管理

### 管理員登錄
```
POST /api/admin/login
```

**請求頭**
```
Content-Type: application/json
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| admin_name | string | ✓ | 管理員使用者名稱 | admin |
| admin_pass | string | ✓ | 管理員密碼 | admin123 |

**請求範例**
```json
{
  "admin_name": "admin",
  "admin_pass": "admin123"
}
```

**響應參數**
| 參數 | 類型 | 含義 | 範例值 |
|------|------|------|--------|
| access_token | string | JWT令牌，格式：Bearer {token} | Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9... |
| expires_in | integer | 令牌有效期（秒） | 86400 |
| admin | object | 管理員資訊對象 | 見下方範例 |

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "access_token": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_in": 86400,
    "admin": {
      "admin_id": 1,
      "admin_name": "admin",
      "is_super": 1,
      "enable": 1,
      "created_at": "2024-01-01T00:00:00"
    }
  }
}
```

### 管理員登出
```
POST /api/admin/logout
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**請求參數**
無

**響應範例**
```json
{
  "code": 0,
  "message": "登出成功"
}
```

### 修改密碼
```
POST /api/admin/change-password
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| old_password | string | ✓ | 當前密碼 | oldpass123 |
| new_password | string | ✓ | 新密碼（至少8位） | newpass123 |

**請求範例**
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass123"
}
```

**響應範例**
```json
{
  "code": 0,
  "message": "密碼修改成功"
}
```

### 獲取個人資訊
```
GET /api/admin/profile
```

**請求頭**
```
Authorization: Bearer <token>
```

**查詢參數**
無

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "admin_id": 1,
    "admin_name": "admin",
    "is_super": 1,
    "enable": 1,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### 更新個人資訊
```
PUT /api/admin/profile
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**請求參數**
根據Admin模型的可更新欄位而定。

**響應範例**
```json
{
  "code": 0,
  "message": "個人資訊更新成功",
  "data": {
    "admin_id": 1,
    "admin_name": "admin",
    "is_super": 1,
    "enable": 1,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

## 管理員管理

### 獲取管理員列表
```
GET /api/admins
```

**請求頭**
```
Authorization: Bearer <token> (需要超級管理員權限)
```

**查詢參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| q | string | - | 搜索關鍵字（使用者名稱） | admin |
| show_all | boolean | - | 是否顯示已刪除（默認false） | true |
| page | integer | - | 頁碼（默認1） | 1 |
| per_page | integer | - | 每頁數量（默認10，最大100） | 10 |

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      {
        "admin_id": 1,
        "admin_name": "admin",
        "is_super": 1,
        "enable": 1,
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10,
    "pages": 1,
    "has_prev": false,
    "has_next": false
  }
}
```

### 創建管理員
```
POST /api/admins
```

**請求頭**
```
Authorization: Bearer <token> (需要超級管理員權限)
Content-Type: application/json
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| admin_name | string | ✓ | 管理員使用者名稱 | newadmin |
| admin_pass | string | ✓ | 管理員密碼 | password123 |
| is_super | integer | - | 是否為超級管理員（0/1，默認0） | 0 |

**請求範例**
```json
{
  "admin_name": "newadmin",
  "admin_pass": "password123",
  "is_super": 0
}
```

### 更新管理員
```
PUT /api/admins/{admin_id}
```

**請求頭**
```
Authorization: Bearer <token> (需要超級管理員權限)
Content-Type: application/json
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| admin_id | integer | ✓ | 要更新的管理員ID | 2 |

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| admin_name | string | - | 管理員使用者名稱 | newname |
| is_super | integer | - | 是否為超級管理員（0/1） | 1 |
| enable | integer | - | 是否啟用（0/1） | 1 |

### 刪除管理員
```
DELETE /api/admins/{admin_id}
```

**請求頭**
```
Authorization: Bearer <token> (需要超級管理員權限)
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| admin_id | integer | ✓ | 要刪除的管理員ID | 2 |

## 實驗室管理

### 獲取實驗室資訊
```
GET /api/lab
```

**請求頭**
無需認證

**查詢參數**
無

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "lab_id": 1,
    "lab_logo_path": "/media/lab_logo/logo.png",
    "lab_zh": "智慧計算實驗室",
    "lab_en": "Intelligent Computing Laboratory",
    "lab_desc_zh": "本實驗室專注於人工智慧、機器學習和計算機視覺領域的研究",
    "lab_desc_en": "Our laboratory focuses on research in artificial intelligence, machine learning, and computer vision",
    "lab_address_zh": "北京市海淀區清華大學FIT樓",
    "lab_address_en": "FIT Building, Tsinghua University, Beijing",
    "lab_email": "contact@lab.tsinghua.edu.cn",
    "lab_phone": "+86-10-62785678",
    "enable": 1
  }
}
```

### 更新實驗室資訊
```
PUT /api/lab
POST /api/lab
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| lab_zh | string | - | 實驗室中文名稱 | 智慧計算實驗室 |
| lab_en | string | - | 實驗室英文名稱 | Intelligent Computing Laboratory |
| lab_desc_zh | string | - | 實驗室中文描述 | 專注於AI研究 |
| lab_desc_en | string | - | 實驗室英文描述 | Focus on AI research |
| lab_address_zh | string | - | 實驗室中文地址 | 北京市海淀區 |
| lab_address_en | string | - | 實驗室英文地址 | Beijing, Haidian |
| lab_email | string | - | 實驗室聯繫信箱 | contact@lab.edu.cn |
| lab_phone | string | - | 實驗室聯絡電話 | +86-10-12345678 |
| lab_logo | file | - | 實驗室Logo文件 | logo.png |

### 刪除實驗室
```
DELETE /api/lab
```

**請求頭**
```
Authorization: Bearer <token>
```

**請求參數**
無

**注意**: 只有當實驗室下沒有有效課題組和成員時才能刪除

## 課題組管理

### 獲取課題組列表
```
GET /api/research-groups
```

**請求頭**
無需認證

**查詢參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| q | string | - | 搜索關鍵字 | 計算機視覺 |
| lab_id | integer | - | 實驗室ID篩選 | 1 |
| show_all | boolean | - | 是否顯示已刪除 | false |
| page | integer | - | 頁碼（默認1） | 1 |
| per_page | integer | - | 每頁數量（默認10） | 10 |

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      {
        "research_group_id": 1,
        "lab_id": 1,
        "research_group_name_zh": "人工智慧研究組",
        "research_group_name_en": "Artificial Intelligence Research Group",
        "research_group_desc_zh": "專注於機器學習和深度學習技術研究",
        "research_group_desc_en": "Focus on machine learning and deep learning research",
        "mem_id": 1,
        "enable": 1,
        "leader": {
          "mem_id": 1,
          "mem_name_zh": "李教授",
          "mem_name_en": "Prof. Li"
        }
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10,
    "pages": 1,
    "has_prev": false,
    "has_next": false
  }
}
```

### 獲取課題組詳情
```
GET /api/research-groups/{group_id}
```

**請求頭**
無需認證

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| group_id | integer | ✓ | 課題組ID | 1 |

### 創建課題組
```
POST /api/research-groups
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| research_group_name_zh | string | ✓ | 課題組中文名稱 | 人工智慧研究組 |
| research_group_name_en | string | - | 課題組英文名稱 | AI Research Group |
| research_group_desc_zh | string | - | 課題組中文描述 | 專注於機器學習研究 |
| research_group_desc_en | string | - | 課題組英文描述 | Focus on ML research |
| mem_id | integer | - | 組長成員ID | 1 |

**請求範例**
```json
{
  "research_group_name_zh": "人工智慧研究組",
  "research_group_name_en": "Artificial Intelligence Research Group",
  "research_group_desc_zh": "專注於機器學習和深度學習技術研究",
  "research_group_desc_en": "Focus on machine learning and deep learning research",
  "mem_id": 1
}
```

### 更新課題組
```
PUT /api/research-groups/{group_id}
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| group_id | integer | ✓ | 課題組ID | 1 |

**請求參數**: 與創建課題組相同，但所有欄位均為可選

### 刪除課題組
```
DELETE /api/research-groups/{group_id}
```

**請求頭**
```
Authorization: Bearer <token>
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| group_id | integer | ✓ | 課題組ID | 1 |

**注意**: 只有當課題組下沒有有效成員時才能刪除

## 成員管理

### 獲取成員列表
```
GET /api/members
```

**請求頭**
無需認證

**查詢參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| q | string | - | 搜索關鍵字（姓名、信箱） | 張教授 |
| type | integer | - | 成員類型（0=教師, 1=學生, 2=其他） | 0 |
| research_group_id | integer | - | 課題組ID篩選 | 1 |
| lab_id | integer | - | 實驗室ID篩選 | 1 |
| show_all | boolean | - | 是否顯示已刪除 | false |
| sort_by | string | - | 排序欄位（name/type/created_at） | name |
| order | string | - | 排序順序（asc/desc） | asc |
| page | integer | - | 頁碼 | 1 |
| per_page | integer | - | 每頁數量 | 10 |

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      {
        "mem_id": 1,
        "mem_avatar_path": "/media/member_avatar/avatar_001.jpg",
        "mem_name_zh": "李教授",
        "mem_name_en": "Prof. Li",
        "mem_desc_zh": "專注於機器學習領域研究",
        "mem_desc_en": "Focus on machine learning research",
        "mem_email": "li@lab.edu.cn",
        "mem_type": 0,
        "job_type": 0,
        "student_type": null,
        "student_grade": null,
        "destination_zh": "清華大學",
        "destination_en": "Tsinghua University",
        "research_group_id": 1,
        "lab_id": 1,
        "enable": 1,
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10,
    "pages": 1,
    "has_prev": false,
    "has_next": false
  }
}
```

### 獲取成員詳情
```
GET /api/members/{mem_id}
```

**請求頭**
無需認證

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| mem_id | integer | ✓ | 成員ID | 1 |

### 創建成員
```
POST /api/members
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| mem_name_zh | string | ✓ | 成員中文姓名 | 李教授 |
| mem_name_en | string | ✓ | 成員英文姓名 | Prof. Li |
| mem_email | string | ✓ | 電子信箱 | li@lab.edu.cn |
| mem_type | integer | ✓ | 成員類型（0=教師, 1=學生, 2=其他） | 0 |
| job_type | integer | - | 職務類型（教師：0=教授, 1=副教授, 2=講師, 3=助理教授, 4=其他） | 0 |
| student_type | integer | - | 學生類型（學生：0=博士, 1=碩士, 2=本科） | 0 |
| student_grade | integer | - | 學生年級 | 1 |
| research_group_id | integer | ✓ | 所屬課題組ID | 1 |
| mem_desc_zh | string | - | 成員中文描述 | 專注於機器學習研究 |
| mem_desc_en | string | - | 成員英文描述 | Focus on ML research |
| destination_zh | string | - | 去向中文 | 清華大學 |
| destination_en | string | - | 去向英文 | Tsinghua University |
| mem_avatar | file | - | 頭像文件 | avatar.jpg |

### 更新成員
```
PUT /api/members/{mem_id}
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| mem_id | integer | ✓ | 成員ID | 1 |

**請求參數**: 與創建成員相同，但所有欄位均為可選

### 刪除成員
```
DELETE /api/members/{mem_id}
```

**請求頭**
```
Authorization: Bearer <token>
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| mem_id | integer | ✓ | 成員ID | 1 |

**注意**: 成員是課題組組長或有關聯論文時無法刪除

### 批次刪除成員
```
DELETE /api/members/batch
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| member_ids | array | ✓ | 要刪除的成員ID數組 | [1, 2, 3] |

**請求範例**
```json
{
  "member_ids": [1, 2, 3]
}
```

### 批次更新成員
```
PUT /api/members/batch
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| member_ids | array | ✓ | 要更新的成員ID數組 | [1, 2, 3] |
| updates | object | ✓ | 要更新的欄位對象 | 見範例 |

**請求範例**
```json
{
  "member_ids": [1, 2, 3],
  "updates": {
    "enable": 1,
    "mem_type": 0,
    "research_group_id": 1
  }
}
```

## 論文管理

### 獲取論文列表
```
GET /api/papers
```

**請求頭**
無需認證

**查詢參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| q | string | - | 搜索關鍵字（標題、期刊） | 深度學習 |
| paper_type | integer | - | 論文類型（0=會議, 1=期刊, 2=專利, 3=書籍, 4=其他） | 1 |
| paper_accept | integer | - | 接收狀態（0=投稿中, 1=已接收） | 1 |
| start_date | string | - | 開始日期（YYYY-MM-DD） | 2024-01-01 |
| end_date | string | - | 結束日期（YYYY-MM-DD） | 2024-12-31 |
| show_all | boolean | - | 是否顯示已刪除 | false |
| sort_by | string | - | 排序欄位（title/venue/type/paper_date） | paper_date |
| order | string | - | 排序順序（asc/desc） | desc |
| page | integer | - | 頁碼 | 1 |
| per_page | integer | - | 每頁數量 | 10 |

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      {
        "paper_id": 1,
        "research_group_id": 1,
        "lab_id": 1,
        "paper_date": "2024-06-15",
        "paper_title_zh": "基於深度學習的圖像識別研究",
        "paper_title_en": "Image Recognition Based on Deep Learning",
        "paper_desc_zh": "本文提出了一種新的深度學習方法",
        "paper_desc_en": "This paper proposes a novel deep learning approach",
        "paper_type": 1,
        "paper_venue": "CVPR 2024",
        "paper_accept": 1,
        "paper_file_path": "/media/paper/paper_001.pdf",
        "paper_url": "https://example.com/paper",
        "enable": 1,
        "authors": [
          {
            "paper_id": 1,
            "mem_id": 1,
            "author_order": 1,
            "is_corresponding": 1,
            "member": {
              "mem_id": 1,
              "mem_name_zh": "李教授",
              "mem_name_en": "Prof. Li"
            }
          }
        ]
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10,
    "pages": 1,
    "has_prev": false,
    "has_next": false
  }
}
```

### 獲取論文詳情
```
GET /api/papers/{paper_id}
```

**請求頭**
無需認證

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| paper_id | integer | ✓ | 論文ID | 1 |

### 創建論文
```
POST /api/papers
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| paper_title_zh | string | ✓ | 論文中文標題 | 基於深度學習的圖像識別 |
| paper_title_en | string | - | 論文英文標題 | Image Recognition with Deep Learning |
| paper_desc_zh | string | - | 論文中文描述 | 本文提出一種新方法 |
| paper_desc_en | string | - | 論文英文描述 | This paper proposes a new method |
| paper_venue | string | - | 發表期刊或會議 | CVPR 2024 |
| paper_type | integer | ✓ | 論文類型 | 1 |
| paper_accept | integer | ✓ | 接收狀態 | 1 |
| paper_date | string | ✓ | 發表日期（YYYY-MM-DD） | 2024-06-15 |
| paper_url | string | - | 論文URL | https://example.com/paper |
| authors | string | ✓ | 作者列表JSON字串 | 見範例 |
| paper_file | file | - | 論文文件 | paper.pdf |

**authors參數格式**
```json
[
  {
    "mem_id": 1,
    "author_order": 1,
    "is_corresponding": 1
  },
  {
    "mem_id": 2,
    "author_order": 2,
    "is_corresponding": 0
  }
]
```

### 更新論文
```
PUT /api/papers/{paper_id}
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| paper_id | integer | ✓ | 論文ID | 1 |

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| paper_title_zh | string | - | 論文中文標題 | 更新的論文標題 |
| paper_title_en | string | - | 論文英文標題 | Updated Paper Title |
| paper_desc_zh | string | - | 論文中文描述 | 更新的描述 |
| paper_desc_en | string | - | 論文英文描述 | Updated description |
| paper_venue | string | - | 發表期刊或會議 | ICCV 2024 |
| paper_type | integer | - | 論文類型 | 0 |
| paper_accept | integer | - | 接收狀態 | 1 |
| paper_date | string | - | 發表日期 | 2024-07-01 |
| paper_url | string | - | 論文URL | https://new-url.com |
| research_group_id | integer | - | 所屬課題組ID | 2 |
| authors | array | - | 作者列表 | 見範例 |

**請求範例**
```json
{
  "paper_title_zh": "更新的論文標題",
  "paper_accept": 1,
  "authors": [
    {
      "mem_id": 1,
      "is_corresponding": 1
    },
    {
      "mem_id": 2,
      "is_corresponding": 0
    }
  ]
}
```

### 刪除論文
```
DELETE /api/papers/{paper_id}
```

**請求頭**
```
Authorization: Bearer <token>
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| paper_id | integer | ✓ | 論文ID | 1 |

## 新聞管理

### 獲取新聞列表
```
GET /api/news
```

**請求頭**
無需認證

**查詢參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| q | string | - | 搜索關鍵字 | 獲獎 |
| news_type | integer | - | 新聞類型（0=論文發表, 1=獲獎消息, 2=學術活動） | 1 |
| start_date | string | - | 開始日期 | 2024-01-01 |
| end_date | string | - | 結束日期 | 2024-12-31 |
| show_all | boolean | - | 是否顯示已刪除 | false |
| page | integer | - | 頁碼 | 1 |
| per_page | integer | - | 每頁數量 | 10 |

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      {
        "news_id": 1,
        "news_type": 0,
        "news_content_zh": "我實驗室論文被CVPR 2024錄用",
        "news_content_en": "Our lab paper accepted by CVPR 2024",
        "news_date": "2024-06-15",
        "enable": 1,
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10,
    "pages": 1,
    "has_prev": false,
    "has_next": false
  }
}
```

### 獲取新聞詳情
```
GET /api/news/{news_id}
```

**請求頭**
無需認證

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| news_id | integer | ✓ | 新聞ID | 1 |

### 創建新聞
```
POST /api/news
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| news_type | integer | ✓ | 新聞類型 | 0 |
| news_content_zh | string | ✓ | 新聞中文內容 | 實驗室最新消息 |
| news_content_en | string | - | 新聞英文內容 | Latest lab news |
| news_date | string | ✓ | 新聞日期（YYYY-MM-DD） | 2024-06-15 |

**請求範例**
```json
{
  "news_type": 0,
  "news_content_zh": "我實驗室論文被CVPR 2024錄用",
  "news_content_en": "Our lab paper accepted by CVPR 2024",
  "news_date": "2024-06-15"
}
```

### 更新新聞
```
PUT /api/news/{news_id}
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| news_id | integer | ✓ | 新聞ID | 1 |

**請求參數**: 與創建新聞相同，但所有欄位均為可選

### 刪除新聞
```
DELETE /api/news/{news_id}
```

**請求頭**
```
Authorization: Bearer <token>
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| news_id | integer | ✓ | 新聞ID | 1 |

## 項目管理

### 獲取項目列表
```
GET /api/projects
```

**請求頭**
無需認證

**查詢參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| q | string | - | 搜索關鍵字（項目名稱、描述） | 智慧系統 |
| is_end | integer | - | 項目狀態（0=進行中, 1=已完成） | 0 |
| start_date | string | - | 開始日期範圍查詢（開始） | 2024-01-01 |
| end_date | string | - | 開始日期範圍查詢（結束） | 2024-12-31 |
| show_all | boolean | - | 是否顯示已刪除 | false |
| sort_by | string | - | 排序欄位（name/status/project_date_start） | project_date_start |
| order | string | - | 排序順序（asc/desc） | desc |
| page | integer | - | 頁碼 | 1 |
| per_page | integer | - | 每頁數量 | 10 |

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      {
        "project_id": 1,
        "project_url": "https://github.com/lab/traffic-system",
        "project_name_zh": "智慧交通管理系統",
        "project_name_en": "Intelligent Traffic Management System",
        "project_desc_zh": "基於人工智慧的交通信號最佳化系統",
        "project_desc_en": "AI-based traffic signal optimization system",
        "project_date_start": "2024-01-01",
        "is_end": 0,
        "enable": 1
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10,
    "pages": 1,
    "has_prev": false,
    "has_next": false
  }
}
```

### 獲取項目詳情
```
GET /api/projects/{project_id}
```

**請求頭**
無需認證

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| project_id | integer | ✓ | 項目ID | 1 |

### 創建項目
```
POST /api/projects
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| project_name_zh | string | ✓ | 項目中文名稱 | 智慧交通管理系統 |
| project_name_en | string | - | 項目英文名稱 | Intelligent Traffic Management System |
| project_desc_zh | string | - | 項目中文描述 | 基於AI的交通最佳化系統 |
| project_desc_en | string | - | 項目英文描述 | AI-based traffic optimization system |
| project_url | string | - | 項目URL | https://github.com/lab/project |
| project_date_start | string | - | 項目開始日期（YYYY-MM-DD） | 2024-01-01 |
| is_end | integer | - | 項目狀態（0=進行中, 1=已完成） | 0 |

**請求範例**
```json
{
  "project_name_zh": "智慧交通管理系統",
  "project_name_en": "Intelligent Traffic Management System",
  "project_desc_zh": "基於人工智慧的交通信號最佳化系統",
  "project_desc_en": "AI-based traffic signal optimization system",
  "project_url": "https://github.com/lab/traffic-system",
  "project_date_start": "2024-01-01",
  "is_end": 0
}
```

### 更新項目
```
PUT /api/projects/{project_id}
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| project_id | integer | ✓ | 項目ID | 1 |

**請求參數**: 與創建項目相同，但所有欄位均為可選

### 刪除項目
```
DELETE /api/projects/{project_id}
```

**請求頭**
```
Authorization: Bearer <token>
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| project_id | integer | ✓ | 項目ID | 1 |

## 媒體檔案管理

### 上傳文件
```
POST /api/media/upload
```

**請求頭**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**請求參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| file | file | ✓ | 要上傳的文件 | image.jpg |
| type | string | ✓ | 文件類型（lab_logo/member_avatar/paper/other） | member_avatar |

**響應範例**
```json
{
  "code": 0,
  "message": "文件上傳成功",
  "data": {
    "filename": "avatar_20241201.jpg",
    "url": "/media/member_avatar/avatar_20241201.jpg"
  }
}
```

**支持的文件類型**
- 圖片: png, jpg, jpeg, gif
- 文件: pdf
- 最大檔案大小: 50MB（論文）/ 5MB（其他）

### 獲取文件
```
GET /api/media/serve/{file_path}
```

**請求頭**
無需認證

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| file_path | string | ✓ | 文件路徑 | member_avatar/avatar_001.jpg |

### 獲取文件資訊
```
GET /api/media/info/{file_path}
```

**請求頭**
無需認證

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| file_path | string | ✓ | 文件路徑 | member_avatar/avatar_001.jpg |

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "filename": "avatar_001.jpg",
    "size": 1024000,
    "mime_type": "image/jpeg",
    "created_at": "2024-01-01T00:00:00",
    "url": "/media/member_avatar/avatar_001.jpg"
  }
}
```

### 媒體服務健康檢查
```
GET /api/media/health
```

**請求頭**
無需認證

**查詢參數**
無

**響應範例**
```json
{
  "code": 0,
  "message": "Media service is healthy",
  "data": {
    "status": "healthy",
    "upload_path": "/home/user/uploads",
    "disk_space": "available"
  }
}
```

## 編輯記錄管理

### 獲取編輯記錄列表
```
GET /api/edit-records
```

**請求頭**
```
Authorization: Bearer <token>
```

**查詢參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| admin_id | integer | - | 管理員ID篩選 | 1 |
| edit_module | integer | - | 編輯模組篩選 | 3 |
| edit_type | string | - | 操作類型篩選（CREATE/UPDATE/DELETE/LOGIN/LOGOUT） | CREATE |
| start_date | string | - | 開始日期 | 2024-01-01 |
| end_date | string | - | 結束日期 | 2024-12-31 |
| page | integer | - | 頁碼 | 1 |
| per_page | integer | - | 每頁數量 | 10 |

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      {
        "edit_id": 1,
        "admin_id": 1,
        "edit_type": "CREATE",
        "edit_module": 3,
        "edit_date": "2024-01-01T00:00:00",
        "edit_content": "{\"mem_name_zh\": \"李教授\"}",
        "admin_name": "admin"
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10,
    "pages": 1,
    "has_prev": false,
    "has_next": false
  }
}
```

**編輯模組說明**
| 模組ID | 說明 |
|-------|------|
| 0 | 管理員/認證 |
| 1 | 實驗室 |
| 2 | 課題組 |
| 3 | 成員 |
| 4 | 論文 |
| 5 | 新聞 |
| 6 | 項目 |

### 獲取編輯記錄詳情
```
GET /api/edit-records/{edit_id}
```

**請求頭**
```
Authorization: Bearer <token>
```

**路徑參數**
| 參數 | 類型 | 必填 | 含義 | 範例值 |
|------|------|------|------|--------|
| edit_id | integer | ✓ | 編輯記錄ID | 1 |

## 系統介面

### 重定向到文件
```
GET /api/
```

**請求頭**
無需認證

**查詢參數**
無

自動重定向到 `/api/docs`

### 健康檢查
```
GET /api/health
```

**請求頭**
無需認證

**查詢參數**
無

**響應範例**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00",
    "version": "1.0.0"
  }
}
```

### API資訊
```
GET /api/api-info
```

**請求頭**
無需認證

**查詢參數**
無

返回API資訊頁面（HTML）

### Swagger文件
```
GET /api/docs
```

**請求頭**
無需認證

**查詢參數**
無

返回Swagger UI頁面

### API規範
```
GET /api/swagger.json
```

**請求頭**
無需認證

**查詢參數**
無

返回OpenAPI規範JSON

## 附錄

### 數據類型說明

**成員類型 (mem_type)**
- 0: 教師
- 1: 學生  
- 2: 其他

**職務類型 (job_type)** - 僅教師
- 0: 教授
- 1: 副教授
- 2: 講師
- 3: 助理教授
- 4: 其他

**學生類型 (student_type)** - 僅學生
- 0: 博士
- 1: 碩士
- 2: 本科

**論文類型 (paper_type)**
- 0: 會議
- 1: 期刊
- 2: 專利
- 3: 書籍
- 4: 其他

**論文接收狀態 (paper_accept)**
- 0: 投稿中
- 1: 已接收

**新聞類型 (news_type)**
- 0: 論文發表
- 1: 獲獎消息
- 2: 學術活動

**項目狀態 (is_end)**
- 0: 進行中
- 1: 已完成

### 軟刪除約束

系統採用軟刪除機制，刪除操作遵循以下約束：

1. **實驗室刪除**: 必須先刪除所有課題組和成員
2. **課題組刪除**: 必須先刪除或遷移所有成員
3. **成員刪除**: 不能是課題組組長，且不能有關聯的有效論文

### 文件上傳說明

**支持的文件類型**
- 圖片: PNG, JPG, JPEG, GIF
- 文件: PDF

**檔案大小限制**
- 論文文件: 最大50MB
- 其他文件: 最大5MB

**儲存路徑**
- 實驗室Logo: `/media/lab_logo/`
- 成員頭像: `/media/member_avatar/`
- 論文文件: `/media/paper/`
- 其他文件: `/media/other/`