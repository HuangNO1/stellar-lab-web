<!-- Language Switcher -->

<div align="right">

[English](messages_usage_guide_EN.md)

</div>

# 統一文本管理使用指南

## 概述

為了解決後端中硬編碼中文消息的問題，我們創建了統一的文本管理系統。所有返回給前端的中文消息都集中在 `app/utils/messages.py` 文件中管理。

## 文件結構

```
app/utils/
├── messages.py          # 統一的文本管理文件
└── ...
```

## 主要特性

- **集中管理**：所有中文消息統一在 `Messages` 類中管理
- **參數化支持**：支持動態參數，如 `{count}`、`{field}` 等
- **類型分類**：成功消息和錯誤消息分別管理
- **簡化調用**：提供 `msg` 快捷方式，使用簡潔
- **易於維護**：便於未來的國際化擴展

## 使用方法

### 1. 在服務層使用

```python
from app.utils.messages import msg

# 基本錯誤消息
raise ValidationError(msg.get_error_message('MEMBER_NOT_FOUND'))

# 帶參數的錯誤消息
raise ValidationError(msg.get_error_message('LAB_HAS_GROUPS', count=5))

# 字段長度錯誤的便捷方法
raise ValidationError(msg.format_field_length_error('name', 100))

# 文件錯誤的便捷方法
raise ValidationError(msg.format_file_error('LOGO_UPLOAD_FAILED', error=str(e)))
```

### 2. 在路由層使用

```python
from app.utils.messages import msg

# 成功消息
return jsonify(success_response(data, msg.get_success_message('MEMBER_CREATE_SUCCESS')))

# 純消息響應
return jsonify(success_response(message=msg.get_success_message('MEMBER_DELETE_SUCCESS')))
```

## 消息類型

### 成功消息 (SUCCESS)

- 通用操作：`CREATE_SUCCESS`、`UPDATE_SUCCESS`、`DELETE_SUCCESS`
- 登錄相關：`LOGIN_SUCCESS`、`LOGOUT_SUCCESS`、`PASSWORD_CHANGE_SUCCESS`
- 具體模塊：`LAB_UPDATE_SUCCESS`、`MEMBER_CREATE_SUCCESS` 等

### 錯誤消息 (ERRORS)

- 通用錯誤：`NOT_FOUND`、`PERMISSION_DENIED`、`INVALID_INPUT`
- 認證錯誤：`USER_NOT_FOUND`、`WRONG_PASSWORD`、`ACCOUNT_DISABLED`
- 業務邏輯：`LAB_HAS_GROUPS`、`MEMBER_IS_GROUP_LEADER`
- 數據校驗：`EMAIL_FORMAT_INVALID`、`FIELD_LENGTH_EXCEEDED`

## 重構進度

### ✅ 已完成
- `app/services/lab_service.py`
- `app/routes/lab.py`
- `app/routes/root.py`
- `app/utils/file_handler.py`

### 📝 待重構的文件

**服務層文件：**
- `app/services/member_service.py`
- `app/services/paper_service.py`
- `app/services/news_service.py`
- `app/services/project_service.py`
- `app/services/research_group_service.py`
- `app/services/admin_service.py`
- `app/services/auth_service.py`
- `app/services/media_service.py`
- `app/services/base_service.py`

**路由層文件：**
- `app/routes/member.py`
- `app/routes/paper.py`
- `app/routes/news.py`
- `app/routes/project.py`
- `app/routes/research_group.py`
- `app/routes/admin.py`
- `app/routes/auth.py`
- `app/routes/media.py`

## 重構步驟

1. **導入消息管理器**
   ```python
   from app.utils.messages import msg
   ```

2. **替換硬編碼消息**
   ```python
   # 原來
   raise ValidationError('用戶不存在')
   
   # 修改後
   raise ValidationError(msg.get_error_message('USER_NOT_FOUND'))
   ```

3. **處理參數化消息**
   ```python
   # 原來
   raise ValidationError(f'實驗室下還有{count}個課題組')
   
   # 修改後
   raise ValidationError(msg.get_error_message('LAB_HAS_GROUPS', count=count))
   ```

## 擴展指南

### 添加新消息

1. 在 `messages.py` 的相應字典中添加新的鍵值對
2. 使用描述性的鍵名（全大寫，下劃線分隔）
3. 如需參數，使用 `{param_name}` 格式

```python
# 在 Messages.SUCCESS 或 Messages.ERRORS 中添加
'NEW_OPERATION_SUCCESS': '新操作執行成功',
'CUSTOM_ERROR_MESSAGE': '自定義錯誤: {detail}',
```

### 國際化準備

未來如需支持多語言，可以擴展 `Messages` 類：

```python
class Messages:
    def __init__(self, language='zh'):
        self.language = language
        self.messages = self._load_messages(language)
    
    def _load_messages(self, language):
        # 根據語言加載不同的消息文件
        pass
```

## 最佳實踐

1. **統一使用**：所有新代碼都應使用統一的消息管理
2. **語義明確**：消息鍵名應清晰表達含義
3. **參數一致**：相同類型的參數使用相同的命名
4. **分類管理**：按功能模塊組織消息
5. **文檔更新**：添加新消息時更新此文檔

## 注意事項

- 不要直接修改消息內容，應通過參數化實現動態內容
- 保持消息鍵名的一致性和可讀性
- 重構時要確保所有引用都正確更新
- 測試重構後的功能確保消息正確顯示