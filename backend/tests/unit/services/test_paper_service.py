"""
PaperService 測試用例
測試論文管理相關的服務層邏輯
"""

import pytest
from unittest.mock import Mock, patch
from app.services.paper_service import PaperService
from app.services.base_service import ValidationError, NotFoundError
from app.models.paper import Paper


class TestPaperService:
    """論文服務層測試"""
    
    @pytest.fixture
    def paper_service(self):
        """創建論文服務實例"""
        return PaperService()
    
    @pytest.fixture
    def mock_paper_data(self):
        """模擬論文數據"""
        return {
            'paper_id': 1,
            'paper_title': '深度學習在計算機視覺中的應用',
            'paper_authors': '張三,李四',
            'paper_journal': 'IEEE Transactions on Pattern Analysis',
            'paper_year': '2023',
            'paper_link': 'https://doi.org/10.1109/example',
            'paper_abstract': '本文介紹了深度學習技術...',
            'paper_file_path': '/media/paper/paper_1.pdf',
            'lab_id': 1,
            'enable': 1
        }
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_papers_list_success(self, paper_service, mock_paper_data):
        """測試獲取論文列表 - 成功場景"""
        # Arrange
        filters = {'page': 1, 'per_page': 10}
        
        mock_paper = Mock(spec=Paper)
        mock_paper.to_dict.return_value = mock_paper_data
        
        mock_pagination = Mock()
        mock_pagination.items = [mock_paper]
        mock_pagination.total = 1
        
        with patch.object(Paper, 'query') as mock_query:
            mock_query.filter_by.return_value.order_by.return_value.paginate.return_value = mock_pagination
            
            # Act
            result = paper_service.get_papers_list(filters)
            
            # Assert
            assert len(result['items']) == 1
            assert result['total'] == 1
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_create_paper_success(self, paper_service, mock_paper_data):
        """測試創建論文 - 成功場景"""
        # Arrange
        create_data = {
            'paper_title': '新論文',
            'paper_authors': '作者1,作者2',
            'paper_journal': '期刊名稱',
            'paper_year': '2024'
        }
        
        with patch.object(paper_service, 'execute_with_audit') as mock_audit:
            mock_audit.return_value = mock_paper_data
            
            # Act
            result = paper_service.create_paper(create_data)
            
            # Assert
            assert result == mock_paper_data
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_create_paper_with_file_upload(self, paper_service, mock_paper_data):
        """測試創建論文 - 帶PDF文件上傳"""
        # Arrange
        create_data = {
            'paper_title': '新論文',
            'paper_authors': '作者1,作者2'
        }
        
        mock_file = Mock()
        mock_file.filename = 'paper.pdf'
        mock_file.read.return_value = b'fake_pdf_data'
        
        with patch('app.services.paper_service.save_upload_file') as mock_save:
            mock_save.return_value = '/media/paper/paper.pdf'
            
            with patch.object(paper_service, 'execute_with_audit') as mock_audit:
                mock_audit.return_value = mock_paper_data
                
                # Act
                result = paper_service.create_paper(create_data, paper_file=mock_file)
                
                # Assert
                assert result == mock_paper_data
                mock_save.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_paper_by_id_success(self, paper_service, mock_paper_data):
        """測試根據ID獲取論文 - 成功場景"""
        # Arrange
        paper_id = 1
        
        mock_paper = Mock(spec=Paper)
        mock_paper.to_dict.return_value = mock_paper_data
        
        with patch.object(Paper, 'query') as mock_query:
            mock_query.get.return_value = mock_paper
            
            # Act
            result = paper_service.get_paper_by_id(paper_id)
            
            # Assert
            assert result == mock_paper_data