#!/bin/bash
echo "=== Docker 網絡調試腳本 ==="

echo "1. 檢查網絡列表:"
docker network ls | grep lab_web

echo -e "\n2. 檢查網絡詳情:"
docker network inspect lab_web_default

echo -e "\n3. 檢查容器網絡:"
docker ps --format "table {{.Names}}\t{{.Networks}}\t{{.Status}}"

echo -e "\n4. 測試從前端容器解析後端主機名:"
if docker ps -q --filter "name=lab_web_frontend" | grep -q .; then
    echo "嘗試從前端容器內解析 'backend' 主機名:"
    docker exec lab_web_frontend nslookup backend 2>/dev/null || echo "nslookup 不可用，嘗試 ping:"
    docker exec lab_web_frontend ping -c 1 backend 2>/dev/null || echo "無法 ping backend"
else
    echo "前端容器未運行"
fi

echo -e "\n5. 檢查後端容器 IP:"
if docker ps -q --filter "name=lab_web_backend" | grep -q .; then
    backend_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' lab_web_backend)
    echo "後端容器 IP: $backend_ip"
else
    echo "後端容器未運行"
fi