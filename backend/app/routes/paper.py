from flask import Blueprint, request, jsonify
from app.auth import admin_required
from app.utils.helpers import success_response, error_response
from app.services import PaperService
from app.services.base_service import ServiceException
import json

bp = Blueprint('paper', __name__)
paper_service = PaperService()

@bp.route('/papers', methods=['GET'])
def get_papers():
    """獲取論文列表"""
    try:
        filters = {
            'q': request.args.get('q', '').strip(),
            'paper_type': request.args.get('paper_type', type=int),
            'paper_accept': request.args.get('paper_accept', type=int),
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'show_all': request.args.get('show_all', 'false').lower() == 'true',
            'sort_by': request.args.get('sort_by', 'paper_date'),
            'order': request.args.get('order', 'desc')
        }
        # 移除空值
        filters = {k: v for k, v in filters.items() if v is not None and v != ''}
        
        result = paper_service.get_papers_list(filters)
        return jsonify(success_response(result))
    except ServiceException as e:
        error_data = paper_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/papers/<int:paper_id>', methods=['GET'])
def get_paper(paper_id):
    """獲取論文詳情"""
    try:
        paper = paper_service.get_paper_detail(paper_id)
        return jsonify(success_response(paper))
    except ServiceException as e:
        error_data = paper_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/papers', methods=['POST'])
@admin_required
def create_paper():
    """創建論文"""
    try:
        # 獲取表單數據
        form_data = dict(request.form)
        
        # 處理文件數據
        files_data = dict(request.files) if request.files else {}
        
        # 處理作者信息
        authors_data = []
        authors_str = request.form.get('authors', '[]')
        if authors_str:
            try:
                authors_data = json.loads(authors_str)
            except json.JSONDecodeError:
                return jsonify(error_response(2000, '作者信息格式錯誤')), 400
        
        paper = paper_service.create_paper(form_data, files_data, authors_data)
        return jsonify(success_response(paper, '論文創建成功')), 201
    except ServiceException as e:
        error_data = paper_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/papers/<int:paper_id>', methods=['PUT'])
@admin_required
def update_paper(paper_id):
    """更新論文"""
    try:
        # 根據Content-Type選擇數據源
        if request.is_json:
            form_data = request.get_json() or {}
            files_data = None
        else:
            form_data = dict(request.form)
            files_data = dict(request.files) if request.files else None
            
        paper = paper_service.update_paper(paper_id, form_data, files_data)
        return jsonify(success_response(paper, '論文更新成功'))
    except ServiceException as e:
        error_data = paper_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/papers/<int:paper_id>', methods=['DELETE'])
@admin_required
def delete_paper(paper_id):
    """刪除論文"""
    try:
        paper_service.delete_paper(paper_id)
        return jsonify(success_response(message='論文刪除成功'))
    except ServiceException as e:
        error_data = paper_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code