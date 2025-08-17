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
        return jsonify({
            'code': 1,
            'message': '獲取資源列表失敗',
            'data': None
        }), 500

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
    try:
        data = request.get_json()
        result = resource_service.create_resource(data)
        
        if result['code'] == 0:
            audit_service.log_operation('resource', 'CREATE', {'resource_name': data.get('resource_name_zh', '')}, g.current_admin.admin_id)
        
        return jsonify(result), 201 if result['code'] == 0 else 400

    except Exception as e:
        logger.error(f"創建資源失敗: {str(e)}")
        return jsonify({
            'code': 1,
            'message': '創建資源失敗',
            'data': None
        }), 500

@resource_bp.route('/api/admin/resources/<int:resource_id>', methods=['PUT'])
@admin_required
def update_resource(resource_id):
    """更新資源 (管理員接口)"""
    try:
        logger.info(f"收到資源更新請求 - ID: {resource_id}, Content-Type: {request.content_type}")
        logger.info(f"請求頭: {dict(request.headers)}")
        
        # 根據Content-Type選擇數據源
        if request.is_json:
            logger.info("處理JSON請求")
            form_data = request.get_json() or {}
            files_data = None
        else:
            logger.info("處理multipart請求")
            form_data = dict(request.form)
            files_data = dict(request.files) if request.files else None
            if files_data and 'resource_image' in files_data:
                file = files_data['resource_image']
                logger.info(f"更新資源圖片: {file.filename}")
        
        logger.info(f"表單數據: {form_data}")
        logger.info(f"文件數據: {list(files_data.keys()) if files_data else None}")
        
        result = resource_service.update_resource(resource_id, form_data, files_data)
        
        if result['code'] == 0:
            audit_service.log_operation('resource', 'UPDATE', {'resource_name': form_data.get('resource_name_zh', '')}, g.current_admin.admin_id)
        
        return jsonify(result), 200 if result['code'] == 0 else 400

    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"更新資源失敗: {str(e)}")
        return jsonify({
            'code': 1,
            'message': '更新資源失敗',
            'data': None
        }), 500

@resource_bp.route('/api/admin/resources/<int:resource_id>', methods=['DELETE'])
@admin_required
def delete_resource(resource_id):
    """刪除資源 (管理員接口)"""
    try:
        # 先獲取資源信息以記錄操作
        resource_info = resource_service.get_resource(resource_id)
        resource_name = ''
        if resource_info['code'] == 0:
            resource_name = resource_info['data'].get('resource_name_zh', '')
        
        result = resource_service.delete_resource(resource_id)
        
        if result['code'] == 0:
            audit_service.log_operation('resource', 'DELETE', {'resource_name': resource_name}, g.current_admin.admin_id)
        
        return jsonify(result), 200 if result['code'] == 0 else 404

    except Exception as e:
        logger.error(f"刪除資源失敗: {str(e)}")
        return jsonify({
            'code': 1,
            'message': '刪除資源失敗',
            'data': None
        }), 500

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
        return jsonify({
            'code': 1,
            'message': '獲取資源列表失敗',
            'data': None
        }), 500

@resource_bp.route('/api/admin/resources/batch', methods=['DELETE'])
@admin_required
def batch_delete_resources():
    """批量刪除資源 (管理員接口)"""
    try:
        data = request.get_json()
        resource_ids = data.get('resource_ids', [])
        
        if not resource_ids:
            return jsonify({
                'code': 1,
                'message': '請選擇要刪除的資源',
                'data': None
            }), 400
        
        result = resource_service.batch_delete_resources(resource_ids)
        
        if result['code'] == 0:
            audit_service.log_operation('resource', 'BATCH_DELETE', {'deleted_count': result['data']['deleted_count']}, g.current_admin.admin_id)
        
        return jsonify(result)

    except Exception as e:
        logger.error(f"批量刪除資源失敗: {str(e)}")
        return jsonify({
            'code': 1,
            'message': '批量刪除資源失敗',
            'data': None
        }), 500