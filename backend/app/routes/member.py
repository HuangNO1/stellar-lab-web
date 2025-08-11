from flask import Blueprint, request, jsonify
from app.services import MemberService
from app.services.base_service import ServiceException
from app.auth import admin_required
from app.utils.helpers import success_response, error_response

bp = Blueprint('member', __name__)

# 初始化服務
member_service = MemberService()

@bp.route('/members', methods=['GET'])
def get_members():
    """
    獲取成員列表
    
    支持的查詢參數：
    - q: 搜索關鍵字
    - type: 成員類型
    - research_group_id: 課題組ID
    - lab_id: 實驗室ID
    - show_all: 是否顯示已刪除
    - sort_by: 排序字段
    - order: 排序順序
    - page: 頁碼
    - per_page: 每頁數量
    - all: 是否獲取所有數據
    """
    try:
        filters = {
            'q': request.args.get('q'),
            'type': request.args.get('type', type=int),
            'research_group_id': request.args.get('research_group_id', type=int),
            'lab_id': request.args.get('lab_id', type=int),
            'show_all': request.args.get('show_all', 'false').lower() == 'true',
            'sort_by': request.args.get('sort_by', 'created_at'),
            'order': request.args.get('order', 'desc')
        }
        
        members_data = member_service.get_members_list(filters)
        return jsonify(success_response(members_data))
        
    except ServiceException as e:
        error_data = member_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '獲取成員列表失敗')), 500

@bp.route('/members/<int:mem_id>', methods=['GET'])
def get_member_detail(mem_id):
    """
    獲取成員詳情
    
    原始版本需要在路由中處理各種邏輯
    重構版本只需要調用服務層方法
    """
    try:
        member_data = member_service.get_member_detail(mem_id)
        return jsonify(success_response(member_data))
        
    except ServiceException as e:
        error_data = member_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '獲取成員詳情失敗')), 500

@bp.route('/members', methods=['POST'])
@admin_required
def create_member():
    """
    創建成員
    
    支持兩種請求格式：
    1. JSON格式（用於API調用）
    2. FormData格式（用於文件上傳）
    """
    try:
        # 根據Content-Type選擇數據源
        if request.is_json:
            form_data = request.get_json() or {}
            files_data = None
        else:
            form_data = dict(request.form)
            files_data = dict(request.files) if request.files else None
            
        member_data = member_service.create_member(
            form_data=form_data,
            files_data=files_data
        )
        return jsonify(success_response(member_data, '成員創建成功')), 201
        
    except ServiceException as e:
        error_data = member_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '創建成員失敗')), 500

@bp.route('/members/<int:mem_id>', methods=['PUT'])
@admin_required
def update_member(mem_id):
    """
    更新成員信息
    
    支持兩種請求格式：
    1. JSON格式（用於API調用）
    2. FormData格式（用於文件上傳）
    """
    try:
        # 根據Content-Type選擇數據源
        if request.is_json:
            form_data = request.get_json() or {}
            files_data = None
        else:
            form_data = dict(request.form)
            files_data = dict(request.files) if request.files else None
            
        member_data = member_service.update_member(
            mem_id=mem_id,
            form_data=form_data,
            files_data=files_data
        )
        return jsonify(success_response(member_data, '成員更新成功'))
        
    except ServiceException as e:
        error_data = member_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '更新成員失敗')), 500

@bp.route('/members/<int:mem_id>', methods=['DELETE'])
@admin_required
def delete_member(mem_id):
    """刪除成員"""
    try:
        member_service.delete_member(mem_id)
        return jsonify(success_response(message='成員刪除成功'))
        
    except ServiceException as e:
        error_data = member_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '刪除成員失敗')), 500

@bp.route('/members/batch', methods=['DELETE'])
@admin_required
def batch_delete_members():
    """
    批量刪除成員
    
    請求體：
    {
        "member_ids": [1, 2, 3]
    }
    """
    try:
        data = request.get_json()
        if not data or 'member_ids' not in data:
            return jsonify(error_response(2000, '請提供要刪除的成員ID列表')), 400
        
        result = member_service.batch_delete_members(data['member_ids'])
        return jsonify(success_response(result, '批量刪除操作完成'))
        
    except ServiceException as e:
        error_data = member_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '批量刪除失敗')), 500

@bp.route('/members/batch', methods=['PUT'])
@admin_required
def batch_update_members():
    """
    批量更新成員
    
    請求體：
    {
        "member_ids": [1, 2, 3],
        "updates": {
            "enable": 1,
            "mem_type": 0
        }
    }
    """
    try:
        data = request.get_json()
        if not data or 'member_ids' not in data or 'updates' not in data:
            return jsonify(error_response(2000, '請提供成員ID列表和更新字段')), 400
        
        result = member_service.batch_update_members(
            member_ids=data['member_ids'],
            update_fields=data['updates']
        )
        return jsonify(success_response(result, '批量更新操作完成'))
        
    except ServiceException as e:
        error_data = member_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
        
    except Exception as e:
        return jsonify(error_response(5000, '批量更新失敗')), 500