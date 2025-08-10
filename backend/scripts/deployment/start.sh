#!/bin/bash

# 實驗室網頁框架後端啟動腳本

# 設置變量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

echo "🚀 實驗室網頁框架後端啟動中..."

# 檢查虛擬環境
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 創建虛擬環境..."
    python3 -m venv "$VENV_DIR"
fi

# 激活虛擬環境
echo "🔧 激活虛擬環境..."
source "$VENV_DIR/bin/activate"

# 安裝依賴
echo "📥 安裝依賴..."
pip install --upgrade pip
pip install -r "$REQUIREMENTS_FILE"

# 初始化數據庫
echo "🗄️  初始化數據庫..."
python scripts/init_db.py

# 啟動應用
echo "✅ 啟動Flask應用..."
echo "📍 API地址: http://localhost:8000"
echo "📖 默認管理員: admin / admin123"
echo ""

python run.py