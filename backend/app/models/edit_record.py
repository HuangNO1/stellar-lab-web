from app import db
from datetime import datetime
import json

class EditRecord(db.Model):
    __tablename__ = 'edit_records'
    
    edit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=False)
    edit_type = db.Column(db.String(50), nullable=False)  # CREATE, UPDATE, DELETE
    edit_module = db.Column(db.Integer, nullable=False)  # 0:實驗室 1:課題組 2:成員 3:論文 4:新聞 5:項目
    edit_content = db.Column(db.Text)
    edit_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
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
            'edit_date': self.edit_date.isoformat(),
            'admin': self.admin.to_dict() if self.admin else None
        }