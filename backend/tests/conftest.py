"""
pytest 配置文件

為服務層測試和整個測試套件提供配置
"""

import pytest
import sys
import os
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def app():
    """創建測試應用實例"""
    # 在導入之前設置環境變量
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    from app import create_app
    
    app = create_app('testing')
    # Override with SQLite for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    # 重新初始化數據庫
    with app.app_context():
        from app import db
        db.drop_all()
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture  
def client(app):
    """創建測試客戶端"""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """創建數據庫會話"""
    from app import db
    
    with app.app_context():
        yield db.session
        db.session.rollback()

# 測試配置
pytest_plugins = [
    'tests.fixtures.user_fixtures',
    'tests.fixtures.data_fixtures'
]

# 測試標記
def pytest_configure(config):
    """配置 pytest 標記"""
    config.addinivalue_line(
        "markers", "unit: 標記單元測試"
    )
    config.addinivalue_line(
        "markers", "integration: 標記集成測試"
    )
    config.addinivalue_line(
        "markers", "slow: 標記慢速測試"
    )
    config.addinivalue_line(
        "markers", "service: 標記服務層測試"
    )