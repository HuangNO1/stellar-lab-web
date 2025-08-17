from typing import Optional, Dict, Any, List
from datetime import datetime
from flask import request
from app.models import Paper, PaperAuthor, Member, ResearchGroup, Lab
from app.utils.validators import validate_string_length, validate_date
from app.utils.helpers import get_pagination_params, paginate_query
from app.utils.file_handler import save_file, delete_file
from app.utils.messages import msg
from .base_service import BaseService, ValidationError, NotFoundError
from .image_upload_service import ImageUploadService
import json


class PaperService(BaseService):
    """
    論文管理服務層
    """
    
    def get_module_id(self) -> int:
        return 4
    
    def get_module_name(self) -> str:
        return 'paper'
    
    def get_papers_list(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """獲取論文列表"""
        query = Paper.query
        
        # 默認只顯示有效論文
        if not filters or not filters.get('show_all', False):
            query = query.filter_by(enable=1)
        
        # 應用篩選條件
        if filters:
            # 搜索關鍵字
            if filters.get('q'):
                search_term = f"%{filters['q']}%"
                query = query.filter(
                    (Paper.paper_title_zh.like(search_term)) |
                    (Paper.paper_title_en.like(search_term)) |
                    (Paper.paper_venue.like(search_term))
                )
            
            # 論文類型篩選
            if filters.get('paper_type') is not None:
                query = query.filter(Paper.paper_type == filters['paper_type'])
            
            # 接收狀態篩選
            if filters.get('paper_accept') is not None:
                query = query.filter(Paper.paper_accept == filters['paper_accept'])
            
            # 日期範圍篩選
            if filters.get('start_date'):
                valid, date_obj = validate_date(filters['start_date'])
                if valid and date_obj:
                    query = query.filter(Paper.paper_date >= date_obj)
            if filters.get('end_date'):
                valid, date_obj = validate_date(filters['end_date'])
                if valid and date_obj:
                    query = query.filter(Paper.paper_date <= date_obj)
        
        # 排序
        sort_by = filters.get('sort_by', 'paper_date') if filters else 'paper_date'
        order = filters.get('order', 'desc') if filters else 'desc'
        
        sort_column = getattr(Paper, sort_by, Paper.paper_date)
        if order.lower() == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # 分頁
        page, per_page = get_pagination_params()
        return paginate_query(query, page, per_page)
    
    def get_paper_detail(self, paper_id: int) -> Dict[str, Any]:
        """獲取論文詳情"""
        paper = Paper.query.filter_by(paper_id=paper_id, enable=1).first()
        if not paper:
            raise NotFoundError(msg.get_error_message('PAPER_NOT_FOUND'))
        
        return paper.to_dict()
    
    def create_paper(self, form_data: Dict[str, Any], files_data: Dict[str, Any] = None, authors_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """創建論文"""
        # 驗證權限
        self.validate_permissions('CREATE')
        
        # 數據校驗
        self._validate_paper_data(form_data, is_create=True)
        
        def _create_operation():
            # 處理文件上傳
            file_path = None
            if files_data and 'paper_file' in files_data:
                file = files_data['paper_file']
                if file and file.filename:
                    file_path = save_file(file, 'document', max_size=50*1024*1024)
            
            # 獲取默認實驗室和課題組
            lab = Lab.query.filter_by(enable=1).first()
            if not lab:
                raise ValidationError(msg.get_error_message('LAB_SETUP_REQUIRED'))
            
            research_group = ResearchGroup.query.filter_by(enable=1).first()
            
            # 創建論文
            paper = Paper(
                research_group_id=research_group.research_group_id if research_group else None,
                lab_id=lab.lab_id,
                enable=1
            )
            
            # 設置基本字段
            self._set_paper_fields(paper, form_data)
            paper.paper_file_path = file_path
            
            self.db.session.add(paper)
            self.db.session.flush()
            
            # 處理描述字段中的圖片管理
            image_upload_service = ImageUploadService()
            for field in ['paper_desc_zh', 'paper_desc_en']:
                if field in form_data and form_data[field]:
                    image_upload_service.mark_images_as_used(
                        content=form_data[field],
                        entity_type='paper',
                        entity_id=paper.paper_id,
                        field_name=field
                    )
            
            # 創建作者關聯
            if authors_data:
                self._create_paper_authors(paper.paper_id, authors_data)
            
            return paper.to_dict()
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_create_operation,
            operation_type='CREATE',
            content={**form_data, 'authors': authors_data or []}
        )
        
        return result
    
    def update_paper(self, paper_id: int, paper_data: Dict[str, Any], files_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """更新論文"""
        # 驗證權限
        self.validate_permissions('UPDATE')
        
        paper = Paper.query.filter_by(paper_id=paper_id, enable=1).first()
        if not paper:
            raise NotFoundError(msg.get_error_message('PAPER_NOT_FOUND'))
        
        # 數據校驗
        self._validate_paper_data(paper_data, is_create=False)
        
        def _update_operation():
            update_data = {}
            
            # 更新基本字段
            basic_fields = [
                'paper_title_zh', 'paper_title_en',
                'paper_desc_zh', 'paper_desc_en',
                'paper_venue', 'paper_url', 'paper_type', 'paper_accept',
                'all_authors_zh', 'all_authors_en'  # 新增：全部作者字段
            ]
            
            for field in basic_fields:
                if field in paper_data:
                    old_value = getattr(paper, field)
                    new_value = paper_data[field]
                    
                    if field in ['paper_type', 'paper_accept'] and isinstance(new_value, str):
                        new_value = int(new_value)
                    
                    if old_value != new_value:
                        setattr(paper, field, new_value)
                        update_data[field] = {'old': old_value, 'new': new_value}
                        
                        # 處理描述字段的圖片管理
                        if field in ['paper_desc_zh', 'paper_desc_en'] and new_value:
                            image_upload_service = ImageUploadService()
                            image_upload_service.mark_images_as_used(
                                content=new_value,
                                entity_type='paper',
                                entity_id=paper_id,
                                field_name=field
                            )
            
            # 更新日期
            if 'paper_date' in paper_data and paper_data['paper_date']:
                try:
                    new_date = datetime.strptime(paper_data['paper_date'], '%Y-%m-%d').date()
                    if paper.paper_date != new_date:
                        update_data['paper_date'] = {'old': str(paper.paper_date), 'new': str(new_date)}
                        paper.paper_date = new_date
                except ValueError:
                    raise ValidationError(msg.get_error_message('DATE_FORMAT_ERROR'))
            
            # 處理文件更新/刪除
            file_update = self._handle_file_update(paper, files_data, paper_data)
            if file_update:
                update_data.update(file_update)
            
            # 更新課題組
            if 'research_group_id' in paper_data:
                research_group_id = paper_data['research_group_id']
                if research_group_id and ResearchGroup.query.get(research_group_id):
                    if paper.research_group_id != research_group_id:
                        update_data['research_group_id'] = {
                            'old': paper.research_group_id,
                            'new': research_group_id
                        }
                        paper.research_group_id = research_group_id
            
            # 更新作者
            if 'authors' in paper_data and isinstance(paper_data['authors'], list):
                self._update_paper_authors(paper_id, paper_data['authors'])
                update_data['authors'] = paper_data['authors']
            
            # 重新加載論文信息以獲取更新後的作者
            self.db.session.flush()
            updated_paper = Paper.query.get(paper_id)
            
            return updated_paper.to_dict(), update_data
        
        # 執行操作並記錄審計
        result, update_data = self.execute_with_audit(
            operation_func=_update_operation,
            operation_type='UPDATE',
            content={}
        )
        
        return result
    
    def _handle_file_update(self, paper: 'Paper', files_data: Dict[str, Any] = None, form_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """處理論文文件更新/刪除"""
        update_result = {}
        
        # 處理論文文件刪除
        if form_data and form_data.get('paper_file_delete'):
            old_file_path = paper.paper_file_path
            if old_file_path:
                delete_file(old_file_path)
                paper.paper_file_path = None
                update_result['paper_file_deleted'] = True
                update_result['old_file_path'] = old_file_path
        
        # 處理預覽圖片刪除
        if form_data and form_data.get('preview_img_delete'):
            old_preview_img = paper.preview_img
            if old_preview_img:
                delete_file(old_preview_img)
                paper.preview_img = None
                update_result['preview_img_deleted'] = True
                update_result['old_preview_img'] = old_preview_img
        
        if files_data:
            # 處理新論文文件上傳
            if 'paper_file' in files_data:
                file = files_data['paper_file']
                if file and file.filename:
                    old_file_path = paper.paper_file_path
                    
                    try:
                        new_file_path = save_file(file, 'document', max_size=50*1024*1024)
                        paper.paper_file_path = new_file_path
                        
                        # 刪除舊文件
                        if old_file_path and old_file_path != new_file_path:
                            delete_file(old_file_path)
                        
                        update_result['paper_file_updated'] = True
                        update_result['new_file_path'] = new_file_path
                        
                    except Exception as e:
                        raise ValidationError(msg.format_file_error('PAPER_FILE_UPLOAD_FAILED', error=str(e)))
            
            # 處理新預覽圖片上傳
            if 'preview_img' in files_data:
                preview_file = files_data['preview_img']
                if preview_file and preview_file.filename:
                    old_preview_img = paper.preview_img
                    
                    try:
                        new_preview_path = save_file(preview_file, 'image', max_size=10*1024*1024)
                        paper.preview_img = new_preview_path
                        
                        # 刪除舊預覽圖片
                        if old_preview_img and old_preview_img != new_preview_path:
                            delete_file(old_preview_img)
                        
                        update_result['preview_img_updated'] = True
                        update_result['new_preview_path'] = new_preview_path
                        
                    except Exception as e:
                        raise ValidationError(msg.format_file_error('PREVIEW_IMG_UPLOAD_FAILED', error=str(e)))
        
        return update_result
    
    def delete_paper(self, paper_id: int) -> None:
        """刪除論文"""
        # 驗證權限
        self.validate_permissions('DELETE')
        
        paper = Paper.query.filter_by(paper_id=paper_id, enable=1).first()
        if not paper:
            raise NotFoundError(msg.get_error_message('PAPER_NOT_FOUND'))
        
        def _delete_operation():
            # 軟刪除
            self.soft_delete(paper, "paper")
            return {'deleted_paper_id': paper_id}
        
        # 執行操作並記錄審計
        self.execute_with_audit(
            operation_func=_delete_operation,
            operation_type='DELETE',
            content={'deleted_paper_id': paper_id}
        )
    
    def _validate_paper_data(self, paper_data: Dict[str, Any], is_create: bool = True) -> None:
        """校驗論文數據"""
        if is_create:
            # 檢查必填字段
            if not paper_data.get('paper_title_zh') and not paper_data.get('paper_title_en'):
                raise ValidationError(msg.get_error_message('PAPER_TITLE_REQUIRED'))
        
        # 論文類型校驗
        if 'paper_type' in paper_data:
            paper_type = paper_data['paper_type']
            if isinstance(paper_type, str):
                try:
                    paper_type = int(paper_type)
                except ValueError:
                    raise ValidationError(msg.get_error_message('PAPER_TYPE_FORMAT_ERROR'))
            
            if paper_type not in [0, 1, 2, 3, 4]:
                raise ValidationError(msg.get_error_message('PAPER_TYPE_INVALID'))
        
        # 接收狀態校驗
        if 'paper_accept' in paper_data:
            paper_accept = paper_data['paper_accept']
            if isinstance(paper_accept, str):
                try:
                    paper_accept = int(paper_accept)
                except ValueError:
                    raise ValidationError(msg.get_error_message('PAPER_ACCEPT_FORMAT_ERROR'))
            
            if paper_accept not in [0, 1]:
                raise ValidationError(msg.get_error_message('PAPER_ACCEPT_INVALID'))
        
        # 字符串長度校驗
        string_fields = {
            'paper_title_zh': 500,
            'paper_title_en': 500,
            'paper_desc_zh': 50000,
            'paper_desc_en': 50000,
            'paper_venue': 500,
            'paper_url': 1000,
            'all_authors_zh': 2000,  # 新增：全部作者中文字段
            'all_authors_en': 2000   # 新增：全部作者英文字段
        }
        
        for field, max_length in string_fields.items():
            if field in paper_data and paper_data[field]:
                if not validate_string_length(paper_data[field], max_length):
                    raise ValidationError(msg.format_field_length_error(field, max_length))
        
        # 日期格式校驗
        if 'paper_date' in paper_data and paper_data['paper_date']:
            try:
                datetime.strptime(paper_data['paper_date'], '%Y-%m-%d')
            except ValueError:
                raise ValidationError(msg.get_error_message('PAPER_DATE_FORMAT_ERROR'))
    
    def _set_paper_fields(self, paper: Paper, paper_data: Dict[str, Any]) -> None:
        """設置論文字段"""
        fields = [
            'paper_title_zh', 'paper_title_en',
            'paper_desc_zh', 'paper_desc_en',
            'paper_venue', 'paper_url', 'paper_type', 'paper_accept',
            'all_authors_zh', 'all_authors_en',  # 全部作者字段
            'preview_img'  # 預覽圖片字段
        ]
        
        for field in fields:
            if field in paper_data:
                value = paper_data[field]
                if field in ['paper_type', 'paper_accept'] and isinstance(value, str):
                    value = int(value)
                setattr(paper, field, value)
        
        # 特殊處理日期字段（必需字段）
        if 'paper_date' in paper_data and paper_data['paper_date']:
            paper.paper_date = datetime.strptime(paper_data['paper_date'], '%Y-%m-%d').date()
        else:
            # 如果沒有提供日期，使用當前日期作為默認值
            paper.paper_date = datetime.now().date()
    
    def _create_paper_authors(self, paper_id: int, authors_data: List[Dict[str, Any]]) -> None:
        """創建論文作者關聯"""
        for author_data in authors_data:
            mem_id = author_data.get('mem_id')
            author_order = author_data.get('author_order', 1)
            is_corresponding = author_data.get('is_corresponding', 0)
            
            # 檢查成員是否存在
            member = Member.query.filter_by(mem_id=mem_id, enable=1).first()
            if not member:
                continue
            
            paper_author = PaperAuthor(
                paper_id=paper_id,
                mem_id=mem_id,
                author_order=author_order,
                is_corresponding=is_corresponding
            )
            self.db.session.add(paper_author)
    
    def _update_paper_authors(self, paper_id: int, authors_data: List[Dict[str, Any]]) -> None:
        """更新論文作者關聯"""
        # 刪除舊的作者關係
        PaperAuthor.query.filter_by(paper_id=paper_id).delete()
        
        # 添加新的作者關係
        for i, author_data in enumerate(authors_data):
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
                    self.db.session.add(author)