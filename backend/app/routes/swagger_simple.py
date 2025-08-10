"""
簡化版自動化 Swagger 文檔生成

完全工作的最小化版本，解決所有語法問題
"""

from flask import Blueprint
from flask_restx import Api, Resource, Namespace, fields

# 創建藍圖
bp = Blueprint('swagger_simple', __name__)

# 創建 API 實例
api = Api(
    bp,
    version='2.0',
    title='實驗室網頁框架 API',
    description='基於三層架構的現代化實驗室管理系統 API - 自動化生成',
    doc='/docs',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Token 格式: Bearer <token>'
        }
    }
)

# 創建命名空間
ns_auth = api.namespace('認證', description='管理員認證相關接口', path='/admin')
ns_lab = api.namespace('實驗室', description='實驗室信息管理', path='/lab')
ns_members = api.namespace('成員', description='實驗室成員管理', path='/members')

# 定義基礎模型
login_model = api.model('Login', {
    'admin_name': fields.String(required=True, description='管理員用戶名', example='admin'),
    'admin_pass': fields.String(required=True, description='管理員密碼', example='admin123')
})

success_response = api.model('SuccessResponse', {
    'code': fields.Integer(example=0, description='狀態碼'),
    'message': fields.String(example='OK', description='響應消息'),
    'data': fields.Raw(description='響應數據')
})

# 認證接口
@ns_auth.route('/login')
class AuthLogin(Resource):
    @ns_auth.doc('管理員登錄')
    @ns_auth.expect(login_model)
    @ns_auth.marshal_with(success_response)
    @ns_auth.response(401, '用戶名或密碼錯誤')
    def post(self):
        """管理員登錄接口"""
        return {'code': 0, 'message': '登錄成功', 'data': {}}

@ns_auth.route('/logout')
class AuthLogout(Resource):
    @ns_auth.doc('管理員登出', security='Bearer')
    @ns_auth.response(200, '登出成功')
    @ns_auth.response(401, '未認證')
    def post(self):
        """管理員登出接口"""
        return {'code': 0, 'message': '登出成功'}

# 實驗室接口
@ns_lab.route('/')
class Lab(Resource):
    @ns_lab.doc('獲取實驗室信息')
    @ns_lab.param('all', '獲取全部數據', _in='query', type='string', enum=['true', 'false'])
    @ns_lab.marshal_with(success_response)
    def get(self):
        """獲取實驗室基本信息"""
        return {'code': 0, 'message': 'OK', 'data': {}}
    
    @ns_lab.doc('更新實驗室信息', security='Bearer')
    @ns_lab.response(200, '更新成功')
    @ns_lab.response(401, '未認證')
    def put(self):
        """更新實驗室信息"""
        return {'code': 0, 'message': '更新成功'}

# 成員接口
@ns_members.route('/')
class MemberList(Resource):
    @ns_members.doc('獲取成員列表')
    @ns_members.param('page', '頁碼', type='int', default=1)
    @ns_members.param('per_page', '每頁數量', type='int', default=10)
    @ns_members.param('all', '獲取全部數據', type='string', enum=['true', 'false'])
    @ns_members.marshal_with(success_response)
    def get(self):
        """獲取實驗室成員列表"""
        return {'code': 0, 'message': 'OK', 'data': []}
    
    @ns_members.doc('創建成員', security='Bearer')
    @ns_members.response(201, '創建成功')
    @ns_members.response(401, '未認證')
    def post(self):
        """創建新的實驗室成員"""
        return {'code': 0, 'message': '創建成功'}, 201

print("✅ 簡化版自動化 Swagger 系統已加載")
print("🔗 文檔地址: /api/docs")
print("📋 支持的接口: 認證、實驗室、成員")