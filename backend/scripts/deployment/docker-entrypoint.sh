#!/bin/bash

# 實驗室網頁框架 Docker 啟動腳本
set -e

echo "🚀 正在啟動實驗室網頁框架..."

# 等待數據庫連接
echo "📡 等待數據庫服務..."

# 使用 Python 腳本等待數據庫（先嘗試連接 root 用戶確保服務可用）
python << 'EOF'
import time
import pymysql
import os

def wait_for_database():
    max_retries = 30
    retry_interval = 2
    
    # 數據庫配置
    host = os.getenv('MYSQL_HOST', 'db')
    port = int(os.getenv('MYSQL_PORT', 3306))
    root_password = os.getenv('MYSQL_ROOT_PASSWORD', 'lab_web_root_123')
    database = os.getenv('MYSQL_DATABASE', 'lab_web')
    
    print(f"📊 連接配置: {host}:{port}")
    print(f"🗄️  目標數據庫: {database}")
    
    for i in range(max_retries):
        try:
            # 先嘗試以 root 用戶連接檢查服務是否可用
            connection = pymysql.connect(
                host=host,
                port=port,
                user='root',
                password=root_password,
                charset='utf8mb4'
            )
            
            with connection.cursor() as cursor:
                # 檢查數據庫是否存在
                cursor.execute("SHOW DATABASES LIKE %s", (database,))
                result = cursor.fetchone()
                
                if result:
                    print(f"✅ 數據庫 '{database}' 已準備就緒")
                else:
                    print(f"⏳ 數據庫 '{database}' 不存在，將通過 init_db.py 自動創建")
            
            connection.close()
            print("✅ MySQL 服務連接成功")
            return True
            
        except Exception as e:
            print(f"⏳ 等待數據庫服務... ({i+1}/{max_retries}): {str(e)}")
            if i == max_retries - 1:
                print(f"❌ 數據庫連接超時失敗")
                return False
            time.sleep(retry_interval)
    
    return False

if not wait_for_database():
    exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ 數據庫連接失敗，退出"
    exit 1
fi

# 設置 Flask 環境
export FLASK_CONFIG=${FLASK_CONFIG:-production}

# 運行現有的數據庫初始化腳本
echo "🔧 初始化數據庫和示例數據..."
python scripts/development/init_db.py

if [ $? -eq 0 ]; then
    echo "✅ 數據庫初始化完成"
else
    echo "❌ 數據庫初始化失敗"
    exit 1
fi

# 啟動應用
echo "🎯 啟動 Flask 應用..."
echo "   - 工作進程: 4"
echo "   - 綁定地址: 0.0.0.0:8000" 
echo "   - 環境: ${FLASK_CONFIG}"

exec gunicorn \
    --workers 4 \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --access-logfile - \
    --error-logfile - \
    run:app