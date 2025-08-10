#!/usr/bin/env python3
"""
登入調試腳本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Admin
from app.services import AuthService
from werkzeug.security import generate_password_hash

def debug_login():
    app = create_app('development')
    
    with app.app_context():
        try:
            print("=== 登入調試 ===")
            
            # 檢查數據庫中的管理員
            print("\n1. 檢查數據庫中的管理員:")
            admins = Admin.query.all()
            print(f"   找到 {len(admins)} 個管理員")
            
            for admin in admins:
                print(f"   - ID: {admin.admin_id}, 用戶名: {admin.admin_name}, 啟用: {admin.enable}")
            
            # 檢查是否存在 admin 用戶
            admin_user = Admin.query.filter_by(admin_name='admin').first()
            if not admin_user:
                print("\n2. 創建管理員用戶 admin:")
                # 創建管理員用戶
                admin_user = Admin(
                    admin_name='admin',
                    admin_pass=generate_password_hash('admin123'),
                    admin_email='admin@lab.com',
                    is_super=1,
                    enable=1
                )
                db.session.add(admin_user)
                db.session.commit()
                print("   管理員用戶創建成功")
            else:
                print(f"\n2. 找到管理員用戶: {admin_user.admin_name}")
                print(f"   啟用狀態: {admin_user.enable}")
                print(f"   超級管理員: {admin_user.is_super}")
                
            # 測試登入邏輯
            print("\n3. 測試登入邏輯:")
            auth_service = AuthService()
            
            try:
                login_info = {
                    'ip_address': '127.0.0.1',
                    'user_agent': 'debug-script'
                }
                
                result = auth_service.login('admin', 'admin123', login_info)
                print("   登入成功！")
                print(f"   令牌: {result['access_token'][:50]}...")
                
            except Exception as e:
                print(f"   登入失敗: {e}")
                print(f"   異常類型: {type(e).__name__}")
                import traceback
                traceback.print_exc()
                
        except Exception as e:
            print(f"調試過程中發生錯誤: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    debug_login()