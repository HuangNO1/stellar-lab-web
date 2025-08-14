import os
import uuid
from datetime import datetime
from flask import current_app
from PIL import Image
import mimetypes
from .messages import msg

def allowed_file(filename, file_type='image'):
    if not filename or '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'image':
        return ext in current_app.config['ALLOWED_IMAGE_EXTENSIONS']
    elif file_type == 'document':
        return ext in current_app.config['ALLOWED_DOCUMENT_EXTENSIONS']
    elif file_type == 'member_avatar':
        return ext in current_app.config['ALLOWED_IMAGE_EXTENSIONS']
    
    return False

def save_file(file, file_type='other', max_size=None):
    if not file or file.filename == '':
        return None
    
    # 檢查文件類型
    if not allowed_file(file.filename, file_type):
        raise ValueError(msg.get_error_message('UNSUPPORTED_FILE_TYPE'))
    
    # 檢查文件大小 - 使用 content_length 避免讀取整個文件
    if max_size:
        # 優先使用 content_length
        if hasattr(file, 'content_length') and file.content_length:
            if file.content_length > max_size:
                raise ValueError(msg.get_error_message('FILE_SIZE_EXCEEDED', max_size=max_size))
        else:
            # 回退到原方法，但先保存當前位置
            current_pos = file.tell()
            file.seek(0, 2)  # 移動到文件末尾
            file_size = file.tell()
            file.seek(current_pos)  # 恢復原位置
            
            if file_size > max_size:
                raise ValueError(msg.get_error_message('FILE_SIZE_EXCEEDED', max_size=max_size))
    
    # 確保文件指針在開始位置
    file.seek(0)
    
    # 生成文件名
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    # 創建目錄結構
    upload_folder = current_app.config['UPLOAD_FOLDER']
    year_month = datetime.now().strftime('%Y%m')
    folder_path = os.path.join(upload_folder, file_type, year_month)
    os.makedirs(folder_path, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(folder_path, filename)
    file.save(file_path)
    
    # 對圖片進行處理
    if file_type in ['image', 'member_avatar']:
        try:
            with Image.open(file_path) as img:
                # 限制最大尺寸
                max_thumbnail_size = (1920, 1920)
                img.thumbnail(max_thumbnail_size, Image.Resampling.LANCZOS)
                img.save(file_path, optimize=True, quality=85)
        except Exception as e:
            os.remove(file_path)
            raise ValueError(msg.get_error_message('IMAGE_PROCESS_FAILED', error=str(e)))
    
    # 返回相對路徑
    relative_path = os.path.join(file_type, year_month, filename).replace('\\', '/')
    return f"/media/{relative_path}"

def delete_file(file_path):
    if not file_path:
        return
    
    try:
        # 將相對路徑轉為絕對路徑
        if file_path.startswith('/media/'):
            file_path = file_path[7:]  # 移除 /media/ 前綴
        
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
    except Exception as e:
        current_app.logger.error(msg.get_error_message('FILE_DELETE_FAILED', error=str(e)))

def get_file_info(file_path):
    if not file_path or not file_path.startswith('/media/'):
        return None
    
    relative_path = file_path[7:]  # 移除 /media/ 前綴
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], relative_path)
    
    if not os.path.exists(full_path):
        return None
    
    stat = os.stat(full_path)
    mime_type, _ = mimetypes.guess_type(full_path)
    
    return {
        'path': file_path,
        'size': stat.st_size,
        'mime_type': mime_type,
        'created_at': datetime.fromtimestamp(stat.st_ctime),
        'modified_at': datetime.fromtimestamp(stat.st_mtime)
    }