from flask import Blueprint, request, jsonify
from app.auth import admin_required
from app.utils.helpers import success_response, error_response
from app.utils.messages import msg
from app.services import ImageUploadService
from app.services.base_service import ServiceException

bp = Blueprint('image_upload', __name__)
image_upload_service = ImageUploadService()

@bp.route('/images/upload', methods=['POST'])
@admin_required
def upload_description_image():
    """上傳描述字段圖片"""
    try:
        if 'file' not in request.files:
            return jsonify(error_response(2000, msg.get_error_message('NO_FILE_SELECTED'))), 400
        
        file = request.files['file']
        entity_type = request.form.get('entity_type')
        entity_id = request.form.get('entity_id', type=int)
        field_name = request.form.get('field_name')
        
        result = image_upload_service.upload_description_image(
            file=file,
            entity_type=entity_type,
            entity_id=entity_id,
            field_name=field_name
        )
        return jsonify(success_response(result, msg.get_success_message('FILE_UPLOAD_SUCCESS')))
    except ServiceException as e:
        print(f"ServiceException: {e}")  # 添加調試日誌
        error_data = image_upload_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
    except Exception as e:
        print(f"Unexpected error: {e}")  # 添加調試日誌
        import traceback
        traceback.print_exc()
        return jsonify(error_response(5000, "系統錯誤")), 500

@bp.route('/images/entity/<entity_type>/<int:entity_id>', methods=['GET'])
@admin_required
def get_entity_images(entity_type, entity_id):
    """獲取實體相關圖片列表"""
    try:
        field_name = request.args.get('field_name')
        images = image_upload_service.get_entity_images(entity_type, entity_id, field_name)
        return jsonify(success_response(images))
    except ServiceException as e:
        error_data = image_upload_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/images/<int:image_id>', methods=['DELETE'])
@admin_required
def delete_image(image_id):
    """刪除指定圖片"""
    try:
        image_upload_service.delete_image(image_id)
        return jsonify(success_response(None, msg.get_success_message('DELETE_SUCCESS')))
    except ServiceException as e:
        error_data = image_upload_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/images/cleanup', methods=['POST'])
@admin_required
def cleanup_unused_images():
    """清理未使用的圖片"""
    try:
        older_than_hours = request.json.get('older_than_hours', 24) if request.json else 24
        result = image_upload_service.cleanup_unused_images(older_than_hours)
        return jsonify(success_response(result, msg.get_success_message('DELETE_SUCCESS')))
    except ServiceException as e:
        error_data = image_upload_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400