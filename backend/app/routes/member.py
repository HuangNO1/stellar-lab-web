from flask import Blueprint, request, jsonify, g
from app import db
from app.models import Member, ResearchGroup, Lab, EditRecord
from app.auth import admin_required
from app.utils.validators import validate_email, validate_string_length, validate_enum
from app.utils.helpers import get_pagination_params, paginate_query, success_response, error_response
from app.utils.file_handler import save_file, delete_file

bp = Blueprint('member', __name__)

@bp.route('/members', methods=['GET'])
def get_members():
    page, per_page = get_pagination_params()
    
    query = Member.query
    
    # 搜索
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(
            db.or_(
                Member.mem_name_zh.contains(q),
                Member.mem_name_en.contains(q),
                Member.mem_email.contains(q)
            )
        )
    
    # 按類型篩選
    mem_type = request.args.get('type', type=int)
    if mem_type is not None:
        query = query.filter(Member.mem_type == mem_type)
    
    # 按課題組篩選
    research_group_id = request.args.get('research_group_id', type=int)
    if research_group_id:
        query = query.filter(Member.research_group_id == research_group_id)
    
    # 按實驗室篩選
    lab_id = request.args.get('lab_id', type=int)
    if lab_id:
        query = query.filter(Member.lab_id == lab_id)
    
    # 是否顯示已刪除
    show_all = request.args.get('show_all', 'false').lower() == 'true'
    if not show_all:
        query = query.filter(Member.enable == 1)
    
    # 排序
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    
    if sort_by == 'name':
        sort_field = Member.mem_name_zh
    elif sort_by == 'type':
        sort_field = Member.mem_type
    else:
        sort_field = Member.created_at
    
    if order.lower() == 'asc':
        query = query.order_by(sort_field.asc())
    else:
        query = query.order_by(sort_field.desc())
    
    result = paginate_query(query, page, per_page)
    return jsonify(success_response(result))

@bp.route('/members/<int:mem_id>', methods=['GET'])
def get_member(mem_id):
    member = Member.query.get_or_404(mem_id)
    return jsonify(success_response(member.to_dict()))

@bp.route('/members', methods=['POST'])
@admin_required
def create_member():
    try:
        # 處理頭像上傳
        avatar_path = None
        if 'mem_avatar' in request.files:
            file = request.files['mem_avatar']
            if file and file.filename:
                avatar_path = save_file(file, 'member_avatar', max_size=5*1024*1024)
        
        # 獲取表單數據
        data = {
            'mem_name_zh': request.form.get('mem_name_zh', '').strip(),
            'mem_name_en': request.form.get('mem_name_en', '').strip(),
            'mem_desc_zh': request.form.get('mem_desc_zh', '').strip(),
            'mem_desc_en': request.form.get('mem_desc_en', '').strip(),
            'mem_email': request.form.get('mem_email', '').strip(),
            'mem_type': int(request.form.get('mem_type', 0)),
            'job_type': request.form.get('job_type', type=int),
            'student_type': request.form.get('student_type', type=int),
            'student_grade': request.form.get('student_grade', type=int),
            'destination_zh': request.form.get('destination_zh', '').strip(),
            'destination_en': request.form.get('destination_en', '').strip(),
            'research_group_id': int(request.form.get('research_group_id')),
        }
        
        # 參數校驗
        if not data['mem_name_zh'] and not data['mem_name_en']:
            return jsonify(error_response(2000, '成員姓名不能為空')), 400
        
        # 郵箱校驗
        if data['mem_email'] and not validate_email(data['mem_email']):
            return jsonify(error_response(2000, '郵箱格式不正確')), 400
        
        # 類型校驗
        if not validate_enum(data['mem_type'], [0, 1, 2]):
            return jsonify(error_response(2000, '成員類型錯誤')), 400
        
        # 職稱類型校驗
        if data['job_type'] is not None and not validate_enum(data['job_type'], [0, 1, 2, 3, 4]):
            return jsonify(error_response(2000, '職稱類型錯誤')), 400
        
        # 學生類型校驗
        if data['student_type'] is not None and not validate_enum(data['student_type'], [0, 1, 2]):
            return jsonify(error_response(2000, '學生類型錯誤')), 400
        
        # 字符串長度校驗
        string_fields = {
            'mem_name_zh': 500, 'mem_name_en': 500,
            'mem_desc_zh': 5000, 'mem_desc_en': 5000,
            'mem_email': 500, 'destination_zh': 500, 'destination_en': 500
        }
        
        for field, max_len in string_fields.items():
            if not validate_string_length(data[field], max_len):
                return jsonify(error_response(2000, f'{field} 長度超過限制')), 400
        
        # 檢查課題組是否存在
        research_group = ResearchGroup.query.filter_by(
            research_group_id=data['research_group_id'],
            enable=1
        ).first()
        if not research_group:
            return jsonify(error_response(3000, '指定的課題組不存在')), 404
        
        # 獲取默認實驗室
        lab = Lab.query.filter_by(enable=1).first()
        if not lab:
            return jsonify(error_response(3000, '請先設置實驗室信息')), 404
        
        # 創建成員
        member = Member(
            mem_avatar_path=avatar_path,
            mem_name_zh=data['mem_name_zh'],
            mem_name_en=data['mem_name_en'],
            mem_desc_zh=data['mem_desc_zh'],
            mem_desc_en=data['mem_desc_en'],
            mem_email=data['mem_email'],
            mem_type=data['mem_type'],
            job_type=data['job_type'],
            student_type=data['student_type'],
            student_grade=data['student_grade'],
            destination_zh=data['destination_zh'],
            destination_en=data['destination_en'],
            research_group_id=data['research_group_id'],
            lab_id=lab.lab_id,
            enable=1
        )
        
        db.session.add(member)
        db.session.flush()
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='CREATE',
            edit_module=3,  # 成員模組
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(member.to_dict(), '成員創建成功')), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'創建失敗: {str(e)}')), 500

@bp.route('/members/<int:mem_id>', methods=['PUT'])
@admin_required
def update_member(mem_id):
    member = Member.query.get_or_404(mem_id)
    
    try:
        # 處理頭像上傳
        old_avatar_path = member.mem_avatar_path
        if 'mem_avatar' in request.files:
            file = request.files['mem_avatar']
            if file and file.filename:
                new_avatar_path = save_file(file, 'member_avatar', max_size=5*1024*1024)
                member.mem_avatar_path = new_avatar_path
                
                # 刪除舊頭像
                if old_avatar_path and old_avatar_path != new_avatar_path:
                    delete_file(old_avatar_path)
        
        # 更新文本字段
        update_data = {}
        text_fields = [
            'mem_name_zh', 'mem_name_en', 'mem_desc_zh', 'mem_desc_en',
            'mem_email', 'destination_zh', 'destination_en'
        ]
        
        for field in text_fields:
            if field in request.form:
                value = request.form[field].strip()
                
                # 特殊校驗
                if field == 'mem_email' and value:
                    if not validate_email(value):
                        return jsonify(error_response(2000, '郵箱格式不正確')), 400
                
                # 長度校驗
                max_len = 5000 if 'desc' in field else 500
                if not validate_string_length(value, max_len):
                    return jsonify(error_response(2000, f'{field} 長度超過限制')), 400
                
                setattr(member, field, value)
                update_data[field] = value
        
        # 更新數字字段
        int_fields = ['mem_type', 'job_type', 'student_type', 'student_grade', 'research_group_id']
        for field in int_fields:
            if field in request.form:
                value = request.form.get(field, type=int)
                
                # 特殊校驗
                if field == 'mem_type' and not validate_enum(value, [0, 1, 2]):
                    return jsonify(error_response(2000, '成員類型錯誤')), 400
                
                if field == 'job_type' and value is not None and not validate_enum(value, [0, 1, 2, 3, 4]):
                    return jsonify(error_response(2000, '職稱類型錯誤')), 400
                
                if field == 'student_type' and value is not None and not validate_enum(value, [0, 1, 2]):
                    return jsonify(error_response(2000, '學生類型錯誤')), 400
                
                if field == 'research_group_id':
                    # 檢查課題組是否存在
                    group = ResearchGroup.query.filter_by(
                        research_group_id=value,
                        enable=1
                    ).first()
                    if not group:
                        return jsonify(error_response(3000, '指定的課題組不存在')), 404
                
                setattr(member, field, value)
                update_data[field] = value
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='UPDATE',
            edit_module=3,
        )
        record.set_content(update_data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(member.to_dict(), '成員更新成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'更新失敗: {str(e)}')), 500

@bp.route('/members/<int:mem_id>', methods=['DELETE'])
@admin_required
def delete_member(mem_id):
    member = Member.query.get_or_404(mem_id)
    
    try:
        # 軟刪除
        member.enable = 0
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='DELETE',
            edit_module=3,
        )
        record.set_content({'deleted_member_id': mem_id})
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(message='成員刪除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'刪除失敗: {str(e)}')), 500

@bp.route('/members/batch', methods=['DELETE'])
@admin_required
def batch_delete_members():
    """批量刪除成員"""
    data = request.get_json()
    
    if not data or 'member_ids' not in data:
        return jsonify(error_response(2000, '缺少member_ids參數')), 400
    
    member_ids = data.get('member_ids', [])
    
    if not isinstance(member_ids, list) or len(member_ids) == 0:
        return jsonify(error_response(2000, 'member_ids必須是非空數組')), 400
    
    try:
        # 批量軟刪除
        updated_count = Member.query.filter(
            Member.mem_id.in_(member_ids),
            Member.enable == 1
        ).update(
            {'enable': 0},
            synchronize_session=False
        )
        
        if updated_count == 0:
            return jsonify(error_response(4000, '沒有找到可刪除的成員')), 404
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='DELETE',
            edit_module=2,  # 成員模組
        )
        record.set_content({
            'batch_operation': True,
            'deleted_member_ids': member_ids,
            'deleted_count': updated_count
        })
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response({
            'deleted_count': updated_count
        }, f'成功刪除 {updated_count} 個成員'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'批量刪除失敗: {str(e)}')), 500

@bp.route('/members/batch', methods=['PUT'])
@admin_required
def batch_update_members():
    """批量更新成員狀態"""
    data = request.get_json()
    
    if not data or 'member_ids' not in data:
        return jsonify(error_response(2000, '缺少member_ids參數')), 400
    
    member_ids = data.get('member_ids', [])
    updates = data.get('updates', {})
    
    if not isinstance(member_ids, list) or len(member_ids) == 0:
        return jsonify(error_response(2000, 'member_ids必須是非空數組')), 400
    
    # 只允許更新某些字段
    allowed_fields = {'enable', 'mem_type', 'research_group_id'}
    update_data = {}
    
    for field, value in updates.items():
        if field in allowed_fields:
            update_data[field] = value
    
    if not update_data:
        return jsonify(error_response(2000, '沒有可更新的字段')), 400
    
    try:
        # 批量更新
        updated_count = Member.query.filter(
            Member.mem_id.in_(member_ids)
        ).update(
            update_data,
            synchronize_session=False
        )
        
        if updated_count == 0:
            return jsonify(error_response(4000, '沒有找到可更新的成員')), 404
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='UPDATE',
            edit_module=2,  # 成員模組
        )
        record.set_content({
            'batch_operation': True,
            'updated_member_ids': member_ids,
            'updated_fields': update_data,
            'updated_count': updated_count
        })
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response({
            'updated_count': updated_count
        }, f'成功更新 {updated_count} 個成員'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'批量更新失敗: {str(e)}')), 500