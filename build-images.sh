#!/bin/bash

# ========================================================
# 本地 Docker 鏡像構建腳本
# 用於在本地構建所有 Docker 鏡像，避免在服務器上耗時構建
# ========================================================

set -e

# 配置
PROJECT_NAME="lab-website"
BACKEND_IMAGE="lab-website-backend"
FRONTEND_IMAGE="lab-website-frontend"
VERSION_TAG="${1:-latest}"

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
本地 Docker 鏡像構建工具

用法: $0 [版本標籤] [選項]

參數:
  版本標籤           鏡像版本標籤 (默認: latest)

選項:
  --no-cache        不使用緩存構建
  --backend-only    僅構建後端鏡像
  --frontend-only   僅構建前端鏡像
  --help, -h        顯示此幫助信息

示例:
  $0                          # 構建 latest 版本
  $0 v1.0.0                   # 構建 v1.0.0 版本
  $0 --no-cache               # 無緩存構建
  $0 latest --backend-only    # 僅構建後端

EOF
}

# 解析命令行參數
parse_args() {
    NO_CACHE=""
    BUILD_TARGET=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-cache)
                NO_CACHE="--no-cache"
                shift
                ;;
            --backend-only)
                BUILD_TARGET="backend"
                shift
                ;;
            --frontend-only)
                BUILD_TARGET="frontend"
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
                fi
                shift
                ;;
        esac
    done
}

# 檢查環境
check_environment() {
    log_info "檢查構建環境..."
    
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
    
    # 檢查必要文件
    local required_files=(
        "backend/Dockerfile"
        "frontend/Dockerfile" 
        "docker-compose.yml"
        ".env"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "缺少必要文件: $file"
            exit 1
        fi
    done
    
    log_success "環境檢查完成"
}

# 構建後端鏡像
build_backend() {
    log_info "構建後端鏡像..."
    
    cd backend
    
    local start_time=$(date +%s)
    
    docker build $NO_CACHE \
        -t "${BACKEND_IMAGE}:${VERSION_TAG}" \
        -t "${BACKEND_IMAGE}:latest" \
        .
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    cd ..
    
    log_success "後端鏡像構建完成 (用時: ${duration}秒)"
    docker images | grep "$BACKEND_IMAGE"
}

# 構建前端鏡像
build_frontend() {
    log_info "構建前端鏡像..."
    
    cd frontend
    
    local start_time=$(date +%s)
    
    docker build $NO_CACHE \
        -t "${FRONTEND_IMAGE}:${VERSION_TAG}" \
        -t "${FRONTEND_IMAGE}:latest" \
        .
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    cd ..
    
    log_success "前端鏡像構建完成 (用時: ${duration}秒)"
    docker images | grep "$FRONTEND_IMAGE"
}

# 構建所有鏡像
build_all() {
    case "$BUILD_TARGET" in
        "backend")
            build_backend
            ;;
        "frontend")
            build_frontend
            ;;
        *)
            build_backend
            build_frontend
            ;;
    esac
}

# 顯示構建結果
show_results() {
    log_info "構建完成，鏡像列表:"
    echo ""
    echo "========== 本地鏡像 ==========="
    docker images | grep -E "(${BACKEND_IMAGE}|${FRONTEND_IMAGE})"
    echo "=============================="
    echo ""
    
    # 計算鏡像大小
    local backend_size=$(docker images --format "{{.Size}}" "${BACKEND_IMAGE}:${VERSION_TAG}" 2>/dev/null || echo "未構建")
    local frontend_size=$(docker images --format "{{.Size}}" "${FRONTEND_IMAGE}:${VERSION_TAG}" 2>/dev/null || echo "未構建")
    
    echo "鏡像信息:"
    echo "  後端鏡像: ${BACKEND_IMAGE}:${VERSION_TAG} (${backend_size})"
    echo "  前端鏡像: ${FRONTEND_IMAGE}:${VERSION_TAG} (${frontend_size})"
    echo ""
    
    log_success "下一步可運行: ./package-images.sh ${VERSION_TAG}"
}

# 主執行函數
main() {
    echo "=========================================="
    echo "       本地 Docker 鏡像構建工具"
    echo "=========================================="
    echo "構建版本: $VERSION_TAG"
    echo "開始時間: $(date)"
    echo ""
    
    parse_args "$@"
    check_environment
    
    local total_start_time=$(date +%s)
    
    build_all
    
    local total_end_time=$(date +%s)
    local total_duration=$((total_end_time - total_start_time))
    
    echo ""
    echo "總構建時間: ${total_duration}秒"
    
    show_results
}

# 執行主函數
main "$@"