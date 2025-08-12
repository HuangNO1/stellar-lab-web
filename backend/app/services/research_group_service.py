from typing import Optional, Dict, Any
from app.models import ResearchGroup, Lab, Member
from app.utils.validators import validate_string_length
from app.utils.helpers import get_pagination_params, paginate_query
from app.utils.messages import msg
from .base_service import BaseService, ValidationError, NotFoundError, BusinessLogicError


class ResearchGroupService(BaseService):
    """
    課題組管理服務層
    """
    
    def get_module_id(self) -> int:
        return 2
    
    def get_module_name(self) -> str:
        return 'research_group'
    
    def get_research_groups_list(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """獲取課題組列表"""
        query = ResearchGroup.query
        
        # 默認只顯示有效課題組
        if not filters or not filters.get('show_all', False):
            query = query.filter_by(enable=1)
        
        # 應用篩選條件
        if filters:
            # 搜索關鍵字
            if filters.get('q'):
                search_term = f"%{filters['q']}%"
                query = query.filter(
                    (ResearchGroup.research_group_name_zh.like(search_term)) |
                    (ResearchGroup.research_group_name_en.like(search_term)) |
                    (ResearchGroup.research_group_desc_zh.like(search_term)) |
                    (ResearchGroup.research_group_desc_en.like(search_term))
                )
            
            # 實驗室篩選
            if filters.get('lab_id'):
                query = query.filter(ResearchGroup.lab_id == filters['lab_id'])
        
        # 按創建時間倒序排序
        query = query.order_by(ResearchGroup.created_at.desc())
        
        # 分頁
        page, per_page = get_pagination_params()
        result = paginate_query(query, page, per_page)
        
        # 為每個課題組添加組長信息
        for item in result['items']:
            if item.get('mem_id'):
                leader = Member.query.filter_by(mem_id=item['mem_id'], enable=1).first()
                item['leader'] = leader.to_dict() if leader else None
        
        return result
    
    def get_research_group_detail(self, group_id: int) -> Dict[str, Any]:
        """獲取課題組詳情"""
        group = ResearchGroup.query.filter_by(research_group_id=group_id, enable=1).first()
        if not group:
            raise NotFoundError(msg.get_error_message('RESEARCH_GROUP_NOT_FOUND'))
        
        result = group.to_dict()
        
        # 添加組長信息
        if result.get('mem_id'):
            leader = Member.query.filter_by(mem_id=result['mem_id'], enable=1).first()
            result['leader'] = leader.to_dict() if leader else None
        
        return result
    
    def create_research_group(self, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """創建課題組"""
        # 驗證權限
        self.validate_permissions('CREATE')
        
        # 數據校驗
        self._validate_group_data(group_data, is_create=True)
        
        def _create_operation():
            group = ResearchGroup(enable=1)
            
            # 設置基本信息
            group.research_group_name_zh = group_data['research_group_name_zh']
            group.research_group_name_en = group_data.get('research_group_name_en', '')
            group.research_group_desc_zh = group_data.get('research_group_desc_zh', '')
            group.research_group_desc_en = group_data.get('research_group_desc_en', '')
            
            # 設置組長和實驗室
            self._set_group_associations(group, group_data)
            
            self.db.session.add(group)
            self.db.session.flush()
            
            return group.to_dict()
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_create_operation,
            operation_type='CREATE',
            content=group_data
        )
        
        return result
    
    def update_research_group(self, group_id: int, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新課題組"""
        # 驗證權限
        self.validate_permissions('UPDATE')
        
        group = ResearchGroup.query.filter_by(research_group_id=group_id, enable=1).first()
        if not group:
            raise NotFoundError(msg.get_error_message('RESEARCH_GROUP_NOT_FOUND'))
        
        # 數據校驗
        self._validate_group_data(group_data, is_create=False)
        
        def _update_operation():
            update_data = {}
            
            # 更新基本信息
            basic_fields = [
                'research_group_name_zh', 'research_group_name_en',
                'research_group_desc_zh', 'research_group_desc_en'
            ]
            
            for field in basic_fields:
                if field in group_data:
                    old_value = getattr(group, field)
                    new_value = group_data[field]
                    
                    if old_value != new_value:
                        setattr(group, field, new_value)
                        update_data[field] = {'old': old_value, 'new': new_value}
            
            # 更新關聯信息
            association_updates = self._update_group_associations(group, group_data)
            update_data.update(association_updates)
            
            return group.to_dict(), update_data
        
        # 執行操作並記錄審計
        result, update_data = self.execute_with_audit(
            operation_func=_update_operation,
            operation_type='UPDATE',
            content={}
        )
        
        return result
    
    def delete_research_group(self, group_id: int) -> None:
        """刪除課題組"""
        # 驗證權限
        self.validate_permissions('DELETE')
        
        group = ResearchGroup.query.filter_by(research_group_id=group_id, enable=1).first()
        if not group:
            raise NotFoundError(msg.get_error_message('RESEARCH_GROUP_NOT_FOUND'))
        
        # 檢查是否可以刪除
        self._check_group_deletable(group)
        
        def _delete_operation():
            # 軟刪除
            self.soft_delete(group, "research_group")
            return {'deleted_group_id': group_id}
        
        # 執行操作並記錄審計
        self.execute_with_audit(
            operation_func=_delete_operation,
            operation_type='DELETE',
            content={'deleted_group_id': group_id}
        )
    
    def _validate_group_data(self, group_data: Dict[str, Any], is_create: bool = True) -> None:
        """校驗課題組數據"""
        if is_create:
            required_fields = ['research_group_name_zh']
            self.validate_required_fields(group_data, required_fields)
        
        # 字符串長度校驗
        string_fields = {
            'research_group_name_zh': 200,
            'research_group_name_en': 200,
            'research_group_desc_zh': 10000,
            'research_group_desc_en': 10000
        }
        
        for field, max_length in string_fields.items():
            if field in group_data and group_data[field]:
                if not validate_string_length(group_data[field], max_length):
                    raise ValidationError(msg.format_field_length_error(field, max_length))
    
    def _set_group_associations(self, group: ResearchGroup, group_data: Dict[str, Any]) -> None:
        """設置課題組關聯信息"""
        # 設置組長
        if 'mem_id' in group_data and group_data['mem_id']:
            member = Member.query.filter_by(mem_id=group_data['mem_id'], enable=1).first()
            if not member:
                raise ValidationError(msg.get_error_message('GROUP_LEADER_NOT_FOUND'))
            
            group.mem_id = group_data['mem_id']
            group.lab_id = member.lab_id
        else:
            # 如果沒有指定組長，需要設置實驗室
            if 'lab_id' not in group_data:
                # 獲取默認實驗室
                lab = Lab.query.filter_by(enable=1).first()
                if lab:
                    group.lab_id = lab.lab_id
                else:
                    raise ValidationError(msg.get_error_message('LAB_OR_LEADER_REQUIRED'))
            else:
                lab = Lab.query.filter_by(lab_id=group_data['lab_id'], enable=1).first()
                if not lab:
                    raise ValidationError(msg.get_error_message('LAB_NOT_FOUND_IN_GROUP'))
                group.lab_id = group_data['lab_id']
    
    def _update_group_associations(self, group: ResearchGroup, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新課題組關聯信息"""
        update_data = {}
        
        # 更新組長
        if 'mem_id' in group_data:
            old_mem_id = group.mem_id
            new_mem_id = group_data['mem_id']
            
            if old_mem_id != new_mem_id:
                if new_mem_id:
                    member = Member.query.filter_by(mem_id=new_mem_id, enable=1).first()
                    if not member:
                        raise ValidationError(msg.get_error_message('GROUP_LEADER_NOT_FOUND'))
                    group.mem_id = new_mem_id
                    # 組長變更時，實驗室也隨之變更
                    if group.lab_id != member.lab_id:
                        group.lab_id = member.lab_id
                        update_data['lab_id'] = {'old': group.lab_id, 'new': member.lab_id}
                else:
                    group.mem_id = None
                
                update_data['mem_id'] = {'old': old_mem_id, 'new': new_mem_id}
        
        return update_data
    
    def _check_group_deletable(self, group: ResearchGroup) -> None:
        """檢查課題組是否可以刪除"""
        # 檢查是否有有效成員
        member_count = Member.query.filter_by(
            research_group_id=group.research_group_id, 
            enable=1
        ).count()
        
        if member_count > 0:
            raise BusinessLogicError(msg.get_error_message('GROUP_HAS_MEMBERS', count=member_count))