"""
統一的消息文本管理
用於管理後端返回給前端的所有中文消息，避免硬編碼
"""

class Messages:
    """統一的消息管理類"""
    
    # 成功消息
    SUCCESS = {
        # 登錄相關
        'LOGIN_SUCCESS': '登錄成功',
        'LOGOUT_SUCCESS': '登出成功',
        'PASSWORD_CHANGE_SUCCESS': '密碼修改成功',
        'PROFILE_UPDATE_SUCCESS': '個人資料更新成功',
        
        # CRUD操作成功
        'CREATE_SUCCESS': '創建成功',
        'UPDATE_SUCCESS': '更新成功',
        'DELETE_SUCCESS': '刪除成功',
        'BATCH_DELETE_SUCCESS': '批量刪除成功',
        'BATCH_UPDATE_SUCCESS': '批量更新成功',
        
        # 具體模塊成功消息
        'LAB_UPDATE_SUCCESS': '實驗室信息更新成功',
        'LAB_DELETE_SUCCESS': '實驗室刪除成功',
        'MEMBER_CREATE_SUCCESS': '成員創建成功',
        'MEMBER_UPDATE_SUCCESS': '成員更新成功',
        'MEMBER_DELETE_SUCCESS': '成員刪除成功',
        'RESEARCH_GROUP_CREATE_SUCCESS': '課題組創建成功',
        'RESEARCH_GROUP_UPDATE_SUCCESS': '課題組更新成功',
        'RESEARCH_GROUP_DELETE_SUCCESS': '課題組刪除成功',
        'PAPER_CREATE_SUCCESS': '論文創建成功',
        'PAPER_UPDATE_SUCCESS': '論文更新成功',
        'PAPER_DELETE_SUCCESS': '論文刪除成功',
        'NEWS_CREATE_SUCCESS': '新聞創建成功',
        'NEWS_UPDATE_SUCCESS': '新聞更新成功',
        'NEWS_DELETE_SUCCESS': '新聞刪除成功',
        'PROJECT_CREATE_SUCCESS': '項目創建成功',
        'PROJECT_UPDATE_SUCCESS': '項目更新成功',
        'PROJECT_DELETE_SUCCESS': '項目刪除成功',
        'ADMIN_CREATE_SUCCESS': '管理員創建成功',
        'ADMIN_UPDATE_SUCCESS': '管理員更新成功',
        'ADMIN_DELETE_SUCCESS': '管理員刪除成功',
        'FILE_UPLOAD_SUCCESS': '文件上傳成功',
        
        # 系統相關
        'HEALTH_CHECK': '實驗室網頁框架後端服務正常運行',
    }
    
    # 錯誤消息
    ERRORS = {
        # 通用錯誤
        'NOT_FOUND': '不存在',
        'OPERATION_FAILED': '操作失敗',
        'PERMISSION_DENIED': '權限不足',
        'UNAUTHORIZED': '未登錄或登錄已過期',
        'INVALID_INPUT': '輸入無效',
        'MISSING_REQUIRED_FIELDS': '缺少必填字段',
        
        # 認證相關錯誤
        'INVALID_CREDENTIALS': '用戶名和密碼不能為空',
        'USER_NOT_FOUND': '用戶名不存在',
        'ACCOUNT_DISABLED': '賬戶已被禁用',
        'WRONG_PASSWORD': '密碼錯誤',
        'OLD_PASSWORD_WRONG': '舊密碼錯誤',
        'PASSWORD_TOO_SHORT': '密碼長度至少6位',
        'PASSWORD_LENGTH_INVALID': '密碼長度至少8位',
        'USERNAME_ALREADY_EXISTS': '用戶名已存在',
        'USERNAME_FORMAT_INVALID': '用戶名格式不正確，只能包含字母、數字、下劃線和連字符，長度3-50位',
        
        # 實驗室相關錯誤
        'LAB_NOT_FOUND': '實驗室不存在',
        'LAB_SETUP_REQUIRED': '請先設置實驗室信息',
        'LAB_HAS_GROUPS': '實驗室下還有{count}個有效課題組，無法刪除',
        'LAB_HAS_MEMBERS': '實驗室下還有{count}個有效成員，無法刪除',
        
        # 成員相關錯誤
        'MEMBER_NOT_FOUND': '成員不存在',
        'MEMBER_IS_GROUP_LEADER': '該成員是課題組 "{group_name}" 的組長，無法刪除',
        'MEMBER_HAS_PAPERS': '該成員關聯了 {count} 篇論文，無法刪除',
        'MEMBER_NOT_SELECTED': '請選擇要刪除的成員',
        'MEMBER_UPDATE_NOT_SELECTED': '請選擇要更新的成員',
        'MEMBER_UPDATE_NO_FIELDS': '請指定要更新的字段',
        'MEMBER_TYPE_INVALID': '成員類型無效',
        'MEMBER_TYPE_FORMAT_ERROR': '成員類型格式錯誤',
        'TITLE_TYPE_INVALID': '職稱類型無效',
        'TITLE_TYPE_TEACHER_ONLY': '職稱類型僅適用於教師',
        'TITLE_TYPE_FORMAT_ERROR': '職稱類型格式錯誤',
        'STUDENT_TYPE_INVALID': '學生類型無效',
        'STUDENT_TYPE_STUDENT_ONLY': '學生類型僅適用於學生',
        'STUDENT_TYPE_FORMAT_ERROR': '學生類型格式錯誤',
        'STATUS_INVALID': '狀態值無效',
        'STATUS_FORMAT_ERROR': '狀態值格式錯誤',
        'RESEARCH_GROUP_ID_FORMAT_ERROR': '課題組ID格式錯誤',
        'BATCH_UPDATE_NOT_ALLOWED': '字段 {field} 不允許批量更新',
        
        # 課題組相關錯誤
        'RESEARCH_GROUP_NOT_FOUND': '課題組不存在',
        'GROUP_LEADER_NOT_FOUND': '指定的組長不存在',
        'LAB_OR_LEADER_REQUIRED': '請先創建實驗室或指定組長',
        'LAB_NOT_FOUND_IN_GROUP': '指定的實驗室不存在',
        'GROUP_HAS_MEMBERS': '該課題組還有 {count} 個有效成員，無法刪除',
        
        # 論文相關錯誤
        'PAPER_NOT_FOUND': '論文不存在',
        'PAPER_TITLE_REQUIRED': '論文標題不能為空',
        'PAPER_TYPE_INVALID': '論文類型無效',
        'PAPER_TYPE_FORMAT_ERROR': '論文類型格式錯誤',
        'PAPER_ACCEPT_INVALID': '接收狀態無效',
        'PAPER_ACCEPT_FORMAT_ERROR': '接收狀態格式錯誤',
        'PAPER_DATE_FORMAT_ERROR': '論文日期格式錯誤，應為 YYYY-MM-DD',
        
        # 新聞相關錯誤
        'NEWS_NOT_FOUND': '新聞不存在',
        'NEWS_TYPE_INVALID': '新聞類型無效',
        'NEWS_TYPE_FORMAT_ERROR': '新聞類型格式錯誤',
        'NEWS_DATE_FORMAT_ERROR': '日期格式錯誤，應為 YYYY-MM-DD',
        
        # 項目相關錯誤
        'PROJECT_NOT_FOUND': '項目不存在',
        'PROJECT_STATUS_INVALID': '項目狀態無效',
        'PROJECT_STATUS_FORMAT_ERROR': '項目狀態格式錯誤',
        'PROJECT_START_DATE_FORMAT_ERROR': '項目開始日期格式錯誤，應為 YYYY-MM-DD',
        
        # 管理員相關錯誤
        'ADMIN_NOT_FOUND': '管理員不存在',
        'CANNOT_MODIFY_SELF': '不能修改自己的賬戶',
        'CANNOT_MODIFY_SUPER_ADMIN': '不能修改其他超級管理員的賬戶',
        'CANNOT_DELETE_SELF': '不能刪除自己的賬戶',
        'CANNOT_DELETE_SUPER_ADMIN': '不能刪除其他超級管理員的賬戶',
        'IS_SUPER_PARAM_ERROR': 'is_super參數錯誤',
        'IS_SUPER_FORMAT_ERROR': 'is_super參數格式錯誤',
        'ENABLE_PARAM_ERROR': 'enable參數錯誤',
        'ENABLE_FORMAT_ERROR': 'enable參數格式錯誤',
        
        # 文件相關錯誤
        'UNSUPPORTED_FILE_TYPE': '不支持的文件類型',
        'FILE_SIZE_EXCEEDED': '文件大小超過限制: {max_size} bytes',
        'IMAGE_PROCESS_FAILED': '圖片處理失敗: {error}',
        'FILE_DELETE_FAILED': '刪除文件失敗: {error}',
        'FILE_UPLOAD_FAILED': '上傳失敗: {error}',
        'FILE_PATH_INVALID': '文件路徑無效',
        'FILE_NOT_FOUND': '文件不存在',
        'PATH_NOT_FILE': '路徑不是文件',
        'FILE_INFO_FAILED': '獲取文件信息失敗',
        'MEDIA_SERVICE_UNHEALTHY': '媒體服務不健康: {error}',
        'NO_FILE_SELECTED': '沒有選擇文件',
        'LOGO_UPLOAD_FAILED': 'Logo上傳失敗: {error}',
        'AVATAR_UPLOAD_FAILED': '頭像上傳失敗: {error}',
        'AVATAR_UPDATE_FAILED': '頭像更新失敗: {error}',
        'PAPER_FILE_UPLOAD_FAILED': '論文文件上傳失敗: {error}',
        
        # 數據校驗錯誤
        'EMAIL_FORMAT_INVALID': '郵箱格式不正確',
        'FIELD_LENGTH_EXCEEDED': '{field} 長度不能超過{max_length}字符',
        'DATE_FORMAT_ERROR': '日期格式錯誤，應為 YYYY-MM-DD',
        'SOFT_DELETE_NOT_SUPPORTED': '{resource}不支持軟刪除',
        'RESOURCE_NOT_FOUND_OR_DELETED': '{resource}不存在或已被刪除',
        
        # 系統錯誤
        'UNKNOWN_MODULE': '未知的模組名稱: {module_name}',
        'UNKNOWN_OPERATION': '未知的操作類型: {operation}',
        'SYSTEM_ERROR': '系統錯誤',
        'PARAMETER_ERROR': '參數錯誤',
    }
    
    @classmethod
    def get_success_message(cls, key: str, **kwargs) -> str:
        """
        獲取成功消息
        
        Args:
            key: 消息鍵
            **kwargs: 格式化參數
            
        Returns:
            格式化後的消息
        """
        message = cls.SUCCESS.get(key, key)
        if kwargs:
            return message.format(**kwargs)
        return message
    
    @classmethod
    def get_error_message(cls, key: str, **kwargs) -> str:
        """
        獲取錯誤消息
        
        Args:
            key: 消息鍵
            **kwargs: 格式化參數
            
        Returns:
            格式化後的消息
        """
        message = cls.ERRORS.get(key, key)
        if kwargs:
            return message.format(**kwargs)
        return message
    
    @classmethod
    def format_field_length_error(cls, field: str, max_length: int) -> str:
        """格式化字段長度錯誤消息"""
        return cls.get_error_message('FIELD_LENGTH_EXCEEDED', field=field, max_length=max_length)
    
    @classmethod
    def format_file_error(cls, error_type: str, **kwargs) -> str:
        """格式化文件錯誤消息"""
        return cls.get_error_message(error_type, **kwargs)
    
    @classmethod
    def format_resource_error(cls, resource: str, error_type: str = 'NOT_FOUND') -> str:
        """格式化資源錯誤消息"""
        if error_type == 'NOT_FOUND':
            return f"{resource}{cls.get_error_message('NOT_FOUND')}"
        return cls.get_error_message(error_type, resource=resource)


# 簡化的消息快捷方式
msg = Messages()