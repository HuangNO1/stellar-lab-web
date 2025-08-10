#!/bin/bash

# Service Layer 測試運行腳本
# 使用方法: ./scripts/development/run_service_tests.sh [選項]

set -e

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

# 幫助信息
show_help() {
    echo "Service Layer 測試運行腳本"
    echo ""
    echo "使用方法:"
    echo "  $0 [選項]"
    echo ""
    echo "選項:"
    echo "  -h, --help           顯示此幫助信息"
    echo "  -a, --all           運行所有服務層測試"
    echo "  -s, --service NAME   運行指定服務的測試 (如: auth, admin, lab)"
    echo "  -c, --coverage      運行測試並生成覆蓋率報告"
    echo "  -v, --verbose       詳細輸出"
    echo "  -f, --fast          快速運行 (並行執行)"
    echo "  -d, --debug         調試模式 (顯示print輸出)"
    echo "  --failed-only       只運行上次失敗的測試"
    echo "  --html-report       生成HTML覆蓋率報告"
    echo ""
    echo "示例:"
    echo "  $0 -a                # 運行所有服務測試"
    echo "  $0 -s auth           # 只運行auth服務測試"
    echo "  $0 -c -v             # 運行測試並顯示覆蓋率"
    echo "  $0 -f --html-report  # 並行運行並生成HTML報告"
}

# 檢查pytest是否安裝
check_requirements() {
    log_info "檢查測試環境..."
    
    if ! command -v pytest &> /dev/null; then
        log_error "pytest 未安裝，請運行: pip install pytest pytest-cov"
        exit 1
    fi
    
    if [ "$FAST_MODE" = true ] && ! python -c "import pytest_xdist" &> /dev/null; then
        log_warning "pytest-xdist 未安裝，無法並行運行，請運行: pip install pytest-xdist"
        FAST_MODE=false
    fi
    
    log_success "測試環境檢查通過"
}

# 設置環境變量
setup_environment() {
    export FLASK_ENV=testing
    export FLASK_CONFIG=testing
    export PYTHONPATH="$(pwd):$PYTHONPATH"
}

# 運行所有服務測試
run_all_tests() {
    log_info "運行所有服務層測試..."
    
    local pytest_args="-v"
    
    if [ "$VERBOSE" = true ]; then
        pytest_args="$pytest_args -s"
    fi
    
    if [ "$FAST_MODE" = true ]; then
        pytest_args="$pytest_args -n auto"
    fi
    
    if [ "$DEBUG_MODE" = true ]; then
        pytest_args="$pytest_args -s --tb=long"
    fi
    
    if [ "$COVERAGE" = true ]; then
        pytest_args="$pytest_args --cov=app/services"
        if [ "$HTML_REPORT" = true ]; then
            pytest_args="$pytest_args --cov-report=html --cov-report=term"
        else
            pytest_args="$pytest_args --cov-report=term-missing"
        fi
    fi
    
    if [ "$FAILED_ONLY" = true ]; then
        pytest_args="$pytest_args --lf"
    fi
    
    # 運行測試
    pytest tests/unit/services/ $pytest_args
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_success "所有測試通過！"
        
        if [ "$HTML_REPORT" = true ]; then
            log_info "HTML覆蓋率報告: file://$(pwd)/htmlcov/index.html"
        fi
    else
        log_error "測試失敗，退出碼: $exit_code"
        exit $exit_code
    fi
}

# 運行指定服務測試
run_service_test() {
    local service_name="$1"
    log_info "運行 ${service_name} 服務測試..."
    
    local test_file="tests/unit/services/test_${service_name}_service.py"
    
    if [ ! -f "$test_file" ]; then
        log_error "測試文件不存在: $test_file"
        log_info "可用的服務測試:"
        ls tests/unit/services/test_*_service.py | sed 's/.*test_\(.*\)_service\.py/  - \1/'
        exit 1
    fi
    
    local pytest_args="-v"
    
    if [ "$VERBOSE" = true ]; then
        pytest_args="$pytest_args -s"
    fi
    
    if [ "$DEBUG_MODE" = true ]; then
        pytest_args="$pytest_args -s --tb=long"
    fi
    
    if [ "$COVERAGE" = true ]; then
        pytest_args="$pytest_args --cov=app/services/${service_name}_service --cov-report=term-missing"
    fi
    
    pytest "$test_file" $pytest_args
    
    if [ $? -eq 0 ]; then
        log_success "${service_name} 服務測試通過！"
    else
        log_error "${service_name} 服務測試失敗"
        exit 1
    fi
}

# 顯示測試統計
show_statistics() {
    log_info "測試統計信息:"
    
    local total_files=$(find tests/unit/services -name "test_*.py" | wc -l)
    local total_tests=$(grep -r "def test_" tests/unit/services/ | wc -l)
    
    echo "  - 測試文件數量: $total_files"
    echo "  - 測試用例數量: $total_tests"
    echo "  - 覆蓋的服務:"
    
    find tests/unit/services -name "test_*_service.py" -exec basename {} .py \; | sed 's/test_//' | sed 's/_service//' | sort | sed 's/^/    ✓ /'
}

# 主函數
main() {
    # 默認參數
    ALL_TESTS=false
    SERVICE_NAME=""
    COVERAGE=false
    VERBOSE=false
    FAST_MODE=false
    DEBUG_MODE=false
    FAILED_ONLY=false
    HTML_REPORT=false
    
    # 解析參數
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -a|--all)
                ALL_TESTS=true
                shift
                ;;
            -s|--service)
                SERVICE_NAME="$2"
                shift 2
                ;;
            -c|--coverage)
                COVERAGE=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -f|--fast)
                FAST_MODE=true
                shift
                ;;
            -d|--debug)
                DEBUG_MODE=true
                shift
                ;;
            --failed-only)
                FAILED_ONLY=true
                shift
                ;;
            --html-report)
                HTML_REPORT=true
                COVERAGE=true  # HTML報告需要覆蓋率
                shift
                ;;
            --stats)
                show_statistics
                exit 0
                ;;
            *)
                log_error "未知參數: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 如果沒有指定操作，默認運行所有測試
    if [ "$ALL_TESTS" = false ] && [ -z "$SERVICE_NAME" ]; then
        ALL_TESTS=true
    fi
    
    log_info "開始 Service Layer 測試..."
    
    # 檢查環境
    check_requirements
    setup_environment
    
    # 執行測試
    if [ "$ALL_TESTS" = true ]; then
        run_all_tests
    elif [ -n "$SERVICE_NAME" ]; then
        run_service_test "$SERVICE_NAME"
    fi
    
    log_success "測試執行完成！"
}

# 執行主函數
main "$@"