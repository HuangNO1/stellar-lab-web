from flask import Blueprint, request, jsonify, g
from app.auth import admin_required, super_admin_required
from app.utils.helpers import success_response, error_response
from app.services import AdminService
from app.services.base_service import ServiceException
from app.utils.messages import msg

bp = Blueprint('admin', __name__)
admin_service = AdminService()

@bp.route('/admins', methods=['GET'])
@super_admin_required
def get_admins():
    """獲取管理員列表"""
    try:
        filters = {
            'q': request.args.get('q', '').strip(),
            'show_all': request.args.get('show_all', 'false').lower() == 'true'
        }
        # 移除空值
        filters = {k: v for k, v in filters.items() if v is not None and v != ''}
        
        result = admin_service.get_admins_list(filters, g.current_admin.admin_id)
        return jsonify(success_response(result))
    except ServiceException as e:
        error_data = admin_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/admins', methods=['POST'])
@super_admin_required
def create_admin():
    """創建管理員"""
    try:
        data = request.get_json()
        admin = admin_service.create_admin(data)
        return jsonify(success_response(admin, msg.get_success_message('ADMIN_CREATE_SUCCESS'))), 201
    except ServiceException as e:
        error_data = admin_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/admins/<int:admin_id>', methods=['PUT'])
@super_admin_required
def update_admin(admin_id):
    """更新管理員"""
    try:
        data = request.get_json()
        admin = admin_service.update_admin(admin_id, data, g.current_admin.admin_id)
        return jsonify(success_response(admin, msg.get_success_message('ADMIN_UPDATE_SUCCESS')))
    except ServiceException as e:
        error_data = admin_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/admins/<int:admin_id>', methods=['DELETE'])
@super_admin_required
def delete_admin(admin_id):
    """刪除管理員"""
    try:
        admin_service.delete_admin(admin_id, g.current_admin.admin_id)
        return jsonify(success_response(message=msg.get_success_message('ADMIN_DELETE_SUCCESS')))
    except ServiceException as e:
        error_data = admin_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/admins/<int:admin_id>/reset-password', methods=['POST'])
@super_admin_required
def reset_admin_password(admin_id):
    """重置管理員密碼"""
    try:
        data = request.get_json()
        if not data or 'new_password' not in data:
            return jsonify(error_response(2000, msg.get_error_message('MISSING_REQUIRED_FIELDS'))), 400
        
        new_password = data.get('new_password', '')
        admin_service.reset_admin_password(admin_id, new_password, g.current_admin.admin_id)
        return jsonify(success_response(message=msg.get_success_message('PASSWORD_RESET_SUCCESS')))
    except ServiceException as e:
        error_data = admin_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code