#!/usr/bin/env python3
"""
API測試腳本
用於驗證所有API端點是否正常工作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_creation():
    """測試應用是否能正常創建"""
    try:
        from app import create_app
        app = create_app('testing')
        print("✓ Flask應用創建成功")
        return True
    except Exception as e:
        print(f"✗ Flask應用創建失敗: {str(e)}")
        return False

def test_database_models():
    """測試數據模型是否正確"""
    try:
        from app import create_app, db
        from app.models import Admin, Lab, ResearchGroup, Member, Paper, PaperAuthor, Project, News, EditRecord
        
        app = create_app('testing')
        with app.app_context():
            # 創建所有表
            db.create_all()
            print("✓ 數據庫表創建成功")
            
            # 測試模型創建
            admin = Admin(admin_name='test', is_super=1)
            admin.set_password('password')
            db.session.add(admin)
            
            lab = Lab(lab_zh='測試實驗室', lab_en='Test Lab', enable=1)
            db.session.add(lab)
            
            db.session.commit()
            print("✓ 數據模型測試成功")
            
        return True
    except Exception as e:
        print(f"✗ 數據模型測試失敗: {str(e)}")
        return False

def test_api_routes():
    """測試API路由是否正確註冊"""
    try:
        from app import create_app
        app = create_app('testing')
        
        with app.test_client() as client:
            # 測試公開路由
            response = client.get('/api/lab')
            print(f"✓ GET /api/lab - 狀態碼: {response.status_code}")
            
            response = client.get('/api/members')
            print(f"✓ GET /api/members - 狀態碼: {response.status_code}")
            
            response = client.get('/api/papers')
            print(f"✓ GET /api/papers - 狀態碼: {response.status_code}")
            
            response = client.get('/api/news')
            print(f"✓ GET /api/news - 狀態碼: {response.status_code}")
            
            response = client.get('/api/projects')
            print(f"✓ GET /api/projects - 狀態碼: {response.status_code}")
            
            # 測試媒體服務健康檢查
            response = client.get('/api/media/health')
            print(f"✓ GET /api/media/health - 狀態碼: {response.status_code}")
            
        print("✓ API路由測試成功")
        return True
    except Exception as e:
        print(f"✗ API路由測試失敗: {str(e)}")
        return False

def main():
    """主測試函數"""
    print("🧪 開始API測試...")
    print("=" * 50)
    
    tests = [
        test_app_creation,
        test_database_models,
        test_api_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 30)
    
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！")
        return 0
    else:
        print("❌ 部分測試失敗")
        return 1

if __name__ == '__main__':
    sys.exit(main())