"""
BaseService 測試用例
測試基礎服務層的核心功能
"""

import pytest
from unittest.mock import Mock, patch
from app.services.base_service import BaseService, ValidationError, NotFoundError, BusinessLogicError
from app.models.edit_record import EditRecord
from app import db


class TestBaseService:
    """基礎服務層測試"""
    
    @pytest.fixture
    def base_service(self):
        """創建基礎服務實例"""
        return BaseService()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_validate_permissions_success(self, base_service):
        """測試權限驗證 - 成功場景"""
        # Arrange
        with patch.object(base_service, 'get_current_admin_id', return_value=1):
            with patch.object(base_service, 'check_admin_permission', return_value=True):
                
                # Act & Assert (should not raise exception)
                base_service.validate_permissions('CREATE')
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_validate_permissions_no_admin(self, base_service):
        """測試權限驗證 - 未登錄"""
        # Arrange
        with patch.object(base_service, 'get_current_admin_id', return_value=None):
            
            # Act & Assert
            with pytest.raises(ValidationError) as exc_info:
                base_service.validate_permissions('CREATE')
            
            assert '未登錄或權限不足' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_validate_permissions_insufficient(self, base_service):
        """測試權限驗證 - 權限不足"""
        # Arrange
        with patch.object(base_service, 'get_current_admin_id', return_value=1):
            with patch.object(base_service, 'check_admin_permission', return_value=False):
                
                # Act & Assert
                with pytest.raises(ValidationError) as exc_info:
                    base_service.validate_permissions('DELETE')
                
                assert '權限不足' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_execute_with_audit_success(self, base_service):
        """測試事務執行與審計 - 成功場景"""
        # Arrange
        def mock_operation():
            return {'test': 'data'}
        
        with patch.object(base_service, 'get_current_admin_id', return_value=1):
            with patch.object(db.session, 'add'):
                with patch.object(db.session, 'commit'):
                    with patch.object(db.session, 'flush'):
                        
                        # Act
                        result = base_service.execute_with_audit(
                            operation_func=mock_operation,
                            operation_type='CREATE',
                            content={'test': 'content'}
                        )
                        
                        # Assert
                        assert result == {'test': 'data'}
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_execute_with_audit_rollback_on_error(self, base_service):
        """測試事務執行與審計 - 異常回滾"""
        # Arrange
        def mock_operation():
            raise Exception('Test error')
        
        with patch.object(base_service, 'get_current_admin_id', return_value=1):
            with patch.object(db.session, 'rollback') as mock_rollback:
                
                # Act & Assert
                with pytest.raises(Exception):
                    base_service.execute_with_audit(
                        operation_func=mock_operation,
                        operation_type='CREATE',
                        content={'test': 'content'}
                    )
                
                mock_rollback.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_create_audit_record_success(self, base_service):
        """測試創建審計記錄 - 成功場景"""
        # Arrange
        audit_data = {
            'admin_id': 1,
            'table_name': 'test_table',
            'record_id': 1,
            'operation_type': 'CREATE',
            'old_data': None,
            'new_data': '{"test": "data"}'
        }
        
        with patch.object(db.session, 'add') as mock_add:
            with patch.object(db.session, 'flush'):
                
                # Act
                base_service.create_audit_record(audit_data)
                
                # Assert
                mock_add.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_format_error_response(self, base_service):
        """測試錯誤響應格式化"""
        # Arrange
        validation_error = ValidationError('測試驗證錯誤')
        not_found_error = NotFoundError('測試未找到錯誤')
        business_error = BusinessLogicError('測試業務邏輯錯誤')
        
        # Act & Assert
        validation_result = base_service.format_error_response(validation_error)
        assert validation_result['code'] == 2000
        assert validation_result['message'] == '測試驗證錯誤'
        
        not_found_result = base_service.format_error_response(not_found_error)
        assert not_found_result['code'] == 3000
        assert not_found_result['message'] == '測試未找到錯誤'
        
        business_result = base_service.format_error_response(business_error)
        assert business_result['code'] == 4000
        assert business_result['message'] == '測試業務邏輯錯誤'
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_module_id_not_implemented(self, base_service):
        """測試模塊ID獲取 - 未實現"""
        # Act & Assert
        with pytest.raises(NotImplementedError):
            base_service.get_module_id()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_module_name_not_implemented(self, base_service):
        """測試模塊名稱獲取 - 未實現"""
        # Act & Assert
        with pytest.raises(NotImplementedError):
            base_service.get_module_name()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_validate_required_fields_success(self, base_service):
        """測試必填字段驗證 - 成功場景"""
        # Arrange
        data = {'name': 'test', 'email': 'test@example.com'}
        required_fields = ['name', 'email']
        
        # Act & Assert (should not raise exception)
        base_service._validate_required_fields(data, required_fields)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_validate_required_fields_missing(self, base_service):
        """測試必填字段驗證 - 缺少字段"""
        # Arrange
        data = {'name': 'test'}
        required_fields = ['name', 'email']
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            base_service._validate_required_fields(data, required_fields)
        
        assert '缺少必填字段' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_sanitize_input_data(self, base_service):
        """測試輸入數據清理"""
        # Arrange
        input_data = {
            'name': '  test name  ',
            'description': '<script>alert("xss")</script>',
            'empty_field': '',
            'none_field': None
        }
        
        # Act
        result = base_service._sanitize_input_data(input_data)
        
        # Assert
        assert result['name'] == 'test name'
        assert '<script>' not in result['description']
        assert 'empty_field' not in result
        assert 'none_field' not in result