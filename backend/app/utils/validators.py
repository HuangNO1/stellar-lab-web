import re
from datetime import datetime
from .security import sanitize_string

def validate_email(email):
    if not email:
        return True  # 郵箱非必填
    
    # 先清理輸入
    email = sanitize_string(email)
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_admin_name(admin_name):
    if not admin_name:
        return False
    
    # 先清理輸入
    admin_name = sanitize_string(admin_name)
    
    pattern = r'^[A-Za-z0-9_\-]{3,50}$'
    return re.match(pattern, admin_name) is not None

def validate_date(date_str):
    if not date_str:
        return True, None
    
    # 先清理輸入
    date_str = sanitize_string(date_str)
    
    try:
        # 首先嘗試解析時間戳（毫秒級）
        if date_str.isdigit() and len(date_str) == 13:
            timestamp_ms = int(date_str)
            date_obj = datetime.fromtimestamp(timestamp_ms / 1000).date()
            return True, date_obj
        
        # 嘗試解析時間戳（秒級）
        if date_str.isdigit() and len(date_str) == 10:
            timestamp_s = int(date_str)
            date_obj = datetime.fromtimestamp(timestamp_s).date()
            return True, date_obj
        
        # 嘗試解析標準日期格式
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        return True, date_obj
    except (ValueError, OSError):
        return False, None

def validate_enum(value, valid_values):
    if value is None:
        return True
    
    try:
        int_value = int(value)
        return int_value in valid_values
    except (ValueError, TypeError):
        return False

def validate_string_length(value, max_length):
    if not value:
        return True
    
    # 先清理輸入
    cleaned_value = sanitize_string(value) if isinstance(value, str) else value
    
    return len(cleaned_value) <= max_length