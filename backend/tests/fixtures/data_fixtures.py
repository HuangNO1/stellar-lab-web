"""
測試數據 fixtures

提供測試所需的模擬數據
"""

import pytest
from datetime import datetime


@pytest.fixture
def sample_lab_data():
    """實驗室測試數據"""
    return {
        'lab_id': 1,
        'lab_zh': '智能計算實驗室',
        'lab_en': 'Intelligent Computing Laboratory',
        'lab_desc_zh': '專注於人工智能、機器學習和計算機視覺領域的研究',
        'lab_desc_en': 'Focus on AI, machine learning and computer vision research',
        'lab_address_zh': '北京市海淀區清華大學FIT樓',
        'lab_address_en': 'FIT Building, Tsinghua University, Beijing',
        'lab_email': 'contact@lab.edu.cn',
        'lab_phone': '+86-10-62785678'
    }


@pytest.fixture
def sample_member_data():
    """成員測試數據"""
    return {
        'mem_id': 1,
        'mem_name_zh': '張教授',
        'mem_name_en': 'Prof. Zhang',
        'mem_email': 'zhang@lab.edu.cn',
        'mem_type': 0,  # 0=教師
        'job_type': 0,  # 0=教授
        'research_group_id': 1,
        'mem_desc_zh': '人工智能專家',
        'mem_desc_en': 'AI Expert',
        'enable': 1
    }


@pytest.fixture  
def sample_paper_data():
    """論文測試數據"""
    return {
        'paper_id': 1,
        'paper_title_zh': '基於深度學習的圖像識別研究',
        'paper_title_en': 'Deep Learning Based Image Recognition Research',
        'paper_desc_zh': '本文提出了一種新的深度學習方法',
        'paper_desc_en': 'This paper proposes a novel deep learning approach',
        'paper_venue': 'CVPR 2024',
        'paper_type': 1,  # 期刊
        'paper_accept': 1,  # 已接收
        'paper_date': datetime(2024, 6, 15).date(),
        'paper_url': 'https://arxiv.org/abs/2024.12345'
    }


@pytest.fixture
def sample_admin_data():
    """管理員測試數據"""
    return {
        'admin_id': 1,
        'admin_name': 'testadmin',
        'admin_pass': 'hashed_password',
        'is_super': 1,
        'enable': 1,
        'created_at': datetime.utcnow()
    }


@pytest.fixture
def sample_research_group_data():
    """課題組測試數據"""
    return {
        'research_group_id': 1,
        'research_group_name_zh': '人工智能研究組',
        'research_group_name_en': 'AI Research Group',
        'research_group_desc_zh': '專注於機器學習和深度學習',
        'research_group_desc_en': 'Focus on ML and DL research',
        'mem_id': 1,  # 組長ID
        'lab_id': 1,
        'enable': 1
    }


@pytest.fixture
def sample_news_data():
    """新聞測試數據"""
    return {
        'news_id': 1,
        'news_type': 0,  # 論文發表
        'news_content_zh': '我實驗室論文被CVPR 2024錄用',
        'news_content_en': 'Our paper accepted by CVPR 2024',
        'news_date': datetime(2024, 6, 15).date(),
        'enable': 1
    }


@pytest.fixture
def sample_project_data():
    """項目測試數據"""
    return {
        'project_id': 1,
        'project_name_zh': '智能交通管理系統',
        'project_name_en': 'Intelligent Traffic Management System',
        'project_desc_zh': '基於AI的交通信號優化',
        'project_desc_en': 'AI-based traffic signal optimization',
        'project_url': 'https://github.com/lab/traffic-system',
        'project_date_start': datetime(2024, 1, 1).date(),
        'is_end': 0,  # 進行中
        'enable': 1
    }