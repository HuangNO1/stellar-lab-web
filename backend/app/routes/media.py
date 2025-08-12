from flask import Blueprint, request, jsonify, send_from_directory
from app.auth import admin_required
from app.utils.helpers import success_response, error_response
from app.utils.messages import msg
from app.services import MediaService
from app.services.base_service import ServiceException

bp = Blueprint('media', __name__)
media_service = MediaService()

@bp.route('/media/upload', methods=['POST'])
@admin_required
def upload_file():
    """上傳媒體文件"""
    try:
        if 'file' not in request.files:
            return jsonify(error_response(2000, '沒有選擇文件')), 400
        
        file = request.files['file']
        file_type = request.form.get('type', 'other')
        
        result = media_service.upload_file(file, file_type)
        return jsonify(success_response(result, msg.get_success_message('FILE_UPLOAD_SUCCESS')))
    except ServiceException as e:
        error_data = media_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/media/serve/<path:file_path>')
def serve_file(file_path):
    """提供文件服務"""
    try:
        file_info = media_service.serve_file(file_path)
        return send_from_directory(file_info['directory'], file_info['filename'])
    except ServiceException as e:
        error_data = media_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 500
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/media/info/<path:file_path>')
def get_media_info(file_path):
    """獲取媒體文件信息"""
    try:
        file_info = media_service.get_media_info(file_path)
        return jsonify(success_response(file_info))
    except ServiceException as e:
        error_data = media_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 500
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/media/health')
def health_check():
    """媒體服務健康檢查"""
    try:
        health_info = media_service.health_check()
        return jsonify(success_response(health_info))
    except ServiceException as e:
        error_data = media_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 500