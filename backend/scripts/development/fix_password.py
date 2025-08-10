#!/usr/bin/env python3
"""
檢查密碼哈希
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Admin
from werkzeug.security import generate_password_hash, check_password_hash

def check_password_hash_issue():
    app = create_app('development')
    
    with app.app_context():
        try:
            admin = Admin.query.filter_by(admin_name='admin').first()
            if admin:
                print(f"管理員密碼哈希值: '{admin.admin_pass}'")
                print(f"密碼哈希長度: {len(admin.admin_pass)}")
                print(f"密碼哈希是否為空: {admin.admin_pass == ''}")
                
                # 生成正確的密碼哈希
                correct_hash = generate_password_hash('admin123')
                print(f"正確的哈希格式: {correct_hash}")
                
                # 更新管理員密碼
                print("更新管理員密碼...")
                admin.admin_pass = correct_hash
                db.session.commit()
                print("密碼更新成功！")
                
                # 測試新密碼
                if check_password_hash(admin.admin_pass, 'admin123'):
                    print("密碼驗證成功！")
                else:
                    print("密碼驗證失敗！")
            else:
                print("找不到admin用戶")
                
        except Exception as e:
            print(f"錯誤: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    check_password_hash_issue()