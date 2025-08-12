from flask import Blueprint, request, jsonify, g
from app import limiter
from app.services import AuthService
from app.services.base_service import ServiceException
from app.auth import admin_required
from app.utils.helpers import success_response, error_response
from app.utils.messages import msg

bp = Blueprint('auth', __name__)

# 初始化服務
auth_service = AuthService()

@bp.route('/admin/login', methods=['POST'])
@limiter.limit("5 per minute")  # 登錄頻率限制
def admin_login():
    """
    管理員登錄
    
    重構後的登錄邏輯：
    - 所有業務邏輯在服務層
    - 統一的錯誤處理
    - 自動審計記錄
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify(error_response(2000, '請提供登錄數據')), 400
        
        admin_name = data.get('admin_name', '').strip()
        admin_pass = data.get('admin_pass', '')
        
        # 收集登錄信息
        login_info = {
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', ''),
            'timestamp': request.timestamp if hasattr(request, 'timestamp') else None
        }
        
        result = auth_service.login(admin_name, admin_pass, login_info)
        return jsonify(success_response(result, msg.get_success_message('LOGIN_SUCCESS')))
        
    except ServiceException as e:
        error_data = auth_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '登錄失敗')), 500

@bp.route('/admin/logout', methods=['POST'])
@admin_required
def admin_logout():
    """管理員登出"""
    try:
        logout_info = {
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')
        }
        
        auth_service.logout(g.current_admin.admin_id, logout_info)
        return jsonify(success_response(message=msg.get_success_message('LOGOUT_SUCCESS')))
        
    except ServiceException as e:
        error_data = auth_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '登出失敗')), 500

@bp.route('/admin/change-password', methods=['POST'])
@admin_required
def change_password():
    """修改密碼"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(error_response(2000, '請提供密碼數據')), 400
        
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        
        auth_service.change_password(
            admin_id=g.current_admin.admin_id,
            old_password=old_password,
            new_password=new_password
        )
        return jsonify(success_response(message=msg.get_success_message('PASSWORD_CHANGE_SUCCESS')))
        
    except ServiceException as e:
        error_data = auth_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '修改密碼失敗')), 500

@bp.route('/admin/profile', methods=['GET'])
@admin_required
def get_profile():
    """獲取個人資料"""
    try:
        profile = auth_service.get_profile(g.current_admin.admin_id)
        return jsonify(success_response(profile))
        
    except ServiceException as e:
        error_data = auth_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '獲取個人資料失敗')), 500

@bp.route('/admin/profile', methods=['PUT'])
@admin_required
def update_profile():
    """更新個人資料"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(error_response(2000, '請提供要更新的資料')), 400
        
        profile = auth_service.update_profile(
            admin_id=g.current_admin.admin_id,
            profile_data=data
        )
        return jsonify(success_response(profile, msg.get_success_message('PROFILE_UPDATE_SUCCESS')))
        
    except ServiceException as e:
        error_data = auth_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '更新個人資料失敗')), 500