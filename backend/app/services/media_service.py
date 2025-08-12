import os
from typing import Dict, Any, Optional
from flask import current_app
from werkzeug.utils import secure_filename
from app.utils.file_handler import save_file, get_file_info, allowed_file
from app.utils.messages import msg
from .base_service import BaseService, ValidationError, NotFoundError


class MediaService(BaseService):
    """
    媒體文件管理服務層
    """
    
    def get_module_id(self) -> int:
        return 7
    
    def get_module_name(self) -> str:
        return 'media'
    
    def upload_file(self, file, file_type: str = 'other') -> Dict[str, Any]:
        """上傳文件"""
        # 驗證權限
        self.validate_permissions('CREATE')
        
        # 基本校驗
        if not file or file.filename == '':
            raise ValidationError(msg.get_error_message('NO_FILE_SELECTED'))
        
        # 根據類型設置大小限制
        max_sizes = {
            'lab_logo': 5 * 1024 * 1024,    # 5MB
            'member_avatar': 5 * 1024 * 1024,  # 5MB  
            'paper': 50 * 1024 * 1024,       # 50MB
            'other': 10 * 1024 * 1024        # 10MB
        }
        max_size = max_sizes.get(file_type, max_sizes['other'])
        
        # 根據類型確定文件類別
        if file_type in ['lab_logo', 'member_avatar']:
            file_category = 'image'
        elif file_type == 'paper':
            file_category = 'document'
        else:
            file_category = 'image'  # 默認為圖片
        
        def _upload_operation():
            try:
                file_path = save_file(file, file_type, max_size)
                
                # 生成訪問URL
                file_url = f"/api/media/serve{file_path}"
                
                return {
                    'path': file_path,
                    'url': file_url,
                    'filename': secure_filename(file.filename),
                    'type': file_type,
                    'category': file_category
                }
                
            except ValueError as e:
                raise ValidationError(str(e))
            except Exception as e:
                current_app.logger.error(f'文件上傳失敗: {str(e)}')
                raise ValidationError(msg.format_file_error('FILE_UPLOAD_FAILED', error=str(e)))
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_upload_operation,
            operation_type='UPLOAD',
            content={
                'filename': file.filename,
                'file_type': file_type,
                'file_size': self._get_file_size(file)
            }
        )
        
        return result
    
    def serve_file(self, file_path: str) -> Dict[str, Any]:
        """獲取文件服務信息"""
        # 安全檢查：確保路徑不包含危險字符
        if '..' in file_path or file_path.startswith('/'):
            raise ValidationError(msg.get_error_message('FILE_PATH_INVALID'))
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        full_path = os.path.join(upload_folder, file_path)
        
        # 檢查文件是否存在
        if not os.path.exists(full_path):
            raise NotFoundError(msg.get_error_message('FILE_NOT_FOUND'))
        
        # 檢查是否為文件
        if not os.path.isfile(full_path):
            raise ValidationError(msg.get_error_message('PATH_NOT_FILE'))
        
        # 獲取目錄和文件名
        directory = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        
        return {
            'directory': directory,
            'filename': filename,
            'full_path': full_path
        }
    
    def get_media_info(self, file_path: str) -> Dict[str, Any]:
        """獲取媒體文件信息"""
        try:
            # 添加/media/前綴如果沒有
            if not file_path.startswith('/media/'):
                file_path = f'/media/{file_path}'
            
            file_info = get_file_info(file_path)
            
            if not file_info:
                raise NotFoundError(msg.get_error_message('FILE_NOT_FOUND'))
            
            return file_info
        
        except Exception as e:
            current_app.logger.error(f'獲取文件信息失敗: {str(e)}')
            raise ValidationError(msg.get_error_message('FILE_INFO_FAILED'))
    
    def health_check(self) -> Dict[str, Any]:
        """媒體服務健康檢查"""
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            # 檢查上傳目錄是否存在和可寫
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder, exist_ok=True)
            
            # 嘗試創建測試文件
            test_file = os.path.join(upload_folder, '.health_check')
            with open(test_file, 'w') as f:
                f.write('ok')
            
            # 清理測試文件
            if os.path.exists(test_file):
                os.remove(test_file)
            
            return {
                'status': 'healthy',
                'upload_folder': upload_folder,
                'writable': True
            }
        
        except Exception as e:
            raise ValidationError(msg.format_file_error('MEDIA_SERVICE_UNHEALTHY', error=str(e)))
    
    def _get_file_size(self, file) -> int:
        """獲取文件大小"""
        try:
            # 保存當前位置
            current_pos = file.tell()
            # 移動到文件末尾
            file.seek(0, 2)
            # 獲取文件大小
            size = file.tell()
            # 恢復到原位置
            file.seek(current_pos)
            return size
        except Exception:
            return 0