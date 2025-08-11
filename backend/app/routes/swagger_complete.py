"""
完整版自动化 Swagger 文档生成系统
包含所有 48+ API 接口的完整文档
基于 Flask-RESTX 的现代化自动生成系统
"""

from flask import Blueprint
from flask_restx import Api, Resource, Namespace, fields

# 创建蓝图
bp = Blueprint('swagger_complete', __name__)

# 创建 API 实例
api = Api(
    bp,
    version='2.0',
    title='实验室网页框架 API - 完整版',
    description='''
## 实验室通用网页框架后端 API

基于**三层架构** (Routes → Services → Models) 的现代化实验室管理系统

### 🏗️ 架构特色
- **服务层封装**: 统一业务逻辑处理
- **自动审计记录**: 所有操作自动记录
- **统一异常处理**: 标准化错误响应
- **完整权限控制**: JWT Token + 角色权限

### 🔑 认证方式
1. 使用 `POST /api/admin/login` 获取 JWT Token
2. 在请求头中添加: `Authorization: Bearer <token>`
3. Token 有效期为 24 小时

### 📊 响应格式
**成功响应**:
```json
{
  "code": 0,
  "message": "OK",
  "data": { ... }
}
```

**分页响应**:
```json
{
  "code": 0, 
  "message": "OK",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "per_page": 10,
    "pages": 10
  }
}
```

### 🔐 默认管理员
- **用户名**: admin  
- **密码**: admin123

### 📈 查询参数
- `page`: 页码 (默认: 1)
- `per_page`: 每页数量 (默认: 10)  
- `all=true`: 获取全部数据，无分页限制
- `q`: 搜索关键词
    ''',
    doc='/docs',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header', 
            'name': 'Authorization',
            'description': 'JWT Token 格式: Bearer <your_token_here>'
        }
    },
    security='Bearer'
)

# ==================== 数据模型定义 ====================

# 基础响应模型
base_response = api.model('BaseResponse', {
    'code': fields.Integer(description='状态码', example=0),
    'message': fields.String(description='响应消息', example='OK'),
    'data': fields.Raw(description='响应数据')
})

# 分页响应模型
pagination_response = api.model('PaginationResponse', {
    'code': fields.Integer(description='状态码', example=0),
    'message': fields.String(description='响应消息', example='OK'),
    'data': fields.Nested(api.model('PaginationData', {
        'items': fields.List(fields.Raw, description='数据列表'),
        'total': fields.Integer(description='总数量', example=100),
        'page': fields.Integer(description='当前页码', example=1),
        'per_page': fields.Integer(description='每页数量', example=10),
        'pages': fields.Integer(description='总页数', example=10),
        'has_prev': fields.Boolean(description='是否有上一页'),
        'has_next': fields.Boolean(description='是否有下一页')
    }))
})

# 登录模型
login_model = api.model('LoginRequest', {
    'admin_name': fields.String(required=True, description='管理员用户名', example='admin'),
    'admin_pass': fields.String(required=True, description='管理员密码', example='admin123')
})

# 实验室模型
lab_model = api.model('Lab', {
    'lab_zh': fields.String(description='实验室中文名', example='人工智能实验室'),
    'lab_en': fields.String(description='实验室英文名', example='AI Laboratory'),
    'lab_desc_zh': fields.String(description='实验室中文描述'),
    'lab_desc_en': fields.String(description='实验室英文描述'),
    'lab_address_zh': fields.String(description='实验室中文地址'),
    'lab_address_en': fields.String(description='实验室英文地址'),
    'lab_email': fields.String(description='联系邮箱', example='lab@university.edu'),
    'lab_phone': fields.String(description='联系电话', example='+86-10-12345678')
})

# 课题组模型
research_group_model = api.model('ResearchGroup', {
    'research_group_name_zh': fields.String(required=True, description='课题组中文名'),
    'research_group_name_en': fields.String(description='课题组英文名'),
    'research_group_desc_zh': fields.String(description='课题组中文描述'),
    'research_group_desc_en': fields.String(description='课题组英文描述'),
    'lab_id': fields.Integer(description='所属实验室ID')
})

# 成员模型
member_model = api.model('Member', {
    'member_name_zh': fields.String(required=True, description='成员中文姓名'),
    'member_name_en': fields.String(description='成员英文姓名'),
    'member_desc_zh': fields.String(description='成员中文描述'),
    'member_desc_en': fields.String(description='成员英文描述'),
    'member_type': fields.String(description='成员类型', example='teacher'),
    'lab_id': fields.Integer(description='所属实验室ID'),
    'research_group_id': fields.Integer(description='所属课题组ID')
})

# 论文模型
paper_model = api.model('Paper', {
    'paper_title': fields.String(required=True, description='论文标题'),
    'paper_authors': fields.String(description='论文作者'),
    'paper_journal': fields.String(description='期刊名称'),
    'paper_year': fields.String(description='发表年份'),
    'paper_link': fields.String(description='论文链接'),
    'paper_abstract': fields.String(description='论文摘要'),
    'lab_id': fields.Integer(description='所属实验室ID')
})

# 新闻模型
news_model = api.model('News', {
    'news_title_zh': fields.String(required=True, description='新闻中文标题'),
    'news_title_en': fields.String(description='新闻英文标题'),
    'news_content_zh': fields.String(description='新闻中文内容'),
    'news_content_en': fields.String(description='新闻英文内容'),
    'news_date': fields.String(description='新闻日期', example='2024-01-01')
})

# 项目模型
project_model = api.model('Project', {
    'project_name_zh': fields.String(required=True, description='项目中文名称'),
    'project_name_en': fields.String(description='项目英文名称'),
    'project_desc_zh': fields.String(description='项目中文描述'),
    'project_desc_en': fields.String(description='项目英文描述'),
    'project_url': fields.String(description='项目链接'),
    'project_date_start': fields.String(description='项目开始日期'),
    'is_end': fields.Integer(description='项目状态', example=0)
})

# 管理员模型
admin_model = api.model('Admin', {
    'admin_name': fields.String(required=True, description='管理员用户名'),
    'admin_pass': fields.String(description='管理员密码'),
    'admin_email': fields.String(description='管理员邮箱'),
    'admin_type': fields.Integer(description='管理员类型', example=1)
})

# ==================== 命名空间定义 ====================

ns_auth = api.namespace('认证管理', description='管理员认证相关接口', path='/admin')
ns_admin = api.namespace('管理员管理', description='管理员账户管理', path='/admins')
ns_lab = api.namespace('实验室管理', description='实验室信息管理', path='/lab')
ns_research_group = api.namespace('课题组管理', description='课题组管理', path='/research-groups')
ns_member = api.namespace('成员管理', description='实验室成员管理', path='/members')
ns_paper = api.namespace('论文管理', description='论文发表管理', path='/papers')
ns_news = api.namespace('新闻管理', description='实验室新闻管理', path='/news')
ns_project = api.namespace('项目管理', description='研究项目管理', path='/projects')
ns_media = api.namespace('媒体管理', description='文件上传管理', path='/media')
ns_edit_record = api.namespace('操作审计', description='编辑记录查询', path='/edit-records')
ns_system = api.namespace('系统接口', description='健康检查等系统接口', path='/')

# ==================== 认证管理接口 ====================

@ns_auth.route('/login')
class AuthLogin(Resource):
    @ns_auth.doc('管理员登录')
    @ns_auth.expect(login_model, validate=True)
    @ns_auth.marshal_with(base_response)
    @ns_auth.response(401, '用户名或密码错误')
    @ns_auth.response(500, '服务器内部错误')
    def post(self):
        """
        管理员登录
        
        **请求示例**:
        ```json
        {
          "admin_name": "admin",
          "admin_pass": "admin123"
        }
        ```
        
        **成功响应**:
        ```json
        {
          "code": 0,
          "message": "登录成功",
          "data": {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "admin": {
              "admin_id": 1,
              "admin_name": "admin",
              "admin_type": 2
            }
          }
        }
        ```
        """
        pass

@ns_auth.route('/logout')
class AuthLogout(Resource):
    @ns_auth.doc('管理员登出', security='Bearer')
    @ns_auth.marshal_with(base_response)
    @ns_auth.response(401, '未认证或Token无效')
    def post(self):
        """管理员登出，使Token失效"""
        pass

@ns_auth.route('/change-password')
class AuthChangePassword(Resource):
    @ns_auth.doc('修改密码', security='Bearer')
    @ns_auth.expect(api.model('ChangePasswordRequest', {
        'old_password': fields.String(required=True, description='旧密码'),
        'new_password': fields.String(required=True, description='新密码')
    }), validate=True)
    @ns_auth.marshal_with(base_response)
    @ns_auth.response(401, '未认证或旧密码错误')
    def post(self):
        """修改管理员密码"""
        pass

@ns_auth.route('/profile')
class AuthProfile(Resource):
    @ns_auth.doc('获取个人信息', security='Bearer')
    @ns_auth.marshal_with(base_response)
    @ns_auth.response(401, '未认证')
    def get(self):
        """获取当前登录管理员的个人信息"""
        pass
    
    @ns_auth.doc('更新个人信息', security='Bearer')
    @ns_auth.expect(api.model('ProfileUpdateRequest', {
        'admin_name': fields.String(description='管理员用户名（必须唯一）', example='super_admin')
    }))
    @ns_auth.marshal_with(base_response)
    @ns_auth.response(401, '未认证')
    @ns_auth.response(400, '用户名已存在或参数错误')
    def put(self):
        """更新当前登录管理员的个人信息
        
        功能说明：
        - 管理员只能修改自己的个人资料
        - 用户名必须唯一，不能与现有管理员重复
        - 修改后的用户名会立即生效，新的JWT token将包含更新后的用户名
        - 所有修改操作都会自动记录到操作日志中
        
        当前支持的可更新字段：
        - admin_name: 管理员用户名
        """
        pass

# ==================== 管理员管理接口 ====================

@ns_admin.route('/')
class AdminList(Resource):
    @ns_admin.doc('获取管理员列表', security='Bearer')
    @ns_admin.param('page', '页码', type='int', default=1)
    @ns_admin.param('per_page', '每页数量', type='int', default=10)
    @ns_admin.param('all', '获取全部数据', type='string', enum=['true', 'false'])
    @ns_admin.param('q', '搜索关键词（用户名、邮箱）', type='string')
    @ns_admin.marshal_with(pagination_response)
    @ns_admin.response(401, '未认证')
    @ns_admin.response(403, '权限不足，需要超级管理员权限')
    def get(self):
        """获取管理员列表（分页查询）"""
        pass
    
    @ns_admin.doc('创建管理员', security='Bearer')
    @ns_admin.expect(admin_model, validate=True)
    @ns_admin.marshal_with(base_response)
    @ns_admin.response(401, '未认证')
    @ns_admin.response(403, '权限不足')
    @ns_admin.response(409, '用户名已存在')
    def post(self):
        """创建新管理员（仅超级管理员）"""
        pass

@ns_admin.route('/<int:admin_id>')
class Admin(Resource):
    @ns_admin.doc('更新管理员信息', security='Bearer')
    @ns_admin.expect(admin_model)
    @ns_admin.marshal_with(base_response)
    @ns_admin.response(401, '未认证')
    @ns_admin.response(403, '权限不足')
    @ns_admin.response(404, '管理员不存在')
    def put(self, admin_id):
        """更新管理员信息"""
        pass
    
    @ns_admin.doc('删除管理员', security='Bearer')
    @ns_admin.marshal_with(base_response)
    @ns_admin.response(401, '未认证')
    @ns_admin.response(403, '权限不足')
    @ns_admin.response(404, '管理员不存在')
    @ns_admin.response(409, '不能删除自己或超级管理员')
    def delete(self, admin_id):
        """删除管理员（软删除）"""
        pass

# ==================== 实验室管理接口 ====================

@ns_lab.route('/')
class Lab(Resource):
    @ns_lab.doc('获取实验室信息')
    @ns_lab.marshal_with(base_response)
    def get(self):
        """
        获取实验室基本信息
        
        包含实验室名称、描述、联系方式、Logo和轮播图片等信息
        """
        pass
    
    @ns_lab.doc('更新实验室信息', security='Bearer')
    @ns_lab.expect(lab_model)
    @ns_lab.marshal_with(base_response)
    @ns_lab.response(401, '未认证')
    @ns_lab.response(403, '权限不足')
    def put(self):
        """
        更新实验室信息
        
        支持文件上传：
        - lab_logo: 实验室Logo图片
        - carousel_img_1 到 carousel_img_4: 轮播图片
        """
        pass
    
    @ns_lab.doc('删除实验室', security='Bearer')
    @ns_lab.marshal_with(base_response)
    @ns_lab.response(401, '未认证')
    @ns_lab.response(403, '权限不足')
    @ns_lab.response(409, '存在关联数据，无法删除')
    def delete(self):
        """删除实验室信息（软删除）"""
        pass

# ==================== 课题组管理接口 ====================

@ns_research_group.route('/')
class ResearchGroupList(Resource):
    @ns_research_group.doc('获取课题组列表')
    @ns_research_group.param('page', '页码', type='int', default=1)
    @ns_research_group.param('per_page', '每页数量', type='int', default=10)
    @ns_research_group.param('all', '获取全部数据', type='string', enum=['true', 'false'])
    @ns_research_group.param('q', '搜索关键词（课题组名称、描述）', type='string')
    @ns_research_group.param('lab_id', '实验室ID过滤', type='int')
    @ns_research_group.param('show_all', '显示所有状态', type='string', enum=['true', 'false'])
    @ns_research_group.marshal_with(pagination_response)
    def get(self):
        """获取课题组列表（支持分页和搜索）"""
        pass
    
    @ns_research_group.doc('创建课题组', security='Bearer')
    @ns_research_group.expect(research_group_model, validate=True)
    @ns_research_group.marshal_with(base_response)
    @ns_research_group.response(401, '未认证')
    @ns_research_group.response(403, '权限不足')
    def post(self):
        """创建新的课题组"""
        pass

@ns_research_group.route('/<int:group_id>')
class ResearchGroup(Resource):
    @ns_research_group.doc('获取课题组详情')
    @ns_research_group.marshal_with(base_response)
    @ns_research_group.response(404, '课题组不存在')
    def get(self, group_id):
        """获取指定课题组的详细信息"""
        pass
    
    @ns_research_group.doc('更新课题组', security='Bearer')
    @ns_research_group.expect(research_group_model)
    @ns_research_group.marshal_with(base_response)
    @ns_research_group.response(401, '未认证')
    @ns_research_group.response(403, '权限不足')
    @ns_research_group.response(404, '课题组不存在')
    def put(self, group_id):
        """更新课题组信息"""
        pass
    
    @ns_research_group.doc('删除课题组', security='Bearer')
    @ns_research_group.marshal_with(base_response)
    @ns_research_group.response(401, '未认证')
    @ns_research_group.response(403, '权限不足')
    @ns_research_group.response(404, '课题组不存在')
    @ns_research_group.response(409, '存在关联成员，无法删除')
    def delete(self, group_id):
        """删除课题组（软删除）"""
        pass

# ==================== 成员管理接口 ====================

@ns_member.route('/')
class MemberList(Resource):
    @ns_member.doc('获取成员列表')
    @ns_member.param('page', '页码', type='int', default=1)
    @ns_member.param('per_page', '每页数量', type='int', default=10)
    @ns_member.param('all', '获取全部数据', type='string', enum=['true', 'false'])
    @ns_member.param('q', '搜索关键词（成员姓名、描述）', type='string')
    @ns_member.param('lab_id', '实验室ID过滤', type='int')
    @ns_member.param('research_group_id', '课题组ID过滤', type='int')
    @ns_member.param('member_type', '成员类型过滤', type='string', enum=['teacher', 'student'])
    @ns_member.param('show_all', '显示所有状态', type='string', enum=['true', 'false'])
    @ns_member.marshal_with(pagination_response)
    def get(self):
        """获取成员列表（支持多维度过滤和搜索）"""
        pass
    
    @ns_member.doc('创建成员', security='Bearer')
    @ns_member.expect(member_model, validate=True)
    @ns_member.marshal_with(base_response)
    @ns_member.response(401, '未认证')
    @ns_member.response(403, '权限不足')
    def post(self):
        """
        创建新成员
        
        支持头像上传：
        - member_avatar: 成员头像图片文件
        """
        pass

@ns_member.route('/<int:member_id>')
class Member(Resource):
    @ns_member.doc('获取成员详情')
    @ns_member.marshal_with(base_response)
    @ns_member.response(404, '成员不存在')
    def get(self, member_id):
        """获取指定成员的详细信息"""
        pass
    
    @ns_member.doc('更新成员', security='Bearer')
    @ns_member.expect(member_model)
    @ns_member.marshal_with(base_response)
    @ns_member.response(401, '未认证')
    @ns_member.response(403, '权限不足')
    @ns_member.response(404, '成员不存在')
    def put(self, member_id):
        """更新成员信息"""
        pass
    
    @ns_member.doc('删除成员', security='Bearer')
    @ns_member.marshal_with(base_response)
    @ns_member.response(401, '未认证')
    @ns_member.response(403, '权限不足')
    @ns_member.response(404, '成员不存在')
    def delete(self, member_id):
        """删除成员（软删除）"""
        pass

@ns_member.route('/batch')
class MemberBatch(Resource):
    @ns_member.doc('批量删除成员', security='Bearer')
    @ns_member.expect(api.model('BatchDeleteRequest', {
        'member_ids': fields.List(fields.Integer, required=True, description='成员ID列表', example=[1, 2, 3])
    }), validate=True)
    @ns_member.marshal_with(base_response)
    @ns_member.response(401, '未认证')
    @ns_member.response(403, '权限不足')
    def delete(self):
        """批量删除成员"""
        pass
    
    @ns_member.doc('批量更新成员', security='Bearer')
    @ns_member.expect(api.model('BatchUpdateRequest', {
        'member_ids': fields.List(fields.Integer, required=True, description='成员ID列表'),
        'updates': fields.Raw(required=True, description='更新数据')
    }), validate=True)
    @ns_member.marshal_with(base_response)
    @ns_member.response(401, '未认证')
    @ns_member.response(403, '权限不足')
    def put(self):
        """批量更新成员信息"""
        pass

# ==================== 论文管理接口 ====================

@ns_paper.route('/')
class PaperList(Resource):
    @ns_paper.doc('获取论文列表')
    @ns_paper.param('page', '页码', type='int', default=1)
    @ns_paper.param('per_page', '每页数量', type='int', default=10)
    @ns_paper.param('all', '获取全部数据', type='string', enum=['true', 'false'])
    @ns_paper.param('q', '搜索关键词（论文标题、作者、期刊）', type='string')
    @ns_paper.param('lab_id', '实验室ID过滤', type='int')
    @ns_paper.param('research_group_id', '课题组ID过滤', type='int')
    @ns_paper.param('paper_year', '发表年份过滤', type='string')
    @ns_paper.param('show_all', '显示所有状态', type='string', enum=['true', 'false'])
    @ns_paper.marshal_with(pagination_response)
    def get(self):
        """获取论文列表（支持多维度过滤和搜索）"""
        pass
    
    @ns_paper.doc('创建论文', security='Bearer')
    @ns_paper.expect(paper_model, validate=True)
    @ns_paper.marshal_with(base_response)
    @ns_paper.response(401, '未认证')
    @ns_paper.response(403, '权限不足')
    def post(self):
        """
        创建新论文
        
        支持文件上传：
        - paper_file: 论文PDF文件
        """
        pass

@ns_paper.route('/<int:paper_id>')
class Paper(Resource):
    @ns_paper.doc('获取论文详情')
    @ns_paper.marshal_with(base_response)
    @ns_paper.response(404, '论文不存在')
    def get(self, paper_id):
        """获取指定论文的详细信息"""
        pass
    
    @ns_paper.doc('更新论文', security='Bearer')
    @ns_paper.expect(paper_model)
    @ns_paper.marshal_with(base_response)
    @ns_paper.response(401, '未认证')
    @ns_paper.response(403, '权限不足')
    @ns_paper.response(404, '论文不存在')
    def put(self, paper_id):
        """更新论文信息"""
        pass
    
    @ns_paper.doc('删除论文', security='Bearer')
    @ns_paper.marshal_with(base_response)
    @ns_paper.response(401, '未认证')
    @ns_paper.response(403, '权限不足')
    @ns_paper.response(404, '论文不存在')
    def delete(self, paper_id):
        """删除论文（软删除）"""
        pass

# ==================== 新闻管理接口 ====================

@ns_news.route('/')
class NewsList(Resource):
    @ns_news.doc('获取新闻列表')
    @ns_news.param('page', '页码', type='int', default=1)
    @ns_news.param('per_page', '每页数量', type='int', default=10)
    @ns_news.param('all', '获取全部数据', type='string', enum=['true', 'false'])
    @ns_news.param('q', '搜索关键词（新闻标题、内容）', type='string')
    @ns_news.param('news_date', '新闻日期过滤 (YYYY-MM-DD)', type='string')
    @ns_news.param('show_all', '显示所有状态', type='string', enum=['true', 'false'])
    @ns_news.marshal_with(pagination_response)
    def get(self):
        """获取新闻列表（按日期倒序）"""
        pass
    
    @ns_news.doc('创建新闻', security='Bearer')
    @ns_news.expect(news_model, validate=True)
    @ns_news.marshal_with(base_response)
    @ns_news.response(401, '未认证')
    @ns_news.response(403, '权限不足')
    def post(self):
        """创建新闻"""
        pass

@ns_news.route('/<int:news_id>')
class News(Resource):
    @ns_news.doc('获取新闻详情')
    @ns_news.marshal_with(base_response)
    @ns_news.response(404, '新闻不存在')
    def get(self, news_id):
        """获取指定新闻的详细信息"""
        pass
    
    @ns_news.doc('更新新闻', security='Bearer')
    @ns_news.expect(news_model)
    @ns_news.marshal_with(base_response)
    @ns_news.response(401, '未认证')
    @ns_news.response(403, '权限不足')
    @ns_news.response(404, '新闻不存在')
    def put(self, news_id):
        """更新新闻信息"""
        pass
    
    @ns_news.doc('删除新闻', security='Bearer')
    @ns_news.marshal_with(base_response)
    @ns_news.response(401, '未认证')
    @ns_news.response(403, '权限不足')
    @ns_news.response(404, '新闻不存在')
    def delete(self, news_id):
        """删除新闻（软删除）"""
        pass

# ==================== 项目管理接口 ====================

@ns_project.route('/')
class ProjectList(Resource):
    @ns_project.doc('获取项目列表')
    @ns_project.param('page', '页码', type='int', default=1)
    @ns_project.param('per_page', '每页数量', type='int', default=10)
    @ns_project.param('all', '获取全部数据', type='string', enum=['true', 'false'])
    @ns_project.param('q', '搜索关键词（项目名称、描述）', type='string')
    @ns_project.param('is_end', '项目状态', type='int', enum=[0, 1])
    @ns_project.param('show_all', '显示所有状态', type='string', enum=['true', 'false'])
    @ns_project.marshal_with(pagination_response)
    def get(self):
        """获取项目列表（支持状态过滤和搜索）"""
        pass
    
    @ns_project.doc('创建项目', security='Bearer')
    @ns_project.expect(project_model, validate=True)
    @ns_project.marshal_with(base_response)
    @ns_project.response(401, '未认证')
    @ns_project.response(403, '权限不足')
    def post(self):
        """创建新项目"""
        pass

@ns_project.route('/<int:project_id>')
class Project(Resource):
    @ns_project.doc('获取项目详情')
    @ns_project.marshal_with(base_response)
    @ns_project.response(404, '项目不存在')
    def get(self, project_id):
        """获取指定项目的详细信息"""
        pass
    
    @ns_project.doc('更新项目', security='Bearer')
    @ns_project.expect(project_model)
    @ns_project.marshal_with(base_response)
    @ns_project.response(401, '未认证')
    @ns_project.response(403, '权限不足')
    @ns_project.response(404, '项目不存在')
    def put(self, project_id):
        """更新项目信息"""
        pass
    
    @ns_project.doc('删除项目', security='Bearer')
    @ns_project.marshal_with(base_response)
    @ns_project.response(401, '未认证')
    @ns_project.response(403, '权限不足')
    @ns_project.response(404, '项目不存在')
    def delete(self, project_id):
        """删除项目（软删除）"""
        pass

# ==================== 媒体管理接口 ====================

@ns_media.route('/upload')
class MediaUpload(Resource):
    @ns_media.doc('文件上传', security='Bearer')
    @ns_media.expect(api.parser().add_argument(
        'file', 
        location='files',
        type='file',
        required=True,
        help='要上传的文件'
    ))
    @ns_media.marshal_with(base_response)
    @ns_media.response(401, '未认证')
    @ns_media.response(403, '权限不足')
    @ns_media.response(413, '文件太大')
    @ns_media.response(415, '不支持的文件类型')
    def post(self):
        """
        文件上传
        
        **支持的文件类型**:
        - 图片: jpg, jpeg, png, gif (最大 5MB)
        - 文档: pdf (最大 50MB)
        
        **响应示例**:
        ```json
        {
          "code": 0,
          "message": "文件上传成功",
          "data": {
            "file_path": "/media/other/filename.jpg",
            "file_url": "http://localhost:8000/api/media/serve/other/filename.jpg",
            "file_name": "filename.jpg",
            "file_size": 1024000
          }
        }
        ```
        """
        pass

@ns_media.route('/serve/<path:file_path>')
class MediaServe(Resource):
    @ns_media.doc('获取文件')
    @ns_media.param('file_path', '文件路径', _in='path')
    @ns_media.response(404, '文件不存在')
    def get(self, file_path):
        """获取上传的文件（图片、PDF等）"""
        pass

@ns_media.route('/info/<path:file_path>')
class MediaInfo(Resource):
    @ns_media.doc('获取文件信息')
    @ns_media.param('file_path', '文件路径', _in='path')
    @ns_media.marshal_with(base_response)
    @ns_media.response(404, '文件不存在')
    def get(self, file_path):
        """获取文件的详细信息（大小、类型等）"""
        pass

@ns_media.route('/health')
class MediaHealth(Resource):
    @ns_media.doc('媒体服务健康检查')
    @ns_media.marshal_with(base_response)
    def get(self):
        """检查媒体服务状态"""
        pass

# ==================== 操作审计接口 ====================

@ns_edit_record.route('/')
class EditRecordList(Resource):
    @ns_edit_record.doc('获取编辑记录', security='Bearer')
    @ns_edit_record.param('page', '页码', type='int', default=1)
    @ns_edit_record.param('per_page', '每页数量', type='int', default=10)
    @ns_edit_record.param('all', '获取全部数据', type='string', enum=['true', 'false'])
    @ns_edit_record.param('admin_id', '操作管理员ID过滤', type='int')
    @ns_edit_record.param('operation_type', '操作类型过滤', type='string', enum=['CREATE', 'UPDATE', 'DELETE'])
    @ns_edit_record.param('table_name', '表名过滤', type='string')
    @ns_edit_record.param('start_date', '开始日期 (YYYY-MM-DD)', type='string')
    @ns_edit_record.param('end_date', '结束日期 (YYYY-MM-DD)', type='string')
    @ns_edit_record.marshal_with(pagination_response)
    @ns_edit_record.response(401, '未认证')
    @ns_edit_record.response(403, '权限不足')
    def get(self):
        """
        获取操作审计记录
        
        记录所有管理员的 CRUD 操作，包括：
        - 操作时间、操作人、操作类型
        - 涉及的表和记录ID
        - 操作前后的数据对比
        """
        pass

@ns_edit_record.route('/<int:record_id>')
class EditRecord(Resource):
    @ns_edit_record.doc('获取编辑记录详情', security='Bearer')
    @ns_edit_record.marshal_with(base_response)
    @ns_edit_record.response(401, '未认证')
    @ns_edit_record.response(403, '权限不足')
    @ns_edit_record.response(404, '记录不存在')
    def get(self, record_id):
        """获取指定编辑记录的详细信息"""
        pass

# ==================== 系统接口 ====================

@ns_system.route('/health')
class SystemHealth(Resource):
    @ns_system.doc('系统健康检查')
    @ns_system.marshal_with(base_response)
    def get(self):
        """
        系统健康检查
        
        **响应示例**:
        ```json
        {
          "code": 0,
          "message": "实验室网页框架后端服务正常运行",
          "data": {
            "status": "healthy",
            "version": "2.0",
            "database": "connected",
            "timestamp": "2024-08-10T17:30:00Z"
          }
        }
        ```
        """
        pass

@ns_system.route('/api-info')
class SystemApiInfo(Resource):
    @ns_system.doc('API信息页面')
    def get(self):
        """返回API信息页面（HTML）"""
        pass

@ns_system.route('/swagger.json')
class SystemSwaggerJson(Resource):
    @ns_system.doc('Swagger JSON规范')
    def get(self):
        """获取 OpenAPI 3.0 JSON 规范文件"""
        pass

print("✅ 完整版自动化 Swagger 系统已加载")
print("📊 包含接口数量: 48+")
print("🔗 文档地址: /api/docs")
print("📋 支持模块: 认证、管理员、实验室、课题组、成员、论文、新闻、项目、媒体、审计、系统")
print("🎯 所有接口已自动生成文档，支持在线测试")