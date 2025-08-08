from flask import Blueprint, request, jsonify, g
from app import db
from app.models import News, EditRecord
from app.auth import admin_required
from app.utils.validators import validate_date, validate_string_length, validate_enum
from app.utils.helpers import get_pagination_params, paginate_query, success_response, error_response

bp = Blueprint('news', __name__)

@bp.route('/news', methods=['GET'])
def get_news():
    page, per_page = get_pagination_params()
    
    query = News.query
    
    # 搜索
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(
            db.or_(
                News.news_content_zh.contains(q),
                News.news_content_en.contains(q)
            )
        )
    
    # 按類型篩選
    news_type = request.args.get('news_type', type=int)
    if news_type is not None:
        query = query.filter(News.news_type == news_type)
    
    # 按日期範圍篩選
    start_date = request.args.get('start_date')
    if start_date:
        valid, date_obj = validate_date(start_date)
        if valid and date_obj:
            query = query.filter(News.news_date >= date_obj)
    
    end_date = request.args.get('end_date')
    if end_date:
        valid, date_obj = validate_date(end_date)
        if valid and date_obj:
            query = query.filter(News.news_date <= date_obj)
    
    # 是否顯示已刪除
    show_all = request.args.get('show_all', 'false').lower() == 'true'
    if not show_all:
        query = query.filter(News.enable == 1)
    
    # 排序
    query = query.order_by(News.news_date.desc(), News.created_at.desc())
    
    result = paginate_query(query, page, per_page)
    return jsonify(success_response(result))

@bp.route('/news/<int:news_id>', methods=['GET'])
def get_news_item(news_id):
    news = News.query.get_or_404(news_id)
    return jsonify(success_response(news.to_dict()))

@bp.route('/news', methods=['POST'])
@admin_required
def create_news():
    data = request.get_json()
    
    # 參數校驗
    news_type = data.get('news_type')
    news_content_zh = data.get('news_content_zh', '').strip()
    news_content_en = data.get('news_content_en', '').strip()
    news_date_str = data.get('news_date')
    
    if not news_content_zh and not news_content_en:
        return jsonify(error_response(2000, '新聞內容不能為空')), 400
    
    if not validate_enum(news_type, [0, 1, 2, 3]):
        return jsonify(error_response(2000, '新聞類型錯誤')), 400
    
    # 日期校驗
    valid, news_date = validate_date(news_date_str)
    if news_date_str and not valid:
        return jsonify(error_response(2000, '日期格式不正確')), 400
    
    # 字符串長度校驗
    if not validate_string_length(news_content_zh, 1000):
        return jsonify(error_response(2000, '中文內容長度不能超過1000字符')), 400
    
    if not validate_string_length(news_content_en, 1000):
        return jsonify(error_response(2000, '英文內容長度不能超過1000字符')), 400
    
    try:
        # 創建新聞
        news = News(
            news_type=news_type,
            news_content_zh=news_content_zh,
            news_content_en=news_content_en,
            news_date=news_date,
            enable=1
        )
        
        db.session.add(news)
        db.session.flush()
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='CREATE',
            edit_module=5,  # 新聞模組
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(news.to_dict(), '新聞創建成功')), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'創建失敗: {str(e)}')), 500

@bp.route('/news/<int:news_id>', methods=['PUT'])
@admin_required
def update_news(news_id):
    news = News.query.get_or_404(news_id)
    data = request.get_json()
    
    try:
        # 更新字段
        if 'news_type' in data:
            if not validate_enum(data['news_type'], [0, 1, 2, 3]):
                return jsonify(error_response(2000, '新聞類型錯誤')), 400
            news.news_type = data['news_type']
        
        if 'news_content_zh' in data:
            value = data['news_content_zh'].strip()
            if not validate_string_length(value, 1000):
                return jsonify(error_response(2000, '中文內容長度不能超過1000字符')), 400
            news.news_content_zh = value
        
        if 'news_content_en' in data:
            value = data['news_content_en'].strip()
            if not validate_string_length(value, 1000):
                return jsonify(error_response(2000, '英文內容長度不能超過1000字符')), 400
            news.news_content_en = value
        
        if 'news_date' in data:
            valid, date_obj = validate_date(data['news_date'])
            if data['news_date'] and not valid:
                return jsonify(error_response(2000, '日期格式不正確')), 400
            news.news_date = date_obj
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='UPDATE',
            edit_module=5,
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(news.to_dict(), '新聞更新成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'更新失敗: {str(e)}')), 500

@bp.route('/news/<int:news_id>', methods=['DELETE'])
@admin_required
def delete_news(news_id):
    news = News.query.get_or_404(news_id)
    
    try:
        # 軟刪除
        news.enable = 0
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='DELETE',
            edit_module=5,
        )
        record.set_content({'deleted_news_id': news_id})
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(message='新聞刪除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'刪除失敗: {str(e)}')), 500