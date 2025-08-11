"""
安全工具模組
提供XSS防護、輸入清理和其他安全相關功能
"""

import re
import html
import logging
from typing import Any, Dict, Union
from markupsafe import escape


class SecurityFilter(logging.Filter):
    """日誌安全過濾器，移除敏感信息"""
    
    SENSITIVE_PATTERNS = [
        r'password["\s]*[:=]["\s]*[^"\s,}]+',
        r'token["\s]*[:=]["\s]*[^"\s,}]+',
        r'secret["\s]*[:=]["\s]*[^"\s,}]+',
        r'key["\s]*[:=]["\s]*[^"\s,}]+',
    ]
    
    def filter(self, record):
        """過濾日誌中的敏感信息"""
        if hasattr(record, 'msg') and record.msg:
            record.msg = self.sanitize_message(str(record.msg))
        return True
    
    def sanitize_message(self, message: str) -> str:
        """清理消息中的敏感信息"""
        for pattern in self.SENSITIVE_PATTERNS:
            message = re.sub(pattern, lambda m: m.group().split(':')[0] + ': ***', message, flags=re.IGNORECASE)
        return message


def sanitize_input(data: Union[str, Dict, Any]) -> Union[str, Dict, Any]:
    """
    清理用戶輸入，防止XSS攻擊
    
    Args:
        data: 需要清理的數據，可以是字符串、字典或其他類型
        
    Returns:
        清理後的數據
    """
    if isinstance(data, str):
        return sanitize_string(data)
    elif isinstance(data, dict):
        return {key: sanitize_input(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    else:
        return data


def sanitize_string(text: str) -> str:
    """
    清理字符串輸入
    
    Args:
        text: 需要清理的字符串
        
    Returns:
        清理後的字符串
    """
    if not isinstance(text, str) or not text:
        return text
    
    # HTML轉義
    text = html.escape(text)
    
    # 移除潛在的腳本標籤
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 移除潛在的事件處理器
    text = re.sub(r'on\w+\s*=\s*["\']?[^"\']*["\']?', '', text, flags=re.IGNORECASE)
    
    # 移除javascript:協議
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    
    return text.strip()


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除危險字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        安全的文件名
    """
    if not filename:
        return filename
    
    # 移除路徑遍歷字符
    filename = filename.replace('..', '').replace('/', '').replace('\\', '')
    
    # 只保留安全字符
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    
    # 限制長度
    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:90] + ('.' + ext if ext else '')
    
    return filename


def validate_content_type(content_type: str, allowed_types: list) -> bool:
    """
    驗證Content-Type是否在允許列表中
    
    Args:
        content_type: 請求的Content-Type
        allowed_types: 允許的Content-Type列表
        
    Returns:
        是否為允許的類型
    """
    if not content_type:
        return False
    
    # 提取主要類型
    main_type = content_type.split(';')[0].strip().lower()
    
    return main_type in [t.lower() for t in allowed_types]


def generate_nonce() -> str:
    """
    生成用於CSP的隨機nonce
    
    Returns:
        隨機nonce字符串
    """
    import secrets
    return secrets.token_urlsafe(16)