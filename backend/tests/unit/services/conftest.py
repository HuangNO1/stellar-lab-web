"""
Service layer tests configuration
確保 PyCharm 能正確運行 services 目錄下的測試
"""

import pytest
import sys
import os
from pathlib import Path

# 確保項目根目錄在 Python 路徑中
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 導入全局 conftest.py 的 fixtures
pytest_plugins = ["tests.conftest"]

# 設置測試環境變量
os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """自動設置測試環境"""
    # 確保在測試會話開始時設置環境
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    yield