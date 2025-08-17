"""資源服務層"""

from app import db
from app.models.resource import Resource
from app.services.base_service import BaseService
from app.utils.messages import get_message
from app.utils.file_handler import save_file, delete_file
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class ResourceService(BaseService):
    """資源服務類"""
    
    def __init__(self):
        super().__init__()
    
    def get_module_id(self) -> int:
        return 9
    
    def get_module_name(self) -> str:
        return 'resource'
        
    def create_resource(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        """創建資源"""
        try:
            # 驗證必填字段
            if not resource_data.get('resource_name_zh'):
                return {
                    'code': 1,
                    'message': get_message('RESOURCE_NAME_ZH_REQUIRED'),
                    'data': None
                }
            
            # 創建資源實例
            resource = Resource(
                resource_name_zh=resource_data.get('resource_name_zh'),
                resource_name_en=resource_data.get('resource_name_en'),
                resource_description_zh=resource_data.get('resource_description_zh'),
                resource_description_en=resource_data.get('resource_description_en'),
                resource_type=resource_data.get('resource_type', 0),
                resource_location_zh=resource_data.get('resource_location_zh'),
                resource_location_en=resource_data.get('resource_location_en'),
                resource_url=resource_data.get('resource_url'),
                resource_file=resource_data.get('resource_file'),
                resource_image=resource_data.get('resource_image'),
                availability_status=resource_data.get('availability_status', 1),
                contact_info=resource_data.get('contact_info')
            )
            
            db.session.add(resource)
            db.session.commit()
            
            return {
                'code': 0,
                'message': get_message('RESOURCE_CREATE_SUCCESS'),
                'data': resource.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"創建資源失敗: {str(e)}")
            return {
                'code': 1,
                'message': get_message('RESOURCE_CREATE_FAILED'),
                'data': None
            }
    
    def get_resource(self, resource_id: int) -> Dict[str, Any]:
        """根據ID獲取資源"""
        try:
            resource = Resource.query.get(resource_id)
            if not resource:
                return {
                    'code': 1,
                    'message': get_message('RESOURCE_NOT_FOUND'),
                    'data': None
                }
            
            return {
                'code': 0,
                'message': get_message('SUCCESS'),
                'data': resource.to_dict()
            }
            
        except Exception as e:
            logger.error(f"獲取資源失敗: {str(e)}")
            return {
                'code': 1,
                'message': get_message('RESOURCE_FETCH_FAILED'),
                'data': None
            }
    
    def get_resources(self, page: int = 1, per_page: int = 20, **kwargs) -> Dict[str, Any]:
        """獲取資源列表"""
        try:
            query = Resource.query
            
            # 搜索過濾
            if kwargs.get('q'):
                search_term = f"%{kwargs['q']}%"
                query = query.filter(
                    db.or_(
                        Resource.resource_name_zh.like(search_term),
                        Resource.resource_name_en.like(search_term),
                        Resource.resource_description_zh.like(search_term),
                        Resource.resource_description_en.like(search_term)
                    )
                )
            
            # 資源類型過濾
            if kwargs.get('resource_type') is not None:
                query = query.filter(Resource.resource_type == kwargs['resource_type'])
            
            # 可用狀態過濾
            if kwargs.get('availability_status') is not None:
                query = query.filter(Resource.availability_status == kwargs['availability_status'])
            
            # 排序
            sort_by = kwargs.get('sort_by', 'created_time')
            order = kwargs.get('order', 'desc')
            
            if hasattr(Resource, sort_by):
                sort_column = getattr(Resource, sort_by)
                if order == 'asc':
                    query = query.order_by(sort_column.asc())
                else:
                    query = query.order_by(sort_column.desc())
            
            # 分頁
            if per_page == -1:  # 獲取所有
                resources = query.all()
                result = {
                    'code': 0,
                    'message': get_message('SUCCESS'),
                    'data': {
                        'items': [resource.to_dict() for resource in resources],
                        'total': len(resources)
                    }
                }
            else:
                pagination = query.paginate(
                    page=page, per_page=per_page, error_out=False
                )
                
                result = {
                    'code': 0,
                    'message': get_message('SUCCESS'),
                    'data': {
                        'items': [resource.to_dict() for resource in pagination.items],
                        'total': pagination.total,
                        'pages': pagination.pages,
                        'per_page': pagination.per_page,
                        'page': pagination.page,
                        'has_prev': pagination.has_prev,
                        'has_next': pagination.has_next
                    }
                }
            
            return result
            
        except Exception as e:
            logger.error(f"獲取資源列表失敗: {str(e)}")
            return {
                'code': 1,
                'message': get_message('RESOURCE_FETCH_FAILED'),
                'data': None
            }
    
    def update_resource(self, resource_id: int, resource_data: Dict[str, Any], files_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """更新資源"""
        try:
            resource = Resource.query.get(resource_id)
            if not resource:
                return {
                    'code': 1,
                    'message': get_message('RESOURCE_NOT_FOUND'),
                    'data': None
                }
            
            # 驗證必填字段
            if not resource_data.get('resource_name_zh'):
                return {
                    'code': 1,
                    'message': get_message('RESOURCE_NAME_ZH_REQUIRED'),
                    'data': None
                }
            
            # 處理圖片刪除
            if resource_data.get('resource_image_delete'):
                old_image_path = resource.resource_image
                if old_image_path:
                    delete_file(old_image_path)
                    resource.resource_image = None
            
            # 處理新圖片上傳
            if files_data and 'resource_image' in files_data:
                image_file = files_data['resource_image']
                if image_file and image_file.filename:
                    old_image_path = resource.resource_image
                    
                    try:
                        new_image_path = save_file(image_file, 'image', max_size=10*1024*1024)
                        resource.resource_image = new_image_path
                        
                        # 刪除舊圖片
                        if old_image_path and old_image_path != new_image_path:
                            delete_file(old_image_path)
                        
                    except Exception as e:
                        logger.error(f"資源圖片上傳失敗: {str(e)}")
                        return {
                            'code': 1,
                            'message': f'圖片上傳失敗: {str(e)}',
                            'data': None
                        }
            
            # 更新其他字段
            for key, value in resource_data.items():
                if hasattr(resource, key) and key not in ['resource_image_delete']:
                    setattr(resource, key, value)
            
            db.session.commit()
            
            return {
                'code': 0,
                'message': get_message('RESOURCE_UPDATE_SUCCESS'),
                'data': resource.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新資源失敗: {str(e)}")
            return {
                'code': 1,
                'message': get_message('RESOURCE_UPDATE_FAILED'),
                'data': None
            }
    
    def delete_resource(self, resource_id: int) -> Dict[str, Any]:
        """刪除資源"""
        try:
            resource = Resource.query.get(resource_id)
            if not resource:
                return {
                    'code': 1,
                    'message': get_message('RESOURCE_NOT_FOUND'),
                    'data': None
                }
            
            db.session.delete(resource)
            db.session.commit()
            
            return {
                'code': 0,
                'message': get_message('RESOURCE_DELETE_SUCCESS'),
                'data': None
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"刪除資源失敗: {str(e)}")
            return {
                'code': 1,
                'message': get_message('RESOURCE_DELETE_FAILED'),
                'data': None
            }
    
    def batch_delete_resources(self, resource_ids: List[int]) -> Dict[str, Any]:
        """批量刪除資源"""
        try:
            deleted_count = 0
            for resource_id in resource_ids:
                resource = Resource.query.get(resource_id)
                if resource:
                    db.session.delete(resource)
                    deleted_count += 1
            
            db.session.commit()
            
            return {
                'code': 0,
                'message': get_message('RESOURCE_BATCH_DELETE_SUCCESS').format(count=deleted_count),
                'data': {'deleted_count': deleted_count}
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"批量刪除資源失敗: {str(e)}")
            return {
                'code': 1,
                'message': get_message('RESOURCE_BATCH_DELETE_FAILED'),
                'data': None
            }