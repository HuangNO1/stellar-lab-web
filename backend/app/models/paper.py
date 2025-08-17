from app import db
from datetime import datetime

class Paper(db.Model):
    __tablename__ = 'papers'
    
    paper_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    research_group_id = db.Column(db.Integer, db.ForeignKey('research_groups.research_group_id'))
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.lab_id'))
    paper_date = db.Column(db.Date, nullable=False, index=True)  # 添加索引用於日期查詢和排序
    paper_title_zh = db.Column(db.String(500), index=True)  # 添加索引用於標題搜索
    paper_title_en = db.Column(db.String(500), index=True)  # 添加索引用於標題搜索
    paper_desc_zh = db.Column(db.Text)
    paper_desc_en = db.Column(db.Text)
    paper_type = db.Column(db.Integer, nullable=False, default=0, index=True)  # 添加索引用於類型篩選
    paper_venue = db.Column(db.String(500), index=True)  # 添加索引用於期刊/會議搜索
    paper_accept = db.Column(db.Integer, nullable=False, default=0, index=True)  # 添加索引用於接收狀態篩選
    paper_file_path = db.Column(db.String(500))
    paper_url = db.Column(db.String(1000))
    preview_img = db.Column(db.String(500))  # 論文預覽圖片路徑
    # 全部作者字段（包含非實驗室成員）
    all_authors_zh = db.Column(db.Text)  # 全部作者中文
    all_authors_en = db.Column(db.Text)  # 全部作者英文
    enable = db.Column(db.Integer, nullable=False, default=1, index=True)  # 添加索引用於啟用狀態篩選
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # 添加索引用於排序
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 複合索引
    __table_args__ = (
        db.Index('ix_paper_enable_date', 'enable', 'paper_date'),  # 用於查詢已發布論文按日期排序
        db.Index('ix_paper_enable_type', 'enable', 'paper_type'),  # 用於篩選已發布的特定類型論文
        db.Index('ix_paper_enable_accept', 'enable', 'paper_accept'),  # 用於篩選已發布的接收狀態論文
    )
    
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
            'preview_img': self.preview_img,
            'all_authors_zh': self.all_authors_zh,
            'all_authors_en': self.all_authors_en,
            'enable': self.enable,
            'authors': [author.to_dict() for author in self.authors]  # 實驗室作者
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
        result = {
            'paper_id': self.paper_id,
            'mem_id': self.mem_id,
            'author_order': self.author_order,
            'is_corresponding': self.is_corresponding
        }
        
        # 避免循環引用，只返回基本信息
        if hasattr(self, 'member') and self.member:
            result['member'] = {
                'mem_id': self.member.mem_id,
                'mem_name_zh': self.member.mem_name_zh,
                'mem_name_en': self.member.mem_name_en
            }
        
        return result