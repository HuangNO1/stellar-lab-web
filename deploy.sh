#!/bin/bash

# Lab Website Full-Stack Deployment Script
# Usage: ./deploy.sh [environment] [action] [options]

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="lab-website"
COMPOSE_PROJECT_NAME="lab_web"

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
Lab Website Full-Stack Deployment Script

Usage: $0 [environment] [action] [options]

Environments:
    prod        Production environment (docker-compose.yml)
    dev         Development environment (docker-compose.dev.yml)

Actions:
    build       Build all services
    start       Start all services
    stop        Stop all services
    restart     Restart all services
    logs        Show logs for all services
    status      Show status of all services
    clean       Remove containers, networks, and images
    db-init     Initialize database with sample data
    db-backup   Backup database
    db-restore  Restore database from backup
    shell       Open shell in specified service
    health      Check health of all services

Service-specific actions (use with --service flag):
    build --service=frontend    Build only frontend
    logs --service=backend      Show only backend logs
    shell --service=db          Open shell in database

Options:
    --service=SERVICE   Target specific service (frontend|backend|db|phpmyadmin)
    --follow, -f        Follow logs
    --detach, -d        Run in background
    --rebuild           Force rebuild images
    --no-cache          Build without cache
    --help, -h          Show this help message

Examples:
    $0 prod start              # Start production environment
    $0 dev start -d            # Start development environment in background
    $0 prod logs -f            # Follow production logs
    $0 prod logs --service=backend -f  # Follow only backend logs
    $0 prod shell --service=db # Open shell in database
    $0 prod db-backup          # Backup production database
    $0 dev clean               # Clean development environment

EOF
}

# Get compose file based on environment
get_compose_file() {
    local env="$1"
    case "$env" in
        prod|production)
            echo "docker-compose.yml"
            ;;
        dev|development)
            echo "docker-compose.dev.yml"
            ;;
        *)
            log_error "Unknown environment: $env. Use 'prod' or 'dev'"
            exit 1
            ;;
    esac
}

# Build services
build_services() {
    local compose_file="$1"
    local service="$2"
    local rebuild="$3"
    local no_cache="$4"
    
    log_info "Building services with $compose_file..."
    
    local build_args=""
    if [[ "$rebuild" == "true" ]]; then
        build_args="--force-rm"
    fi
    if [[ "$no_cache" == "true" ]]; then
        build_args="$build_args --no-cache"
    fi
    
    if [[ -n "$service" ]]; then
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" build $build_args "$service"
        log_success "Service $service built successfully"
    else
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" build $build_args
        log_success "All services built successfully"
    fi
}

# Start services
start_services() {
    local compose_file="$1"
    local service="$2"
    local detach="$3"
    local rebuild="$4"
    
    log_info "Starting services with $compose_file..."
    
    local run_args=""
    if [[ "$detach" == "true" ]]; then
        run_args="-d"
    fi
    
    if [[ "$rebuild" == "true" ]]; then
        run_args="$run_args --build"
    fi
    
    if [[ -n "$service" ]]; then
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" up $run_args "$service"
    else
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" up $run_args
    fi
    
    if [[ "$detach" == "true" ]]; then
        log_success "Services started in background"
        log_info "Frontend: http://localhost:3000"
        log_info "Backend API: http://localhost:8000"
        log_info "phpMyAdmin: http://localhost:8081"
        log_info "API Documentation: http://localhost:8000/api/docs"
    fi
}

# Stop services
stop_services() {
    local compose_file="$1"
    local service="$2"
    
    log_info "Stopping services..."
    
    if [[ -n "$service" ]]; then
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" stop "$service"
        log_success "Service $service stopped"
    else
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" stop
        log_success "All services stopped"
    fi
}

# Restart services
restart_services() {
    local compose_file="$1"
    local service="$2"
    
    log_info "Restarting services..."
    stop_services "$compose_file" "$service"
    start_services "$compose_file" "$service" "true" "false"
}

# Show logs
show_logs() {
    local compose_file="$1"
    local service="$2"
    local follow="$3"
    
    local log_args=""
    if [[ "$follow" == "true" ]]; then
        log_args="-f"
    fi
    
    if [[ -n "$service" ]]; then
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" logs $log_args "$service"
    else
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" logs $log_args
    fi
}

# Show status
show_status() {
    local compose_file="$1"
    
    log_info "Service status:"
    docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" ps
    
    echo
    log_info "Health status:"
    
    # Check each service health
    local services=("lab_web_backend" "lab_web_frontend" "lab_web_db")
    for service in "${services[@]}"; do
        if docker ps --filter "name=$service" --format "table {{.Names}}" | grep -q "$service"; then
            local health=$(docker inspect --format='{{.State.Health.Status}}' "$service" 2>/dev/null || echo "no health check")
            echo "$service: $health"
        else
            echo "$service: not running"
        fi
    done
}

# Clean up
clean_services() {
    local compose_file="$1"
    
    log_warning "This will remove all containers, networks, and images for this project."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Cleaning up services..."
        
        # Stop and remove containers
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" down -v --rmi all --remove-orphans
        
        # Remove dangling images
        docker image prune -f
        
        log_success "Cleanup completed"
    else
        log_info "Cleanup cancelled"
    fi
}

# Initialize database
init_database() {
    local compose_file="$1"
    
    log_info "Initializing database..."
    
    # Make sure database is running
    docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" up -d db
    
    # Wait for database to be ready
    log_info "Waiting for database to be ready..."
    until docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" exec db mysqladmin ping -h"localhost" --silent; do
        sleep 1
    done
    
    # Run initialization script
    docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" exec backend python scripts/development/init_db.py
    
    log_success "Database initialized with sample data"
    log_info "Default admin credentials:"
    log_info "  Username: admin"
    log_info "  Password: admin123"
}

# Backup database
backup_database() {
    local compose_file="$1"
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    
    log_info "Creating database backup: $backup_file"
    
    docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" exec db mysqldump \
        -u root -plab_web_root_123 lab_web > "$backup_file"
    
    log_success "Database backed up to $backup_file"
}

# Restore database
restore_database() {
    local compose_file="$1"
    local backup_file="$2"
    
    if [[ ! -f "$backup_file" ]]; then
        log_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    log_warning "This will restore the database from $backup_file"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Restoring database from $backup_file..."
        
        docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" exec -T db mysql \
            -u root -plab_web_root_123 lab_web < "$backup_file"
        
        log_success "Database restored from $backup_file"
    else
        log_info "Restore cancelled"
    fi
}

# Open shell in service
open_shell() {
    local compose_file="$1"
    local service="$2"
    
    if [[ -z "$service" ]]; then
        log_error "Service name required for shell access"
        exit 1
    fi
    
    case "$service" in
        frontend)
            docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" exec "$service" /bin/sh
            ;;
        backend)
            docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" exec "$service" /bin/bash
            ;;
        db)
            docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" exec "$service" mysql -u root -plab_web_root_123 lab_web
            ;;
        *)
            docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" exec "$service" /bin/bash
            ;;
    esac
}

# Check health of services
check_health() {
    local compose_file="$1"
    
    log_info "Checking service health..."
    
    # Frontend health check
    if curl -sf http://localhost:3000/health > /dev/null 2>&1; then
        log_success "Frontend is healthy"
    else
        log_error "Frontend health check failed"
    fi
    
    # Backend health check
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        log_success "Backend is healthy"
    else
        log_error "Backend health check failed"
    fi
    
    # Database health check
    if docker-compose -f "$compose_file" -p "$COMPOSE_PROJECT_NAME" exec db mysqladmin ping -h"localhost" --silent > /dev/null 2>&1; then
        log_success "Database is healthy"
    else
        log_error "Database health check failed"
    fi
}

# Parse command line arguments
parse_args() {
    ENVIRONMENT=""
    ACTION=""
    SERVICE=""
    FOLLOW="false"
    DETACH="false"
    REBUILD="false"
    NO_CACHE="false"
    BACKUP_FILE=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            prod|production|dev|development)
                ENVIRONMENT="$1"
                ;;
            build|start|stop|restart|logs|status|clean|db-init|db-backup|db-restore|shell|health)
                ACTION="$1"
                ;;
            --service=*)
                SERVICE="${1#*=}"
                ;;
            --follow|-f)
                FOLLOW="true"
                ;;
            --detach|-d)
                DETACH="true"
                ;;
            --rebuild)
                REBUILD="true"
                ;;
            --no-cache)
                NO_CACHE="true"
                ;;
            --backup-file=*)
                BACKUP_FILE="${1#*=}"
                ;;
            --help|-h|help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
        shift
    done
    
    # Validate required arguments
    if [[ -z "$ENVIRONMENT" ]]; then
        log_error "Environment is required (prod or dev)"
        usage
        exit 1
    fi
    
    if [[ -z "$ACTION" ]]; then
        log_error "Action is required"
        usage
        exit 1
    fi
}

# Main script logic
main() {
    parse_args "$@"
    
    local compose_file
    compose_file=$(get_compose_file "$ENVIRONMENT")
    
    log_info "Environment: $ENVIRONMENT"
    log_info "Compose file: $compose_file"
    log_info "Action: $ACTION"
    
    if [[ -n "$SERVICE" ]]; then
        log_info "Service: $SERVICE"
    fi
    
    case "$ACTION" in
        build)
            build_services "$compose_file" "$SERVICE" "$REBUILD" "$NO_CACHE"
            ;;
        start)
            start_services "$compose_file" "$SERVICE" "$DETACH" "$REBUILD"
            ;;
        stop)
            stop_services "$compose_file" "$SERVICE"
            ;;
        restart)
            restart_services "$compose_file" "$SERVICE"
            ;;
        logs)
            show_logs "$compose_file" "$SERVICE" "$FOLLOW"
            ;;
        status)
            show_status "$compose_file"
            ;;
        clean)
            clean_services "$compose_file"
            ;;
        db-init)
            init_database "$compose_file"
            ;;
        db-backup)
            backup_database "$compose_file"
            ;;
        db-restore)
            restore_database "$compose_file" "$BACKUP_FILE"
            ;;
        shell)
            open_shell "$compose_file" "$SERVICE"
            ;;
        health)
            check_health "$compose_file"
            ;;
    esac
}

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed or not in PATH"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    log_error "docker-compose is not installed or not in PATH"
    exit 1
fi

if ! docker info &> /dev/null; then
    log_error "Docker is not running"
    exit 1
fi

# Execute main function
main "$@"