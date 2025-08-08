from app import db
from datetime import datetime

class ResearchGroup(db.Model):
    __tablename__ = 'research_groups'
    
    research_group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.lab_id'), nullable=False)
    research_group_name_zh = db.Column(db.String(500))
    research_group_name_en = db.Column(db.String(500))
    research_group_desc_zh = db.Column(db.Text)
    research_group_desc_en = db.Column(db.Text)
    mem_id = db.Column(db.Integer, db.ForeignKey('members.mem_id'))
    enable = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關係
    lab = db.relationship('Lab', backref='research_groups')
    leader = db.relationship('Member', foreign_keys=[mem_id], backref='led_groups')
    
    def to_dict(self):
        return {
            'research_group_id': self.research_group_id,
            'lab_id': self.lab_id,
            'research_group_name_zh': self.research_group_name_zh,
            'research_group_name_en': self.research_group_name_en,
            'research_group_desc_zh': self.research_group_desc_zh,
            'research_group_desc_en': self.research_group_desc_en,
            'mem_id': self.mem_id,
            'enable': self.enable,
            'leader': self.leader.to_dict() if self.leader else None
        }