import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app.auth import admin_required
from app.utils.file_handler import save_file, get_file_info, allowed_file
from app.utils.helpers import success_response, error_response

bp = Blueprint('media', __name__)

@bp.route('/media/upload', methods=['POST'])
@admin_required
def upload_file():
    if 'file' not in request.files:
        return jsonify(error_response(2000, '沒有選擇文件')), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(error_response(2000, '沒有選擇文件')), 400
    
    file_type = request.form.get('type', 'other')
    
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
    
    try:
        file_path = save_file(file, file_type, max_size)
        
        # 生成訪問URL
        file_url = f"/api/media/serve{file_path}"
        
        return jsonify(success_response({
            'path': file_path,
            'url': file_url,
            'filename': secure_filename(file.filename),
            'type': file_type
        }, '文件上傳成功'))
        
    except ValueError as e:
        return jsonify(error_response(2000, str(e))), 400
    except Exception as e:
        current_app.logger.error(f'文件上傳失敗: {str(e)}')
        return jsonify(error_response(5000, f'上傳失敗: {str(e)}')), 500

@bp.route('/media/serve/<path:file_path>')
def serve_file(file_path):
    try:
        # 安全檢查：確保路徑不包含危險字符
        if '..' in file_path or file_path.startswith('/'):
            return jsonify(error_response(3000, '文件路徑無效')), 404
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        full_path = os.path.join(upload_folder, file_path)
        
        # 檢查文件是否存在
        if not os.path.exists(full_path):
            return jsonify(error_response(3000, '文件不存在')), 404
        
        # 檢查是否為文件
        if not os.path.isfile(full_path):
            return jsonify(error_response(3000, '路徑不是文件')), 404
        
        # 獲取目錄和文件名
        directory = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        
        return send_from_directory(directory, filename)
        
    except Exception as e:
        current_app.logger.error(f'文件服務失敗: {str(e)}')
        return jsonify(error_response(5000, '文件服務錯誤')), 500

@bp.route('/media/info/<path:file_path>')
def get_media_info(file_path):
    try:
        # 添加/media/前綴如果沒有
        if not file_path.startswith('/media/'):
            file_path = f'/media/{file_path}'
        
        file_info = get_file_info(file_path)
        
        if not file_info:
            return jsonify(error_response(3000, '文件不存在')), 404
        
        return jsonify(success_response(file_info))
        
    except Exception as e:
        current_app.logger.error(f'獲取文件信息失敗: {str(e)}')
        return jsonify(error_response(5000, '獲取文件信息失敗')), 500

# 健康檢查端點
@bp.route('/media/health')
def health_check():
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
        
        return jsonify(success_response({
            'status': 'healthy',
            'upload_folder': upload_folder,
            'writable': True
        }))
        
    except Exception as e:
        return jsonify(error_response(5000, f'媒體服務不健康: {str(e)}')), 500