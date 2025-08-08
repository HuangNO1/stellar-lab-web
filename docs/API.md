# API 接口文檔

## 認證鑒權

### 登錄
- **URL**: `POST /api/admin/login`
- **權限**: 公開
- **請求體**:
```json
{
  "admin_name": "string",
  "admin_pass": "string"
}
```
- **響應**:
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "access_token": "Bearer xxx",
    "expires_in": 3600,
    "admin": {
      "admin_id": 1,
      "admin_name": "root",
      "is_super": 1
    }
  }
}
```

### 修改密碼
- **URL**: `POST /api/admin/change-password`
- **權限**: 登錄用戶
- **請求體**:
```json
{
  "old_password": "xxx",
  "new_password": "yyy"
}
```

## 實驗室管理

### 獲取實驗室信息
- **URL**: `GET /api/lab`
- **權限**: 公開

### 更新實驗室信息
- **URL**: `PUT /api/lab`
- **權限**: 管理員
- **Content-Type**: `multipart/form-data`

## 課題組管理

### 課題組列表
- **URL**: `GET /api/research-groups`
- **權限**: 公開
- **查詢參數**: `page`, `per_page`, `q`, `lab_id`, `show_all`

### 創建課題組
- **URL**: `POST /api/research-groups`
- **權限**: 管理員

### 更新課題組
- **URL**: `PUT /api/research-groups/{id}`
- **權限**: 管理員

### 刪除課題組
- **URL**: `DELETE /api/research-groups/{id}`
- **權限**: 管理員

## 成員管理

### 成員列表
- **URL**: `GET /api/members`
- **權限**: 公開
- **查詢參數**: `type`, `research_group_id`, `q`, `page`, `per_page`

### 成員詳情
- **URL**: `GET /api/members/{mem_id}`
- **權限**: 公開

### 創建成員
- **URL**: `POST /api/members`
- **權限**: 管理員
- **Content-Type**: `multipart/form-data`

### 更新成員
- **URL**: `PUT /api/members/{mem_id}`
- **權限**: 管理員

### 刪除成員
- **URL**: `DELETE /api/members/{mem_id}`
- **權限**: 管理員

## 論文管理

### 論文列表
- **URL**: `GET /api/papers`
- **權限**: 公開
- **查詢參數**: `q`, `paper_type`, `paper_accept`, `start_date`, `end_date`, `page`, `per_page`

### 論文詳情
- **URL**: `GET /api/papers/{paper_id}`
- **權限**: 公開

### 創建論文
- **URL**: `POST /api/papers`
- **權限**: 管理員
- **Content-Type**: `multipart/form-data`

### 更新論文
- **URL**: `PUT /api/papers/{paper_id}`
- **權限**: 管理員

### 刪除論文
- **URL**: `DELETE /api/papers/{paper_id}`
- **權限**: 管理員

## 新聞管理

### 新聞列表
- **URL**: `GET /api/news`
- **權限**: 公開
- **查詢參數**: `page`, `per_page`, `q`, `news_type`

### 創建新聞
- **URL**: `POST /api/news`
- **權限**: 管理員

### 更新新聞
- **URL**: `PUT /api/news/{news_id}`
- **權限**: 管理員

### 刪除新聞
- **URL**: `DELETE /api/news/{news_id}`
- **權限**: 管理員

## 項目管理

### 項目列表
- **URL**: `GET /api/projects`
- **權限**: 公開

### 項目詳情
- **URL**: `GET /api/projects/{project_id}`
- **權限**: 公開

### 創建項目
- **URL**: `POST /api/projects`
- **權限**: 管理員

### 更新項目
- **URL**: `PUT /api/projects/{project_id}`
- **權限**: 管理員

### 刪除項目
- **URL**: `DELETE /api/projects/{project_id}`
- **權限**: 管理員

## 文件上傳

### 通用上傳
- **URL**: `POST /api/media/upload`
- **權限**: 管理員
- **Content-Type**: `multipart/form-data`
- **參數**: `file`, `type`

### 媒體訪問
- **URL**: `GET /api/media/serve/{file_id}`
- **權限**: 公開

## 統一響應格式

所有接口均采用統一響應格式：

```json
{
  "code": 0,
  "message": "OK",
  "data": {}
}
```

## 錯誤碼

- `0` - 成功
- `1000` - 未認證或 token 無效
- `1001` - 權限不足  
- `2000` - 參數校驗錯誤
- `3000` - 資源未找到
- `4000` - 操作衝突
- `5000` - 服務器內部錯誤