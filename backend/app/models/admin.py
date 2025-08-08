from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

class Admin(db.Model):
    __tablename__ = 'admins'
    
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_super = db.Column(db.Integer, nullable=False, default=0)
    admin_name = db.Column(db.String(50), nullable=False, unique=True)
    admin_pass = db.Column(db.String(255), nullable=False)
    enable = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.admin_pass = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.admin_pass.encode('utf-8'))
    
    def to_dict(self):
        return {
            'admin_id': self.admin_id,
            'admin_name': self.admin_name,
            'is_super': self.is_super,
            'enable': self.enable,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }