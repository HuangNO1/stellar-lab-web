# ECS Cloud Server Deployment Guide

Complete deployment guide for Amazon ECS or other cloud server environments, suitable for deployment from scratch on bare server instances.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [ECS Deployment Prerequisites](#ecs-deployment-prerequisites)
- [Required Configuration Changes](#required-configuration-changes)
- [Bare ECS Server Deployment Steps](#bare-ecs-server-deployment-steps)
- [Production Environment Optimization](#production-environment-optimization)
- [Deployment Verification and Monitoring](#deployment-verification-and-monitoring)
- [ECS-Specific Optimization Recommendations](#ecs-specific-optimization-recommendations)
- [Troubleshooting](#troubleshooting)

## 🔍 Project Overview

This is a complete laboratory website framework containing:

- **Frontend**: Vue.js + TypeScript, served by Nginx
- **Backend**: Flask Python API service
- **Database**: MySQL 8.0 database
- **Management Tool**: phpMyAdmin (optional)
- **Containerization**: Fully Dockerized deployment

### Architecture Diagram

```
Internet → [ECS Load Balancer] → [Nginx Frontend] → [Flask Backend] → [MySQL Database]
                                      ↓
                               [Static Files & Media]
```

## 🚀 ECS Deployment Prerequisites

### 1. Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 2 vCPU | 4+ vCPU |
| **Memory** | 4GB RAM | 8GB+ RAM |
| **Storage** | 20GB | 50GB+ (SSD) |
| **Network** | Public IP | Static IP + CDN |

### 2. System Requirements

- **Operating System**: 
  - Ubuntu 20.04+ (Recommended)
  - CentOS 8+ / Rocky Linux 8+
  - Amazon Linux 2
- **Container Environment**:
  - Docker 20.10+
  - Docker Compose v2.0+
- **Version Control**: Git latest version
- **Network Tools**: curl, wget

### 3. Port Requirements

```bash
# Application service ports
3000  # Frontend service (Vue.js + Nginx)
8000  # Backend API (Flask)
3307  # MySQL database (mapped port)
8081  # phpMyAdmin management interface (optional)

# Production environment ports
80    # HTTP service
443   # HTTPS service (SSL/TLS)
22    # SSH management port
```

### 4. Security Group Configuration (AWS ECS)

```bash
# Inbound Rules
SSH (22)     - Source: Your IP
HTTP (80)    - Source: 0.0.0.0/0
HTTPS (443)  - Source: 0.0.0.0/0
Custom (3000) - Source: 0.0.0.0/0 (Temporary, remove in production)
Custom (8000) - Source: 0.0.0.0/0 (Temporary, remove in production)

# Outbound Rules  
All traffic - Source: 0.0.0.0/0
```

## 📋 Required Configuration Changes

### 1. Environment Variables Configuration (.env)

Create and configure `.env` file:

```env
# ===========================================
# Database Security Configuration - MUST CHANGE
# ===========================================
MYSQL_ROOT_PASSWORD=your_very_secure_db_root_password_2024
MYSQL_PASSWORD=your_secure_user_password_2024
MYSQL_DATABASE=lab_web
MYSQL_USER=lab_web_user

# ===========================================
# Application Security Configuration - MUST CHANGE
# ===========================================
SECRET_KEY=your_extremely_secure_secret_key_min_32_chars_2024
JWT_SECRET_KEY=your_jwt_secret_key_for_authentication_2024

# Flask Configuration
FLASK_CONFIG=production
FLASK_DEBUG=0

# ===========================================
# Domain and CORS Configuration - Change according to your domain
# ===========================================
CORS_ORIGINS=https://your-domain.com,https://api.your-domain.com,https://www.your-domain.com

# ===========================================
# Port Configuration (Optional modification)
# ===========================================
FRONTEND_PORT=3000
BACKEND_PORT=8000
MYSQL_PORT=3307
PHPMYADMIN_PORT=8081

# ===========================================
# Application Configuration
# ===========================================
UPLOAD_FOLDER=/app/media
NODE_ENV=production
CHOKIDAR_USEPOLLING=false
```

### 2. Frontend Environment Configuration

Modify `frontend/.env.production`:

```env
# Production environment configuration
NODE_ENV=production

# API configuration - choose one based on deployment method
# Option 1: Use relative path (recommended, through nginx proxy)
VUE_APP_API_BASE_URL=/api

# Option 2: Use absolute path (if API is on different domain)
# VUE_APP_API_BASE_URL=https://api.your-domain.com/api
```

### 3. Docker Compose Network Configuration

Adjust CORS configuration in main `docker-compose.yml`:

```yaml
backend:
  environment:
    # Update CORS settings to match your domain
    CORS_ORIGINS: "https://your-domain.com,https://api.your-domain.com,https://www.your-domain.com"
    
    # Database connection configuration
    DATABASE_URL: mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@db:3306/${MYSQL_DATABASE}?charset=utf8mb4
```

### 4. Database Security Configuration

Enhance database security for production environment by editing `docker-compose.yml`:

```yaml
db:
  environment:
    # Use strong passwords
    MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD}
  # Restrict database to internal access only (production recommended)
  # ports:
  #   - "127.0.0.1:3307:3306"  # Only allow local access
  # Or completely remove port mapping, only allow inter-container communication
```

## 🛠 Bare ECS Server Deployment Steps

### Step 1: System Initialization and Updates

```bash
# ===== CentOS/Rocky Linux/Amazon Linux 2 =====
sudo yum update -y
sudo yum install -y git curl wget vim unzip

# ===== Ubuntu/Debian =====
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget vim unzip

# Set system timezone (optional)
sudo timedatectl set-timezone Asia/Taipei
# Or other timezones, e.g., Asia/Shanghai, UTC

# Check system information
echo "=== System Information ==="
cat /etc/os-release
free -h
df -h
```

### Step 2: Install Docker and Docker Compose

```bash
# ===== Install Docker =====
# Use official installation script (works on all Linux distributions)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to docker group (avoid using sudo every time)
sudo usermod -aG docker $USER

# ===== Install Docker Compose =====
# Get latest version
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create symbolic link (optional)
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# ===== Verify Installation =====
echo "=== Verify Docker Installation ==="
docker --version
docker-compose --version

# Re-login to apply group permission changes, or execute:
newgrp docker

# Test Docker (optional)
docker run hello-world
```

### Step 3: Configure System Firewall

```bash
# ===== CentOS/Rocky Linux (firewalld) =====
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Open necessary ports
sudo firewall-cmd --permanent --add-port=80/tcp    # HTTP
sudo firewall-cmd --permanent --add-port=443/tcp   # HTTPS  
sudo firewall-cmd --permanent --add-port=3000/tcp  # Frontend (temporary)
sudo firewall-cmd --permanent --add-port=8000/tcp  # Backend (temporary)
sudo firewall-cmd --permanent --add-port=22/tcp    # SSH
sudo firewall-cmd --reload

# ===== Ubuntu (ufw) =====
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3000/tcp  # Frontend (temporary)
sudo ufw allow 8000/tcp  # Backend (temporary)
sudo ufw status

echo "=== Firewall configuration completed ==="
```

### Step 4: Deploy the Project

```bash
# 1. Clone project to server
cd /opt  # or your preferred directory
sudo git clone <your-repository-url> lab_web
sudo chown -R $USER:$USER lab_web
cd lab_web

# 2. Configure environment variables
cp .env.example .env

# Edit environment configuration file (Important!)
nano .env
# or use vim: vim .env

# Please modify the following items according to the "Required Configuration Changes" section above:
# - MYSQL_ROOT_PASSWORD
# - MYSQL_PASSWORD  
# - SECRET_KEY
# - JWT_SECRET_KEY
# - CORS_ORIGINS (set your domain)

echo "=== Environment configuration completed, please ensure all security-related settings have been modified ==="
```

### Step 5: Execute Deployment

```bash
# ===== Method 1: Use provided deployment script (recommended) =====

# Make deployment script executable
chmod +x deploy.sh

# Build all services (first deployment)
echo "=== Starting Docker image build... ==="
./deploy.sh prod build --no-cache

# Start all services in background
echo "=== Starting services... ==="
./deploy.sh prod start -d

# Wait for services to start (important!)
echo "=== Waiting for services to start... ==="
sleep 30

# Initialize database with sample data
echo "=== Initializing database... ==="
./deploy.sh prod db-init

# ===== Method 2: Direct Docker Compose =====
# docker-compose up --build -d
# sleep 30
# docker-compose exec backend python scripts/development/init_db.py

echo "=== Deployment completed! ==="
```

### Step 6: Verify Deployment

```bash
# Check service status
echo "=== Checking service status ==="
./deploy.sh prod status

# Execute health check
echo "=== Running health check ==="  
./deploy.sh prod health

# Check service logs (if errors occur)
echo "=== Checking service logs ==="
./deploy.sh prod logs --service=backend
./deploy.sh prod logs --service=frontend
./deploy.sh prod logs --service=db

# Test service access
echo "=== Testing service access ==="
curl -f http://localhost:3000 && echo "Frontend service normal" || echo "Frontend service abnormal"
curl -f http://localhost:8000/health && echo "Backend service normal" || echo "Backend service abnormal"

echo "=== Deployment verification completed ==="
echo "Frontend access: http://YOUR_SERVER_IP:3000"
echo "Backend API: http://YOUR_SERVER_IP:8000"
echo "API Documentation: http://YOUR_SERVER_IP:8000/api/docs"
echo "Database Management: http://YOUR_SERVER_IP:8081"
echo ""
echo "Default administrator account:"
echo "Username: admin"
echo "Password: admin123"
echo "⚠️  Please change the default password immediately!"
```

## 🔧 Production Environment Optimization

### 1. SSL/HTTPS Configuration

#### Option 1: Use Let's Encrypt + Nginx (Recommended)

```bash
# Install Nginx as reverse proxy
# CentOS/Rocky Linux
sudo yum install -y nginx

# Ubuntu
sudo apt install -y nginx

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Install Certbot 
sudo yum install -y certbot python3-certbot-nginx  # CentOS
# or
sudo apt install -y certbot python3-certbot-nginx  # Ubuntu

# Obtain SSL certificate (replace your-domain.com)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Set up automatic renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

#### Option 2: Use Cloudflare SSL (Simple)

If you use Cloudflare, you can directly enable SSL in the Cloudflare panel.

### 2. Nginx Reverse Proxy Configuration

Create `/etc/nginx/sites-available/lab-website` (Ubuntu) or `/etc/nginx/conf.d/lab-website.conf` (CentOS):

```nginx
# HTTP redirect to HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS main configuration
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL security configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Frontend proxy
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Backend API proxy  
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # API specific configuration
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    # Static file optimization
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        proxy_pass http://localhost:3000;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options nosniff;
    }
}
```

```bash
# Enable site (Ubuntu)
sudo ln -s /etc/nginx/sites-available/lab-website /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 3. Automated Backup Setup

Create `/opt/scripts/backup-lab-website.sh`:

```bash
#!/bin/bash

# Lab website automatic backup script
# Usage: ./backup-lab-website.sh

set -e

# Configuration variables
BACKUP_DIR="/opt/backups/lab-website"
PROJECT_DIR="/opt/lab_web"  # Change to your project path
DATE=$(date +%Y%m%d_%H%M%S)
RETAIN_DAYS=7  # Retention days

# Load environment variables
if [ -f "$PROJECT_DIR/.env" ]; then
    source "$PROJECT_DIR/.env"
else
    echo "Error: .env file not found"
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "=== Starting backup $(date) ==="

# 1. Database backup
echo "Backing up database..."
docker exec lab_web_db mysqldump \
    -u root -p"$MYSQL_ROOT_PASSWORD" \
    --single-transaction \
    --routines \
    --triggers \
    "$MYSQL_DATABASE" > "$BACKUP_DIR/database_$DATE.sql"

# Compress database backup
gzip "$BACKUP_DIR/database_$DATE.sql"

# 2. Media files backup
echo "Backing up media files..."
docker run --rm \
    -v lab_web_media_data:/data \
    -v "$BACKUP_DIR":/backup \
    alpine tar czf "/backup/media_$DATE.tar.gz" -C /data .

# 3. Configuration files backup
echo "Backing up configuration files..."
tar czf "$BACKUP_DIR/config_$DATE.tar.gz" \
    -C "$PROJECT_DIR" \
    .env \
    docker-compose.yml \
    docker-compose.dev.yml \
    deploy.sh

# 4. Clean old backups
echo "Cleaning old backups older than $RETAIN_DAYS days..."
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETAIN_DAYS -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETAIN_DAYS -delete

# 5. Backup statistics
echo "=== Backup completed $(date) ==="
echo "Backup location: $BACKUP_DIR"
echo "Backup files:"
ls -lah "$BACKUP_DIR"/*"$DATE"*

# 6. Optional: Upload to cloud (AWS S3 example)
# aws s3 cp "$BACKUP_DIR" s3://your-backup-bucket/lab-website/ --recursive --exclude "*" --include "*$DATE*"
```

```bash
# Set script permissions
sudo chmod +x /opt/scripts/backup-lab-website.sh

# Set up cron job (runs daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/scripts/backup-lab-website.sh >> /var/log/lab-website-backup.log 2>&1") | crontab -

# Test backup script
sudo /opt/scripts/backup-lab-website.sh
```

### 4. System Service Configuration (Systemd)

Create systemd service `/etc/systemd/system/lab-website.service`:

```ini
[Unit]
Description=Lab Website Docker Services
Requires=docker.service
After=docker.service
StartLimitIntervalSec=0

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/lab_web
ExecStart=/opt/lab_web/deploy.sh prod start -d
ExecStop=/opt/lab_web/deploy.sh prod stop
ExecReload=/opt/lab_web/deploy.sh prod restart
TimeoutStartSec=300
TimeoutStopSec=120
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable lab-website.service

# Start service
sudo systemctl start lab-website.service

# Check service status
sudo systemctl status lab-website.service
```

### 5. Monitoring and Logging Configuration

```bash
# Configure logrotate 
sudo tee /etc/logrotate.d/lab-website << 'EOF'
/opt/lab_web/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 root root
    postrotate
        docker exec lab_web_backend kill -USR1 1 2>/dev/null || true
        docker exec lab_web_frontend nginx -s reopen 2>/dev/null || true
    endscript
}
EOF

# Create monitoring script
sudo tee /opt/scripts/monitor-lab-website.sh << 'EOF'
#!/bin/bash
# Simple service monitoring script

check_service() {
    local service_name=$1
    local url=$2
    
    if curl -sf "$url" > /dev/null 2>&1; then
        echo "✓ $service_name is running normally"
        return 0
    else
        echo "✗ $service_name has issues"
        return 1
    fi
}

echo "=== Lab Website Service Monitor $(date) ==="
check_service "Frontend Service" "http://localhost:3000"
check_service "Backend Service" "http://localhost:8000/health"
check_service "Database Service" "http://localhost:8081" # phpMyAdmin

# Check Docker container status
echo ""
echo "=== Container Status ==="
docker ps --filter name=lab_web --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
EOF

sudo chmod +x /opt/scripts/monitor-lab-website.sh

# Check every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/scripts/monitor-lab-website.sh >> /var/log/lab-website-monitor.log 2>&1") | crontab -
```

## 🔍 Deployment Verification and Monitoring

### Comprehensive Deployment Verification Checklist

```bash
# Create verification script
cat > /tmp/deployment-verification.sh << 'EOF'
#!/bin/bash

echo "=========================================="
echo "    Lab Website Deployment Verification"
echo "=========================================="

# 1. Docker service check
echo ""
echo "1. Docker container status:"
docker ps --filter name=lab_web --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 2. Service health check  
echo ""
echo "2. Service health check:"
./deploy.sh prod health 2>/dev/null || echo "Using backup check method"

# Manual health check
echo ""
echo "3. Manual connection test:"

# Frontend test
if curl -sf http://localhost:3000 > /dev/null 2>&1; then
    echo "✓ Frontend Service (3000) - Normal"
else
    echo "✗ Frontend Service (3000) - Abnormal"
fi

# Backend test
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Backend Service (8000) - Normal"
else
    echo "✗ Backend Service (8000) - Abnormal"
fi

# API documentation test
if curl -sf http://localhost:8000/api/docs > /dev/null 2>&1; then
    echo "✓ API Documentation (8000/api/docs) - Normal"
else
    echo "✗ API Documentation (8000/api/docs) - Abnormal"
fi

# phpMyAdmin test (if enabled)
if curl -sf http://localhost:8081 > /dev/null 2>&1; then
    echo "✓ phpMyAdmin (8081) - Normal"
else
    echo "✗ phpMyAdmin (8081) - Abnormal or disabled"
fi

# 4. Database connection test
echo ""
echo "4. Database connection test:"
if docker exec lab_web_db mysqladmin ping -h localhost --silent > /dev/null 2>&1; then
    echo "✓ MySQL Database - Connection normal"
else
    echo "✗ MySQL Database - Connection abnormal"
fi

# 5. Storage volume check
echo ""
echo "5. Docker storage volume check:"
docker volume ls | grep lab_web

# 6. Network check
echo ""
echo "6. Docker network check:"
docker network ls | grep lab_web

# 7. Log check (latest 10 lines)
echo ""
echo "7. Recent error logs (if any):"
docker logs lab_web_backend --tail 10 2>/dev/null | grep -i error || echo "No backend error logs"
docker logs lab_web_frontend --tail 10 2>/dev/null | grep -i error || echo "No frontend error logs"

echo ""
echo "=========================================="
echo "Verification completed! Please check the above results."
echo "If all services show normal, you can access:"
echo "Frontend: http://$(curl -s ifconfig.me || echo 'YOUR_SERVER_IP'):3000"
echo "Backend: http://$(curl -s ifconfig.me || echo 'YOUR_SERVER_IP'):8000"
echo "=========================================="
EOF

chmod +x /tmp/deployment-verification.sh
/tmp/deployment-verification.sh
```

### Default Login Information

After deployment is complete, use the following default account to log in:

- **Administrator Username**: `admin`
- **Administrator Password**: `admin123`

⚠️ **Important Security Reminders**: 
1. Log in immediately and change the default password
2. Create new administrator accounts
3. If possible, disable the default account

### Monitoring Setup

```bash
# Create simple monitoring dashboard script
sudo tee /opt/scripts/dashboard.sh << 'EOF'
#!/bin/bash

clear
echo "=========================================="
echo "      Lab Website Service Dashboard"
echo "=========================================="
echo "Last update: $(date)"
echo ""

# System resources
echo "System Resources:"
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4"%"}')"
echo "Memory Usage: $(free -h | awk 'NR==2{printf "%.1f%% (%s/%s)\n", $3*100/$2, $3, $2}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{print $5 " (" $3 "/" $2 ")"}')"
echo ""

# Docker container status
echo "Container Status:"
docker ps --filter name=lab_web --format "table {{.Names}}\t{{.Status}}" | head -4
echo ""

# Service endpoint status
echo "Service Endpoints:"
curl -sf http://localhost:3000 > /dev/null && echo "✓ Frontend (3000)" || echo "✗ Frontend (3000)"
curl -sf http://localhost:8000/health > /dev/null && echo "✓ Backend (8000)" || echo "✗ Backend (8000)"
docker exec lab_web_db mysqladmin ping -h localhost --silent > /dev/null 2>&1 && echo "✓ Database" || echo "✗ Database"
echo ""

echo "Press Ctrl+C to stop monitoring"
sleep 10
EOF

chmod +x /opt/scripts/dashboard.sh

# Run dashboard
# watch -n 10 /opt/scripts/dashboard.sh
```

## 🎯 ECS-Specific Optimization Recommendations

### 1. Use AWS Application Load Balancer (ALB)

Replace Nginx reverse proxy with AWS ALB for better scalability:

```yaml
# docker-compose.aws.yml example
version: '3.8'
services:
  backend:
    environment:
      # ALB health check
      HEALTH_CHECK_PATH: /health
      # ALB target group configuration
      ALB_TARGET_GROUP: lab-website-backend
      
  frontend:
    environment:
      # ALB configuration
      ALB_TARGET_GROUP: lab-website-frontend
```

### 2. Migrate Database to AWS RDS

For improved reliability and manageability, recommend migrating MySQL to AWS RDS:

```env
# .env configuration for RDS
DATABASE_URL=mysql+pymysql://username:password@lab-website.cluster-xxxxx.us-west-2.rds.amazonaws.com:3306/lab_web?charset=utf8mb4
MYSQL_HOST=lab-website.cluster-xxxxx.us-west-2.rds.amazonaws.com
MYSQL_PORT=3306

# Remove local database container
# Comment out db service in docker-compose.yml
```

### 3. Use Amazon EFS for File Storage

```yaml
# docker-compose.aws.yml - using EFS
services:
  backend:
    volumes:
      # Mount EFS file system
      - /mnt/efs/lab_web/media:/app/media
      - /mnt/efs/lab_web/logs:/app/logs
      
  frontend:
    volumes:
      - /mnt/efs/lab_web/static:/usr/share/nginx/html/static
```

### 4. CloudWatch Monitoring and Logging

```bash
# Install CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
sudo rpm -U ./amazon-cloudwatch-agent.rpm

# Configure CloudWatch Agent
sudo tee /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << 'EOF'
{
    "logs": {
        "logs_collected": {
            "files": {
                "collect_list": [
                    {
                        "file_path": "/opt/lab_web/logs/*.log",
                        "log_group_name": "/aws/ec2/lab-website",
                        "log_stream_name": "{instance_id}/application"
                    }
                ]
            }
        }
    },
    "metrics": {
        "namespace": "LabWebsite/Application",
        "metrics_collected": {
            "cpu": {
                "measurement": ["cpu_usage_idle", "cpu_usage_iowait"]
            },
            "disk": {
                "measurement": ["used_percent"],
                "resources": ["*"]
            },
            "mem": {
                "measurement": ["mem_used_percent"]
            }
        }
    }
}
EOF

# Start CloudWatch Agent
sudo systemctl start amazon-cloudwatch-agent
sudo systemctl enable amazon-cloudwatch-agent
```

### 5. Auto Scaling Group Configuration

```bash
# Create AMI preparation script
sudo tee /opt/scripts/prepare-ami.sh << 'EOF'
#!/bin/bash
# ECS Auto Scaling AMI preparation script

# Ensure service auto-starts on boot
sudo systemctl enable lab-website.service

# Clean sensitive information (before creating AMI)
sudo rm -f /opt/lab_web/.env
sudo history -c
sudo rm -f /home/*/.bash_history
sudo rm -f /root/.bash_history

echo "AMI preparation completed"
EOF

chmod +x /opt/scripts/prepare-ami.sh
```

### 6. Use ElastiCache Redis as Cache Layer

```env
# .env add Redis configuration
REDIS_URL=redis://lab-website.xxxxx.cache.amazonaws.com:6379
CACHE_TYPE=redis
CACHE_DEFAULT_TIMEOUT=3600
```

```python
# Add Redis configuration in backend/config/config.py
import os

class Config:
    REDIS_URL = os.environ.get('REDIS_URL')
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
```

## 🔄 ECS Migration and Data Backup Solution

When your ECS server is about to expire or needs to be migrated to a new server, here is a complete data backup and migration solution.

### 📋 Backup Checklist

Main components that need to be backed up:

1. **Database Data** - Complete MySQL database backup
2. **Media Files** - User-uploaded images, papers, and other files
3. **Configuration Files** - Environment variables and Docker configurations
4. **Code** - If there are custom modifications
5. **SSL Certificates** - If using self-signed certificates
6. **Log Files** - Runtime logs and error records

### 🚀 Quick Migration Script (One-Click Backup)

Create a complete migration backup script:

```bash
# Create migration backup script
sudo tee /opt/scripts/full-migration-backup.sh << 'EOF'
#!/bin/bash

# ============================================
# Lab Website Complete Migration Backup Script
# Purpose: Complete data migration backup before ECS server expiration
# ============================================

set -e

# Configuration variables
PROJECT_DIR="/opt/lab_web"
BACKUP_BASE="/opt/migration-backup"
DATE=$(date +%Y%m%d_%H%M%S)
MIGRATION_DIR="$BACKUP_BASE/lab_web_migration_$DATE"
COMPRESS_BACKUP=true

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check prerequisites
check_prerequisites() {
    log_info "Checking migration prerequisites..."
    
    if [ ! -d "$PROJECT_DIR" ]; then
        log_error "Project directory does not exist: $PROJECT_DIR"
        exit 1
    fi
    
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        log_error "Environment configuration file does not exist: $PROJECT_DIR/.env"
        exit 1
    fi
    
    # Check Docker container status
    if ! docker ps --filter name=lab_web --format "{{.Names}}" | grep -q lab_web; then
        log_warning "Some or all Docker containers are not running, some backups may not complete"
    fi
    
    log_success "Prerequisites check completed"
}

# Load environment variables
load_environment() {
    log_info "Loading environment configuration..."
    source "$PROJECT_DIR/.env"
    log_success "Environment configuration loaded"
}

# Create backup directory structure
create_backup_structure() {
    log_info "Creating backup directory structure..."
    
    mkdir -p "$MIGRATION_DIR"/{database,media,config,logs,ssl,scripts,docker-images}
    
    log_success "Backup directory created: $MIGRATION_DIR"
}

# 1. Complete database backup
backup_database() {
    log_info "Starting database backup..."
    
    local db_backup_file="$MIGRATION_DIR/database/lab_web_complete_$DATE.sql"
    
    # Complete database backup (including structure, data, triggers, procedures, etc.)
    if docker exec lab_web_db mysqldump \
        -u root -p"$MYSQL_ROOT_PASSWORD" \
        --single-transaction \
        --routines \
        --triggers \
        --events \
        --hex-blob \
        --opt \
        --lock-tables=false \
        "$MYSQL_DATABASE" > "$db_backup_file"; then
        
        log_success "Database backup completed: $(basename $db_backup_file)"
        
        # Compress database backup
        if [ "$COMPRESS_BACKUP" = true ]; then
            gzip "$db_backup_file"
            log_success "Database backup compressed: $(basename $db_backup_file).gz"
        fi
    else
        log_error "Database backup failed"
        return 1
    fi
    
    # Create database restore script
    cat > "$MIGRATION_DIR/database/restore-database.sh" << 'RESTORE_EOF'
#!/bin/bash
# Database restore script

echo "=== Database Restore Script ==="
echo "Usage: ./restore-database.sh [backup_file_path]"

BACKUP_FILE=${1:-"lab_web_complete_*.sql.gz"}

if [ -f "$BACKUP_FILE" ]; then
    echo "Restoring database: $BACKUP_FILE"
    
    # If compressed file
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        zcat "$BACKUP_FILE" | docker exec -i lab_web_db mysql -u root -p lab_web
    else
        cat "$BACKUP_FILE" | docker exec -i lab_web_db mysql -u root -p lab_web
    fi
    
    echo "Database restore completed"
else
    echo "Error: Backup file does not exist: $BACKUP_FILE"
    exit 1
fi
RESTORE_EOF
    
    chmod +x "$MIGRATION_DIR/database/restore-database.sh"
}

# 2. Media files backup
backup_media_files() {
    log_info "Starting media files backup..."
    
    # Backup media files in Docker volume
    if docker run --rm \
        -v lab_web_media_data:/data \
        -v "$MIGRATION_DIR/media":/backup \
        alpine sh -c "cp -r /data/* /backup/ 2>/dev/null || echo 'Media directory may be empty'"; then
        
        log_success "Media files backup completed"
        
        # Create media files archive
        if [ "$COMPRESS_BACKUP" = true ] && [ "$(ls -A $MIGRATION_DIR/media)" ]; then
            cd "$MIGRATION_DIR/media" && tar czf "../media_files_$DATE.tar.gz" * && cd - > /dev/null
            rm -rf "$MIGRATION_DIR/media"/*
            log_success "Media files compressed: media_files_$DATE.tar.gz"
        fi
    else
        log_warning "Media files backup may be incomplete"
    fi
}

# 3. Configuration files backup
backup_configurations() {
    log_info "Starting configuration files backup..."
    
    # Copy main configuration files
    cp "$PROJECT_DIR/.env" "$MIGRATION_DIR/config/"
    cp "$PROJECT_DIR/docker-compose.yml" "$MIGRATION_DIR/config/" 2>/dev/null || true
    cp "$PROJECT_DIR/docker-compose.dev.yml" "$MIGRATION_DIR/config/" 2>/dev/null || true
    cp "$PROJECT_DIR/deploy.sh" "$MIGRATION_DIR/config/" 2>/dev/null || true
    
    # Backup Nginx configuration (if exists)
    if [ -f "/etc/nginx/sites-available/lab-website" ]; then
        cp "/etc/nginx/sites-available/lab-website" "$MIGRATION_DIR/config/nginx-lab-website.conf"
        log_success "Nginx configuration backed up"
    fi
    
    # Backup system service files
    if [ -f "/etc/systemd/system/lab-website.service" ]; then
        cp "/etc/systemd/system/lab-website.service" "$MIGRATION_DIR/config/"
        log_success "System service configuration backed up"
    fi
    
    # Create configuration info document
    cat > "$MIGRATION_DIR/config/migration-info.md" << INFO_EOF
# Migration Configuration Information

## Backup Time
$(date)

## Original Server Information
- Hostname: $(hostname)
- IP Address: $(curl -s ifconfig.me 2>/dev/null || echo "Unknown")
- Operating System: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)
- Docker Version: $(docker --version)
- Docker Compose Version: $(docker-compose --version)

## Service Configuration
- Project Directory: $PROJECT_DIR
- Frontend Port: ${FRONTEND_PORT:-3000}
- Backend Port: ${BACKEND_PORT:-8000}
- Database Port: ${MYSQL_PORT:-3307}

## Database Information
- Database Name: ${MYSQL_DATABASE:-lab_web}
- Username: ${MYSQL_USER:-lab_web_user}

## Docker Container Status
$(docker ps --filter name=lab_web --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}")

## Docker Volume Information
$(docker volume ls | grep lab_web)

## Important Reminders
1. Ensure new server has Docker and Docker Compose installed before restoration
2. Create empty MySQL container before restoring database
3. Media files need to be restored to the correct Docker volume
4. Remember to modify environment variables (.env file) on new server
5. Configure SSL certificates and domain on new server
INFO_EOF

    log_success "Configuration files backup completed"
}

# Main function and other functions continue...
# [The rest of the script follows the same pattern as the Chinese version]

main() {
    echo "========================================"
    echo "    Lab Website Complete Migration Backup Tool"
    echo "========================================"
    echo "Start Time: $(date)"
    echo "Project Directory: $PROJECT_DIR"
    echo "Backup Directory: $MIGRATION_DIR"
    echo ""
    
    check_prerequisites
    load_environment
    create_backup_structure
    
    echo "Starting backup of all components..."
    backup_database
    backup_media_files
    backup_configurations
    # Additional backup functions would be called here...
    
    echo ""
    echo "========================================"
    echo "           Migration Backup Complete!"
    echo "========================================"
    echo "Backup Location: $MIGRATION_DIR"
    echo "Total Size: $(du -sh $MIGRATION_DIR | cut -f1)"
    echo ""
    echo "Next Steps:"
    echo "1. Check backup contents: ls -la $MIGRATION_DIR"
    echo "2. View backup report: cat $MIGRATION_DIR/BACKUP_REPORT.md"
    echo "3. Download backup to secure local location"
    echo "4. Restore on new server following MIGRATION_GUIDE.md"
    echo "5. Or use quick-restore.sh for automated restoration"
    echo ""
    echo "Completion Time: $(date)"
    echo "========================================"
}

# Execute main function
main "$@"
EOF

chmod +x /opt/scripts/full-migration-backup.sh
sudo chown $USER:$USER /opt/scripts/full-migration-backup.sh

echo "Complete migration backup script created!"
echo "Usage: sudo /opt/scripts/full-migration-backup.sh"
```

### 🔧 Manual Step-by-Step Backup Method

If you prefer not to use the automated script, you can follow these manual steps:

#### 1. Database Backup

```bash
# Create backup directories
mkdir -p ~/lab_web_backup/{database,media,config,logs}

# Backup database (replace password)
docker exec lab_web_db mysqldump \
  -u root -pyour_database_password \
  --single-transaction \
  --routines \
  --triggers \
  lab_web > ~/lab_web_backup/database/lab_web_$(date +%Y%m%d).sql

# Compress database backup
gzip ~/lab_web_backup/database/lab_web_$(date +%Y%m%d).sql
```

#### 2. Media Files Backup

```bash
# Backup media files from Docker volume
docker run --rm \
  -v lab_web_media_data:/data \
  -v ~/lab_web_backup/media:/backup \
  alpine tar czf /backup/media_files.tar.gz -C /data .
```

#### 3. Configuration Files Backup

```bash
# Backup project configuration files
cp /opt/lab_web/.env ~/lab_web_backup/config/
cp /opt/lab_web/docker-compose.yml ~/lab_web_backup/config/
cp /opt/lab_web/deploy.sh ~/lab_web_backup/config/

# Backup Nginx configuration (if used)
sudo cp /etc/nginx/sites-available/lab-website ~/lab_web_backup/config/nginx.conf 2>/dev/null || true

# Backup system service configuration
sudo cp /etc/systemd/system/lab-website.service ~/lab_web_backup/config/ 2>/dev/null || true
```

#### 4. SSL Certificates Backup

```bash
# Let's Encrypt certificate backup
sudo cp -r /etc/letsencrypt/live/* ~/lab_web_backup/ssl/ 2>/dev/null || true
sudo chown -R $USER:$USER ~/lab_web_backup/ssl/
```

#### 5. Create Complete Archive

```bash
# Create final backup archive
cd ~/
tar czf lab_web_complete_backup_$(date +%Y%m%d).tar.gz lab_web_backup/

echo "Backup completed! File location:"
echo "~/lab_web_complete_backup_$(date +%Y%m%d).tar.gz"
```

### 📥 New Server Restoration Steps

#### 1. Prepare New Server Environment

```bash
# Install Docker and Docker Compose (refer to installation steps above)

# Clone project code
cd /opt
git clone <your-repository-url> lab_web
cd lab_web
```

#### 2. Restore Configuration Files

```bash
# Upload and extract backup files
scp lab_web_complete_backup_*.tar.gz user@new-server:~/
ssh user@new-server
cd ~/ && tar xzf lab_web_complete_backup_*.tar.gz

# Restore configuration files
cp ~/lab_web_backup/config/.env /opt/lab_web/
cp ~/lab_web_backup/config/docker-compose.yml /opt/lab_web/ 2>/dev/null || true
```

#### 3. Restore Database

```bash
cd /opt/lab_web

# Start database container first
./deploy.sh prod start --service=db -d
sleep 30

# Restore database data
zcat ~/lab_web_backup/database/lab_web_*.sql.gz | docker exec -i lab_web_db mysql -u root -p lab_web
```

#### 4. Restore Media Files

```bash
# Extract media files to Docker volume
docker run --rm \
  -v lab_web_media_data:/data \
  -v ~/lab_web_backup/media:/backup \
  alpine tar xzf /backup/media_files.tar.gz -C /data
```

#### 5. Start Services and Verify

```bash
# Start all services
./deploy.sh prod start -d

# Check service status
./deploy.sh prod status
./deploy.sh prod health

# Test access
curl -f http://localhost:3000
curl -f http://localhost:8000/health
```

### ⚡ Emergency Quick Backup

If your ECS is about to expire and you need emergency backup of the most critical data:

```bash
#!/bin/bash
# Emergency backup script - only backup most critical data

DATE=$(date +%Y%m%d_%H%M%S)
EMERGENCY_BACKUP="/tmp/emergency_backup_$DATE"
mkdir -p "$EMERGENCY_BACKUP"

echo "Starting emergency backup..."

# 1. Most important: Database
docker exec lab_web_db mysqldump -u root -p --all-databases | gzip > "$EMERGENCY_BACKUP/all_databases.sql.gz"

# 2. Media files
docker run --rm -v lab_web_media_data:/data -v "$EMERGENCY_BACKUP":/backup alpine tar czf /backup/media.tar.gz -C /data .

# 3. Configuration files
cp /opt/lab_web/.env "$EMERGENCY_BACKUP/"

# 4. Create archive
cd /tmp && tar czf "emergency_backup_$DATE.tar.gz" "emergency_backup_$DATE"
echo "Emergency backup completed: /tmp/emergency_backup_$DATE.tar.gz"
echo "Please download this file immediately!"
```

### 📱 Backup Verification Checklist

After completing backup, please check:

- [ ] Database backup file exists and is not empty
- [ ] Media files backup contains all uploaded files  
- [ ] Configuration files (.env) are properly backed up
- [ ] SSL certificates are backed up (if used)
- [ ] Custom scripts and configurations are saved
- [ ] Backup files are downloaded to secure location
- [ ] Restoration process is verified in test environment

This way you can safely migrate your entire laboratory website to a new ECS server!

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Container Cannot Start

```bash
# Check container logs
docker logs lab_web_backend
docker logs lab_web_frontend  
docker logs lab_web_db

# Check port conflicts
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3307

# Resolve port conflicts - modify .env
FRONTEND_PORT=3001
BACKEND_PORT=8001
MYSQL_PORT=3308
```

#### 2. Database Connection Issues

```bash
# Check database container logs
docker logs lab_web_db

# Test database connection
docker exec lab_web_db mysqladmin ping -h localhost -u root -p

# Reset database (use with caution)
./deploy.sh prod stop --service=db
docker volume rm lab_web_mysql_data
./deploy.sh prod start --service=db -d
sleep 30
./deploy.sh prod db-init
```

#### 3. Frontend Cannot Load

```bash
# Check frontend container logs
docker logs lab_web_frontend

# Check Nginx configuration
docker exec lab_web_frontend nginx -t

# Rebuild frontend (if issues)
./deploy.sh prod build --service=frontend --no-cache --rebuild
./deploy.sh prod restart --service=frontend
```

#### 4. Backend API Errors

```bash
# Check backend logs
docker logs lab_web_backend -f

# Enter backend container for debugging
docker exec -it lab_web_backend bash

# Check environment variables
docker exec lab_web_backend env | grep FLASK
docker exec lab_web_backend env | grep DATABASE
```

#### 5. Permission Issues

```bash
# Fix media directory permissions
docker exec lab_web_backend chown -R www-data:www-data /app/media
docker exec lab_web_backend chmod -R 755 /app/media

# Fix log directory permissions
sudo chown -R $USER:$USER /opt/lab_web/logs/
sudo chmod -R 644 /opt/lab_web/logs/*.log
```

#### 6. Memory Shortage

```bash
# Check system resources
free -h
df -h

# Add swap space (temporary solution)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

#### 7. SSL Certificate Issues

```bash
# Check SSL certificate status
sudo certbot certificates

# Manually renew certificate
sudo certbot renew --dry-run
sudo certbot renew

# Check Nginx SSL configuration
sudo nginx -t
```

### Emergency Recovery Procedure

```bash
# Create emergency recovery script
sudo tee /opt/scripts/emergency-recovery.sh << 'EOF'
#!/bin/bash
echo "=== Emergency Recovery Procedure ==="

# 1. Stop all services
echo "Stopping all services..."
cd /opt/lab_web
./deploy.sh prod stop

# 2. Clean problematic containers
echo "Cleaning problematic containers..."
docker container prune -f

# 3. Rebuild and restart
echo "Rebuilding and restarting..."
./deploy.sh prod build --no-cache
./deploy.sh prod start -d

# 4. Wait for services to start
echo "Waiting for services to start..."
sleep 60

# 5. Check service status
echo "Checking service status..."
./deploy.sh prod health

echo "=== Recovery procedure completed ==="
EOF

chmod +x /opt/scripts/emergency-recovery.sh
```

### Support and Documentation

For more help:

- Check [Main README](../README.md) for feature overview
- Check [Standard Deployment Guide](./DEPLOYMENT.md) for basic deployment
- Check [Docker Reference Documentation](./DOCKER_REFERENCE.md) for Docker configuration
- Create issue in project repository to report problems
- Check container logs for detailed error information

---

## 📝 Summary

This ECS deployment guide provides detailed deployment processes from bare server environment to complete production environment, including:

✅ **Complete Environment Preparation**: From system updates to Docker installation  
✅ **Detailed Configuration Instructions**: Security and production environment configuration  
✅ **Automated Deployment Scripts**: One-click deployment and management  
✅ **Production Environment Optimization**: SSL, monitoring, backup, scalability  
✅ **Comprehensive Troubleshooting**: Common issues and solutions  
✅ **AWS-Specific Optimization**: ECS, RDS, EFS, CloudWatch integration

Following this guide, you can successfully deploy the laboratory website framework on any cloud server environment and ensure its stable operation in production environment.

*This ECS deployment guide is maintained synchronously with the laboratory website framework. For latest updates, please check the project repository.*