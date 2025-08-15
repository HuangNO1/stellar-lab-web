# Lab Website Deployment Guide

Complete deployment guide for the Lab Website Framework with Docker containerization.

> 📘 **Cloud Server Users Note**: If you're deploying on ECS, AWS EC2, or other cloud servers from scratch, we recommend checking the **[ECS Cloud Server Deployment Guide](./ECS_DEPLOYMENT.md)** which provides more detailed cloud environment deployment steps and optimization configurations.

> 🚀 **Fast Deployment Recommendation**: If you want to significantly reduce server deployment time (from 10-15 minutes to 2-3 minutes), consider using the **[Local Build + Image Deployment Solution](./IMAGE_DEPLOYMENT.md)**, especially suitable for production environments and multi-server deployments.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Environment Setup](#environment-setup)
- [Production Deployment](#production-deployment)
- [Deployment Optimization & Service Management](#deployment-optimization--service-management)
- [Development Environment](#development-environment)
- [Configuration](#configuration)
- [Database Management](#database-management)
- [SSL/HTTPS Setup](#ssl-https-setup)
- [Backup and Recovery](#backup-and-recovery)
- [Monitoring and Logs](#monitoring-and-logs)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)
- [Related Documentation](#related-documentation)

## Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+, CentOS 8+, etc.), macOS, or Windows with WSL2
- **RAM**: Minimum 2GB, Recommended 4GB+
- **Storage**: Minimum 10GB free space
- **CPU**: 2+ cores recommended

### Software Requirements
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+
- **Git**: For cloning the repository
- **Make**: Optional, for convenience commands

### Network Requirements
- **Ports**: 3000 (Frontend), 8000 (Backend), 3307 (MySQL), 8081 (phpMyAdmin)
- **Internet Access**: Required for downloading Docker images and dependencies

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repository-url>
cd lab_web

# Quick deployment with Make (recommended)
make deploy

# Or manual deployment
cp .env.example .env
./deploy.sh prod build
./deploy.sh prod start -d
./deploy.sh prod db-init
```

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Database Admin**: http://localhost:8081

### 3. Default Login

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the default password immediately in production!

## Environment Setup

### Frontend Environment Configuration

The frontend supports different environment configurations for various deployment scenarios:

#### Development Environment
- **File**: `frontend/.env.development`
- **API Base URL**: `http://127.0.0.1:8000/api`
- **Use Case**: Local development with direct backend connection

```env
NODE_ENV=development
VUE_APP_API_BASE_URL=http://127.0.0.1:8000/api
```

#### Production/Docker Environment
- **File**: `frontend/.env.production` (production), `frontend/.env.docker` (Docker builds)
- **API Base URL**: `/api` (relative path through nginx proxy)
- **Use Case**: Docker containers, production deployments

```env
NODE_ENV=production
VUE_APP_API_BASE_URL=/api
```

#### Custom Environment
Create `frontend/.env.local` for custom configurations (this file is ignored by Docker and git):

```env
NODE_ENV=development
VUE_APP_API_BASE_URL=https://your-custom-api-domain.com/api
```

### Backend Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key variables to modify for production:

```env
# Security - MUST CHANGE
SECRET_KEY=your_very_secure_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
MYSQL_ROOT_PASSWORD=your_secure_db_password

# Ports (if needed)
FRONTEND_PORT=3000
BACKEND_PORT=8000
MYSQL_PORT=3307
PHPMYADMIN_PORT=8081

# CORS (adjust for your domain)
CORS_ORIGINS=https://your-domain.com,https://api.your-domain.com
```

## Production Deployment

### Standard Deployment

```bash
# Build all services
./deploy.sh prod build

# Start in production mode
./deploy.sh prod start -d

# Initialize database with sample data
./deploy.sh prod db-init

# Check service status
./deploy.sh prod status
```

### Advanced Production Setup

#### 1. Custom Network Configuration

```bash
# Create custom network (optional)
docker network create --driver bridge lab_web_network
```

#### 2. Resource Limits

Create `docker-compose.override.yml` for resource limits:

```yaml
version: '3.8'

services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
  
  frontend:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
  
  db:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

#### 3. Persistent Volumes

Data is automatically persisted in Docker volumes:
- `mysql_data`: Database files
- `media_data`: Uploaded files (images, papers, etc.)

## Deployment Optimization & Service Management

### Build Cache Optimization

The deploy.sh script supports Docker layer caching for significantly faster deployment speeds:

#### Quick Deployment (Recommended)
```bash
# Utilize Docker cache for fast builds (1-3 minutes)
./deploy.sh prod build --service=backend
./deploy.sh prod build --service=frontend

# Quick restart individual services
./deploy.sh prod restart --service=backend   # Restart backend
./deploy.sh prod restart --service=frontend  # Restart frontend
```

#### Full Rebuild (Slower but Thorough)
```bash
# Force rebuild without cache (8-12 minutes)
./deploy.sh prod build --service=backend --no-cache
./deploy.sh prod build --service=frontend --no-cache

# Rebuild all services
./deploy.sh prod build --no-cache
```

### Service Management

#### Supported Service Operations

| Service | Description | Build Time (Cached/No-Cache) |
|---------|-------------|-------------------------------|
| `backend` | Flask Backend API | ~2 min / ~10 min |
| `frontend` | Vue.js Frontend | ~3 min / ~8 min |
| `db` | MySQL Database | No build needed |
| `phpmyadmin` | Database Admin | No build needed |

#### Common Service Commands

```bash
# 📊 Monitor Services
./deploy.sh prod status                        # Check all service status
./deploy.sh prod health                        # Health check
./deploy.sh prod logs --service=backend -f    # Real-time backend logs
./deploy.sh prod logs --service=frontend -f   # Real-time frontend logs

# 🔄 Restart Services
./deploy.sh prod restart --service=backend    # Restart backend only
./deploy.sh prod restart --service=frontend   # Restart frontend only
./deploy.sh prod restart                       # Restart all services

# 🛠️ Build Services
./deploy.sh prod build --service=backend      # Build backend only
./deploy.sh prod build --service=frontend     # Build frontend only

# 🚀 Start/Stop Services
./deploy.sh prod start --service=backend -d   # Start backend in background
./deploy.sh prod stop --service=backend       # Stop backend
```

### Deployment Best Practices

#### Daily Development Workflow
```bash
# 1. Quick redeploy after code changes
./deploy.sh prod restart --service=backend

# 2. Check logs to confirm updates
./deploy.sh prod logs --service=backend -f

# 3. Health check
./deploy.sh prod health
```

#### Dependency Update Workflow
```bash
# 1. When modifying requirements.txt or package.json
./deploy.sh prod build --service=backend --no-cache

# 2. Restart service
./deploy.sh prod start --service=backend -d

# 3. Verify deployment
./deploy.sh prod status
```

#### Docker Layer Cache Mechanism

- **Backend Build Layers**:
  1. `apt-get install` - System dependencies (rarely changes, cached)
  2. `pip install` - Python dependencies (only rebuilds when requirements.txt changes)
  3. Copy application code (changes frequently but builds quickly)

- **Frontend Build Layers**:
  1. `npm install` - Node.js dependencies (only rebuilds when package.json changes)
  2. `npm run build` - Vue.js compilation (rebuilds when code changes)
  3. Nginx configuration (rarely changes)

#### When to Use --no-cache

✅ **Recommended Usage**:
- First-time deployment
- Modified `requirements.txt` or `package.json`
- Modified Dockerfile
- Build issues or anomalies

❌ **Not Recommended**:
- Daily code updates
- Business logic modifications only
- Minor configuration changes

## Development Environment

### Start Development Mode

```bash
# Start with hot reloading
./deploy.sh dev start -d

# Or with Make
make dev

# View logs
./deploy.sh dev logs -f
```

### Development URLs

- **Frontend Dev Server**: http://localhost:8080 (hot reload)
- **Backend**: http://localhost:8000
- **Database**: localhost:3307

### Development Features

- **Hot Reloading**: Frontend automatically reloads on file changes
- **Debug Mode**: Backend runs in debug mode with detailed error messages
- **Volume Mounting**: Source code is mounted for live editing

### Container Restart Policy Configuration

#### Production vs Development Environments

**Production Environment** (`./deploy.sh prod start`):
- ✅ **All containers auto-restart**: Set to `restart: unless-stopped`
- Automatically start all services after system reboot
- Automatically restart on container failure
- Includes: database, backend, frontend, phpmyadmin

**Development Environment** (`./deploy.sh dev start`):
- 🔧 **Configurable restart policy**: Controlled via `DEV_RESTART_POLICY` environment variable
- Defaults to `no` (no auto-restart)
- Flexible adjustment based on development needs

#### Development Environment Restart Policy Options

Set `DEV_RESTART_POLICY` variable in `.env` file:

```env
# Restart policy options
DEV_RESTART_POLICY=no              # No auto-restart (default)
DEV_RESTART_POLICY=unless-stopped  # Restart unless manually stopped (recommended for persistent dev)
DEV_RESTART_POLICY=always          # Always restart
DEV_RESTART_POLICY=on-failure       # Restart only on failure
```

#### Restart Policy Explanation

| Policy | Behavior | Use Case |
|--------|----------|----------|
| `no` | Do not restart containers automatically | Daily development, avoid unexpected restarts |
| `unless-stopped` | Auto-start on system reboot, don't restart when manually stopped | Persistent dev environment, want auto-recovery after reboot |
| `always` | Always restart containers | High-availability development environment |
| `on-failure` | Only restart on container failure | Want auto-recovery on errors |

#### Practical Usage Examples

```bash
# Set development environment to auto-start after system reboot
echo "DEV_RESTART_POLICY=unless-stopped" >> .env
./deploy.sh dev restart

# Check container restart policies
docker inspect lab_web_backend_dev | grep -A 1 "RestartPolicy"
docker inspect lab_web_frontend_dev | grep -A 1 "RestartPolicy"
docker inspect lab_web_db_dev | grep -A 1 "RestartPolicy"

# Restore default (no restart)
echo "DEV_RESTART_POLICY=no" >> .env
./deploy.sh dev restart
```

### Restart Policy Best Practices

#### Recommended Configurations

- **Daily Development**: Use `DEV_RESTART_POLICY=no`
  - Avoid unexpected restarts affecting development workflow
  - Manually start services when needed

- **Long-term Development Environment**: Use `DEV_RESTART_POLICY=unless-stopped`
  - Auto-recovery after system reboot
  - Suitable for scenarios requiring persistent service availability

- **Production Environment**: Automatically uses `unless-stopped`
  - Ensures high service availability
  - Auto-recovery after system reboot

## Configuration

### Docker Commands Quick Reference

#### Using Deploy Script (Recommended)

```bash
# Production
./deploy.sh prod start -d          # Start all services
./deploy.sh prod stop              # Stop all services  
./deploy.sh prod restart           # Restart all services
./deploy.sh prod logs -f           # Follow all logs
./deploy.sh prod status            # Show status
./deploy.sh prod health            # Health check

# Development
./deploy.sh dev start -d           # Start dev environment
./deploy.sh dev logs -f            # Follow dev logs

# Database
./deploy.sh prod db-init           # Initialize database
./deploy.sh prod db-backup         # Backup database
./deploy.sh prod shell --service=db  # MySQL shell
```

#### Using Make (Even Simpler)

```bash
make deploy        # Full deployment
make start         # Start services
make stop          # Stop services
make logs          # Follow logs
make status        # Show status
make dev          # Start development
make db-init      # Initialize database
make urls         # Show service URLs
```

#### Direct Docker Commands

```bash
# Container management
docker ps                              # List running containers
docker ps -a                           # List all containers
docker logs lab_web_backend -f         # View backend logs
docker restart lab_web_frontend        # Restart frontend container

# Enter containers
docker exec -it lab_web_backend /bin/bash
docker exec -it lab_web_db mysql -u root -p

# Docker Compose commands
docker-compose up -d                   # Start services
docker-compose down                    # Stop services
docker-compose logs -f backend         # View specific service logs
```

### Frontend Configuration

#### Environment Files Priority
The frontend loads environment variables in this order:
1. `.env.local` (highest priority, not committed to git)
2. `.env.production` / `.env.development` (mode-specific)
3. `.env` (general fallback)

#### API Configuration
- **Development**: Frontend connects directly to backend at `http://127.0.0.1:8000/api`
- **Docker/Production**: Frontend uses nginx proxy with relative path `/api`
- **Custom**: Override with `.env.local` for specific domain requirements

#### Nginx Configuration
Edit `frontend/docker/nginx.conf` for:
- Server settings
- API proxy configurations (routes `/api` to backend container)
- Media proxy configurations (routes `/media` to backend container)
- Security headers
- Cache policies

#### Code Changes Impact
Recent improvements include:
- ✅ **Removed unused Vuex store** (now uses Pinia exclusively)
- ✅ **Cleaned up environment files** (removed empty `.env.prod`, `.env.test`)
- ✅ **Updated TypeScript configuration** to handle build compatibility
- ✅ **Improved Docker networking** (frontend connects to `lab_web_app` container)

### Backend Configuration

Backend configuration is handled through environment variables and `backend/config/config.py`.

### Database Configuration

MySQL is configured with:
- UTF8MB4 character set for full Unicode support
- Optimized settings for small to medium workloads
- Health checks and automatic restart

## Database Management

### Initialize Database

```bash
# Create tables and sample data
./deploy.sh prod db-init

# Or with Make
make db-init
```

### Database Operations

```bash
# Backup database
./deploy.sh prod db-backup

# Access MySQL shell
./deploy.sh prod shell --service=db
# Or: make db-shell

# Custom SQL execution
docker exec -it lab_web_db mysql -u root -plab_web_root_123 lab_web -e "SELECT COUNT(*) FROM admins;"
```

### Database Migrations

```bash
# Access backend container
./deploy.sh prod shell --service=backend

# Inside container, run migrations
flask db upgrade
```

## SSL/HTTPS Setup

### Using Reverse Proxy (Recommended)

#### Option 1: Nginx Reverse Proxy

Create `/etc/nginx/sites-available/lab-website`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Option 2: Traefik (Docker-based)

Add to `docker-compose.yml`:

```yaml
services:
  traefik:
    image: traefik:v2.9
    command:
      - --api.insecure=true
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.myresolver.acme.httpchallenge=true
      - --certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web
      - --certificatesresolvers.myresolver.acme.email=your-email@example.com
      - --certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt
    labels:
      - "traefik.http.routers.http-catchall.rule=hostregexp(`{host:.+}`)"
      - "traefik.http.routers.http-catchall.entrypoints=web"
      - "traefik.http.routers.http-catchall.middlewares=redirect-to-https"
      - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"

  frontend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`your-domain.com`)"
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=myresolver"

volumes:
  letsencrypt:
```

## Backup and Recovery

### Automated Backups

Create backup script `/etc/cron.daily/lab-website-backup`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/lab-website"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Database backup
docker exec lab_web_db mysqldump -u root -plab_web_root_123 lab_web > "$BACKUP_DIR/db_$DATE.sql"

# Media files backup
docker run --rm -v lab_web_media_data:/data -v "$BACKUP_DIR":/backup alpine tar czf "/backup/media_$DATE.tar.gz" -C /data .

# Keep only last 7 days
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

### Manual Backup/Restore

```bash
# Create backup
./deploy.sh prod db-backup

# Restore from backup
./deploy.sh prod db-restore --backup-file=backup_20231201_120000.sql

# Backup media files
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar czf /backup/media_backup.tar.gz -C /data .

# Restore media files
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar xzf /backup/media_backup.tar.gz -C /data
```

## Monitoring and Logs

### View Logs

```bash
# All services
./deploy.sh prod logs -f

# Specific service
./deploy.sh prod logs --service=backend -f
./deploy.sh prod logs --service=frontend -f

# Or with Make
make logs
make backend-logs
make frontend-logs
```

### Health Monitoring

```bash
# Check all services health
./deploy.sh prod health

# Individual service status
./deploy.sh prod status

# Or with Make
make health
make status
```

### Log Management

Configure log rotation in `/etc/logrotate.d/lab-website`:

```
/path/to/lab_web/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 root root
    postrotate
        docker exec lab_web_backend kill -USR1 1 2>/dev/null || true
    endscript
}
```

## Troubleshooting

### Common Issues

#### 1. Port Conflicts

```bash
# Check what's using ports
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000

# Change ports in .env file
FRONTEND_PORT=3001
BACKEND_PORT=8001
```

#### 2. Database Connection Issues

```bash
# Check database container
docker logs lab_web_db

# Test database connection
docker exec lab_web_db mysqladmin ping -h localhost

# Reset database
./deploy.sh prod stop --service=db
docker volume rm lab_web_mysql_data
./deploy.sh prod start --service=db
./deploy.sh prod db-init
```

#### 3. Permission Issues

```bash
# Fix media directory permissions
docker exec lab_web_backend chown -R www-data:www-data /app/media

# Fix log directory permissions
sudo chown -R $USER:$USER logs/
```

#### 4. Build Failures

```bash
# Clean build cache
./deploy.sh prod build --no-cache --rebuild

# Remove all containers and rebuild
./deploy.sh prod clean
./deploy.sh prod build
```

### Docker Troubleshooting Commands

#### Health Checks

```bash
# Check if services are responding
curl http://localhost:3000/health    # Frontend
curl http://localhost:8000/health    # Backend

# Check database connection
docker exec lab_web_db mysqladmin ping -h localhost

# Check container health status
docker inspect lab_web_frontend --format='{{.State.Health.Status}}'
```

#### Resource Usage and Cleanup

```bash
# Container resource usage
docker stats --no-stream

# Disk usage
docker system df

# Clean unused resources
docker container prune              # Remove stopped containers
docker image prune                  # Remove unused images
docker volume prune                 # Remove unused volumes
docker system prune -a --volumes    # Full cleanup (careful!)
```

#### Container Debugging

```bash
# Check container startup failures
docker logs lab_web_backend

# Check container configuration
docker inspect lab_web_backend

# Check network connectivity
docker network inspect lab_web_default

# Test inter-container connectivity
docker exec lab_web_backend ping db
docker exec lab_web_frontend ping backend
```

#### Volume Management

```bash
# List volumes
docker volume ls | grep lab_web

# Backup volumes
docker run --rm -v lab_web_mysql_data:/data -v $(pwd):/backup alpine tar czf /backup/mysql_backup.tar.gz -C /data .

# Restore volumes
docker run --rm -v lab_web_mysql_data:/data -v $(pwd):/backup alpine tar xzf /backup/mysql_backup.tar.gz -C /data
```

### Emergency Procedures

#### Complete Reset

```bash
# Stop all services
./deploy.sh prod stop

# Remove all containers and volumes (destructive!)
./deploy.sh prod clean

# Start fresh
./deploy.sh prod start -d
./deploy.sh prod db-init
```

#### Pre-Emergency Backup

```bash
# Always backup before destructive operations
./deploy.sh prod db-backup

# Backup media files
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar czf /backup/media_emergency_backup.tar.gz -C /data .
```

#### 5. Frontend Not Loading

```bash
# Check nginx logs
docker logs lab_web_frontend

# Rebuild frontend with fresh modules
cd frontend
docker build --no-cache -t lab-website-frontend .
```

### Debug Mode

Enable debug mode in development:

```bash
# Start in development mode
./deploy.sh dev start -d

# View detailed backend logs
./deploy.sh dev logs --service=backend-dev -f
```

### Container Shell Access

```bash
# Backend shell
./deploy.sh prod shell --service=backend
# Or: make backend-shell

# Frontend shell  
./deploy.sh prod shell --service=frontend
# Or: make frontend-shell

# Database shell
./deploy.sh prod shell --service=db
# Or: make db-shell
```

## Maintenance

### Updates

#### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
./deploy.sh prod stop
./deploy.sh prod build --rebuild
./deploy.sh prod start -d

# Run any new migrations
./deploy.sh prod shell --service=backend
flask db upgrade
```

#### Update Docker Images

```bash
# Pull latest base images
docker pull node:18-alpine
docker pull python:3.9-slim
docker pull mysql:8.0
docker pull nginx:stable-alpine

# Rebuild with updated images
./deploy.sh prod build --no-cache --rebuild
./deploy.sh prod restart
```

### Security Updates

1. **Update base Docker images regularly**
2. **Monitor security advisories for dependencies**
3. **Update passwords and secrets**
4. **Review and update CORS settings**
5. **Keep SSL certificates current**

### Performance Tuning

#### Database Optimization

Edit MySQL configuration:

```yaml
# In docker-compose.yml, add command parameters
command: >
  --character-set-server=utf8mb4
  --collation-server=utf8mb4_unicode_ci
  --innodb-buffer-pool-size=512M
  --innodb-log-file-size=128M
  --max-connections=200
```

#### Frontend Optimization

Update `frontend/docker/nginx.conf`:

```nginx
# Enable gzip compression
gzip on;
gzip_vary on;
gzip_min_length 10240;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

# Browser caching
location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Scaling

For high-traffic deployments:

1. **Use multiple frontend replicas**
2. **Implement Redis caching**  
3. **Set up database read replicas**
4. **Use CDN for static assets**
5. **Implement load balancing**

Example scaling configuration:

```yaml
services:
  frontend:
    deploy:
      replicas: 3
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
      
  nginx-lb:
    image: nginx:alpine
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
      - "443:443"
```

## Production Checklist

Before going live:

- [ ] Change all default passwords
- [ ] Update environment variables for production
- [ ] Configure SSL/HTTPS
- [ ] Set up automated backups
- [ ] Configure log rotation
- [ ] Set up monitoring
- [ ] Test backup and recovery procedures
- [ ] Configure firewall rules
- [ ] Set up domain and DNS
- [ ] Test all functionality
- [ ] Update CORS settings
- [ ] Review security headers
- [ ] Set up error tracking
- [ ] Configure email notifications (if implemented)
- [ ] Document custom configurations

## Related Documentation

Based on your deployment environment and requirements, check these related documents:

### Advanced Deployment
- **[Advanced Deployment Guide (English)](./ADVANCED_DEPLOYMENT.md)** - Cloud servers, local build + image deployment, flexible configurations, and advanced scenarios
- **[進階部署指南 (中文)](./ADVANCED_DEPLOYMENT_zh-CN.md)** - Chinese version of advanced deployment scenarios

### Project Documentation
- **[Main README](../README.md)** - Project overview and feature introduction
- **[Backend Documentation](../backend/README.md)** - Flask API detailed documentation
- **[Frontend Documentation](../frontend/README.md)** - Vue.js frontend configuration and development

## Support

For additional help:

- Check the [main README](../README.md) for feature overview
- Review [backend documentation](../backend/README.md) for API details
- Check [frontend documentation](../frontend/README.md) for UI information
- Create an issue on the project repository
- Check Docker and container logs for error details

---

*This deployment guide is maintained alongside the Lab Website Framework. For the latest updates, check the project repository.*