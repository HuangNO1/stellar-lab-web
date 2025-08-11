from functools import wraps
from flask import request, jsonify, current_app, g
from app.models import Admin

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 獲取Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'code': 1000,
                'message': '未認證或 token 無效'
            }), 401
        
        token = auth_header[7:]  # 移除 "Bearer " 前綴
        
        # 使用AuthService驗證token
        from app.services.auth_service import AuthService
        token_data = AuthService.verify_token(token)
        
        if not token_data:
            return jsonify({
                'code': 1000,
                'message': '未認證或 token 無效'
            }), 401
        
        # 獲取admin_id並查詢管理員
        admin_id = token_data.get('sub')  # Flask-JWT-Extended 將 identity 存儲在 sub 中
        if not admin_id:
            return jsonify({
                'code': 1000,
                'message': '未認證或 token 無效'
            }), 401
        
        try:
            admin_id = int(admin_id)  # 轉換為整數
        except (ValueError, TypeError):
            return jsonify({
                'code': 1000,
                'message': '未認證或 token 無效'
            }), 401
            
        admin = Admin.query.filter_by(admin_id=admin_id, enable=1).first()
        if not admin:
            return jsonify({
                'code': 1000,
                'message': '未認證或 token 無效'
            }), 401
            
        g.current_admin = admin
        return func(*args, **kwargs)
    
    return wrapper

def super_admin_required(func):
    @wraps(func)
    @admin_required
    def wrapper(*args, **kwargs):
        if not g.current_admin.is_super:
            return jsonify({
                'code': 1001,
                'message': '權限不足'
            }), 403
            
        return func(*args, **kwargs)
    
    return wrapper