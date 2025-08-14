import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from flask import current_app
from app.models import UploadedImage
from app.utils.messages import msg
from .base_service import BaseService, ValidationError, NotFoundError


class ImageUploadService(BaseService):
    """
    圖片上傳管理服務層 - 專門處理markdown描述字段中的圖片上傳和管理
    """
    
    def get_module_id(self) -> int:
        return 8
    
    def get_module_name(self) -> str:
        return 'image_upload'
    
    def upload_description_image(self, file, entity_type: str = None, entity_id: int = None, field_name: str = None) -> Dict[str, Any]:
        """
        上傳描述字段中的圖片
        
        Args:
            file: 上傳的文件對象
            entity_type: 實體類型 (lab, member, paper, project, research_group)
            entity_id: 實體ID
            field_name: 字段名稱
        """
        # 驗證權限
        self.validate_permissions('CREATE')
        
        # 基本校驗
        if not file or file.filename == '':
            raise ValidationError(msg.get_error_message('NO_FILE_SELECTED'))
        
        # 驗證文件類型
        allowed_types = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_ext not in allowed_types:
            raise ValidationError(msg.get_error_message('UNSUPPORTED_FILE_TYPE'))
        
        # 文件大小限制 (5MB)
        max_size = 5 * 1024 * 1024
        
        def _upload_operation():
            from app.utils.file_handler import save_file
            
            try:
                # 保存文件到描述圖片目錄
                file_path = save_file(file, 'description_image', max_size)
                
                # 生成訪問URL - 確保路徑格式正確
                if file_path.startswith('/media/'):
                    clean_path = file_path[7:]  # 移除 '/media/' 前綴
                else:
                    clean_path = file_path
                file_url = f"/api/media/serve/{clean_path}"
                
                # 獲取文件信息
                file_size = self._get_file_size(file)
                mime_type = self._get_mime_type(file.filename)
                
                # 創建數據庫記錄
                uploaded_image = UploadedImage(
                    filename=file.filename,
                    file_path=file_path,
                    file_url=file_url,
                    file_size=file_size,
                    mime_type=mime_type,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    field_name=field_name,
                    is_used=False  # 初始為未使用狀態
                )
                
                self.db.session.add(uploaded_image)
                self.db.session.flush()
                
                return uploaded_image.to_dict()
                
            except ValueError as e:
                raise ValidationError(str(e))
            except Exception as e:
                current_app.logger.error(f'描述圖片上傳失敗: {str(e)}')
                raise ValidationError(msg.format_file_error('FILE_UPLOAD_FAILED', error=str(e)))
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_upload_operation,
            operation_type='UPLOAD',
            content={
                'filename': file.filename,
                'entity_type': entity_type,
                'entity_id': entity_id,
                'field_name': field_name,
                'file_size': self._get_file_size(file)
            }
        )
        
        return result
    
    def mark_images_as_used(self, content: str, entity_type: str, entity_id: int, field_name: str) -> None:
        """
        標記markdown內容中使用的圖片為已使用狀態
        
        Args:
            content: markdown內容
            entity_type: 實體類型
            entity_id: 實體ID  
            field_name: 字段名稱
        """
        if not content:
            return
        
        # 提取markdown中的圖片URL
        image_urls = self._extract_image_urls_from_markdown(content)
        
        for url in image_urls:
            # 從URL中提取文件路徑
            file_path = self._extract_file_path_from_url(url)
            if file_path:
                # 查找對應的上傳記錄
                uploaded_image = UploadedImage.query.filter_by(file_path=file_path).first()
                if uploaded_image:
                    # 更新使用狀態
                    uploaded_image.is_used = True
                    uploaded_image.used_at = datetime.utcnow()
                    uploaded_image.entity_type = entity_type
                    uploaded_image.entity_id = entity_id
                    uploaded_image.field_name = field_name
        
        self.db.session.commit()
    
    def cleanup_unused_images(self, older_than_hours: int = 24) -> Dict[str, Any]:
        """
        清理未使用的圖片
        
        Args:
            older_than_hours: 清理多少小時前的未使用圖片
        """
        # 驗證權限
        self.validate_permissions('DELETE')
        
        cutoff_time = datetime.utcnow() - timedelta(hours=older_than_hours)
        
        # 查找未使用的圖片
        unused_images = UploadedImage.query.filter(
            UploadedImage.is_used == False,
            UploadedImage.created_at < cutoff_time
        ).all()
        
        deleted_count = 0
        deleted_files = []
        
        for image in unused_images:
            try:
                # 刪除物理文件
                upload_folder = current_app.config['UPLOAD_FOLDER']
                full_path = os.path.join(upload_folder, image.file_path.lstrip('/media/'))
                
                if os.path.exists(full_path):
                    os.remove(full_path)
                
                # 刪除數據庫記錄
                self.db.session.delete(image)
                deleted_files.append(image.filename)
                deleted_count += 1
                
            except Exception as e:
                current_app.logger.error(f'刪除未使用圖片失敗: {image.filename}, 錯誤: {str(e)}')
        
        self.db.session.commit()
        
        return {
            'deleted_count': deleted_count,
            'deleted_files': deleted_files,
            'cutoff_time': cutoff_time.isoformat()
        }
    
    def get_entity_images(self, entity_type: str, entity_id: int, field_name: str = None) -> List[Dict[str, Any]]:
        """
        獲取實體相關的圖片列表
        
        Args:
            entity_type: 實體類型
            entity_id: 實體ID
            field_name: 字段名稱（可選）
        """
        query = UploadedImage.query.filter(
            UploadedImage.entity_type == entity_type,
            UploadedImage.entity_id == entity_id
        )
        
        if field_name:
            query = query.filter(UploadedImage.field_name == field_name)
        
        images = query.order_by(UploadedImage.created_at.desc()).all()
        return [image.to_dict() for image in images]
    
    def delete_image(self, image_id: int) -> None:
        """
        刪除指定圖片
        
        Args:
            image_id: 圖片ID
        """
        # 驗證權限
        self.validate_permissions('DELETE')
        
        uploaded_image = UploadedImage.query.filter_by(image_id=image_id).first()
        if not uploaded_image:
            raise NotFoundError(msg.get_error_message('FILE_NOT_FOUND'))
        
        def _delete_operation():
            try:
                # 刪除物理文件
                upload_folder = current_app.config['UPLOAD_FOLDER']
                full_path = os.path.join(upload_folder, uploaded_image.file_path.lstrip('/media/'))
                
                if os.path.exists(full_path):
                    os.remove(full_path)
                
                # 刪除數據庫記錄
                self.db.session.delete(uploaded_image)
                
                return {'deleted_image_id': image_id}
                
            except Exception as e:
                current_app.logger.error(f'刪除圖片失敗: {uploaded_image.filename}, 錯誤: {str(e)}')
                raise ValidationError(msg.format_file_error('FILE_DELETE_FAILED', error=str(e)))
        
        # 執行操作並記錄審計
        self.execute_with_audit(
            operation_func=_delete_operation,
            operation_type='DELETE',
            content={'deleted_image_id': image_id, 'filename': uploaded_image.filename}
        )
    
    def _extract_image_urls_from_markdown(self, content: str) -> List[str]:
        """從markdown內容中提取圖片URL"""
        # 匹配markdown圖片語法: ![alt](url) 和 HTML img標簽
        md_pattern = r'!\[.*?\]\((.*?)\)'
        html_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        
        urls = []
        urls.extend(re.findall(md_pattern, content))
        urls.extend(re.findall(html_pattern, content))
        
        # 過濾只包含本站圖片URL
        local_urls = []
        for url in urls:
            if url.startswith('/api/media/serve') or url.startswith('/media/'):
                local_urls.append(url)
        
        return local_urls
    
    def _extract_file_path_from_url(self, url: str) -> Optional[str]:
        """從URL中提取文件路徑"""
        if url.startswith('/api/media/serve'):
            return url.replace('/api/media/serve', '')
        elif url.startswith('/media/'):
            return url
        return None
    
    def _get_file_size(self, file) -> int:
        """獲取文件大小"""
        try:
            current_pos = file.tell()
            file.seek(0, 2)
            size = file.tell()
            file.seek(current_pos)
            return size
        except Exception:
            return 0
    
    def _get_mime_type(self, filename: str) -> str:
        """根據文件名獲取MIME類型"""
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'svg': 'image/svg+xml'
        }
        
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return mime_types.get(ext, 'application/octet-stream')