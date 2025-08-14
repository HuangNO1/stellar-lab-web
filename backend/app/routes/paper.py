from flask import Blueprint, request, jsonify, current_app
from app.auth import admin_required
from app.utils.helpers import success_response, error_response
from app.services import PaperService
from app.services.base_service import ServiceException
from app.utils.messages import msg
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
        # 記錄上傳開始時間
        import time
        start_time = time.time()
        current_app.logger.info(f"論文創建開始，Content-Length: {request.headers.get('Content-Length', 'Unknown')}")
        
        # 根據Content-Type選擇數據源
        if request.is_json:
            form_data = request.get_json() or {}
            files_data = None
            # 處理作者信息（JSON格式直接包含在數據中）
            authors_data = form_data.pop('authors', [])
        else:
            # 獲取表單數據
            form_data = dict(request.form)
            
            # 處理文件數據
            files_data = dict(request.files) if request.files else {}
            if files_data and 'paper_file' in files_data:
                file = files_data['paper_file']
                current_app.logger.info(f"上傳文件: {file.filename}, 大小: {getattr(file, 'content_length', 'Unknown')}")
            
            # 處理作者信息
            authors_data = []
            authors_str = request.form.get('authors', '[]')
            if authors_str:
                try:
                    authors_data = json.loads(authors_str)
                except json.JSONDecodeError:
                    return jsonify(error_response(2000, msg.get_error_message('INVALID_INPUT'))), 400
        
        paper = paper_service.create_paper(form_data, files_data, authors_data)
        
        # 記錄處理時間
        end_time = time.time()
        current_app.logger.info(f"論文創建完成，處理時間: {end_time - start_time:.2f}秒")
        
        return jsonify(success_response(paper, msg.get_success_message('PAPER_CREATE_SUCCESS'))), 201
    except ServiceException as e:
        current_app.logger.error(f"論文創建失敗: {str(e)}")
        error_data = paper_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400
    except Exception as e:
        current_app.logger.error(f"論文創建發生未知錯誤: {str(e)}")
        return jsonify(error_response(5000, msg.get_error_message('OPERATION_FAILED'))), 500

@bp.route('/papers/<int:paper_id>', methods=['PUT'])
@admin_required
def update_paper(paper_id):
    """更新論文"""
    try:
        # 記錄上傳開始時間
        import time
        start_time = time.time()
        current_app.logger.info(f"論文更新開始 (ID: {paper_id})，Content-Length: {request.headers.get('Content-Length', 'Unknown')}")
        
        # 根據Content-Type選擇數據源
        if request.is_json:
            form_data = request.get_json() or {}
            files_data = None
        else:
            form_data = dict(request.form)
            files_data = dict(request.files) if request.files else None
            if files_data and 'paper_file' in files_data:
                file = files_data['paper_file']
                current_app.logger.info(f"更新文件: {file.filename}, 大小: {getattr(file, 'content_length', 'Unknown')}")
            
        paper = paper_service.update_paper(paper_id, form_data, files_data)
        
        # 記錄處理時間
        end_time = time.time()
        current_app.logger.info(f"論文更新完成 (ID: {paper_id})，處理時間: {end_time - start_time:.2f}秒")
        
        return jsonify(success_response(paper, msg.get_success_message('PAPER_UPDATE_SUCCESS')))
    except ServiceException as e:
        current_app.logger.error(f"論文更新失敗 (ID: {paper_id}): {str(e)}")
        error_data = paper_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code
    except Exception as e:
        current_app.logger.error(f"論文更新發生未知錯誤 (ID: {paper_id}): {str(e)}")
        return jsonify(error_response(5000, msg.get_error_message('OPERATION_FAILED'))), 500

@bp.route('/papers/<int:paper_id>', methods=['DELETE'])
@admin_required
def delete_paper(paper_id):
    """刪除論文"""
    try:
        paper_service.delete_paper(paper_id)
        return jsonify(success_response(message=msg.get_success_message('PAPER_DELETE_SUCCESS')))
    except ServiceException as e:
        error_data = paper_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code