from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Union
from flask import g
from app import db
from app.models import EditRecord


class ServiceException(Exception):
    """服務層異常基類"""
    pass


class ValidationError(ServiceException):
    """數據校驗異常"""
    pass


class NotFoundError(ServiceException):
    """資源不存在異常"""
    pass


class PermissionError(ServiceException):
    """權限不足異常"""
    pass


class BusinessLogicError(ServiceException):
    """業務邏輯異常"""
    pass


class BaseService(ABC):
    """
    基礎服務類
    
    提供所有服務的通用功能：
    - 資料庫事務管理
    - 審計記錄自動化
    - 統一異常處理
    - 權限校驗
    - 數據校驗基礎方法
    """
    
    def __init__(self):
        self.db = db
        self._audit_service = None
    
    @property
    def audit_service(self):
        """延遲加載審計服務，避免循環依賴"""
        if self._audit_service is None:
            from .audit_service import AuditService
            self._audit_service = AuditService()
        return self._audit_service
    
    @abstractmethod
    def get_module_id(self) -> int:
        """
        獲取當前服務對應的模組ID
        
        Returns:
            int: 模組ID (0-6)
        """
        pass
    
    @abstractmethod
    def get_module_name(self) -> str:
        """
        獲取當前服務對應的模組名稱
        
        Returns:
            str: 模組名稱
        """
        pass
    
    def execute_with_audit(self, 
                          operation_func,
                          operation_type: str,
                          content: Dict[str, Any] = None,
                          admin_id: Optional[int] = None):
        """
        執行操作並自動創建審計記錄
        
        Args:
            operation_func: 要執行的操作函數
            operation_type: 操作類型 (CREATE, UPDATE, DELETE, etc.)
            content: 操作內容
            admin_id: 管理員ID
            
        Returns:
            操作函數的返回值
            
        Raises:
            ServiceException: 操作失敗時拋出相應異常
        """
        try:
            # 執行業務操作
            result = operation_func()
            
            # 創建審計記錄
            self.audit_service.log_operation(
                module_name=self.get_module_name(),
                operation=operation_type,
                content=content or {},
                admin_id=admin_id
            )
            
            # 提交事務
            self.db.session.commit()
            
            return result
            
        except Exception as e:
            self.db.session.rollback()
            
            # 轉換為服務層異常
            if isinstance(e, ServiceException):
                raise e
            else:
                raise ServiceException(f"操作失敗: {str(e)}")
    
    def validate_required_fields(self, 
                                data: Dict[str, Any], 
                                required_fields: List[str]) -> None:
        """
        校驗必填字段
        
        Args:
            data: 要校驗的資料
            required_fields: 必填字段列表
            
        Raises:
            ValidationError: 缺少必填字段
        """
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                missing_fields.append(field)
        
        if missing_fields:
            raise ValidationError(f"缺少必填字段: {', '.join(missing_fields)}")
    
    def validate_permissions(self, 
                           operation: str,
                           resource_id: Optional[int] = None) -> None:
        """
        驗證當前用戶是否有執行指定操作的權限
        
        Args:
            operation: 操作類型
            resource_id: 資源ID（可選）
            
        Raises:
            PermissionError: 權限不足
        """
        # 檢查是否在請求上下文中
        try:
            from flask import has_request_context
            if not has_request_context():
                return True
        except ImportError:
            pass
        
        if not hasattr(g, 'current_admin') or g.current_admin is None:
            raise PermissionError("未登錄或登錄已過期")
        
        # 子類可以重寫此方法實現更複雜的權限控制
        return True
    
    def get_current_admin_id(self) -> int:
        """
        獲取當前登錄管理員ID
        
        Returns:
            int: 管理員ID
            
        Raises:
            PermissionError: 未登錄
        """
        if not hasattr(g, 'current_admin') or g.current_admin is None:
            raise PermissionError("未登錄或登錄已過期")
        
        return g.current_admin.admin_id
    
    def validate_pagination_params(self, 
                                  page: Optional[int] = None, 
                                  per_page: Optional[int] = None) -> tuple:
        """
        校驗分頁參數
        
        Args:
            page: 頁碼
            per_page: 每頁數量
            
        Returns:
            tuple: (page, per_page)
        """
        if page is not None and page < 1:
            page = 1
        if per_page is not None and per_page < 1:
            per_page = 10
        if per_page is not None and per_page > 100:
            per_page = 100
            
        return page, per_page
    
    def format_error_response(self, error: Exception) -> Dict[str, Any]:
        """
        格式化錯誤響應
        
        Args:
            error: 異常對象
            
        Returns:
            Dict: 錯誤響應格式
        """
        if isinstance(error, ValidationError):
            return {"code": 2000, "message": str(error)}
        elif isinstance(error, NotFoundError):
            return {"code": 3000, "message": str(error)}
        elif isinstance(error, PermissionError):
            return {"code": 1001, "message": str(error)}
        elif isinstance(error, BusinessLogicError):
            return {"code": 4000, "message": str(error)}
        else:
            return {"code": 5000, "message": "伺服器內部錯誤"}
    
    def soft_delete(self, model_instance, resource_name: str = "資源") -> None:
        """
        軟刪除資源
        
        Args:
            model_instance: 模型實例
            resource_name: 資源名稱
        """
        if not hasattr(model_instance, 'enable'):
            raise ServiceException(f"{resource_name}不支持軟刪除")
        
        if model_instance.enable == 0:
            raise NotFoundError(f"{resource_name}不存在或已被刪除")
        
        model_instance.enable = 0