from flask import Blueprint, request, jsonify, g
from app import db
from app.models import Project, EditRecord
from app.auth import admin_required
from app.utils.validators import validate_date, validate_string_length, validate_enum
from app.utils.helpers import get_pagination_params, paginate_query, success_response, error_response

bp = Blueprint('project', __name__)

@bp.route('/projects', methods=['GET'])
def get_projects():
    page, per_page = get_pagination_params()
    
    query = Project.query
    
    # 搜索
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(
            db.or_(
                Project.project_name_zh.contains(q),
                Project.project_name_en.contains(q),
                Project.project_desc_zh.contains(q),
                Project.project_desc_en.contains(q)
            )
        )
    
    # 按結項狀態篩選
    is_end = request.args.get('is_end', type=int)
    if is_end is not None:
        query = query.filter(Project.is_end == is_end)
    
    # 按開始日期範圍篩選
    start_date = request.args.get('start_date')
    if start_date:
        valid, date_obj = validate_date(start_date)
        if valid and date_obj:
            query = query.filter(Project.project_date_start >= date_obj)
    
    end_date = request.args.get('end_date')
    if end_date:
        valid, date_obj = validate_date(end_date)
        if valid and date_obj:
            query = query.filter(Project.project_date_start <= date_obj)
    
    # 是否顯示已刪除
    show_all = request.args.get('show_all', 'false').lower() == 'true'
    if not show_all:
        query = query.filter(Project.enable == 1)
    
    # 排序
    sort_by = request.args.get('sort_by', 'project_date_start')
    order = request.args.get('order', 'desc')
    
    if sort_by == 'name':
        sort_field = Project.project_name_zh
    elif sort_by == 'status':
        sort_field = Project.is_end
    else:
        sort_field = Project.project_date_start
    
    if order.lower() == 'asc':
        query = query.order_by(sort_field.asc())
    else:
        query = query.order_by(sort_field.desc())
    
    result = paginate_query(query, page, per_page)
    return jsonify(success_response(result))

@bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(success_response(project.to_dict()))

@bp.route('/projects', methods=['POST'])
@admin_required
def create_project():
    data = request.get_json()
    
    # 參數校驗
    project_name_zh = data.get('project_name_zh', '').strip()
    project_name_en = data.get('project_name_en', '').strip()
    project_desc_zh = data.get('project_desc_zh', '').strip()
    project_desc_en = data.get('project_desc_en', '').strip()
    project_url = data.get('project_url', '').strip()
    project_date_start_str = data.get('project_date_start')
    is_end = data.get('is_end', 0)
    
    if not project_name_zh and not project_name_en:
        return jsonify(error_response(2000, '項目名稱不能為空')), 400
    
    # 日期校驗
    valid, project_date_start = validate_date(project_date_start_str)
    if project_date_start_str and not valid:
        return jsonify(error_response(2000, '日期格式不正確')), 400
    
    # 狀態校驗
    if not validate_enum(is_end, [0, 1]):
        return jsonify(error_response(2000, '結項狀態錯誤')), 400
    
    # 字符串長度校驗
    string_fields = {
        'project_name_zh': 500, 'project_name_en': 500,
        'project_desc_zh': 1000, 'project_desc_en': 1000,
        'project_url': 500
    }
    
    for field, max_len in string_fields.items():
        value = data.get(field, '').strip()
        if not validate_string_length(value, max_len):
            return jsonify(error_response(2000, f'{field} 長度超過限制')), 400
    
    try:
        # 創建項目
        project = Project(
            project_name_zh=project_name_zh,
            project_name_en=project_name_en,
            project_desc_zh=project_desc_zh,
            project_desc_en=project_desc_en,
            project_url=project_url,
            project_date_start=project_date_start,
            is_end=is_end,
            enable=1
        )
        
        db.session.add(project)
        db.session.flush()
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='CREATE',
            edit_module=6,  # 項目模組
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(project.to_dict(), '項目創建成功')), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'創建失敗: {str(e)}')), 500

@bp.route('/projects/<int:project_id>', methods=['PUT'])
@admin_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    
    try:
        # 更新字段
        string_fields = [
            'project_name_zh', 'project_name_en', 
            'project_desc_zh', 'project_desc_en', 
            'project_url'
        ]
        
        for field in string_fields:
            if field in data:
                value = data[field].strip()
                max_len = 1000 if 'desc' in field else 500
                
                if not validate_string_length(value, max_len):
                    return jsonify(error_response(2000, f'{field} 長度超過限制')), 400
                
                setattr(project, field, value)
        
        # 更新日期
        if 'project_date_start' in data:
            valid, date_obj = validate_date(data['project_date_start'])
            if data['project_date_start'] and not valid:
                return jsonify(error_response(2000, '日期格式不正確')), 400
            project.project_date_start = date_obj
        
        # 更新狀態
        if 'is_end' in data:
            if not validate_enum(data['is_end'], [0, 1]):
                return jsonify(error_response(2000, '結項狀態錯誤')), 400
            project.is_end = data['is_end']
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='UPDATE',
            edit_module=6,
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(project.to_dict(), '項目更新成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'更新失敗: {str(e)}')), 500

@bp.route('/projects/<int:project_id>', methods=['DELETE'])
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    try:
        # 軟刪除
        project.enable = 0
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='DELETE',
            edit_module=6,
        )
        record.set_content({'deleted_project_id': project_id})
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(message='項目刪除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'刪除失敗: {str(e)}')), 500