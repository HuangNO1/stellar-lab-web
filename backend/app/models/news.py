from app import db
from datetime import datetime

class News(db.Model):
    __tablename__ = 'news'
    
    news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_type = db.Column(db.Integer, nullable=False, index=True)  # 添加索引用於類型篩選
    news_content_zh = db.Column(db.Text)
    news_content_en = db.Column(db.Text)
    news_date = db.Column(db.Date, index=True)  # 添加索引用於日期查詢和排序
    enable = db.Column(db.Integer, nullable=False, default=1, index=True)  # 添加索引用於啟用狀態篩選
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # 添加索引用於排序
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 複合索引
    __table_args__ = (
        db.Index('ix_news_enable_type', 'enable', 'news_type'),  # 用於篩選已啟用的特定類型新聞
        db.Index('ix_news_enable_date', 'enable', 'news_date'),  # 用於查詢已發布新聞按日期排序
    )
    
    def to_dict(self):
        return {
            'news_id': self.news_id,
            'news_type': self.news_type,
            'news_content_zh': self.news_content_zh,
            'news_content_en': self.news_content_en,
            'news_date': self.news_date.isoformat() if self.news_date else None,
            'enable': self.enable
        }