from app import db
from datetime import datetime

class Lab(db.Model):
    __tablename__ = 'lab'
    
    lab_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_logo_path = db.Column(db.String(500))
    lab_zh = db.Column(db.String(500), index=True)  # 添加索引用於實驗室中文名稱搜索
    lab_en = db.Column(db.String(500), index=True)  # 添加索引用於實驗室英文名稱搜索
    lab_desc_zh = db.Column(db.Text)
    lab_desc_en = db.Column(db.Text)
    lab_address_zh = db.Column(db.String(500), index=True)  # 添加索引用於地址搜索
    lab_address_en = db.Column(db.String(500), index=True)  # 添加索引用於地址搜索
    lab_email = db.Column(db.String(500), index=True)  # 添加索引用於郵箱搜索
    lab_phone = db.Column(db.String(500), index=True)  # 添加索引用於電話搜索
    enable = db.Column(db.Integer, nullable=False, default=1, index=True)  # 添加索引用於啟用狀態篩選
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # 添加索引用於排序
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'lab_id': self.lab_id,
            'lab_logo_path': self.lab_logo_path,
            'lab_zh': self.lab_zh,
            'lab_en': self.lab_en,
            'lab_desc_zh': self.lab_desc_zh,
            'lab_desc_en': self.lab_desc_en,
            'lab_address_zh': self.lab_address_zh,
            'lab_address_en': self.lab_address_en,
            'lab_email': self.lab_email,
            'lab_phone': self.lab_phone,
            'enable': self.enable
        }