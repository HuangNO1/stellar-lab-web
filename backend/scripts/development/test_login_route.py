#!/usr/bin/env python3
"""
直接測試登入路由
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import json

def test_login_route():
    app = create_app('development')
    
    with app.test_client() as client:
        try:
            print("=== 測試登入路由 ===")
            
            # 準備登入數據
            login_data = {
                'admin_name': 'admin',
                'admin_pass': 'admin123'
            }
            
            # 發送POST請求
            response = client.post(
                '/api/admin/login',
                data=json.dumps(login_data),
                content_type='application/json'
            )
            
            print(f"狀態碼: {response.status_code}")
            print(f"響應: {response.get_json()}")
            
            if response.status_code == 200:
                print("登入成功！")
            else:
                print("登入失敗")
                
        except Exception as e:
            print(f"錯誤: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_login_route()