"""
MemberService 測試用例
測試成員管理相關的服務層邏輯
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.member_service import MemberService
from app.services.base_service import ServiceException, ValidationError, NotFoundError
from app.models.member import Member


class TestMemberService:
    """成員服務層測試"""
    
    @pytest.fixture
    def member_service(self):
        """創建成員服務實例"""
        return MemberService()
    
    @pytest.fixture
    def mock_member_data(self):
        """模擬成員數據"""
        return {
            'member_id': 1,
            'member_name_zh': '張三',
            'member_name_en': 'Zhang San',
            'member_desc_zh': '研究生',
            'member_desc_en': 'Graduate Student',
            'member_type': 'student',
            'member_avatar_path': '/media/member_avatar/zhang_san.jpg',
            'lab_id': 1,
            'research_group_id': 1,
            'enable': 1
        }
    
    @pytest.fixture
    def mock_members_list_data(self):
        """模擬成員列表數據"""
        return [
            {'member_id': 1, 'member_name_zh': '張三', 'member_type': 'student'},
            {'member_id': 2, 'member_name_zh': '李四', 'member_type': 'teacher'},
            {'member_id': 3, 'member_name_zh': '王五', 'member_type': 'student'}
        ]
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_members_list_success(self, member_service, mock_members_list_data):
        """測試獲取成員列表 - 成功場景"""
        # Arrange
        filters = {'page': 1, 'per_page': 10}
        
        mock_members = [Mock(spec=Member) for _ in range(3)]
        for i, member in enumerate(mock_members):
            member.to_dict.return_value = mock_members_list_data[i]
        
        mock_pagination = Mock()
        mock_pagination.items = mock_members
        mock_pagination.total = 3
        mock_pagination.page = 1
        mock_pagination.per_page = 10
        
        with patch.object(Member, 'query') as mock_query:
            mock_query.filter_by.return_value.order_by.return_value.paginate.return_value = mock_pagination
            
            # Act
            result = member_service.get_members_list(filters)
            
            # Assert
            assert len(result['items']) == 3
            assert result['total'] == 3
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_members_list_with_filters(self, member_service):
        """測試獲取成員列表 - 帶過濾條件"""
        # Arrange
        filters = {
            'member_type': 'teacher',
            'research_group_id': 1,
            'q': '張',
            'page': 1,
            'per_page': 10
        }
        
        mock_member = Mock(spec=Member)
        mock_member.to_dict.return_value = {'member_id': 1, 'member_name_zh': '張教授'}
        
        mock_pagination = Mock()
        mock_pagination.items = [mock_member]
        mock_pagination.total = 1
        
        with patch.object(Member, 'query') as mock_query:
            mock_filter = mock_query.filter_by.return_value.filter.return_value
            mock_filter.order_by.return_value.paginate.return_value = mock_pagination
            
            # Act
            result = member_service.get_members_list(filters)
            
            # Assert
            assert len(result['items']) == 1
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_member_by_id_success(self, member_service, mock_member_data):
        """測試根據ID獲取成員 - 成功場景"""
        # Arrange
        member_id = 1
        
        mock_member = Mock(spec=Member)
        mock_member.to_dict.return_value = mock_member_data
        
        with patch.object(Member, 'query') as mock_query:
            mock_query.get.return_value = mock_member
            
            # Act
            result = member_service.get_member_by_id(member_id)
            
            # Assert
            assert result == mock_member_data
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_get_member_by_id_not_found(self, member_service):
        """測試根據ID獲取成員 - 成員不存在"""
        # Arrange
        member_id = 999
        
        with patch.object(Member, 'query') as mock_query:
            mock_query.get.return_value = None
            
            # Act & Assert
            with pytest.raises(NotFoundError) as exc_info:
                member_service.get_member_by_id(member_id)
            
            assert '成員不存在' in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_create_member_success(self, member_service, mock_member_data):
        """測試創建成員 - 成功場景"""
        # Arrange
        create_data = {
            'member_name_zh': '新成員',
            'member_name_en': 'New Member',
            'member_type': 'student',
            'lab_id': 1,
            'research_group_id': 1
        }
        
        with patch.object(member_service, 'execute_with_audit') as mock_audit:
            mock_audit.return_value = mock_member_data
            
            # Act
            result = member_service.create_member(create_data)
            
            # Assert
            assert result == mock_member_data
            mock_audit.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_create_member_with_avatar(self, member_service, mock_member_data):
        """測試創建成員 - 帶頭像上傳"""
        # Arrange
        create_data = {
            'member_name_zh': '新成員',
            'member_type': 'student'
        }
        
        mock_avatar = Mock()
        mock_avatar.filename = 'avatar.jpg'
        mock_avatar.read.return_value = b'fake_image_data'
        
        with patch('app.services.member_service.save_upload_file') as mock_save:
            mock_save.return_value = '/media/member_avatar/avatar.jpg'
            
            with patch.object(member_service, 'execute_with_audit') as mock_audit:
                mock_audit.return_value = mock_member_data
                
                # Act
                result = member_service.create_member(create_data, avatar_file=mock_avatar)
                
                # Assert
                assert result == mock_member_data
                mock_save.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_update_member_success(self, member_service, mock_member_data):
        """測試更新成員 - 成功場景"""
        # Arrange
        member_id = 1
        update_data = {'member_desc_zh': '更新的描述'}
        
        mock_member = Mock(spec=Member)
        mock_member.member_id = member_id
        
        with patch.object(Member, 'query') as mock_query:
            mock_query.get.return_value = mock_member
            
            with patch.object(member_service, 'execute_with_audit') as mock_audit:
                mock_audit.return_value = mock_member_data
                
                # Act
                result = member_service.update_member(member_id, update_data)
                
                # Assert
                assert result == mock_member_data
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_delete_member_success(self, member_service):
        """測試刪除成員 - 成功場景"""
        # Arrange
        member_id = 1
        
        mock_member = Mock(spec=Member)
        mock_member.member_id = member_id
        
        with patch.object(Member, 'query') as mock_query:
            mock_query.get.return_value = mock_member
            
            with patch.object(member_service, 'execute_with_audit') as mock_audit:
                mock_audit.return_value = {'message': '刪除成功'}
                
                # Act
                result = member_service.delete_member(member_id)
                
                # Assert
                assert result['message'] == '刪除成功'
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_batch_delete_members_success(self, member_service):
        """測試批量刪除成員 - 成功場景"""
        # Arrange
        member_ids = [1, 2, 3]
        
        mock_members = [Mock(spec=Member) for _ in range(3)]
        for i, member in enumerate(mock_members):
            member.member_id = member_ids[i]
        
        with patch.object(Member, 'query') as mock_query:
            mock_query.filter.return_value.all.return_value = mock_members
            
            with patch.object(member_service, 'execute_with_audit') as mock_audit:
                mock_audit.return_value = {'message': f'成功刪除 {len(member_ids)} 個成員'}
                
                # Act
                result = member_service.batch_delete_members(member_ids)
                
                # Assert
                assert '成功刪除' in result['message']
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_batch_update_members_success(self, member_service):
        """測試批量更新成員 - 成功場景"""
        # Arrange
        member_ids = [1, 2]
        update_data = {'research_group_id': 2}
        
        mock_members = [Mock(spec=Member) for _ in range(2)]
        for i, member in enumerate(mock_members):
            member.member_id = member_ids[i]
        
        with patch.object(Member, 'query') as mock_query:
            mock_query.filter.return_value.all.return_value = mock_members
            
            with patch.object(member_service, 'execute_with_audit') as mock_audit:
                mock_audit.return_value = {'message': f'成功更新 {len(member_ids)} 個成員'}
                
                # Act
                result = member_service.batch_update_members(member_ids, update_data)
                
                # Assert
                assert '成功更新' in result['message']
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_validate_member_type_valid(self, member_service):
        """測試成員類型驗證 - 有效類型"""
        # Arrange & Act & Assert
        assert member_service._validate_member_type('teacher') == True
        assert member_service._validate_member_type('student') == True
    
    @pytest.mark.unit
    @pytest.mark.service
    def test_validate_member_type_invalid(self, member_service):
        """測試成員類型驗證 - 無效類型"""
        # Arrange & Act & Assert
        assert member_service._validate_member_type('invalid_type') == False
        assert member_service._validate_member_type('') == False