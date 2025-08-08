from app import db
from datetime import datetime

class News(db.Model):
    __tablename__ = 'news'
    
    news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_type = db.Column(db.Integer, nullable=False)  # 0:論文 1:獎項 2:報告 3:其它
    news_content_zh = db.Column(db.Text)
    news_content_en = db.Column(db.Text)
    news_date = db.Column(db.Date)
    enable = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'news_id': self.news_id,
            'news_type': self.news_type,
            'news_content_zh': self.news_content_zh,
            'news_content_en': self.news_content_en,
            'news_date': self.news_date.isoformat() if self.news_date else None,
            'enable': self.enable
        }