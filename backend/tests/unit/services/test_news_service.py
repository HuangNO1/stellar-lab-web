"""
NewsService 測試用例
測試新聞管理相關的服務層邏輯
"""

import pytest
from unittest.mock import Mock, patch
from app.services.news_service import NewsService
from app.services.base_service import ValidationError, NotFoundError
from app.models.news import News


class TestNewsService:
    """新聞服務層測試"""
    
    @pytest.fixture
    def news_service(self):
        """創建新聞服務實例"""
        return NewsService()
    
    @pytest.fixture
    def mock_news_data(self):
        """模擬新聞數據"""
        return {
            'news_id': 1,
            'news_title_zh': '實驗室最新成果發布',
            'news_title_en': 'Latest Research Results Published',
            'news_content_zh': '我們的研究團隊發布了最新成果...',
            'news_content_en': 'Our research team published latest results...',
            'news_date': '2024-01-15',
            'enable': 1
        }
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_news_list_success(self, news_service, mock_news_data):
        """測試獲取新聞列表 - 成功場景"""
        # Arrange
        filters = {'page': 1, 'per_page': 10}
        
        mock_news = Mock(spec=News)
        mock_news.to_dict.return_value = mock_news_data
        
        mock_pagination = Mock()
        mock_pagination.items = [mock_news]
        mock_pagination.total = 1
        
        with patch.object(News, 'query') as mock_query:
            mock_query.filter_by.return_value.order_by.return_value.paginate.return_value = mock_pagination
            
            # Act
            result = news_service.get_news_list(filters)
            
            # Assert
            assert len(result['items']) == 1
            assert result['total'] == 1
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_create_news_success(self, news_service, mock_news_data):
        """測試創建新聞 - 成功場景"""
        # Arrange
        create_data = {
            'news_title_zh': '新聞標題',
            'news_content_zh': '新聞內容',
            'news_date': '2024-01-15'
        }
        
        with patch.object(news_service, 'execute_with_audit') as mock_audit:
            mock_audit.return_value = mock_news_data
            
            # Act
            result = news_service.create_news(create_data)
            
            # Assert
            assert result == mock_news_data
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_update_news_success(self, news_service, mock_news_data):
        """測試更新新聞 - 成功場景"""
        # Arrange
        news_id = 1
        update_data = {'news_title_zh': '更新的標題'}
        
        mock_news = Mock(spec=News)
        
        with patch.object(News, 'query') as mock_query:
            mock_query.get.return_value = mock_news
            
            with patch.object(news_service, 'execute_with_audit') as mock_audit:
                mock_audit.return_value = mock_news_data
                
                # Act
                result = news_service.update_news(news_id, update_data)
                
                # Assert
                assert result == mock_news_data