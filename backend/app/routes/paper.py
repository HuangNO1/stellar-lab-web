from flask import Blueprint, request, jsonify, g
from app import db
from app.models import Paper, PaperAuthor, Member, ResearchGroup, Lab, EditRecord
from app.auth import admin_required
from app.utils.validators import validate_date, validate_string_length, validate_enum
from app.utils.helpers import get_pagination_params, paginate_query, success_response, error_response
from app.utils.file_handler import save_file, delete_file
import json

bp = Blueprint('paper', __name__)

@bp.route('/papers', methods=['GET'])
def get_papers():
    page, per_page = get_pagination_params()
    
    query = Paper.query
    
    # 搜索
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(
            db.or_(
                Paper.paper_title_zh.contains(q),
                Paper.paper_title_en.contains(q),
                Paper.paper_venue.contains(q)
            )
        )
    
    # 按類型篩選
    paper_type = request.args.get('paper_type', type=int)
    if paper_type is not None:
        query = query.filter(Paper.paper_type == paper_type)
    
    # 按接收狀態篩選
    paper_accept = request.args.get('paper_accept', type=int)
    if paper_accept is not None:
        query = query.filter(Paper.paper_accept == paper_accept)
    
    # 按日期範圍篩選
    start_date = request.args.get('start_date')
    if start_date:
        valid, date_obj = validate_date(start_date)
        if valid and date_obj:
            query = query.filter(Paper.paper_date >= date_obj)
    
    end_date = request.args.get('end_date')
    if end_date:
        valid, date_obj = validate_date(end_date)
        if valid and date_obj:
            query = query.filter(Paper.paper_date <= date_obj)
    
    # 是否顯示已刪除
    show_all = request.args.get('show_all', 'false').lower() == 'true'
    if not show_all:
        query = query.filter(Paper.enable == 1)
    
    # 排序
    sort_by = request.args.get('sort_by', 'paper_date')
    order = request.args.get('order', 'desc')
    
    if sort_by == 'title':
        sort_field = Paper.paper_title_zh
    elif sort_by == 'venue':
        sort_field = Paper.paper_venue
    elif sort_by == 'type':
        sort_field = Paper.paper_type
    else:
        sort_field = Paper.paper_date
    
    if order.lower() == 'asc':
        query = query.order_by(sort_field.asc())
    else:
        query = query.order_by(sort_field.desc())
    
    result = paginate_query(query, page, per_page)
    return jsonify(success_response(result))

@bp.route('/papers/<int:paper_id>', methods=['GET'])
def get_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    return jsonify(success_response(paper.to_dict()))

@bp.route('/papers', methods=['POST'])
@admin_required
def create_paper():
    try:
        # 處理文件上傳
        file_path = None
        if 'paper_file' in request.files:
            file = request.files['paper_file']
            if file and file.filename:
                file_path = save_file(file, 'paper', max_size=50*1024*1024)
        
        # 獲取表單數據
        paper_date_str = request.form.get('paper_date')
        valid, paper_date = validate_date(paper_date_str)
        if not valid:
            return jsonify(error_response(2000, '日期格式不正確')), 400
        
        data = {
            'paper_date': paper_date,
            'paper_title_zh': request.form.get('paper_title_zh', '').strip(),
            'paper_title_en': request.form.get('paper_title_en', '').strip(),
            'paper_desc_zh': request.form.get('paper_desc_zh', '').strip(),
            'paper_desc_en': request.form.get('paper_desc_en', '').strip(),
            'paper_type': int(request.form.get('paper_type', 0)),
            'paper_venue': request.form.get('paper_venue', '').strip(),
            'paper_accept': int(request.form.get('paper_accept', 0)),
            'paper_url': request.form.get('paper_url', '').strip(),
        }
        
        # 作者信息
        authors_str = request.form.get('authors', '[]')
        try:
            authors = json.loads(authors_str)
        except json.JSONDecodeError:
            return jsonify(error_response(2000, '作者信息格式錯誤')), 400
        
        # 參數校驗
        if not data['paper_title_zh'] and not data['paper_title_en']:
            return jsonify(error_response(2000, '論文標題不能為空')), 400
        
        if not validate_enum(data['paper_type'], [0, 1, 2, 3, 4]):
            return jsonify(error_response(2000, '論文類型錯誤')), 400
        
        if not validate_enum(data['paper_accept'], [0, 1]):
            return jsonify(error_response(2000, '接收狀態錯誤')), 400
        
        # 字符串長度校驗
        string_fields = {
            'paper_title_zh': 500, 'paper_title_en': 500,
            'paper_desc_zh': 1000, 'paper_desc_en': 1000,
            'paper_venue': 500, 'paper_url': 1000
        }
        
        for field, max_len in string_fields.items():
            if not validate_string_length(data[field], max_len):
                return jsonify(error_response(2000, f'{field} 長度超過限制')), 400
        
        # 獲取默認實驗室和課題組
        lab = Lab.query.filter_by(enable=1).first()
        if not lab:
            return jsonify(error_response(3000, '請先設置實驗室信息')), 404
        
        research_group = ResearchGroup.query.filter_by(enable=1).first()
        
        # 創建論文
        paper = Paper(
            research_group_id=research_group.research_group_id if research_group else None,
            lab_id=lab.lab_id,
            paper_date=data['paper_date'],
            paper_title_zh=data['paper_title_zh'],
            paper_title_en=data['paper_title_en'],
            paper_desc_zh=data['paper_desc_zh'],
            paper_desc_en=data['paper_desc_en'],
            paper_type=data['paper_type'],
            paper_venue=data['paper_venue'],
            paper_accept=data['paper_accept'],
            paper_file_path=file_path,
            paper_url=data['paper_url'],
            enable=1
        )
        
        db.session.add(paper)
        db.session.flush()
        
        # 創建作者關聯
        for author_data in authors:
            mem_id = author_data.get('mem_id')
            author_order = author_data.get('author_order', 1)
            is_corresponding = author_data.get('is_corresponding', 0)
            
            # 檢查成員是否存在
            member = Member.query.filter_by(mem_id=mem_id, enable=1).first()
            if not member:
                continue
            
            paper_author = PaperAuthor(
                paper_id=paper.paper_id,
                mem_id=mem_id,
                author_order=author_order,
                is_corresponding=is_corresponding
            )
            db.session.add(paper_author)
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='CREATE',
            edit_module=4,  # 論文模組
        )
        record.set_content({**data, 'authors': authors})
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(paper.to_dict(), '論文創建成功')), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'創建失敗: {str(e)}')), 500

@bp.route('/papers/<int:paper_id>', methods=['PUT'])
@admin_required
def update_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    data = request.get_json()
    
    try:
        # 更新論文信息
        if 'paper_title_zh' in data:
            paper.paper_title_zh = data['paper_title_zh'].strip()
        
        if 'paper_title_en' in data:
            paper.paper_title_en = data['paper_title_en'].strip()
        
        if 'paper_desc_zh' in data:
            paper.paper_desc_zh = data['paper_desc_zh'].strip() if data['paper_desc_zh'] else None
        
        if 'paper_desc_en' in data:
            paper.paper_desc_en = data['paper_desc_en'].strip() if data['paper_desc_en'] else None
            
        if 'paper_venue' in data:
            paper.paper_venue = data['paper_venue'].strip() if data['paper_venue'] else None
            
        if 'paper_type' in data:
            paper_type = int(data['paper_type'])
            if paper_type in [0, 1, 2, 3, 4]:
                paper.paper_type = paper_type
                
        if 'paper_accept' in data:
            paper_accept = int(data['paper_accept'])
            if paper_accept in [0, 1]:
                paper.paper_accept = paper_accept
                
        if 'paper_date' in data:
            paper_date = data['paper_date'].strip()
            if paper_date:
                valid, date_obj = validate_date(paper_date)
                if valid and date_obj:
                    paper.paper_date = date_obj
                    
        if 'paper_url' in data:
            paper.paper_url = data['paper_url'].strip() if data['paper_url'] else None
            
        if 'research_group_id' in data:
            research_group_id = int(data['research_group_id'])
            if ResearchGroup.query.get(research_group_id):
                paper.research_group_id = research_group_id
                
        # 更新作者
        if 'authors' in data and isinstance(data['authors'], list):
            # 刪除舊的作者關係
            PaperAuthor.query.filter_by(paper_id=paper_id).delete()
            
            # 添加新的作者關係
            for i, author_data in enumerate(data['authors']):
                if isinstance(author_data, dict) and 'mem_id' in author_data:
                    mem_id = int(author_data['mem_id'])
                    is_corresponding = int(author_data.get('is_corresponding', 0))
                    
                    if Member.query.get(mem_id):
                        author = PaperAuthor(
                            paper_id=paper_id,
                            mem_id=mem_id,
                            author_order=i + 1,
                            is_corresponding=is_corresponding
                        )
                        db.session.add(author)
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='UPDATE',
            edit_module=4,  # 論文模組
        )
        record.set_content(data)
        db.session.add(record)
        
        db.session.commit()
        
        # 重新加載論文信息以獲取更新後的作者
        updated_paper = Paper.query.get(paper_id)
        return jsonify(success_response(updated_paper.to_dict(), '論文更新成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'更新失敗: {str(e)}')), 500

@bp.route('/papers/<int:paper_id>', methods=['DELETE'])
@admin_required
def delete_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    
    try:
        # 軟刪除
        paper.enable = 0
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='DELETE',
            edit_module=4,
        )
        record.set_content({'deleted_paper_id': paper_id})
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(message='論文刪除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'刪除失敗: {str(e)}')), 500