from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.config import config
from app.utils.security import SecurityFilter, generate_nonce
import os
import logging

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per hour", "100 per minute"],
    storage_uri="memory://"
)

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 配置日誌安全過濾器
    if not app.debug:
        security_filter = SecurityFilter()
        for handler in app.logger.handlers:
            handler.addFilter(security_filter)
    
    # 初始化擴展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    )
    
    # 添加安全響應頭
    @app.after_request
    def set_security_headers(response):
        # CSP with nonce
        nonce = generate_nonce()
        g.csp_nonce = nonce
        
        csp_policy = (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}'; "
            f"style-src 'self' 'unsafe-inline'; "
            f"img-src 'self' data: https:; "
            f"font-src 'self' https:; "
            f"connect-src 'self'; "
            f"frame-ancestors 'none'; "
            f"base-uri 'self'"
        )
        
        response.headers['Content-Security-Policy'] = csp_policy
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # HTTPS安全頭（僅在生產環境）
        if not app.debug and request.is_secure:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # 移除服務器信息
        response.headers.pop('Server', None)
        
        return response
    
    # 添加輸入清理中間件
    @app.before_request
    def sanitize_request_data():
        if request.is_json and request.json:
            from app.utils.security import sanitize_input
            # 清理JSON數據
            request._cached_json = sanitize_input(request.json)
    
    # 註冊根路由
    from app.routes.root import bp as root_bp
    app.register_blueprint(root_bp)
    
    # 註冊API藍圖
    from app.routes.auth import bp as auth_bp
    from app.routes.admin import bp as admin_bp
    from app.routes.lab import bp as lab_bp
    from app.routes.research_group import bp as research_group_bp
    from app.routes.member import bp as member_bp
    from app.routes.paper import bp as paper_bp
    from app.routes.news import bp as news_bp
    from app.routes.project import bp as project_bp
    from app.routes.media import bp as media_bp
    from app.routes.edit_record import bp as edit_record_bp
    # 舊的手工維護 Swagger 系統（1600+ 行代碼）
    # from app.routes.swagger_docs import bp as swagger_bp
    
    # 新的完整版自動化 Swagger 系統（包含所有48+接口）
    from app.routes.swagger_complete import bp as swagger_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(lab_bp, url_prefix='/api')
    app.register_blueprint(research_group_bp, url_prefix='/api')
    app.register_blueprint(member_bp, url_prefix='/api')
    app.register_blueprint(paper_bp, url_prefix='/api')
    app.register_blueprint(news_bp, url_prefix='/api')
    app.register_blueprint(project_bp, url_prefix='/api')
    app.register_blueprint(media_bp, url_prefix='/api')
    app.register_blueprint(edit_record_bp, url_prefix='/api')
    app.register_blueprint(swagger_bp, url_prefix='/api')
    
    # 創建表
    with app.app_context():
        db.create_all()
    
    return app