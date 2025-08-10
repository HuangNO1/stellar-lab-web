from typing import Optional, Dict, Any
from flask import request
from app.models import Lab
from app.utils.validators import validate_email, validate_string_length
from app.utils.file_handler import save_file, delete_file
from .base_service import BaseService, ValidationError, NotFoundError


class LabService(BaseService):
    """
    實驗室管理服務層
    
    負責實驗室信息的業務邏輯：
    - 實驗室信息管理
    - 文件上傳處理
    - 數據校驗
    """
    
    def get_module_id(self) -> int:
        return 1
    
    def get_module_name(self) -> str:
        return 'lab'
    
    def get_lab_info(self) -> Dict[str, Any]:
        """
        獲取實驗室信息
        
        Returns:
            Dict: 實驗室信息
        """
        lab = Lab.query.filter_by(enable=1).first()
        
        if not lab:
            return self._get_default_lab_info()
        
        return lab.to_dict()
    
    def _get_default_lab_info(self) -> Dict[str, Any]:
        """獲取默認實驗室信息"""
        return {
            'lab_id': None,
            'lab_logo_path': None,
            'carousel_img_1': None,
            'carousel_img_2': None,
            'carousel_img_3': None,
            'carousel_img_4': None,
            'lab_zh': '實驗室',
            'lab_en': 'Laboratory',
            'lab_desc_zh': '請在管理後台設置實驗室信息',
            'lab_desc_en': 'Please set lab information in admin panel',
            'lab_address_zh': '',
            'lab_address_en': '',
            'lab_email': '',
            'lab_phone': '',
            'enable': 1
        }
    
    def update_lab_info(self, form_data: Dict[str, Any], files_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新實驗室信息
        
        Args:
            form_data: 表單數據
            files_data: 文件數據
            
        Returns:
            Dict: 更新後的實驗室信息
        """
        # 驗證權限
        self.validate_permissions('UPDATE')
        
        lab = Lab.query.filter_by(enable=1).first()
        is_create = lab is None
        
        if is_create:
            lab = Lab(enable=1)
        
        def _update_operation():
            # 處理文件上傳
            file_updates = self._handle_file_uploads(lab, files_data, form_data)
            
            # 處理文本字段
            text_updates = self._handle_text_fields(lab, form_data)
            
            # 合併更新數據
            update_data = {**file_updates, **text_updates}
            
            if is_create:
                self.db.session.add(lab)
                self.db.session.flush()
            
            return lab.to_dict(), update_data
        
        # 執行操作並記錄審計
        result, update_data = self.execute_with_audit(
            operation_func=_update_operation,
            operation_type='CREATE' if is_create else 'UPDATE',
            content=update_data
        )
        
        return result
    
    def delete_lab(self) -> None:
        """
        刪除實驗室
        
        Raises:
            ValidationError: 實驗室下還有有效的課題組或成員
            NotFoundError: 實驗室不存在
        """
        # 驗證權限
        self.validate_permissions('DELETE')
        
        lab = Lab.query.filter_by(enable=1).first()
        if not lab:
            raise NotFoundError('實驗室不存在')
        
        # 檢查是否可以刪除
        self._check_lab_deletable(lab)
        
        def _delete_operation():
            # 軟刪除
            self.soft_delete(lab, "實驗室")
            
            # 清理相關文件
            self._cleanup_lab_files(lab)
            
            return {'deleted_lab_id': lab.lab_id}
        
        # 執行操作並記錄審計
        self.execute_with_audit(
            operation_func=_delete_operation,
            operation_type='DELETE',
            content={'deleted_lab_id': lab.lab_id}
        )
    
    def _handle_file_uploads(self, lab: Lab, files_data: Dict[str, Any], form_data: Dict[str, Any]) -> Dict[str, Any]:
        """處理文件上傳"""
        updates = {}
        
        # 處理logo上傳
        logo_update = self._handle_logo_upload(lab, files_data)
        if logo_update:
            updates.update(logo_update)
        
        # 處理輪播圖片
        carousel_updates = self._handle_carousel_images(lab, files_data, form_data)
        if carousel_updates:
            updates.update(carousel_updates)
        
        return updates
    
    def _handle_logo_upload(self, lab: Lab, files_data: Dict[str, Any]) -> Dict[str, Any]:
        """處理logo上傳"""
        if 'lab_logo' not in files_data:
            return {}
        
        file = files_data['lab_logo']
        if not file or not file.filename:
            return {}
        
        old_logo_path = lab.lab_logo_path
        
        try:
            new_logo_path = save_file(file, 'lab_logo', max_size=5*1024*1024)
            lab.lab_logo_path = new_logo_path
            
            # 刪除舊文件
            if old_logo_path and old_logo_path != new_logo_path:
                delete_file(old_logo_path)
            
            return {'lab_logo_updated': True, 'new_logo_path': new_logo_path}
            
        except Exception as e:
            raise ValidationError(f"Logo上傳失敗: {str(e)}")
    
    def _handle_carousel_images(self, lab: Lab, files_data: Dict[str, Any], form_data: Dict[str, Any]) -> Dict[str, Any]:
        """處理輪播圖片"""
        updates = {}
        carousel_fields = ['carousel_img_1', 'carousel_img_2', 'carousel_img_3', 'carousel_img_4']
        
        for field in carousel_fields:
            field_update = self._handle_single_carousel(lab, field, files_data, form_data)
            if field_update:
                updates.update(field_update)
        
        return updates
    
    def _handle_single_carousel(self, lab: Lab, field_name: str, files_data: Dict[str, Any], form_data: Dict[str, Any]) -> Dict[str, Any]:
        """處理單個輪播圖片"""
        old_path = getattr(lab, field_name)
        clear_param = f'clear_{field_name}'
        
        # 檢查是否要清除圖片
        if clear_param in form_data and form_data[clear_param].lower() == 'true':
            setattr(lab, field_name, None)
            if old_path:
                delete_file(old_path)
            return {f'{field_name}_cleared': True}
        
        # 檢查是否有新圖片上傳
        if field_name in files_data:
            file = files_data[field_name]
            if file and file.filename:
                try:
                    new_path = save_file(file, field_name, max_size=5*1024*1024)
                    setattr(lab, field_name, new_path)
                    
                    # 刪除舊文件
                    if old_path and old_path != new_path:
                        delete_file(old_path)
                    
                    return {f'{field_name}_updated': True, f'new_{field_name}_path': new_path}
                    
                except Exception as e:
                    raise ValidationError(f"{field_name}上傳失敗: {str(e)}")
        
        return {}
    
    def _handle_text_fields(self, lab: Lab, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """處理文本字段"""
        text_fields = [
            'lab_zh', 'lab_en', 'lab_desc_zh', 'lab_desc_en',
            'lab_address_zh', 'lab_address_en', 'lab_email', 'lab_phone'
        ]
        
        update_data = {}
        
        for field in text_fields:
            if field in form_data:
                value = form_data[field].strip() if form_data[field] else ''
                
                # 數據校驗
                self._validate_text_field(field, value)
                
                # 只有值變化時才記錄
                if getattr(lab, field) != value:
                    setattr(lab, field, value)
                    update_data[field] = value
        
        return update_data
    
    def _validate_text_field(self, field: str, value: str) -> None:
        """校驗文本字段"""
        # 郵箱格式校驗
        if field == 'lab_email' and value:
            if not validate_email(value):
                raise ValidationError('郵箱格式不正確')
        
        # 長度校驗
        if field.startswith('lab_desc'):
            max_length = 1000
        else:
            max_length = 500
        
        if not validate_string_length(value, max_length):
            raise ValidationError(f'{field} 長度不能超過{max_length}字符')
    
    def _check_lab_deletable(self, lab: Lab) -> None:
        """檢查實驗室是否可以刪除"""
        from app.models import ResearchGroup, Member
        
        # 檢查是否有有效的課題組
        active_groups = ResearchGroup.query.filter_by(lab_id=lab.lab_id, enable=1).count()
        if active_groups > 0:
            raise ValidationError(f'實驗室下還有{active_groups}個有效課題組，無法刪除')
        
        # 檢查是否有有效的成員
        active_members = Member.query.filter_by(lab_id=lab.lab_id, enable=1).count()
        if active_members > 0:
            raise ValidationError(f'實驗室下還有{active_members}個有效成員，無法刪除')
    
    def _cleanup_lab_files(self, lab: Lab) -> None:
        """清理實驗室相關文件"""
        files_to_delete = [
            lab.lab_logo_path,
            lab.carousel_img_1,
            lab.carousel_img_2,
            lab.carousel_img_3,
            lab.carousel_img_4
        ]
        
        for file_path in files_to_delete:
            if file_path:
                try:
                    delete_file(file_path)
                except Exception:
                    # 文件刪除失敗不影響業務流程
                    pass