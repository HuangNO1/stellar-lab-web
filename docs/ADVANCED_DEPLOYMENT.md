# Advanced Deployment Guide

Complete guide for advanced deployment scenarios including cloud servers, local build strategies, and flexible deployment configurations.

> 📘 **Main Deployment Guide**: For standard deployment scenarios, see **[DEPLOYMENT.md](./DEPLOYMENT.md)** first.

## 📋 Table of Contents

- [Cloud Server Deployment](#cloud-server-deployment)
- [Local Build + Image Deployment](#local-build--image-deployment)
- [Flexible Deployment Configurations](#flexible-deployment-configurations)
- [Production Environment Optimization](#production-environment-optimization)
- [Multi-Server and Scaling](#multi-server-and-scaling)
- [Advanced Troubleshooting](#advanced-troubleshooting)

---

# Cloud Server Deployment

Complete deployment guide for Amazon ECS, AWS EC2, Alibaba Cloud ECS, Tencent Cloud, or other cloud server environments.

## 🚀 Cloud Deployment Prerequisites

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 2 vCPU | 4+ vCPU |
| **Memory** | 4GB RAM | 8GB+ RAM |
| **Storage** | 20GB | 50GB+ (SSD) |
| **Network** | Public IP | Static IP + CDN |

### System Requirements

- **Operating System**: 
  - Ubuntu 20.04+ (Recommended)
  - CentOS 8+ / Rocky Linux 8+
  - Amazon Linux 2
  - Debian 11+

- **Software Requirements**:
  - Docker 20.10+
  - Docker Compose 2.0+
  - Git
  - curl, wget
  - sudo privileges

### Network Requirements

- **Inbound Ports**: 80, 443, 22 (SSH)
- **Outbound**: Full internet access for Docker image downloads
- **Optional**: Custom ports for development (3000, 8000, 8081)

## 📋 Cloud Server Deployment Steps

### Step 1: Server Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y curl wget git unzip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Step 2: Clone and Configure Project

```bash
# Clone repository
git clone <your-repository-url>
cd lab_web

# Configure environment
cp .env.example .env
nano .env  # Edit production settings
```

### Step 3: Required Configuration Changes for Cloud

Edit `.env` file for cloud deployment:

```env
# Security - MUST CHANGE for production
SECRET_KEY=your_very_secure_secret_key_here_min_32_chars
JWT_SECRET_KEY=your_jwt_secret_key_here_min_32_chars
MYSQL_ROOT_PASSWORD=your_very_secure_database_password

# Network Configuration (adjust ports if needed)
FRONTEND_PORT=3000
BACKEND_PORT=8000
MYSQL_PORT=3307
PHPMYADMIN_PORT=8081

# CORS Configuration (replace with your domain)
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com

# Flask Configuration
FLASK_CONFIG=production
```

### Step 4: Deploy on Cloud Server

```bash
# Build and start services
./deploy.sh prod build
./deploy.sh prod start -d

# Initialize database
./deploy.sh prod db-init

# Verify deployment
./deploy.sh prod status
./deploy.sh prod health
```

### Step 5: Cloud-Specific Optimizations

#### Configure Firewall (Ubuntu/CentOS)

```bash
# Ubuntu (ufw)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

#### Set Up Reverse Proxy (Nginx)

```bash
# Install Nginx
sudo apt install nginx -y

# Configure reverse proxy
sudo tee /etc/nginx/sites-available/lab-website << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/lab-website /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### SSL Certificate with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

# Local Build + Image Deployment

Fast deployment solution: Build Docker images locally, package and upload to server, avoiding time-consuming builds on the server.

## 🚀 Advantages

- **⚡ Fast**: Server deployment time reduced from 10-15 minutes to 2-3 minutes
- **📦 Offline Deployment**: Supports offline environments without server internet access
- **🔄 Version Control**: Support for multi-version image management
- **🛠️ Flexibility**: Selective frontend or backend updates
- **💾 Resource Efficient**: Reduces server CPU and network usage
- **🌏 Optimized**: Built-in mirror acceleration for better network connectivity

## 📋 Local Build Workflow

### Step 1: Local Image Building

Create build script `scripts/build-images.sh`:

```bash
#!/bin/bash
set -e

VERSION="${1:-latest}"
BUILD_BACKEND=true
BUILD_FRONTEND=true
NO_CACHE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            BUILD_FRONTEND=false
            shift
            ;;
        --frontend-only)
            BUILD_BACKEND=false
            shift
            ;;
        --no-cache)
            NO_CACHE="--no-cache"
            shift
            ;;
        *)
            VERSION="$1"
            shift
            ;;
    esac
done

echo "Building images with version: $VERSION"

if [ "$BUILD_BACKEND" = true ]; then
    echo "Building backend image..."
    docker build $NO_CACHE -t lab-website-backend:$VERSION ./backend
fi

if [ "$BUILD_FRONTEND" = true ]; then
    echo "Building frontend image..."
    docker build $NO_CACHE -t lab-website-frontend:$VERSION ./frontend
fi

echo "Build completed!"
docker images | grep lab-website
```

### Step 2: Package and Upload

Create packaging script `scripts/package-images.sh`:

```bash
#!/bin/bash
set -e

VERSION="${1:-latest}"
PACKAGE_ONLY=false
SERVER=""
USER="root"
REMOTE_PATH="/opt/lab_web"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --package-only)
            PACKAGE_ONLY=true
            shift
            ;;
        --server)
            SERVER="$2"
            shift 2
            ;;
        --user)
            USER="$2"
            shift 2
            ;;
        --path)
            REMOTE_PATH="$2"
            shift 2
            ;;
        *)
            VERSION="$1"
            shift
            ;;
    esac
done

# Create deployment package
PACKAGE_DIR="docker-images"
mkdir -p $PACKAGE_DIR

echo "Exporting Docker images..."
docker save lab-website-backend:$VERSION | gzip > $PACKAGE_DIR/backend-$VERSION.tar.gz
docker save lab-website-frontend:$VERSION | gzip > $PACKAGE_DIR/frontend-$VERSION.tar.gz

# Copy deployment files
cp docker-compose.yml $PACKAGE_DIR/
cp .env.example $PACKAGE_DIR/.env
cp deploy.sh $PACKAGE_DIR/

# Create deployment script for server
cat > $PACKAGE_DIR/deploy-from-images.sh << 'EOF'
#!/bin/bash
set -e

VERSION="${1:-latest}"

echo "Loading Docker images..."
docker load < backend-$VERSION.tar.gz
docker load < frontend-$VERSION.tar.gz

echo "Starting services..."
docker-compose down 2>/dev/null || true
docker-compose up -d

echo "Deployment completed!"
EOF

chmod +x $PACKAGE_DIR/deploy-from-images.sh

if [ "$PACKAGE_ONLY" = true ]; then
    echo "Package created in $PACKAGE_DIR/"
    echo "Upload to server and run: ./deploy-from-images.sh $VERSION"
    exit 0
fi

if [ -n "$SERVER" ]; then
    echo "Uploading to server $SERVER..."
    rsync -av --progress $PACKAGE_DIR/ $USER@$SERVER:$REMOTE_PATH/
    
    echo "Deploying on server..."
    ssh $USER@$SERVER "cd $REMOTE_PATH && ./deploy-from-images.sh $VERSION"
    
    echo "Deployment completed on $SERVER!"
fi
```

### Step 3: Server Deployment

On the server, after uploading the package:

```bash
# Load and deploy images
cd /path/to/uploaded/package
./deploy-from-images.sh latest

# Verify deployment
docker-compose ps
curl http://localhost:3000
```

---

# Flexible Deployment Configurations

Support for various deployment scenarios and environment configurations.

## 🎯 Supported Deployment Modes

### 1. Complete Deployment Mode
All components (frontend, backend, database) deployed in the same environment.

### 2. Separated Deployment Mode
Frontend and backend deployed independently, supporting different servers or cloud platforms.

### 3. External Database Mode
Using existing MySQL database servers.

### 4. Development Mode
Suitable for local development and testing.

## 🔧 Environment Variable Configuration

### Frontend Container Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | `http://lab_web_app:8000` | Backend service address (internal communication) |
| `API_BASE_URL` | `/api` | API base path |
| `CORS_ORIGIN` | `*` | CORS settings |
| `APP_TITLE` | `Lab Website Framework` | Application title |
| `APP_DESCRIPTION` | `Modern laboratory website framework` | Application description |

### Backend Container Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `mysql+pymysql://root:lab_web_root_123@db:3306/lab_web` | Complete database connection string |
| `MYSQL_HOST` | `db` | MySQL host address |
| `MYSQL_PORT` | `3306` | MySQL port |
| `MYSQL_ROOT_PASSWORD` | `lab_web_root_123` | MySQL root password |
| `MYSQL_DATABASE` | `lab_web` | Database name |
| `SECRET_KEY` | `change_me_in_production` | Flask secret key |
| `JWT_SECRET_KEY` | `change_me_jwt_in_production` | JWT secret key |
| `FLASK_CONFIG` | `production` | Flask configuration mode |
| `CORS_ORIGINS` | `*` | CORS whitelist |
| `UPLOAD_FOLDER` | `/app/media` | File upload directory |

## 🚀 Deployment Examples

### 1. Complete Deployment (Recommended for Beginners)

```bash
# Create docker-compose.yml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: your_secure_password
      MYSQL_DATABASE: lab_web
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped

  backend:
    image: lab-website-backend:latest
    environment:
      DATABASE_URL: mysql+pymysql://root:your_secure_password@db:3306/lab_web
      SECRET_KEY: your_secret_key
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    image: lab-website-frontend:latest
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  mysql_data:
```

### 2. Separated Deployment

**Backend Server:**
```bash
# docker-compose.backend.yml
version: '3.8'

services:
  backend:
    image: lab-website-backend:latest
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://user:pass@external-db-server:3306/lab_web
      SECRET_KEY: your_secret_key
      CORS_ORIGINS: https://your-frontend-domain.com
    restart: unless-stopped
```

**Frontend Server:**
```bash
# docker-compose.frontend.yml
version: '3.8'

services:
  frontend:
    image: lab-website-frontend:latest
    ports:
      - "80:80"
    environment:
      API_BASE_URL: https://your-backend-domain.com/api
    restart: unless-stopped
```

### 3. External Database Mode

```bash
version: '3.8'

services:
  backend:
    image: lab-website-backend:latest
    environment:
      DATABASE_URL: mysql+pymysql://username:password@external-mysql-server.com:3306/lab_web
      SECRET_KEY: your_secret_key
    restart: unless-stopped

  frontend:
    image: lab-website-frontend:latest
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

---

# Production Environment Optimization

Advanced optimization strategies for production environments.

## 🚀 Performance Optimization

### Database Optimization

```yaml
# Enhanced MySQL configuration
services:
  db:
    image: mysql:8.0
    command: >
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --innodb-buffer-pool-size=1G
      --innodb-log-file-size=256M
      --max-connections=500
      --query-cache-size=128M
      --query-cache-type=1
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
        reservations:
          memory: 1G
          cpus: '1.0'
```

### Frontend Optimization

```bash
# Enhanced Nginx configuration
gzip on;
gzip_vary on;
gzip_min_length 10240;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/x-javascript
    application/xml+rss
    application/javascript
    application/json;

# Browser caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
```

### Backend Optimization

```yaml
services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
    environment:
      WORKERS: 4
      THREADS: 2
      TIMEOUT: 30
```

## 🔒 Security Hardening

### Container Security

```yaml
services:
  backend:
    read_only: true
    user: "1000:1000"
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
```

### Network Security

```yaml
networks:
  frontend:
    driver: bridge
    internal: false
  backend:
    driver: bridge
    internal: true
  database:
    driver: bridge
    internal: true
```

---

# Multi-Server and Scaling

Strategies for deploying across multiple servers and scaling.

## 🏗️ Load Balancing Setup

### Nginx Load Balancer

```nginx
upstream backend_servers {
    server backend1.example.com:8000;
    server backend2.example.com:8000;
    server backend3.example.com:8000;
}

upstream frontend_servers {
    server frontend1.example.com:3000;
    server frontend2.example.com:3000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://frontend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Swarm Deployment

```yaml
version: '3.8'

services:
  frontend:
    image: lab-website-frontend:latest
    deploy:
      replicas: 3
      placement:
        constraints: [node.role == worker]
      restart_policy:
        condition: on-failure
    networks:
      - frontend

  backend:
    image: lab-website-backend:latest
    deploy:
      replicas: 5
      placement:
        constraints: [node.role == worker]
    networks:
      - frontend
      - backend

  db:
    image: mysql:8.0
    deploy:
      replicas: 1
      placement:
        constraints: [node.role == manager]
    networks:
      - backend
```

## 📊 Monitoring and Logging

### Prometheus + Grafana Setup

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Centralized Logging

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node

  logstash:
    image: docker.elastic.co/logstash/logstash:7.14.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    ports:
      - "5601:5601"
```

---

# Advanced Troubleshooting

Advanced troubleshooting techniques for complex deployment scenarios.

## 🔍 Container Debugging

### Deep Container Inspection

```bash
# Inspect container configuration
docker inspect lab_web_backend | jq '.[0].Config'

# Check resource usage
docker stats --no-stream

# View container processes
docker exec lab_web_backend ps aux

# Network connectivity test
docker exec lab_web_backend ping db
docker exec lab_web_backend curl -v http://db:3306
```

### Application-Level Debugging

```bash
# Backend debugging
docker exec -it lab_web_backend bash
python -c "from app import create_app; app = create_app(); print(app.config)"

# Database debugging
docker exec -it lab_web_db mysql -u root -p
mysql> SHOW PROCESSLIST;
mysql> SHOW ENGINE INNODB STATUS\G
```

## 📊 Performance Analysis

### Database Performance

```sql
-- Slow query analysis
SELECT * FROM performance_schema.events_statements_summary_by_digest 
ORDER BY avg_timer_wait DESC LIMIT 10;

-- Connection analysis
SELECT * FROM performance_schema.hosts;
```

### Application Performance

```bash
# Memory usage analysis
docker exec lab_web_backend python -c "
import psutil
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'CPU: {psutil.cpu_percent()}%')
"

# Request tracing
docker logs lab_web_backend | grep -E "(POST|GET|PUT|DELETE)" | tail -50
```

## 🚨 Recovery Procedures

### Database Recovery

```bash
# Point-in-time recovery
docker exec lab_web_db mysqldump --single-transaction \
  --routines --triggers --all-databases > full_backup.sql

# Binary log recovery
docker exec lab_web_db mysqlbinlog /var/lib/mysql/binlog.000001 \
  --start-datetime="2023-12-01 10:00:00" \
  --stop-datetime="2023-12-01 11:00:00" > recovery.sql
```

### Application Recovery

```bash
# Rolling back to previous version
docker tag lab-website-backend:latest lab-website-backend:backup
docker pull lab-website-backend:previous
docker tag lab-website-backend:previous lab-website-backend:latest
docker-compose up -d backend

# Data volume backup and restore
docker run --rm -v lab_web_mysql_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/mysql_backup.tar.gz -C /data .
```

---

## Support and Further Reading

For additional help with advanced deployments:

- **Main Deployment Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Project Documentation**: [../README.md](../README.md)
- **Backend API Reference**: [../backend/README.md](../backend/README.md)
- **Frontend Configuration**: [../frontend/README.md](../frontend/README.md)

---

*This advanced deployment guide is maintained alongside the Lab Website Framework. For the latest updates, check the project repository.*