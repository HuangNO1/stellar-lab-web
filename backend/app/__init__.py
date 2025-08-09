from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.config import config
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化擴展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    )
    
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
    from app.routes.swagger_docs import bp as swagger_bp
    
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