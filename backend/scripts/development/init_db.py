#!/usr/bin/env python3
"""
數據庫初始化腳本
統一使用 MySQL 數據庫（支持開發、測試、生產環境）
根據需求文檔創建完整的示例數據
自動創建數據庫（如果不存在）
"""

import os
import sys
from datetime import date
import re
from urllib.parse import urlparse
import pymysql

# 添加項目根目錄到 Python 路徑
# 在Docker環境中，當前工作目錄應該已經是項目根目錄
current_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))  # 向上兩級目錄
if os.path.exists(os.path.join(project_root, 'app')):
    sys.path.insert(0, project_root)
else:
    # 如果在Docker環境中，嘗試使用當前工作目錄
    sys.path.insert(0, os.getcwd())

from app import create_app, db
from app.models import Admin, Lab, ResearchGroup, Member, Paper, PaperAuthor, Project, News, EditRecord

def get_current_environment():
    """獲取當前運行環境"""
    return os.environ.get('FLASK_CONFIG', 'development')

def create_database_if_not_exists():
    """創建數據庫（如果不存在）"""
    from config.config import config
    
    # 獲取當前環境配置
    env = get_current_environment()
    config_obj = config.get(env, config['default'])
    
    # 解析數據庫 URI
    db_uri = config_obj.SQLALCHEMY_DATABASE_URI
    parsed = urlparse(db_uri)
    
    # 提取連接信息
    host = parsed.hostname or 'localhost'
    port = parsed.port or 3306
    username = parsed.username or 'root'
    password = parsed.password or ''
    database = parsed.path.lstrip('/')
    
    # 移除可能的查詢參數（如 charset）
    if '?' in database:
        database = database.split('?')[0]
    
    print(f"🔧 檢查數據庫 '{database}' 是否存在...")
    print(f"   主機: {host}:{port}")
    print(f"   用戶: {username}")
    
    try:
        # 連接到 MySQL 服務器（不指定數據庫）
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # 檢查數據庫是否存在
            cursor.execute("SHOW DATABASES LIKE %s", (database,))
            result = cursor.fetchone()
            
            if not result:
                print(f"🏗️  創建數據庫 '{database}'...")
                cursor.execute(f"CREATE DATABASE `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅ 數據庫 '{database}' 創建成功")
            else:
                print(f"✅ 數據庫 '{database}' 已存在")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ 數據庫操作失敗: {e}")
        print(f"   請檢查 MySQL/MariaDB 服務是否運行")
        print(f"   以及用戶 '{username}' 是否有足夠權限")
        sys.exit(1)

def print_env_info(app):
    """打印環境信息"""
    env = get_current_environment()
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    
    print(f"🌍 當前環境: {env}")
    print(f"🗄️  數據庫: {'MySQL' if 'mysql' in db_uri else 'Other'}")
    
    if 'mysql' in db_uri:
        # 提取數據庫名稱
        db_name = db_uri.split('/')[-1].split('?')[0]
        print(f"📊 數據庫名稱: {db_name}")

def create_admin_data():
    """創建管理員數據"""
    existing_admin = Admin.query.filter_by(is_super=1, enable=1).first()
    if not existing_admin:
        super_admin = Admin(
            admin_name='admin',
            is_super=1,
            enable=1
        )
        super_admin.set_password('admin123')
        db.session.add(super_admin)
        print("✓ 創建超級管理員 (用戶名: admin, 密碼: admin123)")
        return super_admin
    else:
        print("✓ 超級管理員已存在")
        return existing_admin

def create_lab_data():
    """創建實驗室數據"""
    existing_lab = Lab.query.filter_by(enable=1).first()
    if not existing_lab:
        default_lab = Lab(
            lab_zh='智能計算實驗室',
            lab_en='Intelligent Computing Laboratory',
            lab_desc_zh='本實驗室專注於人工智能、機器學習和計算機視覺領域的研究，致力於推動智能技術的發展與應用。',
            lab_desc_en='Our laboratory focuses on research in artificial intelligence, machine learning, and computer vision, dedicated to advancing the development and application of intelligent technologies.',
            lab_address_zh='北京市海淀區清華大學FIT樓',
            lab_address_en='FIT Building, Tsinghua University, Haidian District, Beijing',
            lab_email='contact@lab.tsinghua.edu.cn',
            lab_phone='+86-10-62785678',
            enable=1
        )
        db.session.add(default_lab)
        db.session.flush()
        print("✓ 創建默認實驗室信息")
        return default_lab
    else:
        print("✓ 實驗室信息已存在")
        return existing_lab

def create_research_groups(lab_id):
    """創建課題組數據"""
    existing_count = ResearchGroup.query.filter_by(enable=1).count()
    if existing_count == 0:
        groups_data = [
            {
                'name_zh': '計算機視覺研究組',
                'name_en': 'Computer Vision Research Group',
                'desc_zh': '專注於圖像識別、目標檢測、語義分割等計算機視覺技術研究',
                'desc_en': 'Focus on computer vision technologies including image recognition, object detection, and semantic segmentation'
            },
            {
                'name_zh': '自然語言處理研究組', 
                'name_en': 'Natural Language Processing Research Group',
                'desc_zh': '致力於機器翻譯、文本理解、對話系統等自然語言處理技術研究',
                'desc_en': 'Dedicated to natural language processing technologies including machine translation, text understanding, and dialogue systems'
            }
        ]
        
        created_groups = []
        for group_data in groups_data:
            group = ResearchGroup(
                lab_id=lab_id,
                research_group_name_zh=group_data['name_zh'],
                research_group_name_en=group_data['name_en'], 
                research_group_desc_zh=group_data['desc_zh'],
                research_group_desc_en=group_data['desc_en'],
                enable=1
            )
            db.session.add(group)
            created_groups.append(group)
        
        db.session.flush()
        print("✓ 創建示例課題組")
        return created_groups
    else:
        groups = ResearchGroup.query.filter_by(enable=1).all()
        print("✓ 課題組已存在")
        return groups

def create_members(lab_id, groups):
    """創建成員數據"""
    existing_count = Member.query.filter_by(enable=1).count()
    if existing_count == 0:
        members_data = [
            {
                'name_zh': '張教授', 'name_en': 'Prof. Zhang',
                'email': 'zhang@lab.edu.cn', 'type': 0, 'job_type': 0,
                'desc_zh': '實驗室主任，長期從事人工智能領域研究，發表論文100餘篇',
                'desc_en': 'Director of the laboratory, long-term research in artificial intelligence, published over 100 papers',
                'group_idx': 0
            },
            {
                'name_zh': '李副教授', 'name_en': 'Assoc. Prof. Li', 
                'email': 'li@lab.edu.cn', 'type': 0, 'job_type': 1,
                'desc_zh': '計算機視覺專家，主要研究圖像處理和模式識別技術',
                'desc_en': 'Computer vision expert, mainly researching image processing and pattern recognition',
                'group_idx': 0
            },
            {
                'name_zh': '王博士', 'name_en': 'Dr. Wang',
                'email': 'wang@lab.edu.cn', 'type': 1, 'student_type': 0, 'student_grade': 3,
                'desc_zh': '博士研究生，研究方向為深度學習和神經網絡',
                'desc_en': 'PhD student, research focus on deep learning and neural networks', 
                'group_idx': 1
            }
        ]
        
        created_members = []
        for member_data in members_data:
            member = Member(
                mem_name_zh=member_data['name_zh'],
                mem_name_en=member_data['name_en'],
                mem_email=member_data['email'],
                mem_type=member_data['type'],
                job_type=member_data.get('job_type'),
                student_type=member_data.get('student_type'),
                student_grade=member_data.get('student_grade'),
                mem_desc_zh=member_data['desc_zh'],
                mem_desc_en=member_data['desc_en'],
                research_group_id=groups[member_data['group_idx']].research_group_id,
                lab_id=lab_id,
                enable=1
            )
            db.session.add(member)
            created_members.append(member)
        
        db.session.flush()

        # 設置課題組組長
        groups[0].mem_id = created_members[0].mem_id  # 張教授領導第一組
        groups[1].mem_id = created_members[1].mem_id  # 李副教授領導第二組
        
        print("✓ 創建示例成員")
        return created_members
    else:
        members = Member.query.filter_by(enable=1).all()
        print("✓ 成員已存在")
        return members

def create_papers(lab_id, groups, members):
    """創建論文數據"""
    existing_count = Paper.query.filter_by(enable=1).count()
    if existing_count == 0:
        papers_data = [
            {
                'title_zh': '基於深度學習的圖像識別技術研究',
                'title_en': 'Research on Image Recognition Technology Based on Deep Learning',
                'desc_zh': '本文提出了一種新的深度學習模型，在圖像識別任務中取得了顯著效果',
                'desc_en': 'This paper proposes a novel deep learning model that achieves significant results in image recognition tasks',
                'venue': 'CVPR 2024', 'type': 1, 'accept': 1,
                'date': date(2024, 6, 15), 'group_idx': 0,
                'authors': [0, 1]  # 張教授和李副教授的索引
            },
            {
                'title_zh': '自然語言處理中的注意力機制優化',
                'title_en': 'Attention Mechanism Optimization in Natural Language Processing', 
                'desc_zh': '針對Transformer模型的注意力機制進行了創新性改進',
                'desc_en': 'Innovative improvements to the attention mechanism of Transformer models',
                'venue': 'AAAI 2024', 'type': 1, 'accept': 1,
                'date': date(2024, 8, 20), 'group_idx': 1,
                'authors': [2]  # 王博士的索引
            }
        ]
        
        for paper_data in papers_data:
            paper = Paper(
                paper_title_zh=paper_data['title_zh'],
                paper_title_en=paper_data['title_en'],
                paper_desc_zh=paper_data['desc_zh'],
                paper_desc_en=paper_data['desc_en'],
                paper_venue=paper_data['venue'],
                paper_type=paper_data['type'],
                paper_accept=paper_data['accept'],
                paper_date=paper_data['date'],
                research_group_id=groups[paper_data['group_idx']].research_group_id,
                lab_id=lab_id,
                enable=1
            )
            db.session.add(paper)
            db.session.flush()
            
            # 添加作者關係
            for order, member_idx in enumerate(paper_data['authors']):
                if member_idx < len(members):  # 檢查索引有效性
                    author = PaperAuthor(
                        paper_id=paper.paper_id,
                        mem_id=members[member_idx].mem_id,
                        author_order=order + 1,
                        is_corresponding=1 if order == 0 else 0
                    )
                    db.session.add(author)
        
        print("✓ 創建示例論文")
    else:
        print("✓ 論文已存在")

def create_news():
    """創建新聞數據"""
    existing_count = News.query.filter_by(enable=1).count()
    if existing_count == 0:
        news_data = [
            {
                'type': 0, 'date': date(2024, 12, 1),
                'content_zh': '🎉 我實驗室論文被CVPR 2024錄用！',
                'content_en': '🎉 Our lab paper accepted by CVPR 2024!'
            },
            {
                'type': 1, 'date': date(2024, 11, 15),
                'content_zh': '🏆 張教授榮獲國家自然科學獎二等獎',
                'content_en': '🏆 Prof. Zhang awarded National Natural Science Award Second Prize'
            },
            {
                'type': 2, 'date': date(2024, 10, 20),
                'content_zh': '📢 實驗室學術報告：深度學習前沿技術',
                'content_en': '📢 Lab seminar: Frontier Technologies in Deep Learning'
            }
        ]
        
        for news_item in news_data:
            news = News(
                news_type=news_item['type'],
                news_date=news_item['date'],
                news_content_zh=news_item['content_zh'],
                news_content_en=news_item['content_en'],
                enable=1
            )
            db.session.add(news)
        
        print("✓ 創建示例新聞")
    else:
        print("✓ 新聞已存在")

def create_projects():
    """創建項目數據"""
    existing_count = Project.query.filter_by(enable=1).count()
    if existing_count == 0:
        projects_data = [
            {
                'name_zh': '智能視覺監控系統',
                'name_en': 'Intelligent Visual Surveillance System',
                'desc_zh': '基於深度學習的智能監控系統，具備人臉識別、行為分析等功能',
                'desc_en': 'AI-powered surveillance system with face recognition and behavior analysis capabilities',
                'url': 'https://github.com/lab/surveillance-system',
                'start_date': date(2023, 1, 1), 'is_end': 0
            },
            {
                'name_zh': '多模態對話機器人',
                'name_en': 'Multimodal Dialogue Robot',
                'desc_zh': '結合語音、文本、圖像的智能對話系統',
                'desc_en': 'Intelligent dialogue system combining speech, text, and image modalities',
                'url': 'https://github.com/lab/dialogue-robot',
                'start_date': date(2023, 6, 1), 'is_end': 1
            }
        ]
        
        for project_data in projects_data:
            project = Project(
                project_name_zh=project_data['name_zh'],
                project_name_en=project_data['name_en'],
                project_desc_zh=project_data['desc_zh'],
                project_desc_en=project_data['desc_en'],
                project_url=project_data['url'],
                project_date_start=project_data['start_date'],
                is_end=project_data['is_end'],
                enable=1
            )
            db.session.add(project)
        
        print("✓ 創建示例項目")
    else:
        print("✓ 項目已存在")

def init_database():
    """初始化數據庫並創建示例數據"""
    print("🚀 開始初始化數據庫...")
    
    # 首先創建數據庫（如果不存在）
    create_database_if_not_exists()
    
    # 創建 Flask 應用並初始化數據
    app = create_app()
    
    with app.app_context():
        print_env_info(app)
        print("-" * 50)
        
        # 檢查是否需要強制重建
        force_recreate = os.environ.get('FORCE_RECREATE', '0') == '1'
        
        if force_recreate:
            print("⚠️  強制重建模式：將刪除並重新創建所有表")
            # 獲取所有表名並逐個刪除
            try:
                # 禁用外鍵檢查
                db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 0"))
                
                # 獲取所有表名
                tables = db.session.execute(db.text("SHOW TABLES")).fetchall()
                for table in tables:
                    table_name = table[0]
                    db.session.execute(db.text(f"DROP TABLE IF EXISTS `{table_name}`"))
                    print(f"✓ 已刪除表: {table_name}")
                
                # 重新啟用外鍵檢查
                db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1"))
                db.session.commit()
                print("✓ 所有舊表已刪除")
            except Exception as e:
                print(f"⚠️  清理表時發生錯誤: {e}")
                # 如果出錯，嘗試回滾並繼續
                db.session.rollback()
        
        # 創建所有表
        db.create_all()
        print("✓ 數據庫表創建成功")
        
        # 檢查是否已經有數據（檢查管理員表是否有數據）
        existing_admin = Admin.query.first()
        if existing_admin and not force_recreate:
            print("✓ 數據庫已有數據，跳過示例數據創建")
            print(f"  現有管理員: {existing_admin.admin_name}")
            return
        
        print("🔧 開始創建示例數據...")
        # 創建數據
        admin = create_admin_data()
        lab = create_lab_data()
        groups = create_research_groups(lab.lab_id)
        members = create_members(lab.lab_id, groups)
        create_papers(lab.lab_id, groups, members)
        create_news()
        create_projects()
        
        # 提交所有更改
        db.session.commit()
        
        print("-" * 50)
        print("🎊 數據庫初始化完成！")
        print("\n📋 創建的示例數據包括：")
        print("   - 超級管理員: admin/admin123")
        print("   - 1個實驗室")
        print("   - 2個課題組")
        print("   - 3個成員（教師、學生）")
        print("   - 2篇論文")
        print("   - 3條新聞")
        print("   - 2個項目")
        print(f"\n🌟 環境: {get_current_environment()}")
        if force_recreate:
            print("🌟 強制重建完成 - 所有表結構已更新")
        print("🌟 現在可以啟動應用了！")

if __name__ == '__main__':
    init_database()