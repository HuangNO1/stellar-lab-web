from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_url = db.Column(db.String(500))
    project_name_zh = db.Column(db.String(500), index=True)  # 添加索引用於項目名稱搜索
    project_name_en = db.Column(db.String(500), index=True)  # 添加索引用於項目名稱搜索
    project_desc_zh = db.Column(db.Text)
    project_desc_en = db.Column(db.Text)
    project_date_start = db.Column(db.Date, index=True)  # 添加索引用於日期查詢和排序
    is_end = db.Column(db.Integer, nullable=False, default=0, index=True)  # 添加索引用於狀態篩選
    enable = db.Column(db.Integer, nullable=False, default=1, index=True)  # 添加索引用於啟用狀態篩選
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # 添加索引用於排序
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 複合索引
    __table_args__ = (
        db.Index('ix_project_enable_status', 'enable', 'is_end'),  # 用於篩選已啟用的特定狀態項目
        db.Index('ix_project_enable_date', 'enable', 'project_date_start'),  # 用於查詢已啟用項目按日期排序
    )
    
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