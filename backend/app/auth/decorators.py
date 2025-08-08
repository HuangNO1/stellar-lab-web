from functools import wraps
from flask import request, jsonify, current_app, g
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Admin

def admin_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        admin_id = get_jwt_identity()
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