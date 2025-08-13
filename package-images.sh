#!/bin/bash

# ========================================================
# Docker 鏡像打包和上傳腳本
# 將本地構建的 Docker 鏡像打包並上傳到服務器
# ========================================================

set -e

# 配置
PROJECT_NAME="lab-website"
BACKEND_IMAGE="lab-website-backend"
FRONTEND_IMAGE="lab-website-frontend"
VERSION_TAG="${1:-latest}"
OUTPUT_DIR="./docker-images"

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
Docker 鏡像打包和上傳工具

用法: $0 [版本標籤] [選項]

參數:
  版本標籤           鏡像版本標籤 (默認: latest)

選項:
  --output-dir DIR   指定輸出目錄 (默認: ./docker-images)
  --upload-only      僅上傳，不重新打包
  --package-only     僅打包，不上傳
  --server HOST      服務器地址 (必填，用於上傳)
  --user USER        SSH 用戶名 (默認: root)
  --path PATH        服務器路徑 (默認: /opt/lab_web)
  --help, -h         顯示此幫助信息

上傳方式:
  scp                通過 SCP 上傳 (默認)
  rsync              通過 rsync 上傳

示例:
  $0 latest --server 192.168.1.100                    # 打包並上傳
  $0 v1.0.0 --server example.com --user ubuntu        # 指定用戶
  $0 --package-only                                    # 僅打包鏡像
  $0 --upload-only --server 192.168.1.100             # 僅上傳現有打包

EOF
}

# 解析命令行參數
parse_args() {
    UPLOAD_METHOD="scp"
    PACKAGE_ONLY="false"
    UPLOAD_ONLY="false"
    SERVER=""
    SSH_USER="root"
    SERVER_PATH="/opt/lab_web"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --output-dir)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            --upload-only)
                UPLOAD_ONLY="true"
                shift
                ;;
            --package-only)
                PACKAGE_ONLY="true"
                shift
                ;;
            --server)
                SERVER="$2"
                shift 2
                ;;
            --user)
                SSH_USER="$2"
                shift 2
                ;;
            --path)
                SERVER_PATH="$2"
                shift 2
                ;;
            --rsync)
                UPLOAD_METHOD="rsync"
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
    
    # 驗證參數
    if [[ "$UPLOAD_ONLY" == "false" && "$PACKAGE_ONLY" == "false" ]]; then
        if [[ -z "$SERVER" ]]; then
            log_error "必須指定服務器地址 (--server)"
            echo "使用 --help 查看幫助信息"
            exit 1
        fi
    fi
}

# 檢查環境
check_environment() {
    log_info "檢查打包環境..."
    
    # 檢查 Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安裝"
        exit 1
    fi
    
    # 檢查鏡像是否存在
    if [[ "$UPLOAD_ONLY" == "false" ]]; then
        local backend_exists=$(docker images -q "${BACKEND_IMAGE}:${VERSION_TAG}" 2>/dev/null)
        local frontend_exists=$(docker images -q "${FRONTEND_IMAGE}:${VERSION_TAG}" 2>/dev/null)
        
        if [[ -z "$backend_exists" ]]; then
            log_error "後端鏡像不存在: ${BACKEND_IMAGE}:${VERSION_TAG}"
            log_error "請先運行: ./build-images.sh ${VERSION_TAG}"
            exit 1
        fi
        
        if [[ -z "$frontend_exists" ]]; then
            log_error "前端鏡像不存在: ${FRONTEND_IMAGE}:${VERSION_TAG}"
            log_error "請先運行: ./build-images.sh ${VERSION_TAG}"
            exit 1
        fi
    fi
    
    # 創建輸出目錄
    mkdir -p "$OUTPUT_DIR"
    
    log_success "環境檢查完成"
}

# 打包鏡像
package_images() {
    if [[ "$UPLOAD_ONLY" == "true" ]]; then
        log_info "跳過打包，僅上傳模式"
        return
    fi
    
    log_info "開始打包 Docker 鏡像..."
    
    local start_time=$(date +%s)
    
    # 打包後端鏡像
    log_info "打包後端鏡像..."
    docker save -o "${OUTPUT_DIR}/${BACKEND_IMAGE}-${VERSION_TAG}.tar" \
        "${BACKEND_IMAGE}:${VERSION_TAG}" "${BACKEND_IMAGE}:latest"
    
    # 打包前端鏡像  
    log_info "打包前端鏡像..."
    docker save -o "${OUTPUT_DIR}/${FRONTEND_IMAGE}-${VERSION_TAG}.tar" \
        "${FRONTEND_IMAGE}:${VERSION_TAG}" "${FRONTEND_IMAGE}:latest"
    
    # 壓縮打包文件
    log_info "壓縮鏡像文件..."
    gzip -f "${OUTPUT_DIR}/${BACKEND_IMAGE}-${VERSION_TAG}.tar" &
    gzip -f "${OUTPUT_DIR}/${FRONTEND_IMAGE}-${VERSION_TAG}.tar" &
    wait
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    log_success "鏡像打包完成 (用時: ${duration}秒)"
    
    # 顯示文件信息
    echo ""
    echo "========== 打包文件信息 =========="
    ls -lh "${OUTPUT_DIR}"/*.tar.gz 2>/dev/null || true
    echo "==============================="
    echo ""
}

# 從 .env 文件讀取端口配置
load_env_ports() {
    if [[ -f ".env" ]]; then
        FRONTEND_PORT=$(grep "^FRONTEND_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "3000")
        BACKEND_PORT=$(grep "^BACKEND_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "8000")
        
        log_info "從 .env 讀取端口配置: 前端=$FRONTEND_PORT, 後端=$BACKEND_PORT"
    else
        # 使用默認值
        FRONTEND_PORT="3000"
        BACKEND_PORT="8000"
        
        log_warning ".env 文件不存在，使用默認端口: 前端=$FRONTEND_PORT, 後端=$BACKEND_PORT"
    fi
}

# 創建部署包
create_deployment_package() {
    if [[ "$UPLOAD_ONLY" == "true" ]]; then
        return
    fi
    
    log_info "創建部署包..."
    
    # 創建臨時部署目錄
    local deploy_dir="${OUTPUT_DIR}/deploy"
    mkdir -p "$deploy_dir"
    
    # 加載端口配置
    load_env_ports
    
    # 複製必要文件
    cp .env "$deploy_dir/" 2>/dev/null || log_warning ".env 文件不存在，跳過"
    cp docker-compose.yml "$deploy_dir/"
    cp deploy.sh "$deploy_dir/"
    
    # 創建服務器部署腳本
    cat > "${deploy_dir}/server-deploy.sh" << 'EOF'
#!/bin/bash
# 服務器端部署腳本 - 自動生成

set -e

VERSION_TAG="${1:-latest}"
BACKEND_IMAGE="lab-website-backend"
FRONTEND_IMAGE="lab-website-frontend"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 從 .env 文件讀取端口配置
load_env_ports() {
    if [[ -f ".env" ]]; then
        FRONTEND_PORT=$(grep "^FRONTEND_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "3000")
        BACKEND_PORT=$(grep "^BACKEND_PORT=" .env 2>/dev/null | cut -d'=' -f2 | tr -d ' "' || echo "8000")
        
        log_info "從 .env 讀取端口配置: 前端=$FRONTEND_PORT, 後端=$BACKEND_PORT"
    else
        # 使用默認值
        FRONTEND_PORT="3000"
        BACKEND_PORT="8000"
        
        log_error ".env 文件不存在，使用默認端口: 前端=$FRONTEND_PORT, 後端=$BACKEND_PORT"
    fi
}

echo "=========================================="
echo "       服務器端部署工具"
echo "=========================================="
echo "版本: $VERSION_TAG"
echo "時間: $(date)"
echo ""

# 載入鏡像
load_env_ports
log_info "載入 Docker 鏡像..."
if [ -f "${BACKEND_IMAGE}-${VERSION_TAG}.tar.gz" ]; then
    log_info "載入後端鏡像..."
    gunzip -c "${BACKEND_IMAGE}-${VERSION_TAG}.tar.gz" | docker load
fi

if [ -f "${FRONTEND_IMAGE}-${VERSION_TAG}.tar.gz" ]; then
    log_info "載入前端鏡像..."  
    gunzip -c "${FRONTEND_IMAGE}-${VERSION_TAG}.tar.gz" | docker load
fi

# 停止舊服務
log_info "停止舊服務..."
./deploy.sh prod stop || true

# 啟動服務
log_info "啟動新服務..."
./deploy.sh prod start -d

# 等待服務啟動
sleep 30

# 健康檢查
log_info "健康檢查..."
./deploy.sh prod health

log_success "部署完成！"
echo ""
echo "服務地址:"
echo "  前端: http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR_SERVER_IP'):$FRONTEND_PORT"
echo "  後端: http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR_SERVER_IP'):$BACKEND_PORT"
EOF
    
    chmod +x "${deploy_dir}/server-deploy.sh"
    
    log_success "部署包創建完成"
}

# 上傳到服務器
upload_to_server() {
    if [[ "$PACKAGE_ONLY" == "true" ]]; then
        log_info "僅打包模式，跳過上傳"
        return
    fi
    
    log_info "上傳到服務器 ${SSH_USER}@${SERVER}:${SERVER_PATH}..."
    
    # 測試 SSH 連接
    if ! ssh -o ConnectTimeout=10 "${SSH_USER}@${SERVER}" "echo 'SSH 連接測試成功'" 2>/dev/null; then
        log_error "無法連接到服務器 ${SSH_USER}@${SERVER}"
        log_error "請檢查："
        echo "  1. SSH 密鑰是否配置正確"
        echo "  2. 服務器地址是否正確"
        echo "  3. 網絡連接是否正常"
        exit 1
    fi
    
    # 創建服務器目錄
    ssh "${SSH_USER}@${SERVER}" "mkdir -p ${SERVER_PATH}"
    
    local start_time=$(date +%s)
    
    case "$UPLOAD_METHOD" in
        "rsync")
            log_info "使用 rsync 上傳..."
            rsync -avz --progress "${OUTPUT_DIR}/"*.tar.gz "${SSH_USER}@${SERVER}:${SERVER_PATH}/"
            rsync -avz --progress "${OUTPUT_DIR}/deploy/" "${SSH_USER}@${SERVER}:${SERVER_PATH}/"
            ;;
        *)
            log_info "使用 SCP 上傳..."
            scp "${OUTPUT_DIR}"/*.tar.gz "${SSH_USER}@${SERVER}:${SERVER_PATH}/"
            scp -r "${OUTPUT_DIR}/deploy/"* "${SSH_USER}@${SERVER}:${SERVER_PATH}/"
            ;;
    esac
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    log_success "上傳完成 (用時: ${duration}秒)"
    
    echo ""
    log_info "在服務器上運行以下命令完成部署:"
    echo ""
    echo "  ssh ${SSH_USER}@${SERVER}"
    echo "  cd ${SERVER_PATH}"
    echo "  chmod +x server-deploy.sh"
    echo "  ./server-deploy.sh ${VERSION_TAG}"
    echo ""
}

# 清理臨時文件
cleanup() {
    log_info "清理臨時文件..."
    rm -rf "${OUTPUT_DIR}/deploy" 2>/dev/null || true
    log_success "清理完成"
}

# 主執行函數
main() {
    echo "=========================================="
    echo "       Docker 鏡像打包上傳工具"
    echo "=========================================="
    echo "版本標籤: $VERSION_TAG"
    echo "輸出目錄: $OUTPUT_DIR"
    if [[ -n "$SERVER" ]]; then
        echo "目標服務器: ${SSH_USER}@${SERVER}:${SERVER_PATH}"
    fi
    echo "開始時間: $(date)"
    echo ""
    
    parse_args "$@"
    check_environment
    
    local total_start_time=$(date +%s)
    
    package_images
    create_deployment_package
    upload_to_server
    
    local total_end_time=$(date +%s)
    local total_duration=$((total_end_time - total_start_time))
    
    cleanup
    
    echo ""
    echo "總處理時間: ${total_duration}秒"
    log_success "任務完成！"
}

# 執行主函數
main "$@"