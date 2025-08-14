from app import db
from datetime import datetime, timezone
import json

class EditRecord(db.Model):
    __tablename__ = 'edit_records'
    
    edit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=False)
    edit_type = db.Column(db.String(50), nullable=False, index=True)  # 添加索引用於操作類型篩選 CREATE, UPDATE, DELETE
    edit_module = db.Column(db.Integer, nullable=False, index=True)  # 添加索引用於模塊篩選 0:管理員 1:實驗室 2:課題組 3:成員 4:論文 5:新聞 6:項目 7:媒體文件 8:圖片上傳
    edit_content = db.Column(db.Text)
    edit_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)  # 明確使用 UTC 時區
    
    # 複合索引
    __table_args__ = (
        db.Index('ix_edit_record_admin_date', 'admin_id', 'edit_date'),  # 用於查詢特定管理員的操作記錄按日期排序
        db.Index('ix_edit_record_type_module', 'edit_type', 'edit_module'),  # 用於篩選特定類型和模塊的操作
        db.Index('ix_edit_record_module_date', 'edit_module', 'edit_date'),  # 用於查詢特定模塊的操作按日期排序
    )
    
    # 關係
    admin = db.relationship('Admin', backref='edit_records')
    
    def set_content(self, content_dict):
        self.edit_content = json.dumps(content_dict, ensure_ascii=False)
    
    def get_content(self):
        if self.edit_content:
            return json.loads(self.edit_content)
        return {}
    
    def to_dict(self):
        return {
            'edit_id': self.edit_id,
            'admin_id': self.admin_id,
            'edit_type': self.edit_type,
            'edit_module': self.edit_module,
            'edit_content': self.get_content(),
            'edit_date': self.edit_date.replace(tzinfo=timezone.utc).isoformat(),  # 明確標示 UTC 時區
            'admin': self.admin.to_dict() if self.admin else None
        }