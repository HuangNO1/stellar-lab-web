"""實驗室資源模型"""

from app import db
from datetime import datetime


class Resource(db.Model):
    __tablename__ = 'lab_resource'
    
    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_name_zh = db.Column(db.String(200), nullable=False)  # 中文資源名稱
    resource_name_en = db.Column(db.String(200), nullable=True)   # 英文資源名稱
    resource_description_zh = db.Column(db.Text, nullable=True)   # 中文資源描述
    resource_description_en = db.Column(db.Text, nullable=True)   # 英文資源描述
    resource_type = db.Column(db.Integer, nullable=False, default=0)  # 資源類型: 0=設備,1=軟件,2=數據庫,3=其他
    resource_location_zh = db.Column(db.String(300), nullable=True)  # 中文位置/連結
    resource_location_en = db.Column(db.String(300), nullable=True)  # 英文位置/連結
    resource_url = db.Column(db.String(500), nullable=True)       # 資源URL連結
    resource_file = db.Column(db.String(500), nullable=True)      # 資源檔案路徑
    resource_image = db.Column(db.String(500), nullable=True)     # 資源圖片
    availability_status = db.Column(db.Integer, nullable=False, default=1)  # 可用狀態: 0=不可用,1=可用,2=維護中
    contact_info = db.Column(db.String(200), nullable=True)       # 聯絡資訊
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """將資源對象轉換為字典"""
        return {
            'resource_id': self.resource_id,
            'resource_name_zh': self.resource_name_zh,
            'resource_name_en': self.resource_name_en,
            'resource_description_zh': self.resource_description_zh,
            'resource_description_en': self.resource_description_en,
            'resource_type': self.resource_type,
            'resource_location_zh': self.resource_location_zh,
            'resource_location_en': self.resource_location_en,
            'resource_url': self.resource_url,
            'resource_file': self.resource_file,
            'resource_image': self.resource_image,
            'availability_status': self.availability_status,
            'contact_info': self.contact_info,
            'created_time': self.created_time.isoformat() if self.created_time else None,
            'updated_time': self.updated_time.isoformat() if self.updated_time else None
        }

    def __repr__(self):
        return f'<Resource {self.resource_id}: {self.resource_name_zh}>'