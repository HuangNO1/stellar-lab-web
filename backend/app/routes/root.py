from flask import Blueprint, redirect, render_template_string

bp = Blueprint('root', __name__)

@bp.route('/')
def index():
    """根路由，重定向到API文檔"""
    return redirect('/api/docs')

@bp.route('/health')
def health():
    """健康檢查"""
    return {"status": "healthy", "message": "實驗室網頁框架後端服務正常運行"}

@bp.route('/api-info')
def api_info():
    """API信息頁面"""
    info_html = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>實驗室網頁框架 API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .header { text-align: center; color: #333; }
            .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
            .api-list { list-style: none; padding: 0; }
            .api-list li { margin: 8px 0; padding: 8px; background: #f5f5f5; border-radius: 4px; }
            .method { font-weight: bold; color: #007bff; }
            .endpoint { font-family: monospace; color: #333; }
            .description { color: #666; }
            .btn { display: inline-block; padding: 10px 20px; background: #007bff; color: white; 
                   text-decoration: none; border-radius: 4px; margin: 5px; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔬 實驗室網頁框架 API</h1>
            <p>一個專為實驗室設計的通用網頁框架後端服務</p>
            
            <a href="/api/docs" class="btn">📖 Swagger文檔</a>
            <a href="/health" class="btn">🏥 健康檢查</a>
        </div>

        <div class="section">
            <h2>🚀 快速開始</h2>
            <p><strong>默認管理員賬戶：</strong></p>
            <ul>
                <li>用戶名: <code>admin</code></li>
                <li>密碼: <code>admin123</code></li>
            </ul>
            
            <p><strong>認證方式：</strong></p>
            <ol>
                <li>使用 POST /api/admin/login 獲取Token</li>
                <li>在請求頭中添加: <code>Authorization: Bearer &lt;token&gt;</code></li>
            </ol>
        </div>

        <div class="section">
            <h2>📡 主要API端點</h2>
            <ul class="api-list">
                <li>
                    <span class="method">POST</span> 
                    <span class="endpoint">/api/admin/login</span>
                    <span class="description">- 管理員登錄</span>
                </li>
                <li>
                    <span class="method">GET</span> 
                    <span class="endpoint">/api/lab</span>
                    <span class="description">- 獲取實驗室信息</span>
                </li>
                <li>
                    <span class="method">GET</span> 
                    <span class="endpoint">/api/research-groups</span>
                    <span class="description">- 獲取課題組列表</span>
                </li>
                <li>
                    <span class="method">GET</span> 
                    <span class="endpoint">/api/members</span>
                    <span class="description">- 獲取成員列表</span>
                </li>
                <li>
                    <span class="method">GET</span> 
                    <span class="endpoint">/api/papers</span>
                    <span class="description">- 獲取論文列表</span>
                </li>
                <li>
                    <span class="method">GET</span> 
                    <span class="endpoint">/api/news</span>
                    <span class="description">- 獲取新聞列表</span>
                </li>
                <li>
                    <span class="method">GET</span> 
                    <span class="endpoint">/api/projects</span>
                    <span class="description">- 獲取項目列表</span>
                </li>
                <li>
                    <span class="method">POST</span> 
                    <span class="endpoint">/api/media/upload</span>
                    <span class="description">- 文件上傳 (需要認證)</span>
                </li>
            </ul>
        </div>

        <div class="section">
            <h2>📊 響應格式</h2>
            <p><strong>成功響應:</strong></p>
            <pre style="background: #f8f9fa; padding: 15px; border-radius: 4px;">
{
  "code": 0,
  "message": "OK",
  "data": { ... }
}</pre>
            
            <p><strong>錯誤響應:</strong></p>
            <pre style="background: #f8f9fa; padding: 15px; border-radius: 4px;">
{
  "code": 2000,
  "message": "參數錯誤",
  "data": null
}</pre>
        </div>

        <div class="section">
            <h2>🔒 錯誤碼說明</h2>
            <ul>
                <li><code>0</code> - 成功</li>
                <li><code>1000</code> - 未認證或token無效</li>
                <li><code>1001</code> - 權限不足</li>
                <li><code>2000</code> - 參數校驗錯誤</li>
                <li><code>3000</code> - 資源未找到</li>
                <li><code>4000</code> - 操作衝突</li>
                <li><code>5000</code> - 服務器內部錯誤</li>
            </ul>
        </div>
    </body>
    </html>
    '''
    return render_template_string(info_html)