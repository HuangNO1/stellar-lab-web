from flask import Blueprint, request, jsonify, g
from app import db
from app.models import ResearchGroup, Member, Lab, EditRecord
from app.auth import admin_required
from app.utils.validators import validate_string_length
from app.utils.helpers import get_pagination_params, paginate_query, success_response, error_response

bp = Blueprint('research_group', __name__)

@bp.route('/research-groups', methods=['GET'])
def get_research_groups():
    page, per_page = get_pagination_params()
    
    query = ResearchGroup.query
    
    # 搜索
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(
            db.or_(
                ResearchGroup.research_group_name_zh.contains(q),
                ResearchGroup.research_group_name_en.contains(q)
            )
        )
    
    # 按實驗室篩選
    lab_id = request.args.get('lab_id', type=int)
    if lab_id:
        query = query.filter(ResearchGroup.lab_id == lab_id)
    
    # 是否顯示已刪除
    show_all = request.args.get('show_all', 'false').lower() == 'true'
    if not show_all:
        query = query.filter(ResearchGroup.enable == 1)
    
    query = query.order_by(ResearchGroup.created_at.desc())
    result = paginate_query(query, page, per_page)
    
    return jsonify(success_response(result))

@bp.route('/research-groups/<int:group_id>', methods=['GET'])
def get_research_group(group_id):
    group = ResearchGroup.query.get_or_404(group_id)
    return jsonify(success_response(group.to_dict()))

@bp.route('/research-groups', methods=['POST'])
@admin_required
def create_research_group():
    data = request.get_json()
    
    # 參數校驗
    name_zh = data.get('research_group_name_zh', '').strip()
    name_en = data.get('research_group_name_en', '').strip()
    desc_zh = data.get('research_group_desc_zh', '').strip()
    desc_en = data.get('research_group_desc_en', '').strip()
    mem_id = data.get('mem_id', type=int)
    
    if not name_zh and not name_en:
        return jsonify(error_response(2000, '課題組名稱不能為空')), 400
    
    # 字符串長度校驗
    for field, value in [('name_zh', name_zh), ('name_en', name_en)]:
        if not validate_string_length(value, 500):
            return jsonify(error_response(2000, f'課題組名稱長度不能超過500字符')), 400
    
    for field, value in [('desc_zh', desc_zh), ('desc_en', desc_en)]:
        if not validate_string_length(value, 1000):
            return jsonify(error_response(2000, f'課題組描述長度不能超過1000字符')), 400
    
    # 檢查組長是否存在
    if mem_id:
        leader = Member.query.filter_by(mem_id=mem_id, enable=1).first()
        if not leader:
            return jsonify(error_response(3000, '指定的組長不存在')), 404
    
    # 獲取默認實驗室
    lab = Lab.query.filter_by(enable=1).first()
    if not lab:
        return jsonify(error_response(3000, '請先設置實驗室信息')), 404
    
    try:
        # 創建課題組
        group = ResearchGroup(
            lab_id=lab.lab_id,
            research_group_name_zh=name_zh,
            research_group_name_en=name_en,
            research_group_desc_zh=desc_zh,
            research_group_desc_en=desc_en,
            mem_id=mem_id,
            enable=1
        )
        
        db.session.add(group)
        db.session.flush()
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='CREATE',
            edit_module=2,  # 課題組模組
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(group.to_dict(), '課題組創建成功')), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'創建失敗: {str(e)}')), 500

@bp.route('/research-groups/<int:group_id>', methods=['PUT'])
@admin_required
def update_research_group(group_id):
    group = ResearchGroup.query.get_or_404(group_id)
    data = request.get_json()
    
    try:
        # 更新字段
        if 'research_group_name_zh' in data:
            value = data['research_group_name_zh'].strip()
            if not validate_string_length(value, 500):
                return jsonify(error_response(2000, '課題組中文名稱長度不能超過500字符')), 400
            group.research_group_name_zh = value
        
        if 'research_group_name_en' in data:
            value = data['research_group_name_en'].strip()
            if not validate_string_length(value, 500):
                return jsonify(error_response(2000, '課題組英文名稱長度不能超過500字符')), 400
            group.research_group_name_en = value
        
        if 'research_group_desc_zh' in data:
            value = data['research_group_desc_zh'].strip()
            if not validate_string_length(value, 1000):
                return jsonify(error_response(2000, '課題組中文描述長度不能超過1000字符')), 400
            group.research_group_desc_zh = value
        
        if 'research_group_desc_en' in data:
            value = data['research_group_desc_en'].strip()
            if not validate_string_length(value, 1000):
                return jsonify(error_response(2000, '課題組英文描述長度不能超過1000字符')), 400
            group.research_group_desc_en = value
        
        if 'mem_id' in data:
            mem_id = data['mem_id']
            if mem_id:
                leader = Member.query.filter_by(mem_id=mem_id, enable=1).first()
                if not leader:
                    return jsonify(error_response(3000, '指定的組長不存在')), 404
            group.mem_id = mem_id
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='UPDATE',
            edit_module=2,
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(group.to_dict(), '課題組更新成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'更新失敗: {str(e)}')), 500

@bp.route('/research-groups/<int:group_id>', methods=['DELETE'])
@admin_required
def delete_research_group(group_id):
    group = ResearchGroup.query.get_or_404(group_id)
    
    # 檢查是否有有效成員
    active_members = Member.query.filter_by(
        research_group_id=group_id,
        enable=1
    ).count()
    
    if active_members > 0:
        return jsonify(error_response(4000, '該課題組下仍有有效成員，無法刪除')), 409
    
    try:
        # 軟刪除
        group.enable = 0
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='DELETE',
            edit_module=2,
        )
        record.set_content({'deleted_group_id': group_id})
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(message='課題組刪除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'刪除失敗: {str(e)}')), 500