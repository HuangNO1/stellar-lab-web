#!/bin/bash

# 從 .env 文件讀取端口配置的輔助函數
load_env_ports() {
    if [[ -f ".env" ]]; then
        # 讀取端口配置，使用默認值作為備用
        export FRONTEND_PORT=$(grep "^FRONTEND_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "3000")
        export BACKEND_PORT=$(grep "^BACKEND_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "8000")
        export MYSQL_PORT=$(grep "^MYSQL_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "3307")
        export PHPMYADMIN_PORT=$(grep "^PHPMYADMIN_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "8081")
        
        log_info "從 .env 讀取端口配置: 前端=$FRONTEND_PORT, 後端=$BACKEND_PORT"
    else
        # 使用默認值
        export FRONTEND_PORT="3000"
        export BACKEND_PORT="8000" 
        export MYSQL_PORT="3307"
        export PHPMYADMIN_PORT="8081"
        
        log_warning ".env 文件不存在，使用默認端口"
    fi
}