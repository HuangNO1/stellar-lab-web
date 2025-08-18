#!/usr/bin/env python3
"""
調試重置密碼功能的腳本
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Admin
from app.services import AdminService
from app.utils import messages as msg

def test_reset_password():
    app = create_app('default')
    
    with app.app_context():
        # 查詢管理員
        super_admin = Admin.query.filter_by(is_super=1).first()
        normal_admin = Admin.query.filter_by(is_super=0).first()
        
        if not super_admin:
            print("❌ 找不到超級管理員")
            return
            
        if not normal_admin:
            print("❌ 找不到普通管理員")
            return
            
        print(f"✓ 找到超級管理員: {super_admin.admin_name} (ID: {super_admin.admin_id})")
        print(f"✓ 找到普通管理員: {normal_admin.admin_name} (ID: {normal_admin.admin_id})")
        
        # 測試重置密碼
        admin_service = AdminService()
        
        try:
            # 設置當前管理員為超級管理員
            from flask import g
            g.current_admin = super_admin
            
            result = admin_service.reset_admin_password(
                admin_id=normal_admin.admin_id,
                new_password="testpassword123",
                current_admin_id=super_admin.admin_id
            )
            
            print(f"✓ 密碼重置成功: {result}")
            
            # 測試新密碼是否有效
            db.session.refresh(normal_admin)
            if normal_admin.check_password("testpassword123"):
                print("✓ 新密碼驗證成功")
            else:
                print("❌ 新密碼驗證失敗")
                
        except Exception as e:
            print(f"❌ 重置密碼失敗: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_reset_password()