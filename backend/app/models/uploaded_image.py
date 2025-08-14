from app import db
from datetime import datetime

class UploadedImage(db.Model):
    __tablename__ = 'uploaded_images'
    
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)  # 原始文件名
    file_path = db.Column(db.String(500), nullable=False, unique=True)  # 服務器存儲路徑
    file_url = db.Column(db.String(500), nullable=False)  # 訪問URL
    file_size = db.Column(db.Integer, nullable=False)  # 文件大小（字節）
    mime_type = db.Column(db.String(100), nullable=False)  # MIME類型
    
    # 關聯信息
    entity_type = db.Column(db.String(50), nullable=True, index=True)  # 關聯實體類型(lab, member, paper, project, research_group)
    entity_id = db.Column(db.Integer, nullable=True, index=True)  # 關聯實體ID
    field_name = db.Column(db.String(100), nullable=True)  # 關聯字段名稱
    
    # 狀態信息
    is_used = db.Column(db.Boolean, default=False, nullable=False, index=True)  # 是否被使用
    used_at = db.Column(db.DateTime, nullable=True)  # 使用時間
    uploaded_by = db.Column(db.Integer, nullable=True)  # 上傳者ID（可選）
    
    # 時間戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 複合索引
    __table_args__ = (
        db.Index('ix_uploaded_images_entity', 'entity_type', 'entity_id'),  # 用於查詢實體相關圖片
        db.Index('ix_uploaded_images_unused', 'is_used', 'created_at'),  # 用於清理未使用的圖片
    )
    
    def to_dict(self):
        return {
            'image_id': self.image_id,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_url': self.file_url,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'field_name': self.field_name,
            'is_used': self.is_used,
            'used_at': self.used_at.isoformat() if self.used_at else None,
            'uploaded_by': self.uploaded_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }