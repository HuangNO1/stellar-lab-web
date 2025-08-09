from flask import Blueprint, render_template_string, jsonify, request
import os

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
                    url: window.location.protocol + '//' + window.location.host + '/api/swagger.json',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    requestInterceptor: function(request) {
                        request.headers['Content-Type'] = 'application/json';
                        return request;
                    },
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
    # 動態獲取主機和端口
    host = request.host
    
    swagger_spec = {
        "swagger": "2.0",
        "info": {
            "title": "實驗室網頁框架 API",
            "version": "1.0.0",
            "description": "實驗室通用網頁框架後端API文檔"
        },
        "host": host,  # 動態設置主機和端口
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
                        "200": {
                            "description": "成功獲取實驗室信息",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "code": {"type": "integer", "example": 0},
                                    "message": {"type": "string", "example": "OK"},
                                    "data": {
                                        "type": "object",
                                        "properties": {
                                            "lab_zh": {"type": "string", "example": "智能計算實驗室"},
                                            "lab_en": {"type": "string", "example": "Intelligent Computing Laboratory"},
                                            "lab_desc_zh": {"type": "string"},
                                            "lab_desc_en": {"type": "string"},
                                            "lab_address_zh": {"type": "string"},
                                            "lab_address_en": {"type": "string"},
                                            "lab_email": {"type": "string"},
                                            "lab_phone": {"type": "string"},
                                            "lab_logo": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "put": {
                    "tags": ["實驗室"],
                    "summary": "更新實驗室信息",
                    "security": [{"Bearer": []}],
                    "consumes": ["multipart/form-data"],
                    "parameters": [
                        {
                            "name": "lab_zh",
                            "in": "formData",
                            "type": "string",
                            "description": "實驗室中文名稱",
                            "example": "智能計算實驗室"
                        },
                        {
                            "name": "lab_en",
                            "in": "formData",
                            "type": "string",
                            "description": "實驗室英文名稱",
                            "example": "Intelligent Computing Laboratory"
                        },
                        {
                            "name": "lab_desc_zh",
                            "in": "formData",
                            "type": "string",
                            "description": "實驗室中文描述",
                            "example": "本實驗室專注於人工智能、機器學習和計算機視覺領域的研究"
                        },
                        {
                            "name": "lab_desc_en",
                            "in": "formData",
                            "type": "string",
                            "description": "實驗室英文描述",
                            "example": "Our laboratory focuses on research in artificial intelligence, machine learning, and computer vision"
                        },
                        {
                            "name": "lab_address_zh",
                            "in": "formData",
                            "type": "string",
                            "description": "實驗室中文地址",
                            "example": "北京市海淀區清華大學FIT樓"
                        },
                        {
                            "name": "lab_address_en",
                            "in": "formData",
                            "type": "string",
                            "description": "實驗室英文地址",
                            "example": "FIT Building, Tsinghua University, Beijing"
                        },
                        {
                            "name": "lab_email",
                            "in": "formData",
                            "type": "string",
                            "description": "實驗室聯系郵箱",
                            "example": "contact@lab.tsinghua.edu.cn"
                        },
                        {
                            "name": "lab_phone",
                            "in": "formData",
                            "type": "string",
                            "description": "實驗室聯系電話",
                            "example": "+86-10-62785678"
                        },
                        {
                            "name": "lab_logo",
                            "in": "formData",
                            "type": "file",
                            "description": "實驗室Logo文件"
                        }
                    ],
                    "responses": {
                        "200": {"description": "更新成功"},
                        "400": {"description": "參數錯誤"},
                        "401": {"description": "未認證"}
                    }
                }
            },
            "/research-groups": {
                "get": {
                    "tags": ["課題組"],
                    "summary": "獲取課題組列表",
                    "parameters": [
                        {
                            "name": "page", 
                            "in": "query", 
                            "type": "integer", 
                            "description": "頁碼",
                            "default": 1,
                            "minimum": 1
                        },
                        {
                            "name": "per_page", 
                            "in": "query", 
                            "type": "integer", 
                            "description": "每頁數量",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 100
                        },
                        {
                            "name": "q", 
                            "in": "query", 
                            "type": "string", 
                            "description": "搜索關鍵字",
                            "example": "計算機視覺"
                        }
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
                                "research_group_name_zh": {
                                    "type": "string",
                                    "description": "課題組中文名稱",
                                    "example": "人工智能研究組"
                                },
                                "research_group_name_en": {
                                    "type": "string",
                                    "description": "課題組英文名稱",
                                    "example": "Artificial Intelligence Research Group"
                                },
                                "research_group_desc_zh": {
                                    "type": "string",
                                    "description": "課題組中文描述",
                                    "example": "專注於機器學習和深度學習技術研究"
                                },
                                "research_group_desc_en": {
                                    "type": "string",
                                    "description": "課題組英文描述",
                                    "example": "Focus on machine learning and deep learning research"
                                },
                                "mem_id": {
                                    "type": "integer", 
                                    "description": "組長成員ID",
                                    "example": 1
                                }
                            },
                            "required": ["research_group_name_zh", "research_group_name_en"]
                        }
                    }],
                    "responses": {
                        "201": {"description": "創建成功"},
                        "401": {"description": "未認證"},
                        "400": {"description": "參數錯誤"}
                    }
                }
            },
            "/members": {
                "get": {
                    "tags": ["成員"],
                    "summary": "獲取成員列表",
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "type": "integer",
                            "description": "頁碼",
                            "default": 1,
                            "minimum": 1
                        },
                        {
                            "name": "per_page",
                            "in": "query",
                            "type": "integer",
                            "description": "每頁數量",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 100
                        },
                        {
                            "name": "type",
                            "in": "query",
                            "type": "integer",
                            "description": "成員類型 (0=教師, 1=學生)",
                            "enum": [0, 1],
                            "example": 0
                        },
                        {
                            "name": "q",
                            "in": "query",
                            "type": "string",
                            "description": "搜索關鍵字",
                            "example": "張教授"
                        }
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
                        {
                            "name": "mem_name_zh",
                            "in": "formData",
                            "type": "string",
                            "required": True,
                            "description": "成員中文姓名",
                            "example": "李教授"
                        },
                        {
                            "name": "mem_name_en",
                            "in": "formData",
                            "type": "string",
                            "required": True,
                            "description": "成員英文姓名",
                            "example": "Prof. Li"
                        },
                        {
                            "name": "mem_email",
                            "in": "formData",
                            "type": "string",
                            "required": True,
                            "description": "電子郵箱",
                            "example": "li@lab.edu.cn"
                        },
                        {
                            "name": "mem_type",
                            "in": "formData",
                            "type": "integer",
                            "required": True,
                            "description": "成員類型 (0=教師, 1=學生)",
                            "enum": [0, 1],
                            "example": 0
                        },
                        {
                            "name": "job_type",
                            "in": "formData",
                            "type": "integer",
                            "description": "職務類型 (僅教師: 0=教授, 1=副教授, 2=講師)",
                            "enum": [0, 1, 2],
                            "example": 0
                        },
                        {
                            "name": "student_type",
                            "in": "formData",
                            "type": "integer",
                            "description": "學生類型 (僅學生: 0=博士, 1=碩士, 2=本科)",
                            "enum": [0, 1, 2],
                            "example": 0
                        },
                        {
                            "name": "student_grade",
                            "in": "formData",
                            "type": "integer",
                            "description": "學生年級 (僅學生)",
                            "example": 1
                        },
                        {
                            "name": "research_group_id",
                            "in": "formData",
                            "type": "integer",
                            "required": True,
                            "description": "所屬課題組ID",
                            "example": 1
                        },
                        {
                            "name": "mem_desc_zh",
                            "in": "formData",
                            "type": "string",
                            "description": "成員中文描述",
                            "example": "專注於機器學習領域研究"
                        },
                        {
                            "name": "mem_desc_en",
                            "in": "formData",
                            "type": "string",
                            "description": "成員英文描述",
                            "example": "Focus on machine learning research"
                        },
                        {
                            "name": "mem_avatar",
                            "in": "formData",
                            "type": "file",
                            "description": "頭像文件"
                        }
                    ],
                    "responses": {
                        "201": {"description": "創建成功"},
                        "400": {"description": "參數錯誤"},
                        "401": {"description": "未認證"}
                    }
                }
            },
            "/papers": {
                "get": {
                    "tags": ["論文"],
                    "summary": "獲取論文列表",
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "type": "integer",
                            "description": "頁碼",
                            "default": 1,
                            "minimum": 1
                        },
                        {
                            "name": "per_page",
                            "in": "query",
                            "type": "integer",
                            "description": "每頁數量",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 100
                        },
                        {
                            "name": "q",
                            "in": "query",
                            "type": "string",
                            "description": "搜索關鍵字",
                            "example": "深度學習"
                        },
                        {
                            "name": "paper_type",
                            "in": "query",
                            "type": "integer",
                            "description": "論文類型 (0=會議, 1=期刊, 2=專利)",
                            "enum": [0, 1, 2],
                            "example": 1
                        },
                        {
                            "name": "accept",
                            "in": "query",
                            "type": "integer",
                            "description": "接收狀態 (0=投稿中, 1=已接收)",
                            "enum": [0, 1],
                            "example": 1
                        }
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
                        {
                            "name": "page",
                            "in": "query",
                            "type": "integer",
                            "description": "頁碼",
                            "default": 1,
                            "minimum": 1
                        },
                        {
                            "name": "per_page",
                            "in": "query",
                            "type": "integer",
                            "description": "每頁數量",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 100
                        },
                        {
                            "name": "news_type",
                            "in": "query",
                            "type": "integer",
                            "description": "新聞類型 (0=論文發表, 1=獲獎消息, 2=學術活動)",
                            "enum": [0, 1, 2],
                            "example": 0
                        }
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
                        {
                            "name": "page",
                            "in": "query",
                            "type": "integer",
                            "description": "頁碼",
                            "default": 1,
                            "minimum": 1
                        },
                        {
                            "name": "per_page",
                            "in": "query",
                            "type": "integer",
                            "description": "每頁數量",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 100
                        },
                        {
                            "name": "q",
                            "in": "query",
                            "type": "string",
                            "description": "搜索關鍵字",
                            "example": "智能系統"
                        },
                        {
                            "name": "is_end",
                            "in": "query",
                            "type": "integer",
                            "description": "項目狀態 (0=進行中, 1=已完成)",
                            "enum": [0, 1],
                            "example": 0
                        }
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
                        {
                            "name": "file",
                            "in": "formData",
                            "type": "file",
                            "required": True,
                            "description": "要上傳的文件 (支持圖片: png, jpg, jpeg, gif；文檔: pdf)"
                        },
                        {
                            "name": "type",
                            "in": "formData",
                            "type": "string",
                            "required": True,
                            "enum": ["lab_logo", "member_avatar", "paper", "other"],
                            "description": "文件類型",
                            "example": "member_avatar"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "上傳成功",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "code": {"type": "integer", "example": 0},
                                    "message": {"type": "string", "example": "文件上傳成功"},
                                    "data": {
                                        "type": "object",
                                        "properties": {
                                            "filename": {"type": "string", "example": "avatar_20241201.jpg"},
                                            "url": {"type": "string", "example": "/media/member_avatar/avatar_20241201.jpg"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {"description": "文件格式不支持或文件過大"},
                        "401": {"description": "未認證"}
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