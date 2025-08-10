#!/usr/bin/env python3
"""
單獨測試auth_service的execute_with_audit
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Admin
from app.services.auth_service import AuthService
from datetime import datetime

def test_auth_service_audit():
    app = create_app('development')
    
    with app.app_context():
        try:
            print("=== 測試AuthService的execute_with_audit ===")
            
            # 找到admin用戶
            admin = Admin.query.filter_by(admin_name='admin').first()
            if not admin:
                print("找不到admin用戶")
                return
            
            print(f"找到用戶: {admin.admin_name}")
            
            # 創建auth_service
            auth_service = AuthService()
            print("AuthService創建成功")
            
            # 測試execute_with_audit
            def test_operation():
                return {"test": "data"}
            
            print("開始測試execute_with_audit...")
            result = auth_service.execute_with_audit(
                operation_func=test_operation,
                operation_type='LOGIN',
                content={'test_field': 'test_value'},
                admin_id=admin.admin_id
            )
            
            print(f"execute_with_audit 成功返回: {result}")
            
        except Exception as e:
            print(f"錯誤: {e}")
            print(f"異常類型: {type(e).__name__}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_auth_service_audit()