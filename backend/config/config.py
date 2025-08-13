import os
from datetime import timedelta

class Config:
    # JWT配置 - 移除硬編碼默認值
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable must be set")
    
    SECRET_KEY = JWT_SECRET_KEY  # Flask-JWT-Extended使用SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # 數據庫配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://lab_web_user:password@localhost/lab_web?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # 文件上傳配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    
    # 允許的文件類型
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'pdf'}
    
    # 分頁配置
    DEFAULT_PER_PAGE = 10
    MAX_PER_PAGE = 100
    
    # 其他配置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 
        'http://localhost:3000,http://127.0.0.1:3000,http://localhost:5000,http://127.0.0.1:5000,http://localhost:8000,http://127.0.0.1:8000,http://localhost:8080,http://127.0.0.1:8080'
    ).split(',') if os.environ.get('CORS_ORIGINS') != '*' else '*'

class DevelopmentConfig(Config):
    DEBUG = True
    # 開發環境允許默認密鑰
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-jwt-secret-please-change-in-production'
    SECRET_KEY = JWT_SECRET_KEY
    
    # 開發環境允許所有CORS來源
    CORS_ORIGINS = '*'
    
class ProductionConfig(Config):
    DEBUG = False
    # 生產環境強制HTTPS
    SSL_REDIRECT = True
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    JWT_SECRET_KEY = 'test-secret-key'
    SECRET_KEY = JWT_SECRET_KEY

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}