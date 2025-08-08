from flask import Blueprint, render_template_string, jsonify
from app.swagger import api

bp = Blueprint('swagger_docs', __name__)

@bp.route('/docs')
def swagger_ui():
    """Swagger UI頁面"""
    swagger_ui_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>實驗室網頁框架 API 文檔</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.51.1/swagger-ui.css" />
        <style>
            html {
                box-sizing: border-box;
                overflow: -moz-scrollbars-vertical;
                overflow-y: scroll;
            }
            *, *:before, *:after {
                box-sizing: inherit;
            }
            body {
                margin: 0;
                background: #fafafa;
            }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@3.51.1/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@3.51.1/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: '/api/swagger.json',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(swagger_ui_html)

@bp.route('/swagger.json')
def swagger_json():
    """返回API規範JSON"""
    swagger_spec = {
        "swagger": "2.0",
        "info": {
            "title": "實驗室網頁框架 API",
            "version": "1.0.0",
            "description": "實驗室通用網頁框架後端API文檔"
        },
        "host": "localhost:8000",
        "basePath": "/api",
        "schemes": ["http", "https"],
        "consumes": ["application/json", "multipart/form-data"],
        "produces": ["application/json"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Token, 格式: Bearer <token>"
            }
        },
        "paths": {
            "/admin/login": {
                "post": {
                    "tags": ["認證"],
                    "summary": "管理員登錄",
                    "description": "使用用戶名和密碼登錄，返回JWT Token",
                    "parameters": [{
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "admin_name": {"type": "string", "example": "admin"},
                                "admin_pass": {"type": "string", "example": "admin123"}
                            },
                            "required": ["admin_name", "admin_pass"]
                        }
                    }],
                    "responses": {
                        "200": {
                            "description": "登錄成功",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "code": {"type": "integer", "example": 0},
                                    "message": {"type": "string", "example": "OK"},
                                    "data": {
                                        "type": "object",
                                        "properties": {
                                            "access_token": {"type": "string"},
                                            "expires_in": {"type": "integer"},
                                            "admin": {"type": "object"}
                                        }
                                    }
                                }
                            }
                        },
                        "401": {"description": "用戶名或密碼錯誤"}
                    }
                }
            },
            "/lab": {
                "get": {
                    "tags": ["實驗室"],
                    "summary": "獲取實驗室信息",
                    "responses": {
                        "200": {"description": "成功獲取實驗室信息"}
                    }
                },
                "put": {
                    "tags": ["實驗室"],
                    "summary": "更新實驗室信息",
                    "security": [{"Bearer": []}],
                    "consumes": ["multipart/form-data"],
                    "parameters": [
                        {"name": "lab_zh", "in": "formData", "type": "string"},
                        {"name": "lab_en", "in": "formData", "type": "string"},
                        {"name": "lab_desc_zh", "in": "formData", "type": "string"},
                        {"name": "lab_desc_en", "in": "formData", "type": "string"},
                        {"name": "lab_address_zh", "in": "formData", "type": "string"},
                        {"name": "lab_address_en", "in": "formData", "type": "string"},
                        {"name": "lab_email", "in": "formData", "type": "string"},
                        {"name": "lab_phone", "in": "formData", "type": "string"},
                        {"name": "lab_logo", "in": "formData", "type": "file"}
                    ],
                    "responses": {
                        "200": {"description": "更新成功"},
                        "401": {"description": "未認證"}
                    }
                }
            },
            "/research-groups": {
                "get": {
                    "tags": ["課題組"],
                    "summary": "獲取課題組列表",
                    "parameters": [
                        {"name": "page", "in": "query", "type": "integer", "description": "頁碼"},
                        {"name": "per_page", "in": "query", "type": "integer", "description": "每頁數量"},
                        {"name": "q", "in": "query", "type": "string", "description": "搜索關鍵字"}
                    ],
                    "responses": {
                        "200": {"description": "成功獲取課題組列表"}
                    }
                },
                "post": {
                    "tags": ["課題組"],
                    "summary": "創建課題組",
                    "security": [{"Bearer": []}],
                    "parameters": [{
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "research_group_name_zh": {"type": "string"},
                                "research_group_name_en": {"type": "string"},
                                "research_group_desc_zh": {"type": "string"},
                                "research_group_desc_en": {"type": "string"},
                                "mem_id": {"type": "integer", "description": "組長ID"}
                            }
                        }
                    }],
                    "responses": {
                        "201": {"description": "創建成功"},
                        "401": {"description": "未認證"}
                    }
                }
            },
            "/members": {
                "get": {
                    "tags": ["成員"],
                    "summary": "獲取成員列表",
                    "parameters": [
                        {"name": "page", "in": "query", "type": "integer"},
                        {"name": "per_page", "in": "query", "type": "integer"},
                        {"name": "type", "in": "query", "type": "integer", "description": "成員類型"},
                        {"name": "q", "in": "query", "type": "string"}
                    ],
                    "responses": {
                        "200": {"description": "成功獲取成員列表"}
                    }
                },
                "post": {
                    "tags": ["成員"],
                    "summary": "創建成員",
                    "security": [{"Bearer": []}],
                    "consumes": ["multipart/form-data"],
                    "parameters": [
                        {"name": "mem_name_zh", "in": "formData", "type": "string"},
                        {"name": "mem_name_en", "in": "formData", "type": "string"},
                        {"name": "mem_email", "in": "formData", "type": "string"},
                        {"name": "mem_type", "in": "formData", "type": "integer"},
                        {"name": "research_group_id", "in": "formData", "type": "integer"},
                        {"name": "mem_avatar", "in": "formData", "type": "file"}
                    ],
                    "responses": {
                        "201": {"description": "創建成功"}
                    }
                }
            },
            "/papers": {
                "get": {
                    "tags": ["論文"],
                    "summary": "獲取論文列表",
                    "parameters": [
                        {"name": "page", "in": "query", "type": "integer"},
                        {"name": "per_page", "in": "query", "type": "integer"},
                        {"name": "q", "in": "query", "type": "string"}
                    ],
                    "responses": {
                        "200": {"description": "成功獲取論文列表"}
                    }
                }
            },
            "/news": {
                "get": {
                    "tags": ["新聞"],
                    "summary": "獲取新聞列表",
                    "parameters": [
                        {"name": "page", "in": "query", "type": "integer"},
                        {"name": "per_page", "in": "query", "type": "integer"},
                        {"name": "news_type", "in": "query", "type": "integer"}
                    ],
                    "responses": {
                        "200": {"description": "成功獲取新聞列表"}
                    }
                }
            },
            "/projects": {
                "get": {
                    "tags": ["項目"],
                    "summary": "獲取項目列表",
                    "parameters": [
                        {"name": "page", "in": "query", "type": "integer"},
                        {"name": "per_page", "in": "query", "type": "integer"},
                        {"name": "q", "in": "query", "type": "string"}
                    ],
                    "responses": {
                        "200": {"description": "成功獲取項目列表"}
                    }
                }
            },
            "/media/upload": {
                "post": {
                    "tags": ["媒體"],
                    "summary": "上傳文件",
                    "security": [{"Bearer": []}],
                    "consumes": ["multipart/form-data"],
                    "parameters": [
                        {"name": "file", "in": "formData", "type": "file", "required": True},
                        {"name": "type", "in": "formData", "type": "string", "enum": ["lab_logo", "member_avatar", "paper", "other"]}
                    ],
                    "responses": {
                        "200": {"description": "上傳成功"}
                    }
                }
            }
        },
        "definitions": {
            "SuccessResponse": {
                "type": "object",
                "properties": {
                    "code": {"type": "integer", "example": 0},
                    "message": {"type": "string", "example": "OK"},
                    "data": {"type": "object"}
                }
            },
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "code": {"type": "integer"},
                    "message": {"type": "string"},
                    "data": {"type": "object"}
                }
            }
        }
    }
    return jsonify(swagger_spec)