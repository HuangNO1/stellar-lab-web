from typing import Optional, Dict, Any, List
from app.models import Member, ResearchGroup, Paper
from app.utils.validators import validate_email, validate_string_length
from app.utils.file_handler import save_file, delete_file
from app.utils.helpers import get_pagination_params, paginate_query
from .base_service import BaseService, ValidationError, NotFoundError, BusinessLogicError


class MemberService(BaseService):
    """
    成員管理服務層
    
    負責成員相關的業務邏輯：
    - 成員CRUD操作
    - 批量操作
    - 關聯數據檢查
    - 文件處理
    """
    
    def get_module_id(self) -> int:
        return 3
    
    def get_module_name(self) -> str:
        return 'member'
    
    def get_members_list(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        獲取成員列表
        
        Args:
            filters: 篩選條件
            
        Returns:
            Dict: 分頁後的成員列表
        """
        query = Member.query
        
        # 默認只顯示有效成員
        if not filters or not filters.get('show_all', False):
            query = query.filter_by(enable=1)
        
        # 應用篩選條件
        query = self._apply_member_filters(query, filters or {})
        
        # 應用排序
        query = self._apply_member_sorting(query, filters or {})
        
        # 分頁
        page, per_page = get_pagination_params()
        return paginate_query(query, page, per_page)
    
    def get_member_detail(self, mem_id: int) -> Dict[str, Any]:
        """
        獲取成員詳情
        
        Args:
            mem_id: 成員ID
            
        Returns:
            Dict: 成員詳情
            
        Raises:
            NotFoundError: 成員不存在
        """
        member = Member.query.filter_by(mem_id=mem_id, enable=1).first()
        if not member:
            raise NotFoundError('成員不存在')
        
        return member.to_dict()
    
    def create_member(self, form_data: Dict[str, Any], files_data: Dict[str, Any] = None, current_admin=None) -> Dict[str, Any]:
        """
        創建成員
        
        Args:
            form_data: 表單數據
            files_data: 文件數據
            
        Returns:
            Dict: 創建的成員信息
        """
        # 驗證權限
        if current_admin:
            # 如果傳遞了管理員，則設置到 g 對象中
            from flask import g
            g.current_admin = current_admin
            
        self.validate_permissions('CREATE')
        
        # 數據校驗
        self._validate_member_data(form_data, is_create=True)
        
        def _create_operation():
            member = Member(enable=1)
            
            # 設置基本信息
            self._set_member_basic_info(member, form_data)
            
            # 處理頭像上傳
            if files_data:
                self._handle_avatar_upload(member, files_data)
            
            # 設置關聯信息
            self._set_member_associations(member, form_data)
            
            self.db.session.add(member)
            self.db.session.flush()
            
            return member.to_dict()
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_create_operation,
            operation_type='CREATE',
            content=dict(form_data)
        )
        
        return result
    
    def update_member(self, mem_id: int, form_data: Dict[str, Any], files_data: Dict[str, Any] = None, current_admin=None) -> Dict[str, Any]:
        """
        更新成員信息
        
        Args:
            mem_id: 成員ID
            form_data: 表單數據
            files_data: 文件數據
            
        Returns:
            Dict: 更新後的成員信息
        """
        # 驗證權限
        if current_admin:
            # 如果傳遞了管理員，則設置到 g 對象中
            from flask import g
            g.current_admin = current_admin
            
        self.validate_permissions('UPDATE', mem_id)
        
        member = Member.query.filter_by(mem_id=mem_id, enable=1).first()
        if not member:
            raise NotFoundError('成員不存在')
        
        # 數據校驗
        self._validate_member_data(form_data, is_create=False)
        
        def _update_operation():
            update_data = {}
            
            # 更新基本信息
            basic_updates = self._update_member_basic_info(member, form_data)
            update_data.update(basic_updates)
            
            # 處理頭像更新/刪除
            avatar_update = self._handle_avatar_update(member, files_data, form_data)
            if avatar_update:
                update_data.update(avatar_update)
            
            # 更新關聯信息
            association_updates = self._update_member_associations(member, form_data)
            update_data.update(association_updates)
            
            return member.to_dict()
        
        # 先收集更新數據用於審計
        update_data = {}
        basic_updates = self._update_member_basic_info(member, form_data)
        update_data.update(basic_updates)
        
        # 處理頭像更新/刪除
        avatar_update = self._handle_avatar_update(member, files_data, form_data)
        if avatar_update:
            update_data.update(avatar_update)
            
        association_updates = self._update_member_associations(member, form_data)
        update_data.update(association_updates)
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_update_operation,
            operation_type='UPDATE',
            content=update_data
        )
        
        return result
    
    def delete_member(self, mem_id: int) -> None:
        """
        刪除成員
        
        Args:
            mem_id: 成員ID
        """
        # 驗證權限
        self.validate_permissions('DELETE', mem_id)
        
        member = Member.query.filter_by(mem_id=mem_id, enable=1).first()
        if not member:
            raise NotFoundError('成員不存在')
        
        # 檢查是否可以刪除
        self._check_member_deletable(member)
        
        def _delete_operation():
            # 軟刪除
            self.soft_delete(member, "成員")
            
            # 清理頭像文件
            if member.mem_avatar_path:
                delete_file(member.mem_avatar_path)
                member.mem_avatar_path = None
            
            return {'deleted_member_id': mem_id}
        
        # 執行操作並記錄審計
        self.execute_with_audit(
            operation_func=_delete_operation,
            operation_type='DELETE',
            content={'deleted_member_id': mem_id}
        )
    
    def batch_delete_members(self, member_ids: List[int]) -> Dict[str, Any]:
        """
        批量刪除成員
        
        Args:
            member_ids: 成員ID列表
            
        Returns:
            Dict: 批量操作結果
        """
        # 驗證權限
        self.validate_permissions('BATCH_DELETE')
        
        if not member_ids:
            raise ValidationError('請選擇要刪除的成員')
        
        def _batch_delete_operation():
            deleted_count = 0
            failed_members = []
            
            for mem_id in member_ids:
                try:
                    member = Member.query.filter_by(mem_id=mem_id, enable=1).first()
                    if member:
                        # 檢查是否可以刪除
                        self._check_member_deletable(member)
                        
                        # 軟刪除
                        self.soft_delete(member, "成員")
                        
                        # 清理頭像文件
                        if member.mem_avatar_path:
                            delete_file(member.mem_avatar_path)
                            member.mem_avatar_path = None
                        
                        deleted_count += 1
                    else:
                        failed_members.append(f"成員ID {mem_id} 不存在")
                        
                except Exception as e:
                    failed_members.append(f"成員ID {mem_id}: {str(e)}")
            
            result = {
                'deleted_count': deleted_count,
                'total_requested': len(member_ids),
                'failed_members': failed_members
            }
            
            return result
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_batch_delete_operation,
            operation_type='BATCH_DELETE',
            content={
                'batch_operation': True,
                'member_ids': member_ids,
                'operation': 'delete'
            }
        )
        
        return result
    
    def batch_update_members(self, member_ids: List[int], update_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        批量更新成員
        
        Args:
            member_ids: 成員ID列表
            update_fields: 要更新的字段
            
        Returns:
            Dict: 批量操作結果
        """
        # 驗證權限
        self.validate_permissions('BATCH_UPDATE')
        
        if not member_ids:
            raise ValidationError('請選擇要更新的成員')
        
        if not update_fields:
            raise ValidationError('請指定要更新的字段')
        
        # 校驗更新字段
        self._validate_batch_update_fields(update_fields)
        
        def _batch_update_operation():
            updated_count = 0
            failed_members = []
            
            for mem_id in member_ids:
                try:
                    member = Member.query.filter_by(mem_id=mem_id, enable=1).first()
                    if member:
                        # 更新允許的字段
                        for field, value in update_fields.items():
                            if hasattr(member, field):
                                setattr(member, field, value)
                        
                        updated_count += 1
                    else:
                        failed_members.append(f"成員ID {mem_id} 不存在")
                        
                except Exception as e:
                    failed_members.append(f"成員ID {mem_id}: {str(e)}")
            
            result = {
                'updated_count': updated_count,
                'total_requested': len(member_ids),
                'failed_members': failed_members
            }
            
            return result
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_batch_update_operation,
            operation_type='BATCH_UPDATE',
            content={
                'batch_operation': True,
                'member_ids': member_ids,
                'update_fields': update_fields
            }
        )
        
        return result
    
    def _apply_member_filters(self, query, filters: Dict[str, Any]):
        """應用成員篩選條件"""
        # 搜索關鍵字
        if 'q' in filters and filters['q']:
            search_term = f"%{filters['q']}%"
            query = query.filter(
                (Member.mem_name_zh.like(search_term)) |
                (Member.mem_name_en.like(search_term)) |
                (Member.mem_email.like(search_term))
            )
        
        # 成員類型篩選
        if 'type' in filters and filters['type'] is not None:
            query = query.filter(Member.mem_type == filters['type'])
        
        # 課題組篩選
        if 'research_group_id' in filters and filters['research_group_id']:
            query = query.filter(Member.research_group_id == filters['research_group_id'])
        
        # 實驗室篩選
        if 'lab_id' in filters and filters['lab_id']:
            query = query.filter(Member.lab_id == filters['lab_id'])
        
        return query
    
    def _apply_member_sorting(self, query, filters: Dict[str, Any]):
        """應用成員排序"""
        sort_by = filters.get('sort_by', 'created_at')
        order = filters.get('order', 'desc')
        
        # 獲取排序字段
        sort_column = getattr(Member, sort_by, Member.created_at)
        
        if order.lower() == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        return query
    
    def _validate_member_data(self, form_data: Dict[str, Any], is_create: bool = True) -> None:
        """校驗成員數據"""
        if is_create:
            required_fields = ['mem_name_zh', 'mem_name_en', 'mem_email', 'mem_type', 'research_group_id']
            self.validate_required_fields(form_data, required_fields)
        
        # 郵箱格式校驗
        if 'mem_email' in form_data and form_data['mem_email']:
            if not validate_email(form_data['mem_email']):
                raise ValidationError('郵箱格式不正確')
        
        # 成員類型校驗
        if 'mem_type' in form_data:
            try:
                mem_type = int(form_data['mem_type'])
                if mem_type not in [0, 1, 2]:  # 0=教師, 1=學生, 2=校友
                    raise ValidationError('成員類型無效')
                form_data['mem_type'] = mem_type  # 確保後續使用整數類型
            except (ValueError, TypeError):
                raise ValidationError('成員類型格式錯誤')
        
        # 職稱類型校驗（僅教師）
        if 'job_type' in form_data and form_data['job_type'] is not None:
            try:
                job_type = int(form_data['job_type'])
                if form_data.get('mem_type') == 0:  # 教師
                    if job_type not in [0, 1, 2, 3, 4]:  # 0=教授, 1=副教授, 2=講師, 3=助理研究員, 4=博士後
                        raise ValidationError('職稱類型無效')
                    form_data['job_type'] = job_type  # 確保後續使用整數類型
                else:
                    raise ValidationError('職稱類型僅適用於教師')
            except (ValueError, TypeError):
                raise ValidationError('職稱類型格式錯誤')
        
        # 學生類型校驗（僅學生）
        if 'student_type' in form_data and form_data['student_type'] is not None:
            try:
                student_type = int(form_data['student_type'])
                if form_data.get('mem_type') == 1:  # 學生
                    if student_type not in [0, 1, 2]:  # 0=博士生, 1=碩士生, 2=大學生
                        raise ValidationError('學生類型無效')
                    form_data['student_type'] = student_type  # 確保後續使用整數類型
                else:
                    raise ValidationError('學生類型僅適用於學生')
            except (ValueError, TypeError):
                raise ValidationError('學生類型格式錯誤')
        
        # 字符串長度校驗
        string_fields = {
            'mem_name_zh': 100,
            'mem_name_en': 100,
            'mem_desc_zh': 1000,
            'mem_desc_en': 1000
        }
        
        for field, max_length in string_fields.items():
            if field in form_data and form_data[field]:
                if not validate_string_length(form_data[field], max_length):
                    raise ValidationError(f'{field} 長度不能超過{max_length}字符')
    
    def _validate_batch_update_fields(self, update_fields: Dict[str, Any]) -> None:
        """校驗批量更新字段"""
        allowed_batch_fields = ['enable', 'mem_type', 'research_group_id', 'job_type', 'student_type']
        
        for field in update_fields:
            if field not in allowed_batch_fields:
                raise ValidationError(f'字段 {field} 不允許批量更新')
        
        # 類型校驗
        if 'mem_type' in update_fields:
            try:
                mem_type = int(update_fields['mem_type'])
                if mem_type not in [0, 1, 2]:  # 0=教師, 1=學生, 2=校友
                    raise ValidationError('成員類型無效')
                update_fields['mem_type'] = mem_type
            except (ValueError, TypeError):
                raise ValidationError('成員類型格式錯誤')
        
        if 'job_type' in update_fields:
            try:
                job_type = int(update_fields['job_type'])
                if job_type not in [0, 1, 2, 3, 4]:  # 0=教授, 1=副教授, 2=講師, 3=助理研究員, 4=博士後
                    raise ValidationError('職稱類型無效')
                update_fields['job_type'] = job_type
            except (ValueError, TypeError):
                raise ValidationError('職稱類型格式錯誤')
        
        if 'student_type' in update_fields:
            try:
                student_type = int(update_fields['student_type'])
                if student_type not in [0, 1, 2]:  # 0=博士生, 1=碩士生, 2=大學生
                    raise ValidationError('學生類型無效')
                update_fields['student_type'] = student_type
            except (ValueError, TypeError):
                raise ValidationError('學生類型格式錯誤')
        
        if 'enable' in update_fields:
            try:
                enable = int(update_fields['enable'])
                if enable not in [0, 1]:  # 0=禁用, 1=啟用
                    raise ValidationError('狀態值無效')
                update_fields['enable'] = enable
            except (ValueError, TypeError):
                raise ValidationError('狀態值格式錯誤')
        
        if 'research_group_id' in update_fields:
            try:
                research_group_id = int(update_fields['research_group_id'])
                update_fields['research_group_id'] = research_group_id
            except (ValueError, TypeError):
                raise ValidationError('課題組ID格式錯誤')
    
    def _set_member_basic_info(self, member: Member, form_data: Dict[str, Any]) -> None:
        """設置成員基本信息"""
        basic_fields = [
            'mem_name_zh', 'mem_name_en', 'mem_email', 'mem_type',
            'job_type', 'student_type', 'student_grade',
            'mem_desc_zh', 'mem_desc_en', 'destination_zh', 'destination_en'
        ]
        
        for field in basic_fields:
            if field in form_data:
                setattr(member, field, form_data[field])
    
    def _update_member_basic_info(self, member: Member, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新成員基本信息"""
        basic_fields = [
            'mem_name_zh', 'mem_name_en', 'mem_email', 'mem_type',
            'job_type', 'student_type', 'student_grade',
            'mem_desc_zh', 'mem_desc_en', 'destination_zh', 'destination_en'
        ]
        
        update_data = {}
        for field in basic_fields:
            if field in form_data:
                old_value = getattr(member, field)
                new_value = form_data[field]
                if old_value != new_value:
                    setattr(member, field, new_value)
                    update_data[field] = {'old': old_value, 'new': new_value}
        
        return update_data
    
    def _handle_avatar_upload(self, member: Member, files_data: Dict[str, Any]) -> None:
        """處理頭像上傳"""
        if 'mem_avatar' not in files_data:
            return
        
        file = files_data['mem_avatar']
        if not file or not file.filename:
            return
        
        try:
            avatar_path = save_file(file, 'member_avatar', max_size=5*1024*1024)
            member.mem_avatar_path = avatar_path
        except Exception as e:
            raise ValidationError(f"頭像上傳失敗: {str(e)}")
    
    def _handle_avatar_update(self, member: Member, files_data: Dict[str, Any] = None, form_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """處理頭像更新/刪除"""
        
        # 檢查是否有刪除標記
        if form_data and form_data.get('mem_avatar_delete'):
            old_avatar_path = member.mem_avatar_path
            if old_avatar_path:
                # 刪除舊頭像文件
                delete_file(old_avatar_path)
                # 清空數據庫中的頭像路徑
                member.mem_avatar_path = None
                return {'avatar_deleted': True, 'old_avatar_path': old_avatar_path}
            return {}
        
        # 檢查是否有新文件上傳
        if not files_data or 'mem_avatar' not in files_data:
            return {}
        
        file = files_data['mem_avatar']
        if not file or not file.filename:
            return {}
        
        old_avatar_path = member.mem_avatar_path
        
        try:
            new_avatar_path = save_file(file, 'member_avatar', max_size=5*1024*1024)
            member.mem_avatar_path = new_avatar_path
            
            # 刪除舊頭像
            if old_avatar_path and old_avatar_path != new_avatar_path:
                delete_file(old_avatar_path)
            
            return {'avatar_updated': True, 'new_avatar_path': new_avatar_path}
            
        except Exception as e:
            raise ValidationError(f"頭像更新失敗: {str(e)}")
    
    def _set_member_associations(self, member: Member, form_data: Dict[str, Any]) -> None:
        """設置成員關聯信息"""
        if 'research_group_id' in form_data:
            research_group_id = int(form_data['research_group_id'])
            research_group = ResearchGroup.query.filter_by(
                research_group_id=research_group_id, 
                enable=1
            ).first()
            
            if not research_group:
                raise ValidationError('指定的課題組不存在')
            
            member.research_group_id = research_group_id
            member.lab_id = research_group.lab_id
    
    def _update_member_associations(self, member: Member, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新成員關聯信息"""
        update_data = {}
        
        if 'research_group_id' in form_data:
            new_group_id = int(form_data['research_group_id'])
            old_group_id = member.research_group_id
            
            if new_group_id != old_group_id:
                research_group = ResearchGroup.query.filter_by(
                    research_group_id=new_group_id, 
                    enable=1
                ).first()
                
                if not research_group:
                    raise ValidationError('指定的課題組不存在')
                
                member.research_group_id = new_group_id
                member.lab_id = research_group.lab_id
                
                update_data['research_group_id'] = {'old': old_group_id, 'new': new_group_id}
                update_data['lab_id'] = {'old': member.lab_id, 'new': research_group.lab_id}
        
        return update_data
    
    def _check_member_deletable(self, member: Member) -> None:
        """檢查成員是否可以刪除"""
        # 檢查是否為課題組組長
        research_group = ResearchGroup.query.filter_by(
            mem_id=member.mem_id, 
            enable=1
        ).first()
        
        if research_group:
            raise BusinessLogicError(f'該成員是課題組 "{research_group.research_group_name_zh}" 的組長，無法刪除')
        
        # 檢查是否有關聯的論文（作為作者）
        from app.models import PaperAuthor
        paper_count = PaperAuthor.query.filter_by(mem_id=member.mem_id).count()
        
        if paper_count > 0:
            raise BusinessLogicError(f'該成員關聯了 {paper_count} 篇論文，無法刪除')