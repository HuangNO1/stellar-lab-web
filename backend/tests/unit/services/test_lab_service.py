"""
LabService 測試用例
測試實驗室管理相關的服務層邏輯
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.lab_service import LabService
from app.services.base_service import ServiceException, ValidationError, NotFoundError
from app.models.lab import Lab


class TestLabService:
    """實驗室服務層測試"""
    
    @pytest.fixture
    def lab_service(self):
        """創建實驗室服務實例"""
        return LabService()
    
    @pytest.fixture
    def mock_lab_data(self):
        """模擬實驗室數據"""
        return {
            'lab_id': 1,
            'lab_zh': '測試實驗室',
            'lab_en': 'Test Laboratory',
            'lab_desc_zh': '這是一個測試實驗室',
            'lab_desc_en': 'This is a test laboratory',
            'lab_email': 'test@lab.edu.cn',
            'lab_phone': '+86-10-12345678',
            'lab_address_zh': '測試地址',
            'lab_address_en': 'Test Address',
            'lab_logo_path': '/media/lab_logo/test.jpg',
            'carousel_img_1': '/media/lab_logo/carousel1.jpg',
            'enable': 1
        }
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_lab_info_success(self, lab_service, mock_lab_data):
        """測試獲取實驗室信息 - 成功場景"""
        # Arrange
        mock_lab = Mock(spec=Lab)
        mock_lab.to_dict.return_value = mock_lab_data
        
        with patch.object(Lab, 'query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_lab
            
            # Act
            result = lab_service.get_lab_info()
            
            # Assert
            assert result == mock_lab_data
            mock_query.filter_by.assert_called_once_with(enable=1)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_lab_info_not_found(self, lab_service):
        """測試獲取實驗室信息 - 實驗室不存在"""
        # Arrange
        with patch.object(Lab, 'query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = None
            
            # Act & Assert
            with pytest.raises(NotFoundError) as exc_info:
                lab_service.get_lab_info()
            
            assert '實驗室信息不存在' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_update_lab_info_success(self, lab_service, mock_lab_data):
        """測試更新實驗室信息 - 成功場景"""
        # Arrange
        update_data = {
            'lab_zh': '更新的實驗室',
            'lab_email': 'updated@lab.edu.cn'
        }
        
        mock_lab = Mock(spec=Lab)
        mock_lab.lab_id = 1
        
        with patch.object(Lab, 'query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_lab
            
            with patch.object(lab_service, 'execute_with_audit') as mock_audit:
                mock_audit.return_value = mock_lab_data
                
                # Act
                result = lab_service.update_lab_info(update_data)
                
                # Assert
                assert result == mock_lab_data
                mock_audit.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_create_lab_info_success(self, lab_service, mock_lab_data):
        """測試創建實驗室信息 - 成功場景"""
        # Arrange
        create_data = {
            'lab_zh': '新實驗室',
            'lab_en': 'New Laboratory',
            'lab_email': 'new@lab.edu.cn'
        }
        
        # 檢查實驗室不存在
        with patch.object(Lab, 'query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = None
            
            with patch.object(lab_service, 'execute_with_audit') as mock_audit:
                mock_audit.return_value = mock_lab_data
                
                # Act
                result = lab_service.create_lab_info(create_data)
                
                # Assert
                assert result == mock_lab_data
                mock_audit.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_create_lab_info_already_exists(self, lab_service):
        """測試創建實驗室信息 - 實驗室已存在"""
        # Arrange
        create_data = {
            'lab_zh': '已存在的實驗室',
            'lab_email': 'existing@lab.edu.cn'
        }
        
        mock_lab = Mock(spec=Lab)
        
        with patch.object(Lab, 'query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_lab
            
            # Act & Assert
            with pytest.raises(ValidationError) as exc_info:
                lab_service.create_lab_info(create_data)
            
            assert '實驗室信息已存在' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_delete_lab_success(self, lab_service):
        """測試刪除實驗室 - 成功場景"""
        # Arrange
        mock_lab = Mock(spec=Lab)
        mock_lab.lab_id = 1
        
        with patch.object(Lab, 'query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_lab
            
            # 檢查沒有關聯數據
            with patch.object(lab_service, '_check_lab_associations') as mock_check:
                mock_check.return_value = True
                
                with patch.object(lab_service, 'execute_with_audit') as mock_audit:
                    mock_audit.return_value = {'message': '刪除成功'}
                    
                    # Act
                    result = lab_service.delete_lab()
                    
                    # Assert
                    assert result['message'] == '刪除成功'
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_delete_lab_with_associations(self, lab_service):
        """測試刪除實驗室 - 存在關聯數據"""
        # Arrange
        mock_lab = Mock(spec=Lab)
        mock_lab.lab_id = 1
        
        with patch.object(Lab, 'query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_lab
            
            # 檢查存在關聯數據
            with patch.object(lab_service, '_check_lab_associations') as mock_check:
                mock_check.return_value = False
                
                # Act & Assert
                with pytest.raises(ValidationError) as exc_info:
                    lab_service.delete_lab()
                
                assert '存在關聯數據，無法刪除' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_upload_lab_logo_success(self, lab_service, mock_lab_data):
        """測試上傳實驗室Logo - 成功場景"""
        # Arrange
        mock_file = Mock()
        mock_file.filename = 'test_logo.jpg'
        mock_file.read.return_value = b'fake_image_data'
        
        mock_lab = Mock(spec=Lab)
        mock_lab.lab_id = 1
        
        with patch.object(Lab, 'query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_lab
            
            with patch('app.services.lab_service.save_upload_file') as mock_save:
                mock_save.return_value = '/media/lab_logo/test_logo.jpg'
                
                with patch.object(lab_service, 'execute_with_audit') as mock_audit:
                    mock_audit.return_value = mock_lab_data
                    
                    # Act
                    result = lab_service.upload_lab_logo(mock_file)
                    
                    # Assert
                    assert result == mock_lab_data
                    mock_save.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_upload_carousel_images_success(self, lab_service, mock_lab_data):
        """測試上傳輪播圖片 - 成功場景"""
        # Arrange
        mock_files = {
            'carousel_img_1': Mock(),
            'carousel_img_2': Mock()
        }
        
        for mock_file in mock_files.values():
            mock_file.filename = 'test_carousel.jpg'
            mock_file.read.return_value = b'fake_image_data'
        
        mock_lab = Mock(spec=Lab)
        mock_lab.lab_id = 1
        
        with patch.object(Lab, 'query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_lab
            
            with patch('app.services.lab_service.save_upload_file') as mock_save:
                mock_save.return_value = '/media/lab_logo/test_carousel.jpg'
                
                with patch.object(lab_service, 'execute_with_audit') as mock_audit:
                    mock_audit.return_value = mock_lab_data
                    
                    # Act
                    result = lab_service.upload_carousel_images(mock_files)
                    
                    # Assert
                    assert result == mock_lab_data
                    assert mock_save.call_count == 2
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_validate_email_format_valid(self, lab_service):
        """測試郵箱格式驗證 - 有效郵箱"""
        # Arrange & Act & Assert
        assert lab_service._validate_email_format('test@example.com') == True
        assert lab_service._validate_email_format('user.name@domain.edu.cn') == True
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_validate_email_format_invalid(self, lab_service):
        """測試郵箱格式驗證 - 無效郵箱"""
        # Arrange & Act & Assert
        assert lab_service._validate_email_format('invalid_email') == False
        assert lab_service._validate_email_format('test@') == False
        assert lab_service._validate_email_format('@domain.com') == False