# Lab Website Makefile
# Convenient shortcuts for common Docker operations

.PHONY: help build start stop restart logs status clean health install dev prod

# Default goal
.DEFAULT_GOAL := help

# Colors
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

help: ## Show this help message
	@echo "Lab Website Docker Management"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  $(BLUE)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install project (create .env and build images)
	@echo "$(GREEN)Setting up Lab Website project...$(NC)"
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file from template"; fi
	@./deploy.sh prod build
	@echo "$(GREEN)Installation complete!$(NC)"

build: ## Build all services (production)
	@./deploy.sh prod build

start: ## Start all services in production mode
	@./deploy.sh prod start -d

stop: ## Stop all services
	@./deploy.sh prod stop

restart: ## Restart all services
	@./deploy.sh prod restart

logs: ## Show logs for all services
	@./deploy.sh prod logs -f

status: ## Show status of all services
	@./deploy.sh prod status

clean: ## Clean up containers, networks and images
	@./deploy.sh prod clean

health: ## Check health of all services
	@./deploy.sh prod health

# Development shortcuts
dev: ## Start development environment with hot reloading
	@echo "$(YELLOW)Starting development environment...$(NC)"
	@./deploy.sh dev start -d

dev-logs: ## Show development environment logs
	@./deploy.sh dev logs -f

dev-stop: ## Stop development environment
	@./deploy.sh dev stop

dev-clean: ## Clean development environment
	@./deploy.sh dev clean

# Database shortcuts
db-init: ## Initialize database with sample data
	@./deploy.sh prod db-init

db-backup: ## Backup database
	@./deploy.sh prod db-backup

db-shell: ## Open MySQL shell
	@./deploy.sh prod shell --service=db

# Service-specific shortcuts
frontend-logs: ## Show frontend logs
	@./deploy.sh prod logs --service=frontend -f

backend-logs: ## Show backend logs
	@./deploy.sh prod logs --service=backend -f

frontend-shell: ## Open frontend shell
	@./deploy.sh prod shell --service=frontend

backend-shell: ## Open backend shell
	@./deploy.sh prod shell --service=backend

# Quick access URLs
urls: ## Show service URLs
	@echo "$(GREEN)Service URLs:$(NC)"
	@echo "  Frontend:      http://localhost:3000"
	@echo "  Backend API:   http://localhost:8000"
	@echo "  API Docs:      http://localhost:8000/api/docs"
	@echo "  phpMyAdmin:    http://localhost:8081"
	@echo ""
	@echo "$(YELLOW)Default Login:$(NC)"
	@echo "  Username: admin"
	@echo "  Password: admin123"

# Full deployment workflow
deploy: install start db-init urls ## Full deployment: install, start, init database, show URLs
	@echo "$(GREEN)Deployment complete!$(NC)"