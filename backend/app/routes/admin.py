from flask import Blueprint, request, jsonify, g
from app import db
from app.models import Admin, EditRecord
from app.auth import admin_required, super_admin_required
from app.utils.validators import validate_admin_name
from app.utils.helpers import get_pagination_params, paginate_query, success_response, error_response

bp = Blueprint('admin', __name__)

@bp.route('/admins', methods=['GET'])
@super_admin_required
def get_admins():
    page, per_page = get_pagination_params()
    
    query = Admin.query
    
    # 搜索
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(Admin.admin_name.contains(q))
    
    # 是否顯示已刪除
    show_all = request.args.get('show_all', 'false').lower() == 'true'
    if not show_all:
        query = query.filter(Admin.enable == 1)
    
    query = query.order_by(Admin.created_at.desc())
    result = paginate_query(query, page, per_page)
    
    return jsonify(success_response(result))

@bp.route('/admins', methods=['POST'])
@super_admin_required
def create_admin():
    data = request.get_json()
    
    # 參數校驗
    admin_name = data.get('admin_name', '').strip()
    admin_pass = data.get('admin_pass', '').strip()
    is_super = int(data.get('is_super', 0))
    
    if not admin_name or not admin_pass:
        return jsonify(error_response(2000, '用戶名和密碼不能為空')), 400
    
    if not validate_admin_name(admin_name):
        return jsonify(error_response(2000, '用戶名格式不正確，只能包含字母、數字、下劃線和連字符，長度3-50位')), 400
    
    if len(admin_pass) < 8:
        return jsonify(error_response(2000, '密碼長度至少8位')), 400
    
    if is_super not in [0, 1]:
        return jsonify(error_response(2000, 'is_super參數錯誤')), 400
    
    # 檢查用戶名是否已存在
    if Admin.query.filter_by(admin_name=admin_name).first():
        return jsonify(error_response(4000, '用戶名已存在')), 409
    
    try:
        # 創建管理員
        admin = Admin(
            admin_name=admin_name,
            is_super=is_super,
            enable=1
        )
        admin.set_password(admin_pass)
        
        db.session.add(admin)
        db.session.flush()  # 獲取admin_id
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='CREATE',
            edit_module=0,  # 管理員模組
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(admin.to_dict(), '管理員創建成功')), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'創建失敗: {str(e)}')), 500

@bp.route('/admins/<int:admin_id>', methods=['PUT'])
@super_admin_required
def update_admin(admin_id):
    admin = Admin.query.get_or_404(admin_id)
    data = request.get_json()
    
    # 不能修改自己
    if admin_id == g.current_admin.admin_id:
        return jsonify(error_response(4000, '不能修改自己的賬戶')), 409
    
    try:
        # 更新字段
        if 'admin_name' in data:
            new_name = data['admin_name'].strip()
            if not validate_admin_name(new_name):
                return jsonify(error_response(2000, '用戶名格式不正確')), 400
            
            # 檢查用戶名是否已被其他用戶使用
            existing = Admin.query.filter(
                Admin.admin_name == new_name,
                Admin.admin_id != admin_id
            ).first()
            if existing:
                return jsonify(error_response(4000, '用戶名已存在')), 409
            
            admin.admin_name = new_name
        
        if 'is_super' in data:
            admin.is_super = int(data['is_super'])
        
        if 'enable' in data:
            admin.enable = int(data['enable'])
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='UPDATE',
            edit_module=0,
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(admin.to_dict(), '管理員更新成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'更新失敗: {str(e)}')), 500

@bp.route('/admins/<int:admin_id>', methods=['DELETE'])
@super_admin_required
def delete_admin(admin_id):
    admin = Admin.query.get_or_404(admin_id)
    
    # 不能刪除自己
    if admin_id == g.current_admin.admin_id:
        return jsonify(error_response(4000, '不能刪除自己的賬戶')), 409
    
    try:
        # 軟刪除
        admin.enable = 0
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='DELETE',
            edit_module=0,
        )
        record.set_content({'deleted_admin_id': admin_id})
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(message='管理員刪除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'刪除失敗: {str(e)}')), 500