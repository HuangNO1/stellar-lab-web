"""
English message configuration
"""

# Success messages
SUCCESS_MESSAGES = {
    # Authentication related
    'LOGIN_SUCCESS': 'Login successful',
    'LOGOUT_SUCCESS': 'Logout successful',
    'PASSWORD_CHANGE_SUCCESS': 'Password changed successfully',
    'PROFILE_UPDATE_SUCCESS': 'Profile updated successfully',
    
    # CRUD operations
    'CREATE_SUCCESS': 'Created successfully',
    'UPDATE_SUCCESS': 'Updated successfully',
    'DELETE_SUCCESS': 'Deleted successfully',
    'BATCH_DELETE_SUCCESS': 'Batch deletion successful',
    'BATCH_UPDATE_SUCCESS': 'Batch update successful',
    
    # Module specific success messages
    'LAB_UPDATE_SUCCESS': 'Laboratory information updated successfully',
    'LAB_DELETE_SUCCESS': 'Laboratory deleted successfully',
    'MEMBER_CREATE_SUCCESS': 'Member created successfully',
    'MEMBER_UPDATE_SUCCESS': 'Member updated successfully',
    'MEMBER_DELETE_SUCCESS': 'Member deleted successfully',
    'RESEARCH_GROUP_CREATE_SUCCESS': 'Research group created successfully',
    'RESEARCH_GROUP_UPDATE_SUCCESS': 'Research group updated successfully',
    'RESEARCH_GROUP_DELETE_SUCCESS': 'Research group deleted successfully',
    'PAPER_CREATE_SUCCESS': 'Paper created successfully',
    'PAPER_UPDATE_SUCCESS': 'Paper updated successfully',
    'PAPER_DELETE_SUCCESS': 'Paper deleted successfully',
    'NEWS_CREATE_SUCCESS': 'News created successfully',
    'NEWS_UPDATE_SUCCESS': 'News updated successfully',
    'NEWS_DELETE_SUCCESS': 'News deleted successfully',
    'PROJECT_CREATE_SUCCESS': 'Project created successfully',
    'PROJECT_UPDATE_SUCCESS': 'Project updated successfully',
    'PROJECT_DELETE_SUCCESS': 'Project deleted successfully',
    'ADMIN_CREATE_SUCCESS': 'Administrator created successfully',
    'ADMIN_UPDATE_SUCCESS': 'Administrator updated successfully',
    'ADMIN_DELETE_SUCCESS': 'Administrator deleted successfully',
    'FILE_UPLOAD_SUCCESS': 'File uploaded successfully',
    
    # System related
    'HEALTH_CHECK': 'Laboratory web framework backend service is running normally',
}

# Error messages
ERROR_MESSAGES = {
    # Generic errors
    'NOT_FOUND': 'not found',
    'OPERATION_FAILED': 'Operation failed',
    'PERMISSION_DENIED': 'Permission denied',
    'UNAUTHORIZED': 'Not logged in or login has expired',
    'INVALID_INPUT': 'Invalid input',
    'MISSING_REQUIRED_FIELDS': 'Missing required fields',
    
    # Authentication related errors
    'INVALID_CREDENTIALS': 'Username and password cannot be empty',
    'USER_NOT_FOUND': 'Username does not exist',
    'ACCOUNT_DISABLED': 'Account has been disabled',
    'WRONG_PASSWORD': 'Incorrect password',
    'OLD_PASSWORD_WRONG': 'Old password is incorrect',
    'PASSWORD_TOO_SHORT': 'Password must be at least 6 characters',
    'PASSWORD_LENGTH_INVALID': 'Password must be at least 8 characters',
    'USERNAME_ALREADY_EXISTS': 'Username already exists',
    'USERNAME_FORMAT_INVALID': 'Invalid username format. Only letters, numbers, underscores and hyphens are allowed, length 3-50 characters',
    
    # Laboratory related errors
    'LAB_NOT_FOUND': 'Laboratory not found',
    'LAB_SETUP_REQUIRED': 'Please set up laboratory information first',
    'LAB_HAS_GROUPS': 'Laboratory has {count} active research groups, cannot delete',
    'LAB_HAS_MEMBERS': 'Laboratory has {count} active members, cannot delete',
    
    # Member related errors
    'MEMBER_NOT_FOUND': 'Member not found',
    'MEMBER_IS_GROUP_LEADER': 'This member is the leader of research group "{group_name}", cannot delete',
    'MEMBER_HAS_PAPERS': 'This member is associated with {count} papers, cannot delete',
    'MEMBER_NOT_SELECTED': 'Please select members to delete',
    'MEMBER_UPDATE_NOT_SELECTED': 'Please select members to update',
    'MEMBER_UPDATE_NO_FIELDS': 'Please specify fields to update',
    'MEMBER_TYPE_INVALID': 'Invalid member type',
    'MEMBER_TYPE_FORMAT_ERROR': 'Member type format error',
    'TITLE_TYPE_INVALID': 'Invalid title type',
    'TITLE_TYPE_TEACHER_ONLY': 'Title type is only applicable to teachers',
    'TITLE_TYPE_FORMAT_ERROR': 'Title type format error',
    'STUDENT_TYPE_INVALID': 'Invalid student type',
    'STUDENT_TYPE_STUDENT_ONLY': 'Student type is only applicable to students',
    'STUDENT_TYPE_FORMAT_ERROR': 'Student type format error',
    'STATUS_INVALID': 'Invalid status value',
    'STATUS_FORMAT_ERROR': 'Status value format error',
    'RESEARCH_GROUP_ID_FORMAT_ERROR': 'Research group ID format error',
    'BATCH_UPDATE_NOT_ALLOWED': 'Field {field} is not allowed for batch update',
    
    # Research group related errors
    'RESEARCH_GROUP_NOT_FOUND': 'Research group not found',
    'GROUP_LEADER_NOT_FOUND': 'Specified group leader not found',
    'LAB_OR_LEADER_REQUIRED': 'Please create laboratory or specify leader first',
    'LAB_NOT_FOUND_IN_GROUP': 'Specified laboratory not found',
    'GROUP_HAS_MEMBERS': 'This research group has {count} active members, cannot delete',
    
    # Paper related errors
    'PAPER_NOT_FOUND': 'Paper not found',
    'PAPER_TITLE_REQUIRED': 'Paper title cannot be empty',
    'PAPER_TYPE_INVALID': 'Invalid paper type',
    'PAPER_TYPE_FORMAT_ERROR': 'Paper type format error',
    'PAPER_ACCEPT_INVALID': 'Invalid acceptance status',
    'PAPER_ACCEPT_FORMAT_ERROR': 'Acceptance status format error',
    'PAPER_DATE_FORMAT_ERROR': 'Paper date format error, should be YYYY-MM-DD',
    
    # News related errors
    'NEWS_NOT_FOUND': 'News not found',
    'NEWS_TYPE_INVALID': 'Invalid news type',
    'NEWS_TYPE_FORMAT_ERROR': 'News type format error',
    'NEWS_DATE_FORMAT_ERROR': 'Date format error, should be YYYY-MM-DD',
    
    # Project related errors
    'PROJECT_NOT_FOUND': 'Project not found',
    'PROJECT_STATUS_INVALID': 'Invalid project status',
    'PROJECT_STATUS_FORMAT_ERROR': 'Project status format error',
    'PROJECT_START_DATE_FORMAT_ERROR': 'Project start date format error, should be YYYY-MM-DD',
    
    # Administrator related errors
    'ADMIN_NOT_FOUND': 'Administrator not found',
    'CANNOT_MODIFY_SELF': 'Cannot modify your own account',
    'CANNOT_MODIFY_SUPER_ADMIN': 'Cannot modify other super administrator accounts',
    'CANNOT_DELETE_SELF': 'Cannot delete your own account',
    'CANNOT_DELETE_SUPER_ADMIN': 'Cannot delete other super administrator accounts',
    'IS_SUPER_PARAM_ERROR': 'is_super parameter error',
    'IS_SUPER_FORMAT_ERROR': 'is_super parameter format error',
    'ENABLE_PARAM_ERROR': 'enable parameter error',
    'ENABLE_FORMAT_ERROR': 'enable parameter format error',
    
    # File related errors
    'UNSUPPORTED_FILE_TYPE': 'Unsupported file type',
    'FILE_SIZE_EXCEEDED': 'File size exceeds limit: {max_size} bytes',
    'IMAGE_PROCESS_FAILED': 'Image processing failed: {error}',
    'FILE_DELETE_FAILED': 'File deletion failed: {error}',
    'FILE_UPLOAD_FAILED': 'Upload failed: {error}',
    'FILE_PATH_INVALID': 'Invalid file path',
    'FILE_NOT_FOUND': 'File not found',
    'PATH_NOT_FILE': 'Path is not a file',
    'FILE_INFO_FAILED': 'Failed to get file information',
    'MEDIA_SERVICE_UNHEALTHY': 'Media service unhealthy: {error}',
    'NO_FILE_SELECTED': 'No file selected',
    'LOGO_UPLOAD_FAILED': 'Logo upload failed: {error}',
    'AVATAR_UPLOAD_FAILED': 'Avatar upload failed: {error}',
    'AVATAR_UPDATE_FAILED': 'Avatar update failed: {error}',
    'PAPER_FILE_UPLOAD_FAILED': 'Paper file upload failed: {error}',
    
    # Data validation errors
    'EMAIL_FORMAT_INVALID': 'Invalid email format',
    'FIELD_LENGTH_EXCEEDED': '{field} length cannot exceed {max_length} characters',
    'DATE_FORMAT_ERROR': 'Date format error, should be YYYY-MM-DD',
    'SOFT_DELETE_NOT_SUPPORTED': '{resource} does not support soft delete',
    'RESOURCE_NOT_FOUND_OR_DELETED': '{resource} not found or has been deleted',
    
    # System errors
    'UNKNOWN_MODULE': 'Unknown module name: {module_name}',
    'UNKNOWN_OPERATION': 'Unknown operation type: {operation}',
    'SYSTEM_ERROR': 'System error',
    'PARAMETER_ERROR': 'Parameter error',
}