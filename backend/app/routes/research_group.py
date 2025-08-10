from flask import Blueprint, request, jsonify
from app.auth import admin_required
from app.utils.helpers import success_response, error_response
from app.services import ResearchGroupService
from app.services.base_service import ServiceException

bp = Blueprint('research_group', __name__)
research_group_service = ResearchGroupService()

@bp.route('/research-groups', methods=['GET'])
def get_research_groups():
    """獲取課題組列表"""
    try:
        filters = {
            'q': request.args.get('q', '').strip(),
            'lab_id': request.args.get('lab_id', type=int),
            'show_all': request.args.get('show_all', 'false').lower() == 'true'
        }
        # 移除空值
        filters = {k: v for k, v in filters.items() if v is not None and v != ''}
        
        result = research_group_service.get_research_groups_list(filters)
        return jsonify(success_response(result))
    except ServiceException as e:
        error_data = research_group_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/research-groups/<int:group_id>', methods=['GET'])
def get_research_group(group_id):
    """獲取課題組詳情"""
    try:
        group = research_group_service.get_research_group_detail(group_id)
        return jsonify(success_response(group))
    except ServiceException as e:
        error_data = research_group_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/research-groups', methods=['POST'])
@admin_required
def create_research_group():
    """創建課題組"""
    try:
        data = request.get_json()
        group = research_group_service.create_research_group(data)
        return jsonify(success_response(group, '課題組創建成功')), 201
    except ServiceException as e:
        error_data = research_group_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/research-groups/<int:group_id>', methods=['PUT'])
@admin_required
def update_research_group(group_id):
    """更新課題組"""
    try:
        data = request.get_json()
        group = research_group_service.update_research_group(group_id, data)
        return jsonify(success_response(group, '課題組更新成功'))
    except ServiceException as e:
        error_data = research_group_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/research-groups/<int:group_id>', methods=['DELETE'])
@admin_required
def delete_research_group(group_id):
    """刪除課題組"""
    try:
        research_group_service.delete_research_group(group_id)
        return jsonify(success_response(message='課題組刪除成功'))
    except ServiceException as e:
        error_data = research_group_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code