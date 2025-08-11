from typing import Optional, Dict, Any
from app.models import Admin
from app.utils.validators import validate_admin_name
from app.utils.helpers import get_pagination_params, paginate_query
from .base_service import BaseService, ValidationError, NotFoundError, BusinessLogicError


class AdminService(BaseService):
    """
    管理員管理服務層
    """
    
    def get_module_id(self) -> int:
        return 0
    
    def get_module_name(self) -> str:
        return 'admin'
    
    def get_admins_list(self, filters: Dict[str, Any] = None, current_admin_id: int = None) -> Dict[str, Any]:
        """獲取管理員列表"""
        query = Admin.query
        
        # 默認只顯示有效管理員
        if not filters or not filters.get('show_all', False):
            query = query.filter_by(enable=1)
        
        # 搜索關鍵字
        if filters and filters.get('q'):
            search_term = f"%{filters['q']}%"
            query = query.filter(Admin.admin_name.like(search_term))
        
        # 按創建時間倒序排序
        query = query.order_by(Admin.created_at.desc())
        
        # 分頁
        page, per_page = get_pagination_params()
        return paginate_query(query, page, per_page)
    
    def create_admin(self, admin_data: Dict[str, Any]) -> Dict[str, Any]:
        """創建管理員"""
        # 驗證權限 - 只有超級管理員可以創建管理員
        self.validate_permissions('CREATE')
        
        # 數據校驗
        self._validate_admin_data(admin_data, is_create=True)
        
        def _create_operation():
            # 檢查用戶名是否已存在
            existing_admin = Admin.query.filter_by(admin_name=admin_data['admin_name']).first()
            if existing_admin:
                raise BusinessLogicError('用戶名已存在')
            
            # 創建管理員
            admin = Admin(
                admin_name=admin_data['admin_name'],
                is_super=admin_data.get('is_super', 0),
                enable=1
            )
            admin.set_password(admin_data['admin_pass'])
            
            self.db.session.add(admin)
            self.db.session.flush()
            
            return admin.to_dict()
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_create_operation,
            operation_type='CREATE',
            content=admin_data
        )
        
        return result
    
    def update_admin(self, admin_id: int, admin_data: Dict[str, Any], current_admin_id: int) -> Dict[str, Any]:
        """更新管理員"""
        # 驗證權限 - 只有超級管理員可以更新管理員
        self.validate_permissions('UPDATE')
        
        admin = Admin.query.get(admin_id)
        if not admin:
            raise NotFoundError('管理員不存在')
        
        # 不能修改自己
        if admin_id == current_admin_id:
            raise BusinessLogicError('不能修改自己的賬戶')
        
        # 只有最高權限的超級管理員才能修改其他超級管理員
        if admin.is_super == 1:
            raise BusinessLogicError('不能修改其他超級管理員的賬戶')
        
        # 數據校驗
        self._validate_admin_data(admin_data, is_create=False)
        
        def _update_operation():
            update_data = {}
            
            # 更新用戶名
            if 'admin_name' in admin_data:
                new_name = admin_data['admin_name'].strip()
                
                # 檢查用戶名是否已被其他用戶使用
                existing = Admin.query.filter(
                    Admin.admin_name == new_name,
                    Admin.admin_id != admin_id
                ).first()
                if existing:
                    raise BusinessLogicError('用戶名已存在')
                
                if admin.admin_name != new_name:
                    update_data['admin_name'] = {'old': admin.admin_name, 'new': new_name}
                    admin.admin_name = new_name
            
            # 更新超級管理員狀態
            if 'is_super' in admin_data:
                new_is_super = int(admin_data['is_super'])
                if admin.is_super != new_is_super:
                    update_data['is_super'] = {'old': admin.is_super, 'new': new_is_super}
                    admin.is_super = new_is_super
            
            # 更新啟用狀態
            if 'enable' in admin_data:
                new_enable = int(admin_data['enable'])
                if admin.enable != new_enable:
                    update_data['enable'] = {'old': admin.enable, 'new': new_enable}
                    admin.enable = new_enable
            
            return admin.to_dict(), update_data
        
        # 先執行更新操作獲取變更詳情
        result, change_details = _update_operation()
        
        # 使用execute_with_audit記錄審計
        def _audit_operation():
            return result
            
        self.execute_with_audit(
            operation_func=_audit_operation,
            operation_type='UPDATE',
            content={'admin_id': admin_id, 'changes': change_details},
            admin_id=current_admin_id
        )
        
        return result
    
    def delete_admin(self, admin_id: int, current_admin_id: int) -> None:
        """刪除管理員"""
        # 驗證權限 - 只有超級管理員可以刪除管理員
        self.validate_permissions('DELETE')
        
        admin = Admin.query.get(admin_id)
        if not admin:
            raise NotFoundError('管理員不存在')
        
        # 不能刪除自己
        if admin_id == current_admin_id:
            raise BusinessLogicError('不能刪除自己的賬戶')
        
        # 只有最高權限的超級管理員才能刪除其他超級管理員
        if admin.is_super == 1:
            raise BusinessLogicError('不能刪除其他超級管理員的賬戶')
        
        def _delete_operation():
            # 軟刪除
            self.soft_delete(admin, "管理員")
            return {'deleted_admin_id': admin_id}
        
        # 執行操作並記錄審計
        self.execute_with_audit(
            operation_func=_delete_operation,
            operation_type='DELETE',
            content={'deleted_admin_id': admin_id}
        )
    
    def _validate_admin_data(self, admin_data: Dict[str, Any], is_create: bool = True) -> None:
        """校驗管理員數據"""
        if is_create:
            # 必填字段檢查
            required_fields = ['admin_name', 'admin_pass']
            self.validate_required_fields(admin_data, required_fields)
            
            # 密碼長度檢查
            if len(admin_data['admin_pass']) < 8:
                raise ValidationError('密碼長度至少8位')
        
        # 用戶名格式檢查
        if 'admin_name' in admin_data:
            if not validate_admin_name(admin_data['admin_name']):
                raise ValidationError('用戶名格式不正確，只能包含字母、數字、下劃線和連字符，長度3-50位')
        
        # 超級管理員狀態檢查
        if 'is_super' in admin_data:
            try:
                is_super_value = int(admin_data['is_super'])
                if is_super_value not in [0, 1]:
                    raise ValidationError('is_super參數錯誤')
                admin_data['is_super'] = is_super_value
            except (ValueError, TypeError):
                raise ValidationError('is_super參數格式錯誤')
        
        # 啟用狀態檢查
        if 'enable' in admin_data:
            try:
                enable_value = int(admin_data['enable'])
                if enable_value not in [0, 1]:
                    raise ValidationError('enable參數錯誤')
                admin_data['enable'] = enable_value
            except (ValueError, TypeError):
                raise ValidationError('enable參數格式錯誤')