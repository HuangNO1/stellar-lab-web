from flask import Blueprint, request, jsonify
from app.auth import admin_required
from app.utils.helpers import success_response, error_response
from app.utils.messages import msg
from app.services import NewsService
from app.services.base_service import ServiceException

bp = Blueprint('news', __name__)
news_service = NewsService()

@bp.route('/news', methods=['GET'])
def get_news():
    """獲取新聞列表"""
    try:
        filters = {
            'q': request.args.get('q', '').strip(),
            'news_type': request.args.get('news_type', type=int),
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'show_all': request.args.get('show_all', 'false').lower() == 'true',
            'sort_by': request.args.get('sort_by', 'news_date'),
            'order': request.args.get('order', 'desc')
        }
        # 移除空值，但保留 sort_by 和 order
        filters = {k: v for k, v in filters.items() if (k in ['sort_by', 'order']) or (v is not None and v != '')}
        
        result = news_service.get_news_list(filters)
        return jsonify(success_response(result))
    except ServiceException as e:
        error_data = news_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/news/<int:news_id>', methods=['GET'])
def get_news_item(news_id):
    """獲取新聞詳情"""
    try:
        news = news_service.get_news_detail(news_id)
        return jsonify(success_response(news))
    except ServiceException as e:
        error_data = news_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/news', methods=['POST'])
@admin_required
def create_news():
    """創建新聞"""
    try:
        data = request.get_json()
        news = news_service.create_news(data)
        return jsonify(success_response(news, msg.get_success_message('NEWS_CREATE_SUCCESS'))), 201
    except ServiceException as e:
        error_data = news_service.format_error_response(e)
        return jsonify(error_response(error_data['code'], error_data['message'])), 400

@bp.route('/news/<int:news_id>', methods=['PUT'])
@admin_required
def update_news(news_id):
    """更新新聞"""
    try:
        data = request.get_json()
        news = news_service.update_news(news_id, data)
        return jsonify(success_response(news, msg.get_success_message('NEWS_UPDATE_SUCCESS')))
    except ServiceException as e:
        error_data = news_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code

@bp.route('/news/<int:news_id>', methods=['DELETE'])
@admin_required
def delete_news(news_id):
    """刪除新聞"""
    try:
        news_service.delete_news(news_id)
        return jsonify(success_response(message=msg.get_success_message('NEWS_DELETE_SUCCESS')))
    except ServiceException as e:
        error_data = news_service.format_error_response(e)
        status_code = 404 if 'NotFoundError' in str(type(e)) else 400
        return jsonify(error_response(error_data['code'], error_data['message'])), status_code