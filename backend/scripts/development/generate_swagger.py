#!/usr/bin/env python3
"""
真正自动化的 Swagger 生成工具
基于路由扫描和AST分析自动生成 Swagger 定义

使用方法:
    python scripts/development/generate_swagger.py --output app/routes/swagger_auto_generated.py
    python scripts/development/generate_swagger.py --scan-only  # 仅扫描不生成
"""

import os
import sys
import ast
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class RouteAnalyzer:
    """路由分析器 - 扫描并解析路由文件"""
    
    def __init__(self, routes_dir: str):
        self.routes_dir = Path(routes_dir)
        self.routes_info = {}
        
    def scan_routes(self) -> Dict[str, Any]:
        """扫描所有路由文件"""
        route_files = self.routes_dir.glob("*.py")
        
        for route_file in route_files:
            if route_file.name.startswith('__') or route_file.name.startswith('swagger'):
                continue
                
            module_name = route_file.stem
            print(f"🔍 扫描模块: {module_name}")
            
            routes = self.analyze_file(route_file)
            if routes:
                self.routes_info[module_name] = routes
                
        return self.routes_info
    
    def analyze_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """分析单个路由文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content)
            routes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    route_info = self.extract_route_info(node, content)
                    if route_info:
                        routes.append(route_info)
                        
            return routes
            
        except Exception as e:
            print(f"⚠️  分析文件 {file_path} 时出错: {e}")
            return []
    
    def extract_route_info(self, func_node: ast.FunctionDef, content: str) -> Optional[Dict[str, Any]]:
        """从函数节点提取路由信息"""
        route_info = {
            'function_name': func_node.name,
            'docstring': ast.get_docstring(func_node) or '',
            'decorators': [],
            'methods': ['GET'],  # 默认
            'path': '',
            'security': False
        }
        
        # 分析装饰器
        for decorator in func_node.decorator_list:
            decorator_info = self.parse_decorator(decorator, content)
            if decorator_info:
                route_info['decorators'].append(decorator_info)
                
                # 提取路由信息
                if decorator_info['name'] in ['route', 'bp.route']:
                    route_info['path'] = decorator_info.get('path', '')
                    route_info['methods'] = decorator_info.get('methods', ['GET'])
                elif decorator_info['name'] in ['admin_required', 'super_admin_required']:
                    route_info['security'] = True
        
        # 只返回有路由装饰器的函数
        if route_info['path']:
            return route_info
        return None
    
    def parse_decorator(self, decorator: ast.AST, content: str) -> Optional[Dict[str, Any]]:
        """解析装饰器"""
        if isinstance(decorator, ast.Name):
            return {'name': decorator.id}
        
        elif isinstance(decorator, ast.Attribute):
            if isinstance(decorator.value, ast.Name):
                return {'name': f"{decorator.value.id}.{decorator.attr}"}
        
        elif isinstance(decorator, ast.Call):
            decorator_name = None
            if isinstance(decorator.func, ast.Attribute):
                if isinstance(decorator.func.value, ast.Name):
                    decorator_name = f"{decorator.func.value.id}.{decorator.func.attr}"
            elif isinstance(decorator.func, ast.Name):
                decorator_name = decorator.func.id
                
            if decorator_name:
                result = {'name': decorator_name}
                
                # 解析参数
                for i, arg in enumerate(decorator.args):
                    if isinstance(arg, ast.Constant):
                        if i == 0 and decorator_name in ['route', 'bp.route']:
                            result['path'] = arg.value
                
                # 解析关键字参数
                for keyword in decorator.keywords:
                    if keyword.arg == 'methods' and isinstance(keyword.value, ast.List):
                        methods = []
                        for method in keyword.value.elts:
                            if isinstance(method, ast.Constant):
                                methods.append(method.value)
                        result['methods'] = methods
                
                return result
        
        return None


class SwaggerGenerator:
    """Swagger 生成器"""
    
    def __init__(self):
        self.namespace_mapping = {
            'auth': ('认证管理', '管理员认证相关接口'),
            'admin': ('管理员管理', '管理员账户管理'),
            'lab': ('实验室管理', '实验室信息管理'),
            'research_group': ('课题组管理', '课题组管理'),
            'member': ('成员管理', '实验室成员管理'),
            'paper': ('论文管理', '论文发表管理'),
            'news': ('新闻管理', '实验室新闻管理'),
            'project': ('项目管理', '研究项目管理'),
            'media': ('媒体管理', '文件上传管理'),
            'edit_record': ('操作审计', '编辑记录查询')
        }
        
    def generate(self, routes_info: Dict[str, Any], output_file: str):
        """生成完整的 Swagger 文档文件"""
        
        swagger_content = self.generate_header()
        swagger_content += self.generate_models()
        swagger_content += self.generate_namespaces(routes_info)
        swagger_content += self.generate_routes(routes_info)
        swagger_content += self.generate_footer()
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(swagger_content)
            
        print(f"✅ Swagger 文档已生成: {output_file}")
        
    def generate_header(self) -> str:
        """生成文件头部"""
        return f'''"""
自动生成的 Swagger 文档
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
生成工具: scripts/development/generate_swagger.py

⚠️  警告: 此文件由工具自动生成，请勿手动修改！
如需更新文档，请运行: python scripts/development/generate_swagger.py
"""

from flask import Blueprint
from flask_restx import Api, Resource, Namespace, fields

# 创建蓝图
bp = Blueprint('swagger_auto', __name__)

# 创建 API 实例
api = Api(
    bp,
    version='2.0',
    title='实验室网页框架 API - 自动生成版',
    description=\'''
## 🤖 自动生成的 API 文档

此文档基于路由文件自动扫描生成，包含项目中的所有API接口。

### 🔄 更新方式
```bash
python scripts/development/generate_swagger.py
```

### 🔑 认证方式  
在请求头中添加: `Authorization: Bearer <token>`

### 📊 响应格式
成功响应: `{{"code": 0, "message": "OK", "data": {{...}}}}`
    \''',
    doc='/docs',
    authorizations={{
        'Bearer': {{
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }}
    }}
)

# 基础响应模型
base_response = api.model('BaseResponse', {{
    'code': fields.Integer(description='状态码', example=0),
    'message': fields.String(description='响应消息', example='OK'),
    'data': fields.Raw(description='响应数据')
}})

'''

    def generate_models(self) -> str:
        """生成数据模型"""
        return '''# 通用数据模型
pagination_response = api.model('PaginationResponse', {
    'code': fields.Integer(description='状态码', example=0),
    'message': fields.String(description='响应消息', example='OK'),
    'data': fields.Nested(api.model('PaginationData', {
        'items': fields.List(fields.Raw, description='数据列表'),
        'total': fields.Integer(description='总数量'),
        'page': fields.Integer(description='当前页码'),
        'per_page': fields.Integer(description='每页数量')
    }))
})

'''

    def generate_namespaces(self, routes_info: Dict[str, Any]) -> str:
        """生成命名空间定义"""
        content = "# 命名空间定义\\n"
        
        for module_name, routes in routes_info.items():
            if module_name in self.namespace_mapping:
                name, desc = self.namespace_mapping[module_name]
                path_prefix = self.get_path_prefix(routes)
                
                content += f"ns_{module_name} = api.namespace('{name}', description='{desc}', path='{path_prefix}')\\n"
        
        content += "\\n"
        return content
    
    def get_path_prefix(self, routes: List[Dict[str, Any]]) -> str:
        """从路由中提取路径前缀"""
        if not routes:
            return '/'
            
        # 取第一个路由的路径作为前缀参考
        first_path = routes[0]['path']
        if '/' in first_path:
            parts = first_path.strip('/').split('/')
            if parts:
                return f"/{parts[0]}"
        return '/'
    
    def generate_routes(self, routes_info: Dict[str, Any]) -> str:
        """生成路由定义"""
        content = "# 自动生成的 API 接口\\n\\n"
        
        for module_name, routes in routes_info.items():
            if module_name not in self.namespace_mapping:
                continue
                
            content += f"# ========== {self.namespace_mapping[module_name][0]} ==========\\n\\n"
            
            # 按路径分组路由
            route_groups = {}
            for route in routes:
                path = route['path']
                # 标准化路径 (去除参数)
                clean_path = re.sub(r'<[^>]+>', '{id}', path)
                if clean_path not in route_groups:
                    route_groups[clean_path] = []
                route_groups[clean_path].append(route)
            
            # 为每个路径组生成 Resource 类
            for clean_path, route_group in route_groups.items():
                class_name = self.generate_class_name(clean_path, module_name)
                route_path = self.clean_route_path(clean_path)
                
                content += f"@ns_{module_name}.route('{route_path}')\\n"
                content += f"class {class_name}(Resource):\\n"
                
                for route in route_group:
                    content += self.generate_method(route, module_name)
                
                content += "\\n"
        
        return content
    
    def generate_class_name(self, path: str, module_name: str) -> str:
        """生成类名"""
        # 移除路径中的特殊字符，转为驼峰命名
        clean_path = re.sub(r'[^a-zA-Z0-9]', ' ', path)
        words = clean_path.split()
        
        if words:
            class_name = ''.join(word.capitalize() for word in words)
        else:
            class_name = module_name.replace('_', '').capitalize()
            
        return class_name + 'Resource'
    
    def clean_route_path(self, path: str) -> str:
        """清理路由路径"""
        # 移除 API 前缀
        path = re.sub(r'^/api', '', path)
        if not path:
            path = '/'
        return path
    
    def generate_method(self, route: Dict[str, Any], module_name: str) -> str:
        """生成方法定义"""
        method_name = route['methods'][0].lower() if route['methods'] else 'get'
        function_name = route['function_name']
        docstring = route['docstring'][:100] + '...' if len(route['docstring']) > 100 else route['docstring']
        security = ', security=\\'Bearer\\'' if route['security'] else ''
        
        content = f"    @ns_{module_name}.doc('{function_name}'{security})\\n"
        content += f"    @ns_{module_name}.marshal_with(base_response)\\n"
        
        if route['security']:
            content += f"    @ns_{module_name}.response(401, '未认证')\\n"
            content += f"    @ns_{module_name}.response(403, '权限不足')\\n"
        
        content += f"    def {method_name}(self"
        
        # 添加路径参数
        if '{id}' in route['path']:
            content += ", resource_id"
            
        content += f"):\\n"
        content += f"        \\"\\"\\"\\n        {docstring or function_name}\\n        \\"\\"\\"\\n"
        content += f"        pass\\n\\n"
        
        return content
    
    def generate_footer(self) -> str:
        """生成文件尾部"""
        return f'''
print("🤖 自动生成的 Swagger 文档已加载")
print("⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🔄 更新方式: python scripts/development/generate_swagger.py")
'''


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自动生成 Swagger 文档')
    parser.add_argument('--output', default='app/routes/swagger_auto_generated.py',
                      help='输出文件路径')
    parser.add_argument('--scan-only', action='store_true',
                      help='仅扫描路由，不生成文件')
    parser.add_argument('--routes-dir', default='app/routes',
                      help='路由文件目录')
    
    args = parser.parse_args()
    
    print("🚀 开始自动扫描路由文件...")
    
    # 扫描路由
    analyzer = RouteAnalyzer(args.routes_dir)
    routes_info = analyzer.scan_routes()
    
    # 显示扫描结果
    total_routes = sum(len(routes) for routes in routes_info.values())
    print(f"\\n📊 扫描结果:")
    print(f"   - 模块数量: {len(routes_info)}")
    print(f"   - 接口总数: {total_routes}")
    
    for module_name, routes in routes_info.items():
        print(f"   - {module_name}: {len(routes)} 个接口")
    
    if args.scan_only:
        print("\\n✅ 扫描完成 (仅扫描模式)")
        return
    
    # 生成 Swagger 文档
    print(f"\\n📝 生成 Swagger 文档到: {args.output}")
    
    generator = SwaggerGenerator()
    generator.generate(routes_info, args.output)
    
    print(f"\\n🎉 自动化 Swagger 文档生成完成！")
    print(f"   - 文件位置: {args.output}")
    print(f"   - 包含接口: {total_routes} 个")
    print(f"   - 更新 app/__init__.py 以使用新文档")


if __name__ == '__main__':
    main()