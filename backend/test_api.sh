#!/bin/bash

# API 測試腳本
# 用於驗證 Docker 部署是否成功

BASE_URL="http://localhost:8000"
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}===========================================${NC}"
echo -e "${BLUE}  實驗室網頁框架 API 測試${NC}"
echo -e "${BLUE}===========================================${NC}"
echo ""

# 測試健康檢查
echo -e "${BLUE}1. 測試健康檢查...${NC}"
response=$(curl -s -w "%{http_code}" -o /tmp/health.json "$BASE_URL/health")
if [ "$response" = "200" ]; then
    echo -e "   ${GREEN}✓ 健康檢查通過${NC}"
else
    echo -e "   ${RED}✗ 健康檢查失敗 (HTTP $response)${NC}"
    exit 1
fi

# 測試根路由
echo -e "${BLUE}2. 測試根路由重定向...${NC}"
response=$(curl -s -w "%{http_code}" -o /dev/null "$BASE_URL/")
if [ "$response" = "302" ] || [ "$response" = "200" ]; then
    echo -e "   ${GREEN}✓ 根路由正常${NC}"
else
    echo -e "   ${RED}✗ 根路由異常 (HTTP $response)${NC}"
fi

# 測試實驗室信息接口
echo -e "${BLUE}3. 測試實驗室信息接口...${NC}"
response=$(curl -s -w "%{http_code}" -o /tmp/lab.json "$BASE_URL/api/lab")
if [ "$response" = "200" ]; then
    echo -e "   ${GREEN}✓ 實驗室信息接口正常${NC}"
else
    echo -e "   ${RED}✗ 實驗室信息接口異常 (HTTP $response)${NC}"
fi

# 測試管理員登錄
echo -e "${BLUE}4. 測試管理員登錄...${NC}"
login_response=$(curl -s -X POST "$BASE_URL/api/admin/login" \
    -H "Content-Type: application/json" \
    -d '{"admin_name":"admin","admin_pass":"admin123"}' \
    -w "%{http_code}")

http_code="${login_response: -3}"
response_body="${login_response%???}"

if [ "$http_code" = "200" ]; then
    echo -e "   ${GREEN}✓ 管理員登錄成功${NC}"
    
    # 提取 token
    token=$(echo "$response_body" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)
    
    if [ -n "$token" ]; then
        echo -e "   ${GREEN}✓ Token 提取成功${NC}"
        
        # 測試需要認證的接口
        echo -e "${BLUE}5. 測試管理員個人信息接口...${NC}"
        profile_response=$(curl -s -w "%{http_code}" -o /tmp/profile.json \
            -H "Authorization: $token" \
            "$BASE_URL/api/admin/profile")
        
        if [ "$profile_response" = "200" ]; then
            echo -e "   ${GREEN}✓ 管理員個人信息接口正常${NC}"
        else
            echo -e "   ${RED}✗ 管理員個人信息接口異常 (HTTP $profile_response)${NC}"
        fi
    else
        echo -e "   ${RED}✗ Token 提取失敗${NC}"
    fi
else
    echo -e "   ${RED}✗ 管理員登錄失敗 (HTTP $http_code)${NC}"
    echo "   響應內容: $response_body"
fi

# 測試 Swagger 文檔
echo -e "${BLUE}6. 測試 Swagger 文檔...${NC}"
swagger_response=$(curl -s -w "%{http_code}" -o /dev/null "$BASE_URL/api/docs")
if [ "$swagger_response" = "200" ]; then
    echo -e "   ${GREEN}✓ Swagger 文檔正常${NC}"
else
    echo -e "   ${RED}✗ Swagger 文檔異常 (HTTP $swagger_response)${NC}"
fi

echo ""
echo -e "${BLUE}===========================================${NC}"
echo -e "${GREEN}  測試完成！${NC}"
echo -e "${BLUE}===========================================${NC}"
echo ""

echo -e "${BLUE}服務訪問地址：${NC}"
echo -e "  🌐 API 主頁:    ${GREEN}http://localhost:8000${NC}"
echo -e "  📖 API 文檔:    ${GREEN}http://localhost:8000/api/docs${NC}"
echo -e "  🏥 健康檢查:    ${GREEN}http://localhost:8000/health${NC}"
echo -e "  🗄️  數據庫管理: ${GREEN}http://localhost:8080${NC}"

echo ""
echo -e "${BLUE}清理臨時文件...${NC}"
rm -f /tmp/health.json /tmp/lab.json /tmp/profile.json

echo -e "${GREEN}測試腳本執行完成！${NC}"