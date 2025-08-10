"""
MediaService 測試用例
測試媒體文件管理相關的服務層邏輯
"""

import pytest
from unittest.mock import Mock, patch
from app.services.media_service import MediaService
from app.services.base_service import ValidationError, NotFoundError


class TestMediaService:
    """媒體服務層測試"""
    
    @pytest.fixture
    def media_service(self):
        """創建媒體服務實例"""
        return MediaService()
    
    @pytest.fixture
    def mock_file(self):
        """模擬上傳文件"""
        mock_file = Mock()
        mock_file.filename = 'test_image.jpg'
        mock_file.content_type = 'image/jpeg'
        mock_file.read.return_value = b'fake_image_data'
        return mock_file
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_upload_file_success(self, media_service, mock_file):
        """測試文件上傳 - 成功場景"""
        # Arrange
        with patch('app.services.media_service.save_upload_file') as mock_save:
            mock_save.return_value = '/media/other/test_image.jpg'
            
            with patch('app.services.media_service.get_file_size') as mock_size:
                mock_size.return_value = 1024000  # 1MB
                
                # Act
                result = media_service.upload_file(mock_file)
                
                # Assert
                assert result['file_path'] == '/media/other/test_image.jpg'
                assert result['file_name'] == 'test_image.jpg'
                assert result['file_size'] == 1024000
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_upload_file_invalid_type(self, media_service):
        """測試文件上傳 - 無效文件類型"""
        # Arrange
        mock_file = Mock()
        mock_file.filename = 'test.exe'
        mock_file.content_type = 'application/x-executable'
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            media_service.upload_file(mock_file)
        
        assert '不支持的文件類型' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_upload_file_too_large(self, media_service, mock_file):
        """測試文件上傳 - 文件過大"""
        # Arrange
        mock_file.read.return_value = b'x' * (6 * 1024 * 1024)  # 6MB
        
        with patch('app.services.media_service.get_file_size') as mock_size:
            mock_size.return_value = 6 * 1024 * 1024  # 6MB
            
            # Act & Assert
            with pytest.raises(ValidationError) as exc_info:
                media_service.upload_file(mock_file)
            
            assert '文件太大' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_file_info_success(self, media_service):
        """測試獲取文件信息 - 成功場景"""
        # Arrange
        file_path = 'other/test_image.jpg'
        
        with patch('os.path.exists', return_value=True):
            with patch('os.path.getsize', return_value=1024000):
                with patch('os.path.getmtime', return_value=1640995200):
                    
                    # Act
                    result = media_service.get_file_info(file_path)
                    
                    # Assert
                    assert result['file_name'] == 'test_image.jpg'
                    assert result['file_size'] == 1024000
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_serve_file_success(self, media_service):
        """測試文件服務 - 成功場景"""
        # Arrange
        file_path = 'other/test_image.jpg'
        
        with patch('os.path.exists', return_value=True):
            with patch('flask.send_from_directory') as mock_send:
                mock_send.return_value = 'file_response'
                
                # Act
                result = media_service.serve_file(file_path)
                
                # Assert
                assert result == 'file_response'
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_serve_file_not_found(self, media_service):
        """測試文件服務 - 文件不存在"""
        # Arrange
        file_path = 'other/nonexistent.jpg'
        
        with patch('os.path.exists', return_value=False):
            
            # Act & Assert
            with pytest.raises(NotFoundError) as exc_info:
                media_service.serve_file(file_path)
            
            assert '文件不存在' in str(exc_info.value)