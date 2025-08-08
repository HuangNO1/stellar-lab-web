from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_url = db.Column(db.String(500))
    project_name_zh = db.Column(db.String(500))
    project_name_en = db.Column(db.String(500))
    project_desc_zh = db.Column(db.Text)
    project_desc_en = db.Column(db.Text)
    project_date_start = db.Column(db.Date)
    is_end = db.Column(db.Integer, nullable=False, default=0)
    enable = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'project_id': self.project_id,
            'project_url': self.project_url,
            'project_name_zh': self.project_name_zh,
            'project_name_en': self.project_name_en,
            'project_desc_zh': self.project_desc_zh,
            'project_desc_en': self.project_desc_en,
            'project_date_start': self.project_date_start.isoformat() if self.project_date_start else None,
            'is_end': self.is_end,
            'enable': self.enable
        }