from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
from app.models import Admin
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