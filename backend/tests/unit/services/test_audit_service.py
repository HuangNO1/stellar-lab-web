"""
AuditService 測試用例 (修復版)
測試審計服務相關的服務層邏輯
"""

import pytest
from unittest.mock import Mock, patch
from app.services.audit_service import AuditService


class TestAuditService:
    """審計服務層測試"""
    
    @pytest.fixture
    def audit_service(self):
        """創建審計服務實例"""
        return AuditService()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_module_id_by_name_success(self, audit_service):
        """測試根據模組名稱獲取ID - 成功場景"""
        # Act & Assert
        assert audit_service.get_module_id_by_name('admin') == 0
        assert audit_service.get_module_id_by_name('lab') == 1
        assert audit_service.get_module_id_by_name('member') == 3
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_module_id_by_name_invalid(self, audit_service):
        """測試根據模組名稱獲取ID - 無效模組名"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            audit_service.get_module_id_by_name('invalid_module')
        
        assert '未知的模組名稱' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_log_operation_success(self, audit_service):
        """測試記錄操作日誌 - 成功場景"""
        # Arrange
        module_name = 'member'
        operation = 'CREATE'
        content = {'member_name_zh': '張三'}
        admin_id = 1
        
        mock_record = Mock()
        mock_record.edit_record_id = 1
        mock_record.set_content = Mock()
        
        with patch('app.services.audit_service.EditRecord') as MockEditRecord, \
             patch('app.services.audit_service.db') as mock_db:
            
            MockEditRecord.return_value = mock_record
            
            # Act
            result = audit_service.log_operation(module_name, operation, content, admin_id)
            
            # Assert
            assert result == mock_record
            MockEditRecord.assert_called_once_with(
                admin_id=admin_id,
                edit_type=operation,
                edit_module=3  # member module id
            )
            mock_record.set_content.assert_called_once_with(content)
            mock_db.session.add.assert_called_once_with(mock_record)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_log_operation_invalid_operation(self, audit_service):
        """測試記錄操作日誌 - 無效操作類型"""
        # Arrange
        module_name = 'member'
        operation = 'INVALID_OPERATION'
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            audit_service.log_operation(module_name, operation)
        
        assert '未知的操作類型' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_log_operation_without_content(self, audit_service):
        """測試記錄操作日誌 - 無內容"""
        # Arrange
        module_name = 'member'
        operation = 'CREATE'
        admin_id = 1
        
        mock_record = Mock()
        
        with patch('app.services.audit_service.EditRecord') as MockEditRecord, \
             patch('app.services.audit_service.db') as mock_db:
            
            MockEditRecord.return_value = mock_record
            
            # Act
            result = audit_service.log_operation(module_name, operation, None, admin_id)
            
            # Assert
            assert result == mock_record
            MockEditRecord.assert_called_once_with(
                admin_id=admin_id,
                edit_type=operation,
                edit_module=3
            )
            # set_content should not be called when content is None
            assert not hasattr(mock_record, 'set_content') or not mock_record.set_content.called
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_log_batch_operation_success(self, audit_service):
        """測試記錄批量操作日誌"""
        # Arrange
        module_name = 'member'
        operation = 'CREATE'
        items = [{'id': 1}, {'id': 2}, {'id': 3}]
        admin_id = 1
        
        mock_record = Mock()
        
        with patch.object(audit_service, 'log_operation') as mock_log_op:
            mock_log_op.return_value = mock_record
            
            # Act
            result = audit_service.log_batch_operation(module_name, operation, items, None, admin_id)
            
            # Assert
            assert result == mock_record
            mock_log_op.assert_called_once_with(
                module_name=module_name,
                operation='BATCH_CREATE',
                content={
                    'batch_operation': True,
                    'items_count': 3,
                    'items': items
                },
                admin_id=admin_id
            )
    
    @pytest.mark.unit
    @pytest.mark.service 
    def test_log_login_success(self, audit_service):
        """測試記錄登錄操作"""
        # Arrange
        admin_id = 1
        login_info = {'ip': '127.0.0.1', 'user_agent': 'Mozilla/5.0'}
        mock_record = Mock()
        
        with patch.object(audit_service, 'log_operation') as mock_log_op:
            mock_log_op.return_value = mock_record
            
            # Act
            result = audit_service.log_login(admin_id, login_info)
            
            # Assert
            assert result == mock_record
            mock_log_op.assert_called_once()
            args, kwargs = mock_log_op.call_args
            assert kwargs['module_name'] == 'admin'
            assert kwargs['operation'] == 'LOGIN'
            assert kwargs['admin_id'] == admin_id
            assert 'admin_id' in kwargs['content']
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_log_logout_success(self, audit_service):
        """測試記錄登出操作"""
        # Arrange
        admin_id = 1
        logout_info = {'reason': 'manual'}
        mock_record = Mock()
        
        with patch.object(audit_service, 'log_operation') as mock_log_op:
            mock_log_op.return_value = mock_record
            
            # Act
            result = audit_service.log_logout(admin_id, logout_info)
            
            # Assert
            assert result == mock_record
            mock_log_op.assert_called_once()
            args, kwargs = mock_log_op.call_args
            assert kwargs['module_name'] == 'admin'
            assert kwargs['operation'] == 'LOGOUT'
            assert kwargs['admin_id'] == admin_id
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_audit_records_success(self, audit_service):
        """測試獲取審計記錄列表"""
        # Arrange
        filters = {'admin_id': 1}
        expected_result = {
            'items': [{'edit_record_id': 1}],
            'total': 1,
            'page': 1,
            'per_page': 10
        }
        
        with patch('app.services.audit_service.EditRecord') as MockEditRecord, \
             patch('app.utils.helpers.paginate_query') as mock_paginate:
            
            mock_paginate.return_value = expected_result
            
            # Act
            result = audit_service.get_audit_records(filters, 1, 10)
            
            # Assert
            assert result == expected_result
            mock_paginate.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_module_id(self, audit_service):
        """測試獲取模塊ID"""
        assert audit_service.get_module_id() == 0
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_module_name(self, audit_service):
        """測試獲取模塊名稱"""
        assert audit_service.get_module_name() == 'admin'
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_operation_types_defined(self, audit_service):
        """測試操作類型常量是否正確定義"""
        expected_types = [
            'CREATE', 'UPDATE', 'DELETE',
            'LOGIN', 'LOGOUT', 'CHANGE_PASSWORD',
            'BATCH_CREATE', 'BATCH_UPDATE', 'BATCH_DELETE',
            'UPLOAD', 'DOWNLOAD', 'EXPORT'
        ]
        
        assert audit_service.OPERATION_TYPES == expected_types
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_module_mapping_defined(self, audit_service):
        """測試模組映射是否正確定義"""
        expected_mapping = {
            'admin': 0,
            'lab': 1,
            'research_group': 2,
            'member': 3,
            'paper': 4,
            'news': 5,
            'project': 6
        }
        
        assert audit_service.MODULE_MAPPING == expected_mapping