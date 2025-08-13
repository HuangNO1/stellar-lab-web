#!/bin/bash

# 實驗室網頁框架 Docker 一鍵部署腳本
# 使用方法: ./deploy.sh [start|stop|restart|logs|status]

set -e

COMPOSE_FILE="docker-compose.yml"
PROJECT_NAME="lab_web"

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日誌函數
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查 Docker 和 Docker Compose
check_requirements() {
    log_info "檢查系統要求..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安裝或不在 PATH 中"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安裝或不在 PATH 中"
        exit 1
    fi
    
    log_success "系統要求檢查通過"
}

# 檢查文件
check_files() {
    log_info "檢查必需文件..."
    
    required_files=("Dockerfile" "docker-compose.yml" "docker-entrypoint.sh" ".env.docker")
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "缺少必需文件: $file"
            exit 1
        fi
    done
    
    log_success "所有必需文件檢查通過"
}

# 啟動服務
start_services() {
    log_info "啟動實驗室網頁框架服務..."
    
    # 確保腳本執行權限
    chmod +x docker-entrypoint.sh
    
    # 停止並清理現有容器（如果存在）
    log_info "清理現有容器..."
    docker-compose --project-name $PROJECT_NAME down 2>/dev/null || true
    
    # 構建並啟動服務
    log_info "構建並啟動服務..."
    docker-compose --project-name $PROJECT_NAME up --build -d
    
    if [ $? -ne 0 ]; then
        log_error "Docker Compose 啟動失敗"
        log_info "查看詳細錯誤日誌："
        docker-compose --project-name $PROJECT_NAME logs
        exit 1
    fi
    
    log_info "等待服務啟動完成..."
    sleep 15
    
    # 檢查服務狀態
    log_info "檢查服務狀態..."
    if docker-compose --project-name $PROJECT_NAME ps | grep -q "Up"; then
        log_success "服務啟動成功！"
        show_urls
    else
        log_error "服務啟動失敗，請查看日誌："
        docker-compose --project-name $PROJECT_NAME ps
        echo ""
        log_info "詳細日誌："
        docker-compose --project-name $PROJECT_NAME logs --tail=50
        exit 1
    fi
}

# 停止服務
stop_services() {
    log_info "停止實驗室網頁框架服務..."
    docker-compose --project-name $PROJECT_NAME down
    log_success "服務已停止"
}

# 重啟服務
restart_services() {
    log_info "重啟實驗室網頁框架服務..."
    stop_services
    sleep 2
    start_services
}

# 顯示日誌
show_logs() {
    log_info "顯示服務日誌..."
    docker-compose --project-name $PROJECT_NAME logs -f
}

# 顯示狀態
show_status() {
    log_info "服務狀態："
    docker-compose --project-name $PROJECT_NAME ps
    
    echo ""
    log_info "數據卷："
    docker volume ls | grep $PROJECT_NAME || echo "沒有找到相關數據卷"
    
    echo ""
    log_info "網絡："
    docker network ls | grep $PROJECT_NAME || echo "沒有找到相關網絡"
}

# 顯示訪問URLs
show_urls() {
    echo ""
    log_success "=========================================="
    log_success "  實驗室網頁框架部署成功！"
    log_success "=========================================="
    echo ""
    log_info "服務訪問地址："
    echo -e "  🌐 後端API:     ${GREEN}http://localhost:${BACKEND_PORT:-8000}${NC}"
    echo -e "  📖 API文檔:     ${GREEN}http://localhost:${BACKEND_PORT:-8000}/api/docs${NC}"
    echo -e "  🗄️  數據庫管理:  ${GREEN}http://localhost:${PHPMYADMIN_PORT:-8081}${NC}"
    echo ""
    log_info "默認管理員賬戶："
    echo -e "  👤 用戶名: ${YELLOW}admin${NC}"
    echo -e "  🔑 密碼:   ${YELLOW}admin123${NC}"
    echo ""
    log_info "常用命令："
    echo -e "  查看日誌: ${BLUE}./deploy.sh logs${NC}"
    echo -e "  查看狀態: ${BLUE}./deploy.sh status${NC}"
    echo -e "  停止服務: ${BLUE}./deploy.sh stop${NC}"
    echo ""
}

# 主函數
main() {
    case "${1:-start}" in
        start)
            check_requirements
            check_files
            start_services
            ;;
        stop)
            stop_services
            ;;
        restart)
            check_requirements
            restart_services
            ;;
        logs)
            show_logs
            ;;
        status)
            show_status
            ;;
        *)
            echo "使用方法: $0 [start|stop|restart|logs|status]"
            echo ""
            echo "命令說明："
            echo "  start   - 啟動所有服務（默認）"
            echo "  stop    - 停止所有服務"
            echo "  restart - 重啟所有服務"
            echo "  logs    - 查看服務日誌"
            echo "  status  - 查看服務狀態"
            exit 1
            ;;
    esac
}

main "$@"