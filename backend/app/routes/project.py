from flask import Blueprint, request, jsonify
from app.auth import admin_required
from app.utils.helpers import success_response, error_response
from app.utils.messages import msg
from app.services import ProjectService
from app.services.base_service import ServiceException

bp = Blueprint('project', __name__)
project_service = ProjectService()

@bp.route('/projects', methods=['GET'])
def get_projects():
    """獲取項目列表"""
    try:
        filters = {
            'q': request.args.get('q', '').strip(),
            'is_end': request.args.get('is_end', type=int),
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'show_all': request.args.get('show_all', 'false').lower() == 'true',
            'sort_by': request.args.get('sort_by', 'project_date_start'),
            'order': request.args.get('order', 'desc')
        }
        # 移除空值
        filters = {k: v for k, v in filters.items() if v is not None and v != ''}
        
        result = project_service.get_projects_list(filters)
        return jsonify(success_response(result))
    except ServiceException as e:
        error_data = project_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """獲取項目詳情"""
    try:
        project = project_service.get_project_detail(project_id)
        return jsonify(success_response(project))
    except ServiceException as e:
        error_data = project_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/projects', methods=['POST'])
@admin_required
def create_project():
    """創建項目"""
    try:
        data = request.get_json()
        project = project_service.create_project(data)
        return jsonify(success_response(project, msg.get_success_message('PROJECT_CREATE_SUCCESS'))), 201
    except ServiceException as e:
        error_data = project_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/projects/<int:project_id>', methods=['PUT'])
@admin_required
def update_project(project_id):
    """更新項目"""
    try:
        data = request.get_json()
        project = project_service.update_project(project_id, data)
        return jsonify(success_response(project, msg.get_success_message('PROJECT_UPDATE_SUCCESS')))
    except ServiceException as e:
        error_data = project_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/projects/<int:project_id>', methods=['DELETE'])
@admin_required
def delete_project(project_id):
    """刪除項目"""
    try:
        project_service.delete_project(project_id)
        return jsonify(success_response(message=msg.get_success_message('PROJECT_DELETE_SUCCESS')))
    except ServiceException as e:
        error_data = project_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code