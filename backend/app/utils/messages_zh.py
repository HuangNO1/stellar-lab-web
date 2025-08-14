"""
中文消息配置
"""

# 成功消息
SUCCESS_MESSAGES = {
    # 登录相关
    'LOGIN_SUCCESS': '登录成功',
    'LOGOUT_SUCCESS': '登出成功',
    'PASSWORD_CHANGE_SUCCESS': '密码修改成功',
    'PROFILE_UPDATE_SUCCESS': '个人资料更新成功',
    
    # CRUD操作成功
    'CREATE_SUCCESS': '创建成功',
    'UPDATE_SUCCESS': '更新成功',
    'DELETE_SUCCESS': '删除成功',
    'BATCH_DELETE_SUCCESS': '批量删除成功',
    'BATCH_UPDATE_SUCCESS': '批量更新成功',
    
    # 具体模块成功消息
    'LAB_UPDATE_SUCCESS': '实验室信息更新成功',
    'LAB_DELETE_SUCCESS': '实验室删除成功',
    'MEMBER_CREATE_SUCCESS': '成员创建成功',
    'MEMBER_UPDATE_SUCCESS': '成员更新成功',
    'MEMBER_DELETE_SUCCESS': '成员删除成功',
    'RESEARCH_GROUP_CREATE_SUCCESS': '课题组创建成功',
    'RESEARCH_GROUP_UPDATE_SUCCESS': '课题组更新成功',
    'RESEARCH_GROUP_DELETE_SUCCESS': '课题组删除成功',
    'PAPER_CREATE_SUCCESS': '论文创建成功',
    'PAPER_UPDATE_SUCCESS': '论文更新成功',
    'PAPER_DELETE_SUCCESS': '论文删除成功',
    'NEWS_CREATE_SUCCESS': '新闻创建成功',
    'NEWS_UPDATE_SUCCESS': '新闻更新成功',
    'NEWS_DELETE_SUCCESS': '新闻删除成功',
    'PROJECT_CREATE_SUCCESS': '项目创建成功',
    'PROJECT_UPDATE_SUCCESS': '项目更新成功',
    'PROJECT_DELETE_SUCCESS': '项目删除成功',
    'ADMIN_CREATE_SUCCESS': '管理员创建成功',
    'ADMIN_UPDATE_SUCCESS': '管理员更新成功',
    'ADMIN_DELETE_SUCCESS': '管理员删除成功',
    'FILE_UPLOAD_SUCCESS': '文件上传成功',
    
    # 系统相关
    'HEALTH_CHECK': '实验室网页框架后端服务正常运行',
}

# 错误消息
ERROR_MESSAGES = {
    # 通用错误
    'NOT_FOUND': '不存在',
    'OPERATION_FAILED': '操作失败',
    'PERMISSION_DENIED': '权限不足',
    'UNAUTHORIZED': '未登录或登录已过期',
    'INVALID_INPUT': '输入无效',
    'MISSING_REQUIRED_FIELDS': '缺少必填字段',
    
    # 认证相关错误
    'INVALID_CREDENTIALS': '用户名和密码不能为空',
    'USER_NOT_FOUND': '用户名不存在',
    'ACCOUNT_DISABLED': '账户已被禁用',
    'WRONG_PASSWORD': '密码错误',
    'OLD_PASSWORD_WRONG': '旧密码错误',
    'PASSWORD_TOO_SHORT': '密码长度至少6位',
    'PASSWORD_LENGTH_INVALID': '密码长度至少8位',
    'USERNAME_ALREADY_EXISTS': '用户名已存在',
    'USERNAME_FORMAT_INVALID': '用户名格式不正确，只能包含字母、数字、下划线和连字符，长度3-50位',
    
    # 实验室相关错误
    'LAB_NOT_FOUND': '实验室不存在',
    'LAB_SETUP_REQUIRED': '请先设置实验室信息',
    'LAB_HAS_GROUPS': '实验室下还有{count}个有效课题组，无法删除',
    'LAB_HAS_MEMBERS': '实验室下还有{count}个有效成员，无法删除',
    
    # 成员相关错误
    'MEMBER_NOT_FOUND': '成员不存在',
    'MEMBER_IS_GROUP_LEADER': '该成员是课题组 "{group_name}" 的组长，无法删除',
    'MEMBER_HAS_PAPERS': '该成员关联了 {count} 篇论文，无法删除',
    'MEMBER_NOT_SELECTED': '请选择要删除的成员',
    'MEMBER_UPDATE_NOT_SELECTED': '请选择要更新的成员',
    'MEMBER_UPDATE_NO_FIELDS': '请指定要更新的字段',
    'MEMBER_TYPE_INVALID': '成员类型无效',
    'MEMBER_TYPE_FORMAT_ERROR': '成员类型格式错误',
    'TITLE_TYPE_INVALID': '职称类型无效',
    'TITLE_TYPE_TEACHER_ONLY': '职称类型仅适用于教师',
    'TITLE_TYPE_FORMAT_ERROR': '职称类型格式错误',
    'STUDENT_TYPE_INVALID': '学生类型无效',
    'STUDENT_TYPE_STUDENT_ONLY': '学生类型仅适用于学生',
    'STUDENT_TYPE_FORMAT_ERROR': '学生类型格式错误',
    'STATUS_INVALID': '状态值无效',
    'STATUS_FORMAT_ERROR': '状态值格式错误',
    'RESEARCH_GROUP_ID_FORMAT_ERROR': '课题组ID格式错误',
    'BATCH_UPDATE_NOT_ALLOWED': '字段 {field} 不允许批量更新',
    
    # 课题组相关错误
    'RESEARCH_GROUP_NOT_FOUND': '课题组不存在',
    'GROUP_LEADER_NOT_FOUND': '指定的组长不存在',
    'LAB_OR_LEADER_REQUIRED': '请先创建实验室或指定组长',
    'LAB_NOT_FOUND_IN_GROUP': '指定的实验室不存在',
    'GROUP_HAS_MEMBERS': '该课题组还有 {count} 个有效成员，无法删除',
    
    # 论文相关错误
    'PAPER_NOT_FOUND': '论文不存在',
    'PAPER_TITLE_REQUIRED': '论文标题不能为空',
    'PAPER_TYPE_INVALID': '论文类型无效',
    'PAPER_TYPE_FORMAT_ERROR': '论文类型格式错误',
    'PAPER_ACCEPT_INVALID': '接收状态无效',
    'PAPER_ACCEPT_FORMAT_ERROR': '接收状态格式错误',
    'PAPER_DATE_FORMAT_ERROR': '论文日期格式错误，应为 YYYY-MM-DD',
    
    # 新闻相关错误
    'NEWS_NOT_FOUND': '新闻不存在',
    'NEWS_TITLE_REQUIRED': '新闻标题不能为空',
    'NEWS_TYPE_INVALID': '新闻类型无效',
    'NEWS_TYPE_FORMAT_ERROR': '新闻类型格式错误',
    'NEWS_DATE_FORMAT_ERROR': '日期格式错误，应为 YYYY-MM-DD',
    
    # 项目相关错误
    'PROJECT_NOT_FOUND': '项目不存在',
    'PROJECT_STATUS_INVALID': '项目状态无效',
    'PROJECT_STATUS_FORMAT_ERROR': '项目状态格式错误',
    'PROJECT_START_DATE_FORMAT_ERROR': '项目开始日期格式错误，应为 YYYY-MM-DD',
    
    # 管理员相关错误
    'ADMIN_NOT_FOUND': '管理员不存在',
    'CANNOT_MODIFY_SELF': '不能修改自己的账户',
    'CANNOT_MODIFY_SUPER_ADMIN': '不能修改其他超级管理员的账户',
    'CANNOT_DELETE_SELF': '不能删除自己的账户',
    'CANNOT_DELETE_SUPER_ADMIN': '不能删除其他超级管理员的账户',
    'IS_SUPER_PARAM_ERROR': 'is_super参数错误',
    'IS_SUPER_FORMAT_ERROR': 'is_super参数格式错误',
    'ENABLE_PARAM_ERROR': 'enable参数错误',
    'ENABLE_FORMAT_ERROR': 'enable参数格式错误',
    
    # 文件相关错误
    'UNSUPPORTED_FILE_TYPE': '不支持的文件类型',
    'FILE_SIZE_EXCEEDED': '文件大小超过限制: {max_size} bytes',
    'IMAGE_PROCESS_FAILED': '图片处理失败: {error}',
    'FILE_DELETE_FAILED': '删除文件失败: {error}',
    'FILE_UPLOAD_FAILED': '上传失败: {error}',
    'FILE_PATH_INVALID': '文件路径无效',
    'FILE_NOT_FOUND': '文件不存在',
    'PATH_NOT_FILE': '路径不是文件',
    'FILE_INFO_FAILED': '获取文件信息失败',
    'MEDIA_SERVICE_UNHEALTHY': '媒体服务不健康: {error}',
    'NO_FILE_SELECTED': '没有选择文件',
    'LOGO_UPLOAD_FAILED': 'Logo上传失败: {error}',
    'AVATAR_UPLOAD_FAILED': '头像上传失败: {error}',
    'AVATAR_UPDATE_FAILED': '头像更新失败: {error}',
    'PAPER_FILE_UPLOAD_FAILED': '论文文件上传失败: {error}',
    
    # 数据校验错误
    'EMAIL_FORMAT_INVALID': '邮箱格式不正确',
    'FIELD_LENGTH_EXCEEDED': '{field} 长度不能超过{max_length}字符',
    'DATE_FORMAT_ERROR': '日期格式错误，应为 YYYY-MM-DD',
    'SOFT_DELETE_NOT_SUPPORTED': '{resource}不支持软删除',
    'RESOURCE_NOT_FOUND_OR_DELETED': '{resource}不存在或已被删除',
    
    # 系统错误
    'UNKNOWN_MODULE': '未知的模组名称: {module_name}',
    'UNKNOWN_OPERATION': '未知的操作类型: {operation}',
    'SYSTEM_ERROR': '系统错误',
    'PARAMETER_ERROR': '参数错误',
}