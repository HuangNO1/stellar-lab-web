from typing import Optional, Dict, Any
from datetime import datetime
from app.models import News
from app.utils.validators import validate_string_length
from app.utils.helpers import get_pagination_params, paginate_query
from .base_service import BaseService, ValidationError, NotFoundError


class NewsService(BaseService):
    """
    新聞管理服務層
    """
    
    def get_module_id(self) -> int:
        return 5
    
    def get_module_name(self) -> str:
        return 'news'
    
    def get_news_list(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """獲取新聞列表"""
        query = News.query
        
        # 默認只顯示有效新聞
        if not filters or not filters.get('show_all', False):
            query = query.filter_by(enable=1)
        
        # 應用篩選條件
        if filters:
            # 搜索關鍵字
            if filters.get('q'):
                search_term = f"%{filters['q']}%"
                query = query.filter(
                    (News.news_content_zh.like(search_term)) |
                    (News.news_content_en.like(search_term))
                )
            
            # 新聞類型篩選
            if filters.get('news_type') is not None:
                query = query.filter(News.news_type == filters['news_type'])
            
            # 日期範圍篩選
            if filters.get('start_date'):
                query = query.filter(News.news_date >= filters['start_date'])
            if filters.get('end_date'):
                query = query.filter(News.news_date <= filters['end_date'])
        
        # 按日期倒序排序
        query = query.order_by(News.news_date.desc())
        
        # 分頁
        page, per_page = get_pagination_params()
        return paginate_query(query, page, per_page)
    
    def get_news_detail(self, news_id: int) -> Dict[str, Any]:
        """獲取新聞詳情"""
        news = News.query.filter_by(news_id=news_id, enable=1).first()
        if not news:
            raise NotFoundError('新聞不存在')
        
        return news.to_dict()
    
    def create_news(self, news_data: Dict[str, Any]) -> Dict[str, Any]:
        """創建新聞"""
        # 驗證權限
        self.validate_permissions('CREATE')
        
        # 數據校驗
        self._validate_news_data(news_data, is_create=True)
        
        def _create_operation():
            news = News(enable=1)
            
            # 設置新聞信息
            news.news_type = news_data['news_type']
            news.news_content_zh = news_data['news_content_zh']
            news.news_content_en = news_data.get('news_content_en', '')
            news.news_date = datetime.strptime(news_data['news_date'], '%Y-%m-%d').date()
            
            self.db.session.add(news)
            self.db.session.flush()
            
            return news.to_dict()
        
        # 執行操作並記錄審計
        result = self.execute_with_audit(
            operation_func=_create_operation,
            operation_type='CREATE',
            content=news_data
        )
        
        return result
    
    def update_news(self, news_id: int, news_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新新聞"""
        # 驗證權限
        self.validate_permissions('UPDATE')
        
        news = News.query.filter_by(news_id=news_id, enable=1).first()
        if not news:
            raise NotFoundError('新聞不存在')
        
        # 數據校驗
        self._validate_news_data(news_data, is_create=False)
        
        def _update_operation():
            update_data = {}
            
            # 更新字段
            fields = ['news_type', 'news_content_zh', 'news_content_en', 'news_date']
            for field in fields:
                if field in news_data:
                    old_value = getattr(news, field)
                    if field == 'news_date':
                        new_value = datetime.strptime(news_data[field], '%Y-%m-%d').date()
                    else:
                        new_value = news_data[field]
                    
                    if old_value != new_value:
                        setattr(news, field, new_value)
                        update_data[field] = {'old': str(old_value), 'new': str(new_value)}
            
            return news.to_dict(), update_data
        
        # 執行操作並記錄審計
        result, update_data = self.execute_with_audit(
            operation_func=_update_operation,
            operation_type='UPDATE',
            content={}
        )
        
        return result
    
    def delete_news(self, news_id: int) -> None:
        """刪除新聞"""
        # 驗證權限
        self.validate_permissions('DELETE')
        
        news = News.query.filter_by(news_id=news_id, enable=1).first()
        if not news:
            raise NotFoundError('新聞不存在')
        
        def _delete_operation():
            # 軟刪除
            self.soft_delete(news, "新聞")
            return {'deleted_news_id': news_id}
        
        # 執行操作並記錄審計
        self.execute_with_audit(
            operation_func=_delete_operation,
            operation_type='DELETE',
            content={'deleted_news_id': news_id}
        )
    
    def _validate_news_data(self, news_data: Dict[str, Any], is_create: bool = True) -> None:
        """校驗新聞數據"""
        if is_create:
            required_fields = ['news_type', 'news_content_zh', 'news_date']
            self.validate_required_fields(news_data, required_fields)
        
        # 新聞類型校驗
        if 'news_type' in news_data:
            try:
                news_type_value = int(news_data['news_type'])
                if news_type_value not in [0, 1, 2]:  # 0=論文發表, 1=獲獎消息, 2=學術活動
                    raise ValidationError('新聞類型無效')
                news_data['news_type'] = news_type_value
            except (ValueError, TypeError):
                raise ValidationError('新聞類型格式錯誤')
        
        # 字符串長度校驗
        string_fields = {
            'news_content_zh': 10000,
            'news_content_en': 10000
        }
        
        for field, max_length in string_fields.items():
            if field in news_data and news_data[field]:
                if not validate_string_length(news_data[field], max_length):
                    raise ValidationError(f'{field} 長度不能超過{max_length}字符')
        
        # 日期格式校驗
        if 'news_date' in news_data:
            try:
                datetime.strptime(news_data['news_date'], '%Y-%m-%d')
            except ValueError:
                raise ValidationError('日期格式錯誤，應為 YYYY-MM-DD')