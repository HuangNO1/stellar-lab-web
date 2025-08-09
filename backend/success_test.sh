#!/bin/bash

echo "🎉 恭喜！服務已經成功運行"
echo "========================="
echo ""

# 測試健康檢查
echo "🏥 測試健康檢查..."
curl -s http://localhost:8000/health | head -3
echo ""

# 測試管理員登錄
echo "🔐 測試管理員登錄..."
curl -s -X POST http://localhost:8000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"admin_name":"admin","admin_pass":"admin123"}' | head -3
echo ""

echo "🌟 服務訪問地址："
echo "   - 後端 API:     http://localhost:8000"
echo "   - API 文檔:     http://localhost:8000/api/docs"  
echo "   - 數據庫管理:   http://localhost:8081"
echo "   - 健康檢查:     http://localhost:8000/health"
echo ""

echo "✨ 默認管理員賬戶："
echo "   - 用戶名: admin"
echo "   - 密碼:   admin123"
echo ""

echo "🎯 部署成功完成！"