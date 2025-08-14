from typing import Optional, Dict, Any
from datetime import datetime
from app.models import Project
from app.utils.validators import validate_string_length
from app.utils.helpers import get_pagination_params, paginate_query
from app.utils.messages import msg
from .base_service import BaseService, ValidationError, NotFoundError
from .image_upload_service import ImageUploadService


class ProjectService(BaseService):
    """
    項目管理服務層
    """
    
    def get_module_id(self) -> int:
        return 6
    
    def get_module_name(self) -> str:
        return 'project'
    
    def get_projects_list(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """獲取項目列表"""
        query = Project.query
        
        # 默認只顯示有效項目
        if not filters or not filters.get('show_all', False):
            query = query.filter_by(enable=1)
        
        # 應用篩選條件
        if filters:
            # 搜索關鍵字
            if filters.get('q'):
                search_term = f"%{filters['q']}%"
                query = query.filter(
                    (Project.project_name_zh.like(search_term)) |
                    (Project.project_name_en.like(search_term)) |
                    (Project.project_desc_zh.like(search_term)) |
                    (Project.project_desc_en.like(search_term))
                )
            
            # 項目狀態篩選
            if filters.get('is_end') is not None:
                query = query.filter(Project.is_end == filters['is_end'])
            
            # 日期範圍篩選
            if filters.get('start_date'):
                query = query.filter(Project.project_date_start >= filters['start_date'])
            if filters.get('end_date'):
                query = query.filter(Project.project_date_start <= filters['end_date'])
        
        # 排序
        sort_by = filters.get('sort_by', 'project_date_start') if filters else 'project_date_start'
        order = filters.get('order', 'desc') if filters else 'desc'
        
        sort_column = getattr(Project, sort_by, Project.project_date_start)
        if order.lower() == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # 分頁
        page, per_page = get_pagination_params()
        return paginate_query(query, page, per_page)
    
    def get_project_detail(self, project_id: int) -> Dict[str, Any]:
        """獲取項目詳情"""
        project = Project.query.filter_by(project_id=project_id, enable=1).first()
        if not project:
            raise NotFoundError(msg.get_error_message('PROJECT_NOT_FOUND'))
        
        return project.to_dict()
    
    def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """創建項目"""
        # 驗證權限
        self.validate_permissions('CREATE')
        
        # 數據校驗
        self._validate_project_data(project_data, is_create=True)
        
        def _create_operation():
            project = Project(enable=1)
            
            # 設置項目信息
            self._set_project_fields(project, project_data)
            
            self.db.session.add(project)
            self.db.session.flush()
            
            # 處理描述字段中的圖片管理
            image_upload_service = ImageUploadService()
            for field in ['project_desc_zh', 'project_desc_en']:
                if field in project_data and project_data[field]:
                    image_upload_service.mark_images_as_used(
                        content=project_data[field],
                        entity_type='project',
                        entity_id=project.project_id,
                        field_name=field
                    )
            
            return project.to_dict()
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_create_operation,
            operation_type='CREATE',
            content=project_data
        )
        
        return result
    
    def update_project(self, project_id: int, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新項目"""
        # 驗證權限
        self.validate_permissions('UPDATE')
        
        project = Project.query.filter_by(project_id=project_id, enable=1).first()
        if not project:
            raise NotFoundError(msg.get_error_message('PROJECT_NOT_FOUND'))
        
        # 數據校驗
        self._validate_project_data(project_data, is_create=False)
        
        def _update_operation():
            update_data = {}
            
            # 更新字段
            fields = [
                'project_name_zh', 'project_name_en', 
                'project_desc_zh', 'project_desc_en',
                'project_url', 'project_date_start', 'is_end'
            ]
            
            for field in fields:
                if field in project_data:
                    old_value = getattr(project, field)
                    if field == 'project_date_start':
                        new_value = datetime.strptime(project_data[field], '%Y-%m-%d').date()
                    else:
                        new_value = project_data[field]
                    
                    if old_value != new_value:
                        setattr(project, field, new_value)
                        update_data[field] = {'old': str(old_value), 'new': str(new_value)}
                        
                        # 處理描述字段的圖片管理
                        if field in ['project_desc_zh', 'project_desc_en'] and new_value:
                            image_upload_service = ImageUploadService()
                            image_upload_service.mark_images_as_used(
                                content=new_value,
                                entity_type='project',
                                entity_id=project_id,
                                field_name=field
                            )
            
            return project.to_dict(), update_data
        
        # 執行操作並記錄審計
        result, update_data = self.execute_with_audit(
            operation_func=_update_operation,
            operation_type='UPDATE',
            content={}
        )
        
        return result
    
    def delete_project(self, project_id: int) -> None:
        """刪除項目"""
        # 驗證權限
        self.validate_permissions('DELETE')
        
        project = Project.query.filter_by(project_id=project_id, enable=1).first()
        if not project:
            raise NotFoundError(msg.get_error_message('PROJECT_NOT_FOUND'))
        
        def _delete_operation():
            # 軟刪除
            self.soft_delete(project, "project")
            return {'deleted_project_id': project_id}
        
        # 執行操作並記錄審計
        self.execute_with_audit(
            operation_func=_delete_operation,
            operation_type='DELETE',
            content={'deleted_project_id': project_id}
        )
    
    def _validate_project_data(self, project_data: Dict[str, Any], is_create: bool = True) -> None:
        """校驗項目數據"""
        if is_create:
            required_fields = ['project_name_zh']
            self.validate_required_fields(project_data, required_fields)
        
        # 字符串長度校驗
        string_fields = {
            'project_name_zh': 200,
            'project_name_en': 200,
            'project_desc_zh': 10000,
            'project_desc_en': 10000,
            'project_url': 500
        }
        
        for field, max_length in string_fields.items():
            if field in project_data and project_data[field]:
                if not validate_string_length(project_data[field], max_length):
                    raise ValidationError(msg.format_field_length_error(field, max_length))
        
        # 項目狀態校驗
        if 'is_end' in project_data:
            try:
                is_end_value = int(project_data['is_end'])
                if is_end_value not in [0, 1]:
                    raise ValidationError(msg.get_error_message('PROJECT_STATUS_INVALID'))
                project_data['is_end'] = is_end_value
            except (ValueError, TypeError):
                raise ValidationError(msg.get_error_message('PROJECT_STATUS_FORMAT_ERROR'))
        
        # 日期格式校驗
        if 'project_date_start' in project_data and project_data['project_date_start']:
            try:
                datetime.strptime(project_data['project_date_start'], '%Y-%m-%d')
            except ValueError:
                raise ValidationError(msg.get_error_message('PROJECT_START_DATE_FORMAT_ERROR'))
    
    def _set_project_fields(self, project: Project, project_data: Dict[str, Any]) -> None:
        """設置項目字段"""
        fields = [
            'project_name_zh', 'project_name_en', 
            'project_desc_zh', 'project_desc_en',
            'project_url', 'is_end'
        ]
        
        for field in fields:
            if field in project_data:
                setattr(project, field, project_data[field])
        
        # 特殊處理日期字段
        if 'project_date_start' in project_data and project_data['project_date_start']:
            project.project_date_start = datetime.strptime(
                project_data['project_date_start'], '%Y-%m-%d'
            ).date()