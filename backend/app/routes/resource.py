"""資源相關路由"""

from flask import Blueprint, request, jsonify, g
from app.auth.decorators import admin_required
from app.services.resource_service import ResourceService
from app.services.audit_service import AuditService
import logging

logger = logging.getLogger(__name__)

resource_bp = Blueprint('resource', __name__)
resource_service = ResourceService()
audit_service = AuditService()

@resource_bp.route('/api/resources', methods=['GET'])
def get_resources():
    """獲取資源列表 (公開接口)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        q = request.args.get('q', '')
        resource_type = request.args.get('resource_type')
        availability_status = request.args.get('availability_status')
        sort_by = request.args.get('sort_by', 'created_time')
        order = request.args.get('order', 'desc')

        # 類型轉換
        if resource_type is not None:
            resource_type = int(resource_type)
        if availability_status is not None:
            availability_status = int(availability_status)

        result = resource_service.get_resources(
            page=page,
            per_page=per_page,
            q=q,
            resource_type=resource_type,
            availability_status=availability_status,
            sort_by=sort_by,
            order=order
        )

        return jsonify(result)

    except Exception as e:
        logger.error(f"獲取資源列表失敗: {str(e)}")
        from app.utils.helpers import error_response
        from app.utils.messages import msg
        return jsonify(error_response(1, msg.get_error_message('RESOURCE_FETCH_FAILED'))), 500

@resource_bp.route('/api/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    """獲取單個資源 (公開接口)"""
    result = resource_service.get_resource(resource_id)
    
    if result['code'] == 0:
        return jsonify(result)
    else:
        return jsonify(result), 404

@resource_bp.route('/api/admin/resources', methods=['POST'])
@admin_required
def create_resource():
    """創建資源 (管理員接口)"""
    from app.utils.helpers import success_response, error_response
    from app.services.base_service import ServiceException
    
    try:
        data = request.get_json()
        result = resource_service.create_resource(data, g.current_admin.admin_id)
        return jsonify(success_response(result))
    except ServiceException as e:
        error_data = resource_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@resource_bp.route('/api/admin/resources/<int:resource_id>', methods=['PUT'])
@admin_required
def update_resource(resource_id):
    """更新資源 (管理員接口)"""
    from app.utils.helpers import success_response, error_response
    from app.services.base_service import ServiceException
    
    try:
        # 根據Content-Type選擇數據源
        if request.is_json:
            form_data = request.get_json() or {}
            files_data = None
        else:
            form_data = dict(request.form)
            files_data = dict(request.files) if request.files else None
        
        result = resource_service.update_resource(resource_id, form_data, g.current_admin.admin_id, files_data)
        return jsonify(success_response(result))
    except ServiceException as e:
        error_data = resource_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@resource_bp.route('/api/admin/resources/<int:resource_id>', methods=['DELETE'])
@admin_required
def delete_resource(resource_id):
    """刪除資源 (管理員接口)"""
    from app.utils.helpers import success_response, error_response
    from app.services.base_service import ServiceException
    
    try:
        result = resource_service.delete_resource(resource_id, g.current_admin.admin_id)
        return jsonify(success_response(result))
    except ServiceException as e:
        error_data = resource_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@resource_bp.route('/api/admin/resources', methods=['GET'])
@admin_required
def get_admin_resources():
    """獲取資源列表 (管理員接口)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        q = request.args.get('q', '')
        resource_type = request.args.get('resource_type')
        availability_status = request.args.get('availability_status')
        sort_by = request.args.get('sort_by', 'created_time')
        order = request.args.get('order', 'desc')

        # 類型轉換
        if resource_type is not None:
            resource_type = int(resource_type)
        if availability_status is not None:
            availability_status = int(availability_status)

        result = resource_service.get_resources(
            page=page,
            per_page=per_page,
            q=q,
            resource_type=resource_type,
            availability_status=availability_status,
            sort_by=sort_by,
            order=order
        )

        return jsonify(result)

    except Exception as e:
        logger.error(f"獲取資源列表失敗: {str(e)}")
        from app.utils.helpers import error_response
        from app.utils.messages import msg
        return jsonify(error_response(1, msg.get_error_message('RESOURCE_FETCH_FAILED'))), 500

@resource_bp.route('/api/admin/resources/batch', methods=['DELETE'])
@admin_required
def batch_delete_resources():
    """批量刪除資源 (管理員接口)"""
    from app.utils.helpers import success_response, error_response
    from app.services.base_service import ServiceException
    
    try:
        data = request.get_json()
        resource_ids = data.get('resource_ids', [])
        
        if not resource_ids:
            from app.utils.messages import msg
            return jsonify(error_response(1, msg.get_error_message('RESOURCE_SELECT_REQUIRED'))), 400
        
        result = resource_service.batch_delete_resources(resource_ids, g.current_admin.admin_id)
        return jsonify(success_response(result))
    except ServiceException as e:
        error_data = resource_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400