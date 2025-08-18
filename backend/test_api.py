#!/usr/bin/env python3
"""
測試重置密碼API的簡單腳本
"""
import requests
import json

# 你的實際token和目標管理員ID
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTUyNDU3OCwianRpIjoiNzhlMzNmM2MtMjU4ZS00NjE5LTg3YWYtOWMyOTRjZmVhNzQxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTU1MjQ1NzgsImV4cCI6MTc1NTYxMDk3OCwiYWRtaW5fbmFtZSI6ImFkbWluIiwiaXNfc3VwZXIiOjF9.yBb6ePXhAdAYKcFABviiyB7RVQdY-jf-Wj5sTvyLnEI"
ADMIN_ID = 2

def test_reset_password():
    url = f"http://127.0.0.1:8000/api/admins/{ADMIN_ID}/reset-password"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "X-Language": "zh"
    }
    data = {
        "new_password": "testpassword123"  # 15個字符，確保滿足要求
    }
    
    print(f"測試URL: {url}")
    print(f"請求頭: {headers}")
    print(f"請求數據: {json.dumps(data)}")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"響應狀態碼: {response.status_code}")
        print(f"響應頭: {dict(response.headers)}")
        print(f"響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✓ 密碼重置成功!")
        else:
            print(f"❌ 密碼重置失敗，狀態碼: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 請求失敗: {str(e)}")

def test_get_admins():
    """測試獲取管理員列表，確保API和權限工作正常"""
    url = "http://127.0.0.1:8000/api/admins"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "X-Language": "zh"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"獲取管理員列表響應狀態碼: {response.status_code}")
        if response.status_code == 200:
            print("✓ 能夠正常獲取管理員列表")
        else:
            print(f"❌ 獲取管理員列表失敗: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 請求失敗: {str(e)}")

if __name__ == '__main__':
    print("=== 測試獲取管理員列表（驗證token有效性） ===")
    test_get_admins()
    print("\n=== 測試重置密碼 ===")
    test_reset_password()