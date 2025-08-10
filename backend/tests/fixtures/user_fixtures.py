"""
用戶和認證相關的測試 fixtures
"""

import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token


@pytest.fixture
def mock_admin_user():
    """模擬管理員用戶"""
    admin = Mock()
    admin.admin_id = 1
    admin.admin_name = 'testadmin'
    admin.is_super = 1
    admin.enable = 1
    admin.created_at = datetime.utcnow()
    admin.last_login = datetime.utcnow()
    return admin


@pytest.fixture
def mock_regular_admin():
    """模擬普通管理員"""
    admin = Mock()
    admin.admin_id = 2
    admin.admin_name = 'regularadmin'
    admin.is_super = 0
    admin.enable = 1
    admin.created_at = datetime.utcnow()
    admin.last_login = datetime.utcnow()
    return admin


@pytest.fixture
def mock_disabled_admin():
    """模擬禁用的管理員"""
    admin = Mock()
    admin.admin_id = 3
    admin.admin_name = 'disabledadmin'
    admin.is_super = 0
    admin.enable = 0
    admin.created_at = datetime.utcnow()
    admin.last_login = None
    return admin


@pytest.fixture
def valid_login_data():
    """有效的登錄數據"""
    return {
        'admin_name': 'testadmin',
        'admin_pass': 'testpass123'
    }


@pytest.fixture
def invalid_login_data():
    """無效的登錄數據"""
    return {
        'admin_name': 'wronguser',
        'admin_pass': 'wrongpass'
    }


@pytest.fixture
def access_token(app, mock_admin_user):
    """生成有效的訪問令牌"""
    with app.app_context():
        token = create_access_token(
            identity=mock_admin_user.admin_id,
            expires_delta=timedelta(hours=24),
            additional_claims={
                'admin_name': mock_admin_user.admin_name,
                'is_super': mock_admin_user.is_super
            }
        )
        return token


@pytest.fixture
def expired_token(app, mock_admin_user):
    """生成過期的令牌"""
    with app.app_context():
        token = create_access_token(
            identity=mock_admin_user.admin_id,
            expires_delta=timedelta(seconds=-1),  # 已過期
            additional_claims={
                'admin_name': mock_admin_user.admin_name,
                'is_super': mock_admin_user.is_super
            }
        )
        return token


@pytest.fixture
def auth_headers(access_token):
    """認證請求頭"""
    return {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def super_admin_headers(app):
    """超級管理員請求頭"""
    with app.app_context():
        token = create_access_token(
            identity=1,
            additional_claims={
                'admin_name': 'superadmin', 
                'is_super': 1
            }
        )
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }


@pytest.fixture
def regular_admin_headers(app):
    """普通管理員請求頭"""
    with app.app_context():
        token = create_access_token(
            identity=2,
            additional_claims={
                'admin_name': 'regularadmin',
                'is_super': 0
            }
        )
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }


@pytest.fixture
def change_password_data():
    """修改密碼數據"""
    return {
        'old_password': 'oldpass123',
        'new_password': 'newpass456'
    }