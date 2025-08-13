#!/bin/bash

# Docker 診斷腳本

echo "🔍 Docker 環境診斷"
echo "=================="

# 檢查 Docker 是否安裝
echo "1. 檢查 Docker 安裝..."
if command -v docker &> /dev/null; then
    echo "✅ Docker 已安裝: $(docker --version)"
else
    echo "❌ Docker 未安裝"
    exit 1
fi

# 檢查 Docker Compose 是否安裝
echo "2. 檢查 Docker Compose 安裝..."
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose 已安裝: $(docker-compose --version)"
else
    echo "❌ Docker Compose 未安裝"
    exit 1
fi

# 檢查 Docker 服務狀態
echo "3. 檢查 Docker 服務狀態..."
if sudo systemctl is-active --quiet docker; then
    echo "✅ Docker 服務正在運行"
else
    echo "❌ Docker 服務未運行"
    echo "   請執行: sudo systemctl start docker"
    exit 1
fi

# 檢查用戶權限
echo "4. 檢查用戶 Docker 權限..."
if groups $USER | grep -q docker; then
    echo "✅ 用戶已加入 docker 組"
else
    echo "⚠️  用戶未加入 docker 組"
    echo "   請執行以下命令添加用戶到 docker 組："
    echo "   sudo usermod -aG docker $USER"
    echo "   newgrp docker"
fi

# 檢查端口佔用
echo "5. 檢查端口佔用..."
ports=(${MYSQL_PORT:-3306} ${BACKEND_PORT:-8000} ${PHPMYADMIN_PORT:-8081})
for port in "${ports[@]}"; do
    if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        echo "⚠️  端口 $port 已被佔用:"
        netstat -tlnp 2>/dev/null | grep ":$port "
    else
        echo "✅ 端口 $port 可用"
    fi
done

# 檢查現有容器
echo "6. 檢查現有容器..."
if docker ps -a --filter "name=lab_web" --format "table {{.Names}}\t{{.Status}}" | grep -q lab_web; then
    echo "📦 發現相關容器:"
    docker ps -a --filter "name=lab_web" --format "table {{.Names}}\t{{.Status}}"
else
    echo "✅ 沒有發現相關容器"
fi

# 檢查 Docker 鏡像
echo "7. 檢查相關鏡像..."
if docker images | grep -q lab_web; then
    echo "🖼️  發現相關鏡像:"
    docker images | grep lab_web
else
    echo "✅ 沒有發現相關鏡像"
fi

# 測試 Docker 基本功能
echo "8. 測試 Docker 基本功能..."
if docker run --rm hello-world >/dev/null 2>&1; then
    echo "✅ Docker 基本功能正常"
else
    echo "❌ Docker 基本功能異常"
fi

echo ""
echo "🎯 診斷完成！"
echo ""

# 如果有問題，給出建議
if ! groups $USER | grep -q docker; then
    echo "🔧 建議的解決方案："
    echo "1. 添加用戶到 docker 組:"
    echo "   sudo usermod -aG docker $USER"
    echo "   newgrp docker"
    echo ""
    echo "2. 重新運行部署腳本:"
    echo "   ./deploy.sh start"
    echo ""
fi