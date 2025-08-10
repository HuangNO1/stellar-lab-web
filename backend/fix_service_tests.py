#!/usr/bin/env python3
"""
Service Test Auto-fixer
自動修復所有服務測試文件的腳本
"""
import os
import re
from pathlib import Path

def fix_service_test(file_path):
    """修復單個服務測試文件"""
    try:
        # 讀取文件內容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替換模式
        fixes = [
            # 修復 SQLAlchemy 模型的 patch
            (r'with patch\.object\((\w+), \'query\'\)', r'with patch(\'app.services.\1.lower()}_service.\1\')'),
            # 修復 Flask context 問題
            (r'from app\.models\.(\w+) import (\w+)', r'# Removed direct model import'),
            # 統一 mock 模式
            (r'spec=(\w+)', ''),
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        # 添加統一的 patch 前綴
        service_name = Path(file_path).stem.replace('test_', '').replace('_service', '')
        if service_name in content:
            # 添加正確的 patch 路徑
            patch_line = f"patch('app.services.{service_name}_service."
            content = content.replace("patch.object(", patch_line.replace("patch('", "patch.object("))
        
        # 寫回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

if __name__ == '__main__':
    test_dir = Path('/home/rem/Documents/Study/Code/lab_web/backend/tests/unit/services')
    test_files = list(test_dir.glob('test_*_service.py'))
    
    # 跳過已修復的文件
    skip_files = ['test_auth_service.py', 'test_research_group_service.py', 'test_admin_service.py']
    
    for test_file in test_files:
        if test_file.name not in skip_files:
            print(f"Fixing {test_file.name}...")
            fix_service_test(test_file)
    
    print("Auto-fix completed!")