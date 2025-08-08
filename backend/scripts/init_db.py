#!/usr/bin/env python3
"""
數據庫初始化腳本
"""

import os
import sys
from datetime import datetime

# 添加項目根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Admin, Lab

def init_database():
    app = create_app()
    
    with app.app_context():
        # 創建所有表
        db.create_all()
        print("✓ 數據庫表創建成功")
        
        # 檢查是否已存在超級管理員
        existing_admin = Admin.query.filter_by(is_super=1, enable=1).first()
        if existing_admin:
            print("✓ 超級管理員已存在")
        else:
            # 創建超級管理員
            super_admin = Admin(
                admin_name='admin',
                is_super=1,
                enable=1
            )
            super_admin.set_password('admin123')
            
            db.session.add(super_admin)
            print("✓ 創建超級管理員 (用戶名: admin, 密碼: admin123)")
        
        # 檢查是否已存在實驗室信息
        existing_lab = Lab.query.filter_by(enable=1).first()
        if existing_lab:
            print("✓ 實驗室信息已存在")
        else:
            # 創建默認實驗室信息
            default_lab = Lab(
                lab_zh='示例實驗室',
                lab_en='Example Laboratory',
                lab_desc_zh='這是一個示例實驗室，請在管理後台修改相關信息。',
                lab_desc_en='This is an example laboratory. Please modify the information in the admin panel.',
                lab_address_zh='請填寫實驗室地址',
                lab_address_en='Please fill in the laboratory address',
                lab_email='lab@example.com',
                lab_phone='請填寫聯繫電話',
                enable=1
            )
            
            db.session.add(default_lab)
            print("✓ 創建默認實驗室信息")
        
        # 提交更改
        db.session.commit()
        print("✓ 數據庫初始化完成")

if __name__ == '__main__':
    init_database()