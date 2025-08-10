from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from flask import request
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import Admin
from config.config import Config
from .base_service import BaseService, ValidationError, NotFoundError, PermissionError


class AuthService(BaseService):
    """
    認證服務層
    
    負責用戶認證相關的業務邏輯：
    - 登錄驗證
    - JWT令牌管理
    - 密碼管理
    - 會話管理
    """
    
    def get_module_id(self) -> int:
        return 0
    
    def get_module_name(self) -> str:
        return 'admin'
    
    def login(self, admin_name: str, admin_pass: str, login_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        管理員登錄
        
        Args:
            admin_name: 管理員用戶名
            admin_pass: 管理員密碼
            login_info: 登錄附加信息（IP、瀏覽器等）
            
        Returns:
            Dict: 包含令牌和管理員信息的字典
            
        Raises:
            ValidationError: 參數錯誤
            NotFoundError: 用戶不存在
            PermissionError: 密碼錯誤或賬戶被禁用
        """
        # 數據校驗
        if not admin_name or not admin_pass:
            raise ValidationError('用戶名和密碼不能為空')
        
        # 查找管理員
        admin = Admin.query.filter_by(admin_name=admin_name).first()
        if not admin:
            raise NotFoundError('用戶名不存在')
        
        # 檢查賬戶狀態
        if not admin.enable:
            raise PermissionError('賬戶已被禁用')
        
        # 驗證密碼
        if not check_password_hash(admin.admin_pass, admin_pass):
            raise PermissionError('密碼錯誤')
        
        def _login_operation():
            # 生成JWT令牌
            token_data = {
                'admin_id': admin.admin_id,
                'admin_name': admin.admin_name,
                'is_super': admin.is_super,
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            
            access_token = jwt.encode(
                token_data,
                Config.JWT_SECRET_KEY,
                algorithm='HS256'
            )
            
            # 更新最後登錄時間
            admin.last_login = datetime.utcnow()
            
            return {
                'access_token': f'Bearer {access_token}',
                'expires_in': 86400,  # 24小時
                'admin': admin.to_dict()
            }
        
        # 執行登錄操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_login_operation,
            operation_type='LOGIN',
            content={
                'admin_name': admin_name,
                'login_time': datetime.utcnow().isoformat(),
                'login_info': login_info or {}
            },
            admin_id=admin.admin_id
        )
        
        return result
    
    def logout(self, admin_id: int, logout_info: Dict[str, Any] = None) -> None:
        """
        管理員登出
        
        Args:
            admin_id: 管理員ID
            logout_info: 登出附加信息
        """
        admin = Admin.query.get(admin_id)
        if not admin:
            raise NotFoundError('管理員不存在')
        
        def _logout_operation():
            # 這裡可以添加令牌黑名單邏輯
            # 或者更新最後登出時間等
            return {'admin_id': admin_id, 'logout_time': datetime.utcnow().isoformat()}
        
        # 執行登出操作並記錄審計
        self.execute_with_audit(
            operation_func=_logout_operation,
            operation_type='LOGOUT',
            content={
                'admin_id': admin_id,
                'logout_time': datetime.utcnow().isoformat(),
                'logout_info': logout_info or {}
            },
            admin_id=admin_id
        )
    
    def change_password(self, admin_id: int, old_password: str, new_password: str) -> None:
        """
        修改密碼
        
        Args:
            admin_id: 管理員ID
            old_password: 舊密碼
            new_password: 新密碼
            
        Raises:
            ValidationError: 參數錯誤
            NotFoundError: 管理員不存在
            PermissionError: 舊密碼錯誤
        """
        # 數據校驗
        if not old_password or not new_password:
            raise ValidationError('舊密碼和新密碼不能為空')
        
        if len(new_password) < 6:
            raise ValidationError('新密碼長度至少6位')
        
        # 查找管理員
        admin = Admin.query.get(admin_id)
        if not admin:
            raise NotFoundError('管理員不存在')
        
        # 驗證舊密碼
        if not check_password_hash(admin.admin_pass, old_password):
            raise PermissionError('舊密碼錯誤')
        
        def _change_password_operation():
            # 更新密碼
            admin.admin_pass = generate_password_hash(new_password)
            admin.updated_at = datetime.utcnow()
            
            return {'password_changed': True}
        
        # 執行操作並記錄審計
        self.execute_with_audit(
            operation_func=_change_password_operation,
            operation_type='CHANGE_PASSWORD',
            content={
                'admin_id': admin_id,
                'change_time': datetime.utcnow().isoformat()
            },
            admin_id=admin_id
        )
    
    def get_profile(self, admin_id: int) -> Dict[str, Any]:
        """
        獲取管理員資料
        
        Args:
            admin_id: 管理員ID
            
        Returns:
            Dict: 管理員資料
        """
        admin = Admin.query.get(admin_id)
        if not admin:
            raise NotFoundError('管理員不存在')
        
        return admin.to_dict()
    
    def update_profile(self, admin_id: int, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新管理員資料
        
        Args:
            admin_id: 管理員ID
            profile_data: 要更新的資料
            
        Returns:
            Dict: 更新後的管理員資料
        """
        admin = Admin.query.get(admin_id)
        if not admin:
            raise NotFoundError('管理員不存在')
        
        def _update_profile_operation():
            update_data = {}
            
            # 可更新的字段（排除敏感字段）
            allowed_fields = ['admin_name', 'email', 'phone', 'description']
            
            for field in allowed_fields:
                if field in profile_data:
                    old_value = getattr(admin, field, None)
                    new_value = profile_data[field]
                    
                    if old_value != new_value:
                        setattr(admin, field, new_value)
                        update_data[field] = {'old': old_value, 'new': new_value}
            
            if update_data:
                admin.updated_at = datetime.utcnow()
            
            return admin.to_dict(), update_data
        
        # 執行操作並記錄審計
        result, update_data = self.execute_with_audit(
            operation_func=_update_profile_operation,
            operation_type='UPDATE',
            content=update_data,
            admin_id=admin_id
        )
        
        return result
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        驗證JWT令牌
        
        Args:
            token: JWT令牌
            
        Returns:
            Dict: 解碼後的令牌數據，無效時返回None
        """
        try:
            # 移除 "Bearer " 前綴
            if token.startswith('Bearer '):
                token = token[7:]
            
            # 解碼令牌
            payload = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def get_admin_from_token(token: str) -> Optional[Admin]:
        """
        從令牌獲取管理員對象
        
        Args:
            token: JWT令牌
            
        Returns:
            Admin: 管理員對象，無效時返回None
        """
        payload = AuthService.verify_token(token)
        if not payload:
            return None
        
        admin_id = payload.get('admin_id')
        if not admin_id:
            return None
        
        admin = Admin.query.filter_by(admin_id=admin_id, enable=1).first()
        return admin