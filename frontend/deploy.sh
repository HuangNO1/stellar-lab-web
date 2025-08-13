#!/bin/bash

# Frontend Deployment Script
# Usage: ./deploy.sh [action] [options]

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="lab-frontend"
FRONTEND_IMAGE="lab-website-frontend:latest"
FRONTEND_PORT="${FRONTEND_PORT:-3000}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Display usage information
usage() {
    cat << EOF
Lab Website Frontend Deployment Script

Usage: $0 [action] [options]

Actions:
    build       Build frontend Docker image
    start       Start frontend container
    stop        Stop frontend container
    restart     Restart frontend container
    logs        Show frontend logs
    status      Show container status
    clean       Remove containers and images
    health      Check container health
    shell       Open shell in frontend container

Options:
    --port PORT     Specify port (default: 3000)
    --detach, -d    Run in background (default for start)
    --follow, -f    Follow logs
    --help, -h      Show this help message

Examples:
    $0 build                    # Build frontend image
    $0 start                    # Start frontend container
    $0 restart                  # Restart frontend container
    $0 logs -f                  # Follow logs
    $0 status                   # Check status

EOF
}

# Build frontend image
build_frontend() {
    log_info "Building frontend Docker image..."
    
    # Check if Dockerfile exists
    if [[ ! -f "$SCRIPT_DIR/Dockerfile" ]]; then
        log_error "Dockerfile not found in $SCRIPT_DIR"
        exit 1
    fi

    # Build image
    docker build -t "$FRONTEND_IMAGE" "$SCRIPT_DIR"
    
    if [[ $? -eq 0 ]]; then
        log_success "Frontend image built successfully: $FRONTEND_IMAGE"
    else
        log_error "Failed to build frontend image"
        exit 1
    fi
}

# Start frontend container
start_frontend() {
    local detach_flag=""
    
    if [[ "$1" == "--detach" ]] || [[ "$1" == "-d" ]]; then
        detach_flag="-d"
    fi

    log_info "Starting frontend container..."
    
    # Create network if it doesn't exist
    docker network ls | grep -q lab_web_default || {
        log_info "Creating lab_web_default network..."
        docker network create lab_web_default
    }
    
    # Stop existing container if running
    if docker ps -q -f name="$PROJECT_NAME" | grep -q .; then
        log_info "Stopping existing container..."
        docker stop "$PROJECT_NAME"
        docker rm "$PROJECT_NAME"
    fi
    
    # Run new container
    docker run $detach_flag \
        --name "$PROJECT_NAME" \
        --network lab_web_default \
        -p "${FRONTEND_PORT}:80" \
        -v "$SCRIPT_DIR/docker/nginx.conf:/etc/nginx/nginx.conf:ro" \
        --restart unless-stopped \
        --health-cmd="wget --quiet --tries=1 --spider http://localhost/health" \
        --health-interval=30s \
        --health-timeout=10s \
        --health-retries=3 \
        --health-start-period=30s \
        "$FRONTEND_IMAGE"
    
    if [[ $? -eq 0 ]]; then
        log_success "Frontend container started successfully"
        log_info "Frontend is available at: http://localhost:$FRONTEND_PORT"
    else
        log_error "Failed to start frontend container"
        exit 1
    fi
}

# Stop frontend container
stop_frontend() {
    log_info "Stopping frontend container..."
    
    if docker ps -q -f name="$PROJECT_NAME" | grep -q .; then
        docker stop "$PROJECT_NAME"
        docker rm "$PROJECT_NAME"
        log_success "Frontend container stopped"
    else
        log_warning "Frontend container is not running"
    fi
}

# Restart frontend container
restart_frontend() {
    log_info "Restarting frontend container..."
    stop_frontend
    start_frontend -d
}

# Show logs
show_logs() {
    local follow_flag=""
    
    if [[ "$1" == "--follow" ]] || [[ "$1" == "-f" ]]; then
        follow_flag="-f"
    fi
    
    if docker ps -q -f name="$PROJECT_NAME" | grep -q .; then
        docker logs $follow_flag "$PROJECT_NAME"
    else
        log_error "Frontend container is not running"
    fi
}

# Show container status
show_status() {
    log_info "Frontend container status:"
    
    if docker ps -a -f name="$PROJECT_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q "$PROJECT_NAME"; then
        docker ps -a -f name="$PROJECT_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        
        # Health check
        if docker ps -q -f name="$PROJECT_NAME" | grep -q .; then
            echo
            log_info "Health status:"
            docker inspect --format='{{.State.Health.Status}}' "$PROJECT_NAME" 2>/dev/null || echo "No health check configured"
        fi
    else
        log_warning "Frontend container does not exist"
    fi
}

# Clean up containers and images
clean_frontend() {
    log_info "Cleaning up frontend containers and images..."
    
    # Stop and remove container
    if docker ps -a -q -f name="$PROJECT_NAME" | grep -q .; then
        docker stop "$PROJECT_NAME" 2>/dev/null || true
        docker rm "$PROJECT_NAME" 2>/dev/null || true
    fi
    
    # Remove image
    if docker images -q "$FRONTEND_IMAGE" | grep -q .; then
        docker rmi "$FRONTEND_IMAGE"
    fi
    
    log_success "Frontend cleanup completed"
}

# Check health
check_health() {
    log_info "Checking frontend health..."
    
    if docker ps -q -f name="$PROJECT_NAME" | grep -q .; then
        # Container health
        health_status=$(docker inspect --format='{{.State.Health.Status}}' "$PROJECT_NAME" 2>/dev/null || echo "unknown")
        echo "Container health: $health_status"
        
        # HTTP health check
        if curl -sf "http://localhost:$FRONTEND_PORT/health" > /dev/null; then
            log_success "Frontend is healthy and responding"
        else
            log_error "Frontend is not responding to health checks"
            exit 1
        fi
    else
        log_error "Frontend container is not running"
        exit 1
    fi
}

# Open shell in container
open_shell() {
    if docker ps -q -f name="$PROJECT_NAME" | grep -q .; then
        log_info "Opening shell in frontend container..."
        docker exec -it "$PROJECT_NAME" /bin/sh
    else
        log_error "Frontend container is not running"
        exit 1
    fi
}

# Main script logic
main() {
    local action="$1"
    local option="$2"
    
    case "$action" in
        build)
            build_frontend
            ;;
        start)
            build_frontend
            start_frontend "$option"
            ;;
        stop)
            stop_frontend
            ;;
        restart)
            restart_frontend
            ;;
        logs)
            show_logs "$option"
            ;;
        status)
            show_status
            ;;
        clean)
            clean_frontend
            ;;
        health)
            check_health
            ;;
        shell)
            open_shell
            ;;
        --help|-h|help)
            usage
            ;;
        *)
            log_error "Unknown action: $action"
            echo
            usage
            exit 1
            ;;
    esac
}

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed or not in PATH"
    exit 1
fi

if ! docker info &> /dev/null; then
    log_error "Docker is not running"
    exit 1
fi

# Execute main function
main "$@"