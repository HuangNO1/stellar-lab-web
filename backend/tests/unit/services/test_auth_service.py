"""
AuthService 測試用例 (修復版)
測試管理員認證相關的服務層邏輯
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.auth_service import AuthService
from app.services.base_service import ValidationError, NotFoundError, PermissionError


class TestAuthService:
    """認證服務層測試"""
    
    @pytest.fixture
    def auth_service(self, app):
        """創建認證服務實例"""
        with app.app_context():
            return AuthService()
    
    @pytest.fixture
    def mock_admin_data(self):
        """模擬管理員數據"""
        return {
            'admin_id': 1,
            'admin_name': 'test_admin',
            'admin_email': 'test@example.com',
            'admin_type': 1,
            'enable': 1
        }
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_login_success(self, auth_service, mock_admin_data):
        """測試管理員登錄 - 成功場景"""
        # Arrange
        mock_admin = Mock()
        mock_admin.admin_id = 1
        mock_admin.admin_name = 'test_admin'
        mock_admin.admin_pass = 'hashed_password'
        mock_admin.enable = 1
        mock_admin.is_super = 0
        mock_admin.check_password.return_value = True  # Mock check_password method
        mock_admin.to_dict.return_value = mock_admin_data
        
        with patch('app.services.auth_service.Admin') as MockAdmin:
            MockAdmin.query.filter_by.return_value.first.return_value = mock_admin
            
            with patch('app.services.auth_service.jwt.encode') as mock_jwt:
                mock_jwt.return_value = 'mock_jwt_token'
                
                with patch.object(auth_service, 'execute_with_audit') as mock_audit:
                    mock_audit.return_value = {
                        'access_token': 'Bearer mock_jwt_token',
                        'expires_in': 86400,
                        'admin': mock_admin_data
                    }
                    
                    # Act
                    result = auth_service.login('test_admin', 'test_password')
                    
                    # Assert
                    assert 'access_token' in result
                    assert result['admin'] == mock_admin_data
                    mock_admin.check_password.assert_called_once_with('test_password')
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_login_empty_credentials(self, auth_service):
        """測試管理員登錄 - 空用戶名密碼"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            auth_service.login('', 'password')
        
        assert '用戶名和密碼不能為空' in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            auth_service.login('username', '')
        
        assert '用戶名和密碼不能為空' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_login_user_not_found(self, auth_service):
        """測試管理員登錄 - 用戶不存在"""
        # Arrange
        with patch('app.services.auth_service.Admin') as MockAdmin:
            MockAdmin.query.filter_by.return_value.first.return_value = None
            
            # Act & Assert
            with pytest.raises(NotFoundError) as exc_info:
                auth_service.login('nonexistent_user', 'password')
            
            assert '用戶名不存在' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_login_disabled_account(self, auth_service):
        """測試管理員登錄 - 賬號被禁用"""
        # Arrange
        mock_admin = Mock()
        mock_admin.enable = 0
        
        with patch('app.services.auth_service.Admin') as MockAdmin:
            MockAdmin.query.filter_by.return_value.first.return_value = mock_admin
            
            # Act & Assert
            with pytest.raises(PermissionError) as exc_info:
                auth_service.login('test_user', 'password')
            
            assert '賬戶已被禁用' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_login_wrong_password(self, auth_service):
        """測試管理員登錄 - 密碼錯誤"""
        # Arrange
        mock_admin = Mock()
        mock_admin.enable = 1
        mock_admin.admin_pass = 'hashed_password'
        mock_admin.check_password.return_value = False  # Mock check_password method
        
        with patch('app.services.auth_service.Admin') as MockAdmin:
            MockAdmin.query.filter_by.return_value.first.return_value = mock_admin
            
            # Act & Assert
            with pytest.raises(PermissionError) as exc_info:
                auth_service.login('test_user', 'wrong_password')
            
            assert '密碼錯誤' in str(exc_info.value)
            mock_admin.check_password.assert_called_once_with('wrong_password')
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_module_id(self, auth_service):
        """測試獲取模塊ID"""
        assert auth_service.get_module_id() == 0
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_module_name(self, auth_service):
        """測試獲取模塊名稱"""
        assert auth_service.get_module_name() == 'admin'