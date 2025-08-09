from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from app import db
from app.models import Admin, EditRecord
from app.auth import admin_required
from flask import g

bp = Blueprint('auth', __name__)

@bp.route('/admin/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('admin_name') or not data.get('admin_pass'):
        return jsonify({
            'code': 2000,
            'message': '用戶名和密碼不能為空'
        }), 400
    
    admin = Admin.query.filter_by(
        admin_name=data['admin_name'], 
        enable=1
    ).first()
    
    if not admin or not admin.check_password(data['admin_pass']):
        return jsonify({
            'code': 1000,
            'message': '用戶名或密碼錯誤'
        }), 401
    
    access_token = create_access_token(identity=admin.admin_id)
    
    return jsonify({
        'code': 0,
        'message': 'OK',
        'data': {
            'access_token': f'Bearer {access_token}',
            'expires_in': 86400,  # 24小時
            'admin': admin.to_dict()
        }
    })

@bp.route('/admin/change-password', methods=['POST'])
@admin_required
def change_password():
    data = request.get_json()
    
    if not data or not data.get('old_password') or not data.get('new_password'):
        return jsonify({
            'code': 2000,
            'message': '舊密碼和新密碼不能為空'
        }), 400
    
    admin = g.current_admin
    
    if not admin.check_password(data['old_password']):
        return jsonify({
            'code': 1000,
            'message': '原密碼錯誤'
        }), 400
    
    if len(data['new_password']) < 8:
        return jsonify({
            'code': 2000,
            'message': '新密碼長度至少8位'
        }), 400
    
    admin.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '密碼修改成功'
    })

@bp.route('/admin/logout', methods=['POST'])
@admin_required
def logout():
    """管理員登出
    
    雖然JWT是無狀態的，但我們記錄登出操作以便審計
    前端應該在收到成功響應後主動刪除本地存儲的token
    """
    try:
        # 記錄登出操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='LOGOUT',
            edit_module=0,  # 管理員模組
        )
        record.set_content({
            'admin_name': g.current_admin.admin_name,
            'logout_time': record.edit_date.isoformat()
        })
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'message': '登出成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 5000,
            'message': f'登出失敗: {str(e)}'
        }), 500

@bp.route('/admin/profile', methods=['GET'])
@admin_required 
def get_profile():
    """獲取當前登錄管理員信息"""
    return jsonify({
        'code': 0,
        'message': 'OK',
        'data': g.current_admin.to_dict()
    })

@bp.route('/admin/profile', methods=['PUT'])
@admin_required
def update_profile():
    """更新當前管理員個人信息"""
    data = request.get_json()
    admin = g.current_admin
    
    try:
        # 只允許更新某些字段
        updated_fields = {}
        
        # 這裡可以根據需要添加其他可更新的個人信息字段
        # 比如：姓名、郵箱等（需要先在Admin模型中添加這些字段）
        
        # 記錄操作
        record = EditRecord(
            admin_id=admin.admin_id,
            edit_type='UPDATE',
            edit_module=0,
        )
        record.set_content({
            'updated_fields': updated_fields,
            'admin_name': admin.admin_name
        })
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'message': '個人信息更新成功',
            'data': admin.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 5000,
            'message': f'更新失敗: {str(e)}'
        }), 500