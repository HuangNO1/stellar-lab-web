from app import db
from datetime import datetime

class Paper(db.Model):
    __tablename__ = 'papers'
    
    paper_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    research_group_id = db.Column(db.Integer, db.ForeignKey('research_groups.research_group_id'))
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.lab_id'))
    paper_date = db.Column(db.Date, nullable=False)
    paper_title_zh = db.Column(db.String(500))
    paper_title_en = db.Column(db.String(500))
    paper_desc_zh = db.Column(db.Text)
    paper_desc_en = db.Column(db.Text)
    paper_type = db.Column(db.Integer, nullable=False, default=0)  # 0:期刊 1:會議 2:學位 3:專著 4:其它
    paper_venue = db.Column(db.String(500))
    paper_accept = db.Column(db.Integer, nullable=False, default=0)
    paper_file_path = db.Column(db.String(500))
    paper_url = db.Column(db.String(1000))
    enable = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關係
    research_group = db.relationship('ResearchGroup', backref='papers')
    lab = db.relationship('Lab', backref='papers')
    authors = db.relationship('PaperAuthor', backref='paper', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'paper_id': self.paper_id,
            'research_group_id': self.research_group_id,
            'lab_id': self.lab_id,
            'paper_date': self.paper_date.isoformat() if self.paper_date else None,
            'paper_title_zh': self.paper_title_zh,
            'paper_title_en': self.paper_title_en,
            'paper_desc_zh': self.paper_desc_zh,
            'paper_desc_en': self.paper_desc_en,
            'paper_type': self.paper_type,
            'paper_venue': self.paper_venue,
            'paper_accept': self.paper_accept,
            'paper_file_path': self.paper_file_path,
            'paper_url': self.paper_url,
            'enable': self.enable,
            'authors': [author.to_dict() for author in self.authors]
        }

class PaperAuthor(db.Model):
    __tablename__ = 'paper_authors'
    
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.paper_id'), primary_key=True)
    mem_id = db.Column(db.Integer, db.ForeignKey('members.mem_id'), primary_key=True)
    author_order = db.Column(db.Integer, nullable=False)
    is_corresponding = db.Column(db.Integer, nullable=False, default=0)
    
    # 關係
    member = db.relationship('Member', backref='authored_papers')
    
    def to_dict(self):
        return {
            'paper_id': self.paper_id,
            'mem_id': self.mem_id,
            'author_order': self.author_order,
            'is_corresponding': self.is_corresponding,
            'member': self.member.to_dict() if self.member else None
        }