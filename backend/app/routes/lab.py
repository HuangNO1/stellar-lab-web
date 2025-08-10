from flask import Blueprint, request, jsonify
from app.services import LabService
from app.services.base_service import ServiceException
from app.auth import admin_required
from app.utils.helpers import success_response, error_response

bp = Blueprint('lab', __name__)

# 初始化服務
lab_service = LabService()

@bp.route('/lab', methods=['GET'])
def get_lab():
    """
    獲取實驗室信息
    
    重構後的路由：
    - 只負責HTTP請求/響應處理
    - 業務邏輯完全在服務層
    - 統一的錯誤處理
    """
    try:
        lab_info = lab_service.get_lab_info()
        return jsonify(success_response(lab_info))
        
    except ServiceException as e:
        error_data = lab_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '獲取實驗室信息失敗')), 500

@bp.route('/lab', methods=['PUT', 'POST'])
@admin_required
def update_lab():
    """
    更新實驗室信息
    
    優勢對比：
    原始版本: 191行，包含大量業務邏輯
    重構版本: ~20行，純HTTP處理
    """
    try:
        lab_info = lab_service.update_lab_info(
            form_data=dict(request.form),
            files_data=dict(request.files)
        )
        return jsonify(success_response(lab_info, '實驗室信息更新成功'))
        
    except ServiceException as e:
        error_data = lab_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '更新實驗室信息失敗')), 500

@bp.route('/lab', methods=['DELETE'])
@admin_required
def delete_lab():
    """
    刪除實驗室
    """
    try:
        lab_service.delete_lab()
        return jsonify(success_response(message='實驗室刪除成功'))
        
    except ServiceException as e:
        error_data = lab_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '刪除實驗室失敗')), 500