#!/bin/bash

# ========================================================
# 服務器快速部署腳本
# 用於在服務器上快速部署預構建的 Docker 鏡像
# ========================================================

set -e

# 配置
BACKEND_IMAGE="lab-website-backend"
FRONTEND_IMAGE="lab-website-frontend"
VERSION_TAG="${1:-latest}"
COMPOSE_PROJECT_NAME="lab_web"

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日誌函數
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 顯示幫助信息
show_help() {
    cat << EOF
服務器快速部署工具

用法: $0 [版本標籤] [選項]

參數:
  版本標籤           鏡像版本標籤 (默認: latest)

選項:
  --no-health-check  跳過健康檢查
  --keep-old         保留舊鏡像
  --force-recreate   強制重新創建容器
  --china            使用中國鏡像源加速（適用於中國服務器）
  --help, -h         顯示此幫助信息

部署流程:
  1. 載入 Docker 鏡像
  2. 停止舊服務
  3. 清理舊容器
  4. 啟動新服務
  5. 健康檢查

示例:
  $0                    # 部署 latest 版本
  $0 v1.0.0            # 部署 v1.0.0 版本
  $0 --no-health-check # 跳過健康檢查
  $0 --china           # 使用中國鏡像源加速

EOF
}

# 解析命令行參數
parse_args() {
    HEALTH_CHECK="true"
    KEEP_OLD="false"
    FORCE_RECREATE=""
    USE_CHINA_MIRROR="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-health-check)
                HEALTH_CHECK="false"
                shift
                ;;
            --keep-old)
                KEEP_OLD="true"
                shift
                ;;
            --force-recreate)
                FORCE_RECREATE="--force-recreate"
                shift
                ;;
            --china)
                USE_CHINA_MIRROR="true"
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                if [[ "$1" =~ ^- ]]; then
                    log_error "未知選項: $1"
                    exit 1
                else
                    # 這是版本標籤，保存它
                    VERSION_TAG="$1"
                fi
                shift
                ;;
        esac
    done
}

# 從 .env 文件讀取端口配置
load_env_ports() {
    if [[ -f ".env" ]]; then
        # 讀取端口配置，使用默認值作為備用
        FRONTEND_PORT=$(grep "^FRONTEND_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "3000")
        BACKEND_PORT=$(grep "^BACKEND_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "8000")
        MYSQL_PORT=$(grep "^MYSQL_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "3306")
        PHPMYADMIN_PORT=$(grep "^PHPMYADMIN_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "8081")
        
        log_info "從 .env 讀取端口配置: 前端=$FRONTEND_PORT, 後端=$BACKEND_PORT"
    else
        # 使用默認值
        FRONTEND_PORT="3000"
        BACKEND_PORT="8000"
        MYSQL_PORT="3306" 
        PHPMYADMIN_PORT="8081"
        
        log_warning ".env 文件不存在，使用默認端口: 前端=$FRONTEND_PORT, 後端=$BACKEND_PORT"
    fi
}

# 檢查環境
check_environment() {
    log_info "檢查部署環境..."
    
    # 加載端口配置
    load_env_ports
    
    # 檢查 Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安裝"
        exit 1
    fi
    
    # 檢查 Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安裝"
        exit 1
    fi
    
    # 檢查 Docker 服務
    if ! docker info &>/dev/null; then
        log_error "Docker 守護進程未運行"
        exit 1
    fi
    
    # 配置中國鏡像源（如果指定）
    if [[ "$USE_CHINA_MIRROR" == "true" ]]; then
        setup_docker_mirrors
    fi
    
    # 檢查必要文件
    local required_files=("docker-compose.yml" ".env")
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "缺少必要文件: $file"
            exit 1
        fi
    done
    
    log_success "環境檢查完成"
}

# 配置 Docker 鏡像加速器
setup_docker_mirrors() {
    log_info "配置 Docker 鏡像加速器..."
    
    # 備份原配置
    if [ -f /etc/docker/daemon.json ]; then
        log_info "備份原有 Docker 配置..."
        cp /etc/docker/daemon.json /etc/docker/daemon.json.backup.$(date +%Y%m%d_%H%M%S)
    fi
    
    # 創建 Docker 配置目錄
    mkdir -p /etc/docker
    
    # 配置鏡像加速器
    cat > /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn", 
    "https://reg-mirror.qiniu.com",
    "https://hub-mirror.c.163.com"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  },
  "insecure-registries": [],
  "exec-opts": ["native.cgroupdriver=systemd"],
  "live-restore": true
}
EOF
    
    # 重啟 Docker 服務
    log_info "重啟 Docker 服務應用配置..."
    systemctl daemon-reload
    systemctl restart docker
    
    # 等待 Docker 啟動
    sleep 5
    
    # 驗證配置
    if docker info | grep -A 10 "Registry Mirrors" | grep -q "mirror" 2>/dev/null; then
        log_success "Docker 鏡像加速器配置成功"
    else
        log_warning "無法確認鏡像加速器是否生效，但配置文件已更新"
    fi
}

# 載入 Docker 鏡像
load_images() {
    log_info "載入 Docker 鏡像..."
    
    local images_loaded=0
    
    # 載入後端鏡像
    local backend_file="${BACKEND_IMAGE}-${VERSION_TAG}.tar.gz"
    if [[ -f "$backend_file" ]]; then
        log_info "載入後端鏡像: $backend_file"
        gunzip -c "$backend_file" | docker load
        images_loaded=$((images_loaded + 1))
    else
        log_warning "後端鏡像文件不存在: $backend_file"
    fi
    
    # 載入前端鏡像
    local frontend_file="${FRONTEND_IMAGE}-${VERSION_TAG}.tar.gz"
    if [[ -f "$frontend_file" ]]; then
        log_info "載入前端鏡像: $frontend_file"
        gunzip -c "$frontend_file" | docker load
        images_loaded=$((images_loaded + 1))
    else
        log_warning "前端鏡像文件不存在: $frontend_file"
    fi
    
    if [[ $images_loaded -eq 0 ]]; then
        log_error "沒有找到任何鏡像文件"
        exit 1
    fi
    
    log_success "成功載入 $images_loaded 個鏡像"
    
    # 顯示載入的鏡像
    echo ""
    echo "========== 載入的鏡像 =========="
    docker images | grep -E "(${BACKEND_IMAGE}|${FRONTEND_IMAGE})" | head -10
    echo "============================="
    echo ""
}

# 停止舊服務
stop_old_services() {
    log_info "停止舊服務..."
    
    # 檢查是否有運行中的服務
    if docker-compose -p "$COMPOSE_PROJECT_NAME" ps -q | grep -q .; then
        docker-compose -p "$COMPOSE_PROJECT_NAME" down
        log_success "舊服務已停止"
    else
        log_info "沒有運行中的服務"
    fi
}

# 清理舊鏡像和容器
cleanup_old_resources() {
    if [[ "$KEEP_OLD" == "true" ]]; then
        log_info "保留舊資源模式，跳過清理"
        return
    fi
    
    log_info "清理舊資源..."
    
    # 清理停止的容器
    local stopped_containers=$(docker ps -aq -f status=exited)
    if [[ -n "$stopped_containers" ]]; then
        docker rm $stopped_containers 2>/dev/null || true
        log_info "已清理停止的容器"
    fi
    
    # 清理懸掛鏡像
    local dangling_images=$(docker images -q -f dangling=true)
    if [[ -n "$dangling_images" ]]; then
        docker rmi $dangling_images 2>/dev/null || true
        log_info "已清理懸掛鏡像"
    fi
    
    log_success "資源清理完成"
}

# 啟動新服務
start_new_services() {
    log_info "啟動新服務..."
    
    # 啟動服務
    docker-compose -p "$COMPOSE_PROJECT_NAME" up -d $FORCE_RECREATE
    
    log_success "服務啟動完成"
    
    # 等待服務啟動
    log_info "等待服務完全啟動..."
    sleep 30
}

# 健康檢查
health_check() {
    if [[ "$HEALTH_CHECK" == "false" ]]; then
        log_info "跳過健康檢查"
        return
    fi
    
    log_info "執行健康檢查..."
    
    local health_ok=true
    
    # 檢查容器狀態
    echo ""
    echo "========== 容器狀態 =========="
    docker-compose -p "$COMPOSE_PROJECT_NAME" ps
    echo "============================"
    echo ""
    
    # 前端健康檢查
    log_info "檢查前端服務..."
    if curl -sf http://localhost:$FRONTEND_PORT > /dev/null 2>&1; then
        log_success "✓ 前端服務 ($FRONTEND_PORT) - 正常"
    else
        log_error "✗ 前端服務 ($FRONTEND_PORT) - 異常"
        health_ok=false
    fi
    
    # 後端健康檢查
    log_info "檢查後端服務..."
    if curl -sf http://localhost:$BACKEND_PORT/health > /dev/null 2>&1; then
        log_success "✓ 後端服務 ($BACKEND_PORT) - 正常"
    else
        log_error "✗ 後端服務 ($BACKEND_PORT) - 異常"
        health_ok=false
    fi
    
    # 資料庫健康檢查
    log_info "檢查資料庫服務..."
    if docker-compose -p "$COMPOSE_PROJECT_NAME" exec -T db mysqladmin ping -h"localhost" --silent > /dev/null 2>&1; then
        log_success "✓ 資料庫服務 - 正常"
    else
        log_warning "⚠ 資料庫服務 - 可能還在啟動中"
    fi
    
    if [[ "$health_ok" == "true" ]]; then
        log_success "所有核心服務健康檢查通過"
    else
        log_error "部分服務健康檢查失敗"
        echo ""
        log_info "查看服務日誌："
        echo "  docker-compose -p $COMPOSE_PROJECT_NAME logs frontend"
        echo "  docker-compose -p $COMPOSE_PROJECT_NAME logs backend"
    fi
}

# 顯示部署結果
show_deployment_result() {
    local public_ip=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "YOUR_SERVER_IP")
    
    echo ""
    echo "=========================================="
    echo "           部署完成！"
    echo "=========================================="
    echo "🌐 前端訪問: http://$public_ip:$FRONTEND_PORT"
    echo "🔌 後端 API: http://$public_ip:$BACKEND_PORT"
    echo "📚 API 文檔: http://$public_ip:$BACKEND_PORT/api/docs"
    echo "🗄️ 資料庫管理: http://$public_ip:$PHPMYADMIN_PORT"
    echo ""
    echo "👤 預設管理員帳號:"
    echo "   用戶名: admin"
    echo "   密碼: admin123"
    echo ""
    echo "🔧 常用命令:"
    echo "   查看狀態: docker-compose -p $COMPOSE_PROJECT_NAME ps"
    echo "   查看日誌: docker-compose -p $COMPOSE_PROJECT_NAME logs -f"
    echo "   重啟服務: docker-compose -p $COMPOSE_PROJECT_NAME restart"
    echo "   停止服務: docker-compose -p $COMPOSE_PROJECT_NAME down"
    echo ""
    echo "⚠️ 重要提醒:"
    echo "1. 請立即修改預設管理員密碼"
    echo "2. 請檢查防火牆設置"
    echo "3. 建議設置域名和 SSL 證書"
    echo "=========================================="
}

# 清理打包文件
cleanup_package_files() {
    log_info "清理打包文件..."
    
    local files_to_remove=(
        "${BACKEND_IMAGE}-${VERSION_TAG}.tar.gz"
        "${FRONTEND_IMAGE}-${VERSION_TAG}.tar.gz"
    )
    
    for file in "${files_to_remove[@]}"; do
        if [[ -f "$file" ]]; then
            read -p "是否刪除 $file？(y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                rm -f "$file"
                log_success "已刪除 $file"
            fi
        fi
    done
}

# 主執行函數
main() {
    echo "=========================================="
    echo "       服務器快速部署工具"
    echo "=========================================="
    echo "版本標籤: $VERSION_TAG"
    echo "項目名稱: $COMPOSE_PROJECT_NAME"
    echo "開始時間: $(date)"
    echo ""
    
    parse_args "$@"
    check_environment
    
    local total_start_time=$(date +%s)
    
    load_images
    stop_old_services
    cleanup_old_resources
    start_new_services
    health_check
    
    local total_end_time=$(date +%s)
    local total_duration=$((total_end_time - total_start_time))
    
    show_deployment_result
    
    echo ""
    echo "總部署時間: ${total_duration}秒"
    log_success "部署任務完成！"
    
    cleanup_package_files
}

# 執行主函數
main "$@"