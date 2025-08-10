from typing import Dict, Any, Optional
from flask import g
from app import db
from app.models import EditRecord
from .base_service import BaseService


class AuditService(BaseService):
    """
    審計服務
    
    統一管理所有操作的審計記錄
    提供標準化的審計日誌接口
    """
    
    def get_module_id(self) -> int:
        return 0  # 管理員模組
    
    def get_module_name(self) -> str:
        return 'admin'
    
    # 模組ID映射
    MODULE_MAPPING = {
        'admin': 0,
        'lab': 1,
        'research_group': 2,
        'member': 3,
        'paper': 4,
        'news': 5,
        'project': 6
    }
    
    # 操作類型枚舉
    OPERATION_TYPES = [
        'CREATE', 'UPDATE', 'DELETE',
        'LOGIN', 'LOGOUT', 'CHANGE_PASSWORD',
        'BATCH_CREATE', 'BATCH_UPDATE', 'BATCH_DELETE',
        'UPLOAD', 'DOWNLOAD', 'EXPORT'
    ]
    
    @classmethod
    def get_module_id_by_name(cls, module_name: str) -> int:
        """
        根據模組名稱獲取模組ID
        
        Args:
            module_name: 模組名稱
            
        Returns:
            int: 模組ID
            
        Raises:
            ValueError: 未知的模組名稱
        """
        if module_name not in cls.MODULE_MAPPING:
            raise ValueError(f"未知的模組名稱: {module_name}")
        
        return cls.MODULE_MAPPING[module_name]
    
    def log_operation(self, 
                     module_name: str,
                     operation: str, 
                     content: Dict[str, Any] = None,
                     admin_id: Optional[int] = None) -> EditRecord:
        """
        記錄操作日誌
        
        Args:
            module_name: 模組名稱
            operation: 操作類型
            content: 操作內容
            admin_id: 管理員ID
            
        Returns:
            EditRecord: 創建的審計記錄
            
        Raises:
            ValueError: 參數錯誤
        """
        # 校驗操作類型
        if operation not in self.OPERATION_TYPES:
            raise ValueError(f"未知的操作類型: {operation}")
        
        # 獲取模組ID
        module_id = self.get_module_id_by_name(module_name)
        
        # 獲取管理員ID
        if admin_id is None:
            if hasattr(g, 'current_admin') and g.current_admin:
                admin_id = g.current_admin.admin_id
            else:
                # 對於某些系統操作，可能沒有當前管理員
                admin_id = None
        
        # 創建審計記錄
        record = EditRecord(
            admin_id=admin_id,
            edit_type=operation,
            edit_module=module_id
        )
        
        if content:
            record.set_content(content)
        
        db.session.add(record)
        return record
    
    def log_batch_operation(self,
                           module_name: str,
                           operation: str,
                           items: list,
                           extra_data: Dict[str, Any] = None,
                           admin_id: Optional[int] = None) -> EditRecord:
        """
        記錄批量操作日誌
        
        Args:
            module_name: 模組名稱
            operation: 操作類型
            items: 操作的項目列表
            extra_data: 額外數據
            admin_id: 管理員ID
            
        Returns:
            EditRecord: 創建的審計記錄
        """
        content = {
            'batch_operation': True,
            'items_count': len(items),
            'items': items[:50]  # 限制記錄數量，避免過大
        }
        
        if len(items) > 50:
            content['total_items'] = len(items)
        
        if extra_data:
            content.update(extra_data)
        
        return self.log_operation(
            module_name=module_name,
            operation=f"BATCH_{operation}",
            content=content,
            admin_id=admin_id
        )
    
    def log_login(self, admin_id: int, login_info: Dict[str, Any] = None) -> EditRecord:
        """
        記錄登錄操作
        
        Args:
            admin_id: 管理員ID
            login_info: 登錄信息（IP、瀏覽器等）
            
        Returns:
            EditRecord: 審計記錄
        """
        content = login_info or {}
        content.update({
            'admin_id': admin_id,
            'timestamp': content.get('timestamp', None)
        })
        
        return self.log_operation(
            module_name='admin',
            operation='LOGIN',
            content=content,
            admin_id=admin_id
        )
    
    def log_logout(self, admin_id: int, logout_info: Dict[str, Any] = None) -> EditRecord:
        """
        記錄登出操作
        
        Args:
            admin_id: 管理員ID
            logout_info: 登出信息
            
        Returns:
            EditRecord: 審計記錄
        """
        content = logout_info or {}
        content.update({
            'admin_id': admin_id
        })
        
        return self.log_operation(
            module_name='admin',
            operation='LOGOUT',
            content=content,
            admin_id=admin_id
        )
    
    def get_audit_records(self, 
                         filters: Dict[str, Any] = None,
                         page: int = 1,
                         per_page: int = 10) -> Dict[str, Any]:
        """
        獲取審計記錄列表
        
        Args:
            filters: 篩選條件
            page: 頁碼
            per_page: 每頁數量
            
        Returns:
            Dict: 分頁後的審計記錄
        """
        from app.utils.helpers import paginate_query
        
        query = EditRecord.query
        
        if filters:
            # 按管理員ID篩選
            if 'admin_id' in filters:
                query = query.filter(EditRecord.admin_id == filters['admin_id'])
            
            # 按模組篩選
            if 'edit_module' in filters:
                query = query.filter(EditRecord.edit_module == filters['edit_module'])
            
            # 按操作類型篩選
            if 'edit_type' in filters:
                query = query.filter(EditRecord.edit_type == filters['edit_type'])
            
            # 按日期範圍篩選
            if 'start_date' in filters:
                query = query.filter(EditRecord.edit_date >= filters['start_date'])
            
            if 'end_date' in filters:
                query = query.filter(EditRecord.edit_date <= filters['end_date'])
        
        # 按時間倒序排序
        query = query.order_by(EditRecord.edit_date.desc())
        
        return paginate_query(query, page, per_page)