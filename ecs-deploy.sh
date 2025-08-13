#!/bin/bash

# ========================================================
# 實驗室網站 ECS 統一部署腳本
# 支持多種部署方式：Git、壓縮包、本地項目
# 支持多種系統：Ubuntu、CentOS、OpenCloudOS 等
# ========================================================

set -e

# 默認配置
PROJECT_DIR="/opt/lab_web"
LOG_FILE="/tmp/lab_web_deploy.log"
GITHUB_REPO=""
ARCHIVE_PATH=""
DEPLOY_MODE=""
USE_CHINA_MIRROR=false

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日誌函數
log_info() { echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"; }

# 顯示幫助信息
show_help() {
    cat << EOF
實驗室網站 ECS 部署工具

用法: $0 [OPTIONS] <MODE>

部署模式:
  git <repo_url>     從 Git 倉庫克隆部署
  archive [path]     從壓縮包部署 (默認路径: /opt/lab_web_deploy.tar.gz)
  local              部署已存在的本地項目

選項:
  -h, --help         顯示此幫助信息
  -d, --dir <path>   指定項目目錄 (默認: /opt/lab_web)
  -l, --log <path>   指定日誌文件 (默認: /tmp/lab_web_deploy.log)
  -c, --china        使用中國大陸鏡像源優化
  --no-firewall      跳過防火牆配置
  --no-service       跳過系統服務創建

示例:
  $0 git https://github.com/user/lab_web.git
  $0 archive /root/lab_web_deploy.tar.gz
  $0 local -d /home/user/lab_web
  $0 archive --china

EOF
}

# 解析命令行參數
parse_args() {
    SKIP_FIREWALL=false
    SKIP_SERVICE=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -d|--dir)
                PROJECT_DIR="$2"
                shift 2
                ;;
            -l|--log)
                LOG_FILE="$2"
                shift 2
                ;;
            -c|--china)
                USE_CHINA_MIRROR=true
                shift
                ;;
            --no-firewall)
                SKIP_FIREWALL=true
                shift
                ;;
            --no-service)
                SKIP_SERVICE=true
                shift
                ;;
            git)
                DEPLOY_MODE="git"
                GITHUB_REPO="$2"
                if [ -z "$GITHUB_REPO" ]; then
                    log_error "Git 模式需要提供倉庫 URL"
                    exit 1
                fi
                shift 2
                ;;
            archive)
                DEPLOY_MODE="archive"
                if [[ -n "$2" && ! "$2" =~ ^- ]]; then
                    ARCHIVE_PATH="$2"
                    shift 2
                else
                    ARCHIVE_PATH="/opt/lab_web_deploy.tar.gz"
                    shift
                fi
                ;;
            local)
                DEPLOY_MODE="local"
                shift
                ;;
            *)
                log_error "未知參數: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    if [ -z "$DEPLOY_MODE" ]; then
        log_error "必須指定部署模式"
        show_help
        exit 1
    fi
}

# 檢查系統環境
check_system() {
    log_info "檢查系統環境..."
    
    echo "========== 系統信息 ==========" | tee -a "$LOG_FILE"
    echo "主機名: $(hostname)" | tee -a "$LOG_FILE"
    echo "操作系統: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)" | tee -a "$LOG_FILE"
    echo "內核版本: $(uname -r)" | tee -a "$LOG_FILE"
    echo "CPU 信息: $(nproc) 核心" | tee -a "$LOG_FILE"
    echo "內存信息: $(free -h | awk 'NR==2{print $2}')" | tee -a "$LOG_FILE"
    echo "磁盤信息: $(df -h / | awk 'NR==2{print $2 " 總計, " $4 " 可用"}')" | tee -a "$LOG_FILE"
    
    # 嘗試獲取公網IP
    PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "無法獲取")
    echo "公網IP: $PUBLIC_IP" | tee -a "$LOG_FILE"
    echo "=============================" | tee -a "$LOG_FILE"
    
    # 檢查資源
    TOTAL_MEM=$(free -m | awk 'NR==2{print $2}')
    AVAILABLE_DISK=$(df / | awk 'NR==2{print $4}')
    
    if [ "$TOTAL_MEM" -lt 1024 ]; then
        log_warning "內存少於 1GB，可能影響性能"
    fi
    
    if [ "$AVAILABLE_DISK" -lt 5242880 ]; then  # 5GB in KB
        log_warning "可用磁盤空間少於 5GB，可能不足"
    fi
    
    log_success "系統環境檢查完成"
}

# 檢測系統類型
detect_system() {
    if grep -qi "opencloudos" /etc/os-release 2>/dev/null; then
        SYSTEM="opencloudos"
    elif [ -f /etc/centos-release ] || [ -f /etc/redhat-release ]; then
        SYSTEM="centos"
    elif [ -f /etc/debian_version ]; then
        SYSTEM="ubuntu"
    elif command -v dnf &> /dev/null; then
        SYSTEM="fedora"
    elif command -v yum &> /dev/null; then
        SYSTEM="centos"
    elif command -v apt &> /dev/null; then
        SYSTEM="ubuntu"
    else
        SYSTEM="unknown"
    fi
    
    log_info "檢測到系統類型: $SYSTEM"
}

# 更新系統
update_system() {
    log_info "更新系統套件..."
    
    detect_system
    
    case $SYSTEM in
        opencloudos|centos|fedora)
            if [ "$USE_CHINA_MIRROR" = true ] && [ "$SYSTEM" = "centos" ]; then
                setup_china_yum_repos
            fi
            
            if command -v dnf &> /dev/null; then
                dnf update -y
                dnf install -y git curl wget vim unzip net-tools tar gzip which
            elif command -v yum &> /dev/null; then
                yum update -y
                yum install -y git curl wget vim unzip net-tools tar gzip which
            fi
            ;;
        ubuntu)
            if [ "$USE_CHINA_MIRROR" = true ]; then
                setup_china_apt_repos
            fi
            apt update && apt upgrade -y
            apt install -y git curl wget vim unzip net-tools tar gzip
            ;;
        *)
            log_error "不支持的系統類型: $SYSTEM"
            exit 1
            ;;
    esac
    
    log_success "系統更新完成"
}

# 配置中國大陸 yum 鏡像源
setup_china_yum_repos() {
    log_info "配置阿里雲 YUM 鏡像源..."
    
    mkdir -p /etc/yum.repos.d/backup
    mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/backup/ 2>/dev/null || true
    
    cat > /etc/yum.repos.d/CentOS-Base.repo << 'EOF'
[base]
name=CentOS-$releasever - Base - mirrors.aliyun.com
baseurl=http://mirrors.aliyun.com/centos/$releasever/os/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7

[updates]
name=CentOS-$releasever - Updates - mirrors.aliyun.com
baseurl=http://mirrors.aliyun.com/centos/$releasever/updates/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7

[extras]
name=CentOS-$releasever - Extras - mirrors.aliyun.com
baseurl=http://mirrors.aliyun.com/centos/$releasever/extras/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
EOF
    
    yum clean all && yum makecache
}

# 配置中國大陸 apt 鏡像源
setup_china_apt_repos() {
    log_info "配置阿里雲 APT 鏡像源..."
    
    cp /etc/apt/sources.list /etc/apt/sources.list.backup
    
    cat > /etc/apt/sources.list << 'EOF'
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
EOF
    
    apt update
}

# 準備項目文件
prepare_project() {
    case $DEPLOY_MODE in
        git)
            prepare_git_project
            ;;
        archive)
            prepare_archive_project
            ;;
        local)
            prepare_local_project
            ;;
    esac
}

# Git 方式準備項目
prepare_git_project() {
    log_info "從 Git 倉庫克隆項目..."
    
    if [[ "$GITHUB_REPO" == *"YOUR_USERNAME"* ]]; then
        log_error "請提供有效的 Git 倉庫地址"
        exit 1
    fi
    
    mkdir -p $(dirname "$PROJECT_DIR")
    
    if [ -d "$PROJECT_DIR" ]; then
        log_warning "項目目錄已存在，創建備份..."
        mv "$PROJECT_DIR" "${PROJECT_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
    fi
    
    git clone "$GITHUB_REPO" "$PROJECT_DIR"
    
    cd "$PROJECT_DIR"
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        log_warning "請編輯 .env 文件配置環境變數"
    else
        log_error "未找到 .env.example 文件"
        exit 1
    fi
    
    log_success "Git 項目準備完成"
}

# 壓縮包方式準備項目
prepare_archive_project() {
    log_info "從壓縮包準備項目..."
    
    # 檢查壓縮包
    if [ ! -f "$ARCHIVE_PATH" ]; then
        # 嘗試其他位置
        for path in "/root/lab_web_deploy.tar.gz" "./lab_web_deploy.tar.gz"; do
            if [ -f "$path" ]; then
                ARCHIVE_PATH="$path"
                break
            fi
        done
        
        if [ ! -f "$ARCHIVE_PATH" ]; then
            log_error "找不到壓縮包文件"
            echo "請確保壓縮包位於以下位置之一："
            echo "  - $ARCHIVE_PATH"
            echo "  - /root/lab_web_deploy.tar.gz"
            echo "  - ./lab_web_deploy.tar.gz"
            exit 1
        fi
    fi
    
    log_info "找到壓縮包: $ARCHIVE_PATH ($(du -h $ARCHIVE_PATH | cut -f1))"
    
    # 備份舊目錄
    if [ -d "$PROJECT_DIR" ]; then
        log_warning "項目目錄已存在，創建備份..."
        mv "$PROJECT_DIR" "${PROJECT_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
    fi
    
    # 解壓
    mkdir -p "$PROJECT_DIR"
    tar -xzf "$ARCHIVE_PATH" -C "$PROJECT_DIR"
    
    # 檢查必要文件
    check_required_files
    
    log_success "壓縮包項目準備完成"
}

# 本地項目準備
prepare_local_project() {
    log_info "檢查本地項目..."
    
    if [ ! -d "$PROJECT_DIR" ]; then
        log_error "項目目錄不存在: $PROJECT_DIR"
        echo "請先將項目文件上傳到指定目錄"
        exit 1
    fi
    
    cd "$PROJECT_DIR"
    check_required_files
    
    log_success "本地項目檢查完成"
}

# 檢查必要文件
check_required_files() {
    local required_files=(
        "docker-compose.yml"
        "deploy.sh"
        "backend/Dockerfile"
        "frontend/Dockerfile"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$PROJECT_DIR/$file" ]; then
            log_error "缺少必要文件: $PROJECT_DIR/$file"
            exit 1
        fi
    done
    
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        log_warning "缺少 .env 文件，請確保已配置環境變數"
    fi
}

# 安裝 Docker
install_docker() {
    log_info "安裝 Docker..."
    
    if command -v docker &> /dev/null; then
        log_info "Docker 已安裝: $(docker --version)"
        
        if ! systemctl is-active docker &>/dev/null; then
            systemctl start docker
            systemctl enable docker
        fi
        return
    fi
    
    if [ "$USE_CHINA_MIRROR" = true ]; then
        install_docker_china
    else
        install_docker_official
    fi
    
    # 配置 Docker
    systemctl start docker
    systemctl enable docker
    usermod -aG docker $USER
    
    # 配置鏡像加速器（中國用戶）
    if [ "$USE_CHINA_MIRROR" = true ]; then
        setup_docker_mirrors
    fi
    
    log_success "Docker 安裝完成: $(docker --version)"
}

# 官方方式安裝 Docker
install_docker_official() {
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm -f get-docker.sh
}

# 中國鏡像方式安裝 Docker
install_docker_china() {
    case $SYSTEM in
        opencloudos|centos|fedora)
            if command -v dnf &> /dev/null; then
                dnf install -y dnf-utils device-mapper-persistent-data lvm2
                dnf config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
                dnf install -y docker-ce docker-ce-cli containerd.io
            else
                yum install -y yum-utils device-mapper-persistent-data lvm2
                yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
                yum install -y docker-ce docker-ce-cli containerd.io
            fi
            ;;
        ubuntu)
            apt update
            apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
            curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
            echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
            apt update
            apt install -y docker-ce docker-ce-cli containerd.io
            ;;
    esac
}

# 配置 Docker 鏡像加速器
setup_docker_mirrors() {
    log_info "配置 Docker 鏡像加速器..."
    
    mkdir -p /etc/docker
    cat > /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn",
    "https://reg-mirror.qiniu.com"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
EOF
    
    systemctl daemon-reload
    systemctl restart docker
}

# 安裝 Docker Compose
install_docker_compose() {
    log_info "安裝 Docker Compose..."
    
    if command -v docker-compose &> /dev/null && timeout 5 docker-compose --version &>/dev/null; then
        log_info "Docker Compose 已安裝: $(docker-compose --version)"
        return
    fi
    
    # 首先嘗試使用系統包管理器安裝（更穩定）
    log_info "嘗試使用系統包管理器安裝 Docker Compose..."
    case $SYSTEM in
        opencloudos|centos|fedora)
            if command -v dnf &> /dev/null; then
                if dnf install -y docker-compose-plugin 2>/dev/null || dnf install -y docker-compose 2>/dev/null; then
                    log_success "使用 dnf 安裝 Docker Compose 成功"
                    # 創建 docker-compose 別名指向插件
                    if command -v docker &> /dev/null && docker compose version &>/dev/null; then
                        echo '#!/bin/bash' > /usr/local/bin/docker-compose
                        echo 'exec docker compose "$@"' >> /usr/local/bin/docker-compose
                        chmod +x /usr/local/bin/docker-compose
                    fi
                    return
                fi
            elif command -v yum &> /dev/null; then
                if yum install -y docker-compose-plugin 2>/dev/null || yum install -y docker-compose 2>/dev/null; then
                    log_success "使用 yum 安裝 Docker Compose 成功"
                    return
                fi
            fi
            ;;
        ubuntu)
            if apt update && apt install -y docker-compose-plugin 2>/dev/null; then
                log_success "使用 apt 安裝 Docker Compose 成功"
                return
            fi
            ;;
    esac
    
    log_info "系統包管理器安裝失敗，嘗試手動下載安裝..."
    
    # 獲取版本
    log_info "獲取 Docker Compose 版本信息..."
    DOCKER_COMPOSE_VERSION=$(timeout 10 curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4 2>/dev/null)
    if [ -z "$DOCKER_COMPOSE_VERSION" ]; then
        log_warning "無法獲取最新版本，使用固定版本 v2.24.1"
        DOCKER_COMPOSE_VERSION="v2.24.1"
    else
        log_info "找到最新版本: $DOCKER_COMPOSE_VERSION"
    fi
    
    # 下載
    DOWNLOAD_SUCCESS=false
    if [ "$USE_CHINA_MIRROR" = true ]; then
        # 嘗試中國鏡像
        log_info "使用中國鏡像源下載 Docker Compose..."
        mirrors=("https://ghproxy.com/" "https://mirror.ghproxy.com/" "")
        
        for mirror in "${mirrors[@]}"; do
            if [ "$DOWNLOAD_SUCCESS" = false ]; then
                url="${mirror}https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)"
                log_info "嘗試下載: ${mirror}github.com"
                
                if timeout 30 curl -L --connect-timeout 10 --max-time 120 "$url" -o /usr/local/bin/docker-compose; then
                    # 立即設置執行權限
                    chmod 755 /usr/local/bin/docker-compose
                    chown root:root /usr/local/bin/docker-compose
                    
                    # 快速測試下載的文件
                    if timeout 5 /usr/local/bin/docker-compose --version &>/dev/null; then
                        DOWNLOAD_SUCCESS=true
                        log_success "下載並驗證成功"
                        break
                    else
                        log_warning "下載的文件無法執行，嘗試下一個源..."
                        rm -f /usr/local/bin/docker-compose
                    fi
                else
                    log_warning "下載失敗，嘗試下一個鏡像源..."
                    rm -f /usr/local/bin/docker-compose
                fi
            fi
        done
    else
        log_info "從官方源下載 Docker Compose..."
        url="https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)"
        if timeout 60 curl -L --connect-timeout 15 --max-time 180 "$url" -o /usr/local/bin/docker-compose; then
            # 立即設置執行權限
            chmod 755 /usr/local/bin/docker-compose
            chown root:root /usr/local/bin/docker-compose
            
            # 快速測試下載的文件
            if timeout 5 /usr/local/bin/docker-compose --version &>/dev/null; then
                DOWNLOAD_SUCCESS=true
                log_success "下載並驗證成功"
            else
                log_warning "下載的文件無法執行"
                rm -f /usr/local/bin/docker-compose
            fi
        fi
    fi
    
    if [ "$DOWNLOAD_SUCCESS" = false ]; then
        log_error "所有下載源都無法下載有效的 Docker Compose"
        log_error "請檢查網絡連接或手動安裝 Docker Compose"
        log_error "OpenCloudOS 用戶可嘗試: dnf install docker-compose-plugin"
        exit 1
    fi
    
    # 檢查下載的文件
    if [ ! -f /usr/local/bin/docker-compose ] || [ ! -s /usr/local/bin/docker-compose ]; then
        log_error "Docker Compose 下載文件無效"
        exit 1
    fi
    
    # 確保權限和所有權正確設置（防止權限問題）
    log_info "最終確認 Docker Compose 權限..."
    chmod 755 /usr/local/bin/docker-compose
    chown root:root /usr/local/bin/docker-compose
    
    # 檢查文件類型確認是可執行文件
    file_type=$(file /usr/local/bin/docker-compose | grep -o "ELF.*executable")
    if [ -z "$file_type" ]; then
        log_error "下載的文件不是有效的可執行文件"
        log_error "文件信息: $(file /usr/local/bin/docker-compose)"
        exit 1
    else
        log_info "文件驗證通過: $file_type"
    fi
    
    # 創建符號連結
    rm -f /usr/bin/docker-compose
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    
    # 確保 PATH 中能找到
    export PATH="/usr/local/bin:$PATH"
    
    # 等待一下讓文件系統同步
    sleep 1
    
    # 驗證安裝
    log_info "驗證 Docker Compose 安裝..."
    if timeout 5 /usr/local/bin/docker-compose --version &>/dev/null; then
        log_success "Docker Compose 安裝完成: $(/usr/local/bin/docker-compose --version)"
    else
        log_error "Docker Compose 安裝失敗，權限檢查:"
        ls -la /usr/local/bin/docker-compose
        log_error "嘗試最後一次權限修復..."
        
        # 最後嘗試：使用更寬泛的權限
        chmod 755 /usr/local/bin/docker-compose
        chown root:root /usr/local/bin/docker-compose
        
        if timeout 5 /usr/local/bin/docker-compose --version &>/dev/null; then
            log_success "權限修復成功: $(/usr/local/bin/docker-compose --version)"
        else
            log_error "Docker Compose 無法執行"
            log_error "文件狀態: $(ls -la /usr/local/bin/docker-compose)"
            log_error "文件類型: $(file /usr/local/bin/docker-compose)"
            log_error "系統信息: $(uname -a)"
            exit 1
        fi
    fi
}

# 配置防火牆
configure_firewall() {
    if [ "$SKIP_FIREWALL" = true ]; then
        log_info "跳過防火牆配置"
        return
    fi
    
    log_info "配置防火牆..."
    
    if systemctl is-active firewalld &>/dev/null; then
        log_info "配置 firewalld..."
        firewall-cmd --permanent --add-port=22/tcp     # SSH
        firewall-cmd --permanent --add-port=80/tcp     # HTTP
        firewall-cmd --permanent --add-port=443/tcp    # HTTPS
        firewall-cmd --permanent --add-port=3000/tcp   # Frontend
        firewall-cmd --permanent --add-port=8000/tcp   # Backend
        firewall-cmd --permanent --add-port=8081/tcp   # phpMyAdmin
        firewall-cmd --reload
        log_success "firewalld 配置完成"
    elif command -v ufw &> /dev/null && [ "$SYSTEM" = "ubuntu" ]; then
        log_info "配置 ufw..."
        ufw --force enable
        ufw allow 22/tcp    # SSH
        ufw allow 80/tcp    # HTTP
        ufw allow 443/tcp   # HTTPS
        ufw allow 3000/tcp  # Frontend
        ufw allow 8000/tcp  # Backend
        ufw allow 8081/tcp  # phpMyAdmin
        log_success "ufw 配置完成"
    else
        log_warning "未檢測到防火牆，跳過本地防火牆配置"
    fi
    
    log_info "請確保雲服務器安全組也開放了相應端口"
}

# 設置項目權限
setup_project_permissions() {
    log_info "設置項目權限..."
    
    cd "$PROJECT_DIR"
    
    chown -R $USER:$USER "$PROJECT_DIR"
    
    if [ -f "deploy.sh" ]; then
        chmod +x deploy.sh
    fi
    
    if [ -f ".env" ]; then
        chmod 600 .env
    fi
    
    mkdir -p logs
    chmod 755 logs
    
    log_success "項目權限設置完成"
}

# 部署服務
deploy_services() {
    log_info "構建和啟動服務..."
    
    cd "$PROJECT_DIR"
    
    # 檢查 Docker 守護進程
    if ! docker info &>/dev/null; then
        log_warning "Docker 守護進程未運行，嘗試啟動..."
        systemctl start docker
        sleep 5
        
        if ! docker info &>/dev/null; then
            log_error "Docker 守護進程啟動失敗"
            exit 1
        fi
    fi
    
    # 再次檢查並修復 Docker Compose 狀態
    log_info "檢查 Docker Compose 狀態..."
    
    # 檢查是否存在段錯誤或其他問題
    if ! timeout 5 docker-compose --version &>/dev/null; then
        # 獲取具體的錯誤信息
        compose_error=$(docker-compose --version 2>&1 || echo "執行失敗")
        
        if echo "$compose_error" | grep -q "Segmentation fault"; then
            log_error "Docker Compose 出現段錯誤，二進制文件可能損壞或不兼容"
            log_info "當前系統: $(uname -a)"
            log_info "嘗試重新下載 Docker Compose..."
            
            # 刪除損壞的文件
            rm -f /usr/local/bin/docker-compose /usr/bin/docker-compose
            
            # 重新安裝
            install_docker_compose
        else
            log_warning "Docker Compose 權限或其他問題，嘗試修復..."
            
            # 檢查文件狀態
            log_info "當前 docker-compose 文件狀態:"
            ls -la /usr/local/bin/docker-compose 2>/dev/null || log_warning "文件不存在於 /usr/local/bin/"
            ls -la /usr/bin/docker-compose 2>/dev/null || log_warning "文件不存在於 /usr/bin/"
            
            # 嘗試修復權限
            if [ -f /usr/local/bin/docker-compose ]; then
                chmod 755 /usr/local/bin/docker-compose
                chown root:root /usr/local/bin/docker-compose
            fi
            
            # 重新創建符號連結
            rm -f /usr/bin/docker-compose
            ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
            
            # 再次測試
            if ! timeout 5 docker-compose --version &>/dev/null; then
                log_error "無法修復 Docker Compose 問題"
                log_error "錯誤信息: $compose_error"
                log_error "請手動安裝 Docker Compose"
                exit 1
            else
                log_success "Docker Compose 修復成功"
            fi
        fi
    else
        log_success "Docker Compose 狀態正常: $(docker-compose --version)"
    fi
    
    # 清理舊容器
    log_info "清理舊容器..."
    docker-compose -p lab_web down --remove-orphans 2>/dev/null || true
    
    # 構建服務
    log_info "構建 Docker 鏡像（可能需要幾分鐘）..."
    ./deploy.sh prod build --no-cache
    
    # 啟動服務
    log_info "啟動所有服務..."
    ./deploy.sh prod start -d
    
    # 等待服務啟動
    log_info "等待服務啟動（30秒）..."
    sleep 30
    
    # 初始化資料庫
    log_info "初始化資料庫..."
    ./deploy.sh prod db-init
    
    log_success "服務部署完成"
}

# 創建系統服務
create_system_service() {
    if [ "$SKIP_SERVICE" = true ]; then
        log_info "跳過系統服務創建"
        return
    fi
    
    log_info "創建系統服務..."
    
    cat > /etc/systemd/system/lab-website.service << EOF
[Unit]
Description=Lab Website Docker Services
Requires=docker.service
After=docker.service
StartLimitIntervalSec=0

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/deploy.sh prod start -d
ExecStop=$PROJECT_DIR/deploy.sh prod stop
TimeoutStartSec=300
TimeoutStopSec=120
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable lab-website.service
    
    log_success "系統服務創建完成，已設置開機自啟動"
}

# 驗證部署
verify_deployment() {
    log_info "驗證部署..."
    
    cd "$PROJECT_DIR"
    
    # 檢查服務狀態
    echo "========== 服務狀態 ==========" | tee -a "$LOG_FILE"
    ./deploy.sh prod status 2>&1 | tee -a "$LOG_FILE"
    
    # 健康檢查
    echo "========== 健康檢查 ==========" | tee -a "$LOG_FILE"
    ./deploy.sh prod health 2>&1 | tee -a "$LOG_FILE"
    
    # 等待服務完全啟動
    sleep 10
    
    # 測試端點
    echo "========== 端點測試 ==========" | tee -a "$LOG_FILE"
    
    if curl -sf http://localhost:3000 > /dev/null 2>&1; then
        echo "✓ 前端服務 (3000) - 正常" | tee -a "$LOG_FILE"
    else
        echo "✗ 前端服務 (3000) - 異常" | tee -a "$LOG_FILE"
    fi
    
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ 後端服務 (8000) - 正常" | tee -a "$LOG_FILE"
    else
        echo "✗ 後端服務 (8000) - 異常" | tee -a "$LOG_FILE"
    fi
    
    # 獲取公網 IP
    if [ -n "$PUBLIC_IP" ] && [ "$PUBLIC_IP" != "無法獲取" ]; then
        DISPLAY_IP="$PUBLIC_IP"
    else
        DISPLAY_IP="您的服務器IP"
    fi
    
    echo "=============================" | tee -a "$LOG_FILE"
    log_success "部署驗證完成"
    
    echo ""
    echo "=========================================="
    echo "           部署完成！"
    echo "=========================================="
    echo "🌐 前端訪問: http://$DISPLAY_IP:3000"
    echo "🔌 後端 API: http://$DISPLAY_IP:8000"
    echo "📚 API 文檔: http://$DISPLAY_IP:8000/api/docs"
    echo "🗄️ 資料庫管理: http://$DISPLAY_IP:8081"
    echo ""
    echo "👤 預設管理員帳號:"
    echo "   用戶名: admin"
    echo "   密碼: admin123"
    echo ""
    echo "⚠️ 重要提醒:"
    echo "1. 請立即修改預設管理員密碼"
    echo "2. 請檢查雲服務器安全組，確保開放以下端口:"
    echo "   - 22 (SSH)、80 (HTTP)、443 (HTTPS)"
    echo "   - 3000 (前端服務)、8000 (後端 API)、8081 (phpMyAdmin)"
    echo "3. 建議設置域名和 SSL 證書"
    echo "=========================================="
}

# 清理工作
cleanup() {
    log_info "清理臨時文件..."
    rm -f get-docker.sh
    
    if [ "$DEPLOY_MODE" = "archive" ] && [ -f "$ARCHIVE_PATH" ]; then
        echo ""
        echo "壓縮包位置: $ARCHIVE_PATH ($(du -h $ARCHIVE_PATH | cut -f1))"
        read -p "是否刪除原壓縮包以節省空間？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -f "$ARCHIVE_PATH"
            log_success "原壓縮包已刪除"
        fi
    fi
}

# 主執行函數
main() {
    echo "=========================================="
    echo "       實驗室網站 ECS 統一部署工具"
    echo "=========================================="
    echo "開始時間: $(date)"
    echo "日誌文件: $LOG_FILE"
    echo "部署模式: $DEPLOY_MODE"
    [ "$USE_CHINA_MIRROR" = true ] && echo "使用中國鏡像: 是"
    echo ""
    
    # 檢查 root 權限
    if [ "$EUID" -ne 0 ]; then
        log_error "請以 root 身份運行此腳本"
        echo "使用: sudo $0 [選項] <模式>"
        exit 1
    fi
    
    # 執行部署步驟
    check_system
    prepare_project
    update_system
    install_docker
    install_docker_compose
    configure_firewall
    setup_project_permissions
    deploy_services
    create_system_service
    verify_deployment
    cleanup
    
    echo ""
    echo "🎉 部署完成時間: $(date)"
    echo "📋 詳細日誌: $LOG_FILE"
    echo ""
    echo "如需重新部署，可以運行:"
    echo "  cd $PROJECT_DIR && ./deploy.sh prod restart"
}

# 解析參數並執行
parse_args "$@"
main