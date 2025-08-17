"""
統一的國際化消息文本管理
用於管理後端返回給前端的中英文消息，支持多語言國際化
"""

from flask import request, has_request_context
from .messages_zh import SUCCESS_MESSAGES as SUCCESS_ZH, ERROR_MESSAGES as ERROR_ZH
from .messages_en import SUCCESS_MESSAGES as SUCCESS_EN, ERROR_MESSAGES as ERROR_EN


class Messages:
    """國際化消息管理類"""
    
    # 支持的語言
    SUPPORTED_LANGUAGES = ['zh', 'en']
    DEFAULT_LANGUAGE = 'zh'  # 默認語言為中文
    
    # 消息字典
    SUCCESS_MESSAGES = {
        'zh': SUCCESS_ZH,
        'en': SUCCESS_EN
    }
    
    ERROR_MESSAGES = {
        'zh': ERROR_ZH,
        'en': ERROR_EN
    }
    
    @classmethod
    def _get_current_language(cls) -> str:
        """
        安全獲取當前請求的語言設置
        
        Returns:
            語言代碼 (zh/en)
        """
        # 使用 Flask 的 has_request_context() 安全檢查
        if not has_request_context():
            # 不在請求上下文中，返回默認語言
            return cls.DEFAULT_LANGUAGE
            
        try:
            # 在請求上下文中，安全訪問 request
            # 優先使用 Accept-Language 頭
            accept_language = request.headers.get('Accept-Language', '').lower()
            if 'en' in accept_language:
                return 'en'
            elif 'zh' in accept_language:
                return 'zh'
            
            # 檢查自定義語言頭
            custom_lang = request.headers.get('X-Language', '').lower()
            if custom_lang in cls.SUPPORTED_LANGUAGES:
                return custom_lang
                
        except Exception:
            # 任何異常都返回默認語言
            pass
        
        # 默認返回中文
        return cls.DEFAULT_LANGUAGE
    
    @classmethod
    def get_success_message(cls, key: str, lang: str = None, **kwargs) -> str:
        """
        獲取成功消息
        
        Args:
            key: 消息鍵
            lang: 指定語言，如不指定則從請求頭獲取
            **kwargs: 格式化參數
            
        Returns:
            格式化後的消息
        """
        if lang is None:
            lang = cls._get_current_language()
        
        # 確保語言支持，如不支持則使用默認語言
        if lang not in cls.SUPPORTED_LANGUAGES:
            lang = cls.DEFAULT_LANGUAGE
        
        messages = cls.SUCCESS_MESSAGES.get(lang, cls.SUCCESS_MESSAGES[cls.DEFAULT_LANGUAGE])
        message = messages.get(key, key)
        
        if kwargs:
            try:
                return message.format(**kwargs)
            except (KeyError, ValueError):
                return message
        return message
    
    @classmethod
    def get_error_message(cls, key: str, lang: str = None, **kwargs) -> str:
        """
        獲取錯誤消息
        
        Args:
            key: 消息鍵
            lang: 指定語言，如不指定則從請求頭獲取
            **kwargs: 格式化參數
            
        Returns:
            格式化後的消息
        """
        if lang is None:
            lang = cls._get_current_language()
            
        # 確保語言支持，如不支持則使用默認語言
        if lang not in cls.SUPPORTED_LANGUAGES:
            lang = cls.DEFAULT_LANGUAGE
        
        messages = cls.ERROR_MESSAGES.get(lang, cls.ERROR_MESSAGES[cls.DEFAULT_LANGUAGE])
        message = messages.get(key, key)
        
        if kwargs:
            try:
                return message.format(**kwargs)
            except (KeyError, ValueError):
                return message
        return message
    
    @classmethod
    def format_field_length_error(cls, field: str, max_length: int, lang: str = None) -> str:
        """格式化字段長度錯誤消息"""
        return cls.get_error_message('FIELD_LENGTH_EXCEEDED', lang=lang, field=field, max_length=max_length)
    
    @classmethod
    def format_file_error(cls, error_type: str, lang: str = None, **kwargs) -> str:
        """格式化文件錯誤消息"""
        return cls.get_error_message(error_type, lang=lang, **kwargs)
    
    @classmethod
    def format_resource_error(cls, resource: str, error_type: str = 'NOT_FOUND', lang: str = None) -> str:
        """格式化資源錯誤消息"""
        if error_type == 'NOT_FOUND':
            return f"{resource}{cls.get_error_message('NOT_FOUND', lang=lang)}"
        return cls.get_error_message(error_type, lang=lang, resource=resource)
    
    # 保持向後兼容的舊屬性 (已廢棄，建議使用新方法)
    @property
    def SUCCESS(self):
        """向後兼容：獲取中文成功消息"""
        return self.SUCCESS_MESSAGES['zh']
    
    @property  
    def ERRORS(self):
        """向後兼容：獲取中文錯誤消息"""
        return self.ERROR_MESSAGES['zh']


# 簡化的消息快捷方式
msg = Messages()


def get_message(key, lang=None, **kwargs):
    """快捷獲取消息的函數"""
    try:
        # 先嘗試從成功消息中獲取
        return Messages.get_success_message(key, lang=lang, **kwargs)
    except:
        # 如果找不到，嘗試從錯誤消息中獲取
        return Messages.get_error_message(key, lang=lang, **kwargs)