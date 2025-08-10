"""
ResearchGroupService 測試用例
測試課題組管理相關的服務層邏輯
"""

import pytest
from unittest.mock import Mock, patch
from app.services.research_group_service import ResearchGroupService
from app.services.base_service import ValidationError, NotFoundError
from app.models.research_group import ResearchGroup


class TestResearchGroupService:
    """課題組服務層測試"""
    
    @pytest.fixture
    def research_group_service(self):
        """創建課題組服務實例"""
        return ResearchGroupService()
    
    @pytest.fixture
    def mock_group_data(self):
        """模擬課題組數據"""
        return {
            'research_group_id': 1,
            'research_group_name_zh': '計算機視覺課題組',
            'research_group_name_en': 'Computer Vision Group',
            'research_group_desc_zh': '專注於計算機視覺研究',
            'research_group_desc_en': 'Focus on computer vision research',
            'lab_id': 1,
            'enable': 1
        }
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_research_groups_list_success(self, research_group_service, mock_group_data):
        """測試獲取課題組列表 - 成功場景"""
        # Arrange
        filters = {'page': 1, 'per_page': 10}
        
        expected_result = {
            'items': [mock_group_data],
            'total': 1,
            'pages': 1,
            'page': 1,
            'per_page': 10
        }
        
        # Mock the entire method chain
        with patch('app.services.research_group_service.ResearchGroup') as MockResearchGroup, \
             patch('app.services.research_group_service.Member') as MockMember, \
             patch('app.services.research_group_service.get_pagination_params') as mock_get_pagination, \
             patch('app.services.research_group_service.paginate_query') as mock_paginate:
            
            mock_get_pagination.return_value = (1, 10)
            mock_paginate.return_value = expected_result
            
            # Act
            result = research_group_service.get_research_groups_list(filters)
            
            # Assert
            assert 'items' in result
            assert 'total' in result
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_create_research_group_success(self, research_group_service, mock_group_data):
        """測試創建課題組 - 成功場景"""
        # Arrange
        create_data = {
            'research_group_name_zh': '新課題組',
            'research_group_name_en': 'New Research Group',
            'lab_id': 1
        }
        
        with patch.object(research_group_service, 'validate_permissions'), \
             patch.object(research_group_service, 'execute_with_audit') as mock_audit:
            
            mock_audit.return_value = mock_group_data
            
            # Act
            result = research_group_service.create_research_group(create_data)
            
            # Assert
            assert result == mock_group_data
            mock_audit.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_delete_research_group_with_members(self, research_group_service):
        """測試刪除課題組 - 存在關聯成員"""
        # Arrange
        group_id = 1
        
        mock_group = Mock()
        mock_group.research_group_id = group_id
        
        with patch('app.services.research_group_service.ResearchGroup') as MockResearchGroup, \
             patch('app.services.research_group_service.Member') as MockMember, \
             patch.object(research_group_service, 'validate_permissions'):
            
            MockResearchGroup.query.filter_by.return_value.first.return_value = mock_group
            MockMember.query.filter_by.return_value.count.return_value = 5  # 存在5個成員
            
            # Act & Assert  
            with pytest.raises(Exception):  # Should raise BusinessLogicError
                research_group_service.delete_research_group(group_id)