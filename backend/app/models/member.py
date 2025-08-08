from app import db
from datetime import datetime

class Member(db.Model):
    __tablename__ = 'members'
    
    mem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mem_avatar_path = db.Column(db.String(500))
    mem_name_zh = db.Column(db.String(500))
    mem_name_en = db.Column(db.String(500))
    mem_desc_zh = db.Column(db.Text)
    mem_desc_en = db.Column(db.Text)
    mem_email = db.Column(db.String(500))
    mem_type = db.Column(db.Integer, nullable=False, default=0)  # 0:教師 1:學生 2:校友
    job_type = db.Column(db.Integer)  # 0:教授 1:副教授 2:講師 3:助理研究員 4:博士後
    student_type = db.Column(db.Integer)  # 0:博士生 1:碩士生 2:大學生
    student_grade = db.Column(db.Integer)
    destination_zh = db.Column(db.String(500))
    destination_en = db.Column(db.String(500))
    research_group_id = db.Column(db.Integer, db.ForeignKey('research_groups.research_group_id'), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.lab_id'), nullable=False)
    enable = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關係
    research_group = db.relationship('ResearchGroup', foreign_keys=[research_group_id], backref='members')
    lab = db.relationship('Lab', backref='members')
    
    def to_dict(self):
        return {
            'mem_id': self.mem_id,
            'mem_avatar_path': self.mem_avatar_path,
            'mem_name_zh': self.mem_name_zh,
            'mem_name_en': self.mem_name_en,
            'mem_desc_zh': self.mem_desc_zh,
            'mem_desc_en': self.mem_desc_en,
            'mem_email': self.mem_email,
            'mem_type': self.mem_type,
            'job_type': self.job_type,
            'student_type': self.student_type,
            'student_grade': self.student_grade,
            'destination_zh': self.destination_zh,
            'destination_en': self.destination_en,
            'research_group_id': self.research_group_id,
            'lab_id': self.lab_id,
            'enable': self.enable,
            'research_group': self.research_group.to_dict() if self.research_group else None
        }