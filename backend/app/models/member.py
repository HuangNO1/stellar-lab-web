from app import db
from datetime import datetime

class Member(db.Model):
    __tablename__ = 'members'
    
    mem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mem_avatar_path = db.Column(db.String(500))
    mem_name_zh = db.Column(db.String(500), index=True)  # 添加索引用於姓名搜索
    mem_name_en = db.Column(db.String(500), index=True)  # 添加索引用於姓名搜索
    mem_desc_zh = db.Column(db.Text)
    mem_desc_en = db.Column(db.Text)
    mem_email = db.Column(db.String(500), index=True)  # 添加索引用於郵箱搜索
    mem_type = db.Column(db.Integer, nullable=False, default=0, index=True)  # 添加索引用於類型篩選
    job_type = db.Column(db.Integer)
    student_type = db.Column(db.Integer)
    student_grade = db.Column(db.Integer)
    destination_zh = db.Column(db.String(500))
    destination_en = db.Column(db.String(500))
    research_group_id = db.Column(db.Integer, db.ForeignKey('research_groups.research_group_id'), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.lab_id'), nullable=False)
    enable = db.Column(db.Integer, nullable=False, default=1, index=True)  # 添加索引用於啟用狀態篩選
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # 添加索引用於排序
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 複合索引
    __table_args__ = (
        db.Index('ix_member_enable_type', 'enable', 'mem_type'),  # 用於篩選啟用的特定類型成員
        db.Index('ix_member_enable_created', 'enable', 'created_at'),  # 用於分頁查詢已啟用成員
    )
    
    # 關係
    research_group = db.relationship('ResearchGroup', foreign_keys=[research_group_id], backref='members')
    lab = db.relationship('Lab', backref='members')
    
    def to_dict(self):
        result = {
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
            'enable': self.enable
        }
        
        # 避免循環引用，只返回基本信息
        if hasattr(self, 'research_group') and self.research_group:
            result['research_group'] = {
                'research_group_id': self.research_group.research_group_id,
                'research_group_name_zh': self.research_group.research_group_name_zh,
                'research_group_name_en': self.research_group.research_group_name_en
            }
        
        return result