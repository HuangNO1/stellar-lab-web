<!-- Language Switcher -->

<div align="right">

[简体中文](DOCKER_DEPLOY.md)

</div>

# 🐳 Docker Deployment Guide

This guide will help you deploy the Laboratory Web Framework backend service in local Docker containers.

## 🚀 Quick Start

### Prerequisites
- Docker Desktop or Docker Engine (20.10+)
- Docker Compose (2.0+)
- At least 2GB available disk space

### One-Click Deployment
```bash
# 1. Clone project to local
cd /home/rem/Documents/Study/Code/lab_web/backend

# 2. Build and start all services (including phpMyAdmin)
docker-compose up --build -d

# Or start minimal configuration (backend + database only, without phpMyAdmin)
docker-compose -f docker-compose-minimal.yml up --build -d

# 3. Check service status
docker-compose ps
```

## 📋 Service Overview

### Port Mapping
- **Flask Backend**: [http://localhost:8000](http://localhost:8000)
- **MySQL Database**: `localhost:3307` (to avoid conflicts with local MySQL)
- **phpMyAdmin** (optional): [http://localhost:8081](http://localhost:8081)

### Default Account Information
- **Admin Account**: `admin` / `admin123`
- **MySQL Root**: `root` / `lab_web_root_123`
- **MySQL User**: `lab_web_user` / `lab_web_pass_123`

## 🛠️ Detailed Deployment Steps

### Step 1: Prepare Files
Ensure the following files exist in the project root directory:
```
backend/
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── .env.docker
└── .dockerignore
```

### Step 2: Build Images
```bash
# Build backend application image only
docker-compose build app

# Or build all services
docker-compose build
```

### Step 3: Start Services
```bash
# Start in foreground (view real-time logs)
docker-compose up

# Start in background
docker-compose up -d

# Start services in specific order
docker-compose up -d db    # Start database first
docker-compose up -d app   # Then start application
```

### Step 4: Verify Deployment
```bash
# Check service status
docker-compose ps

# View application logs
docker-compose logs app

# View database logs
docker-compose logs db

# Test API health status
curl http://localhost:8000/health
```

## 🔧 Common Operation Commands

### Service Management
```bash
# Stop all services
docker-compose down

# Stop and remove data volumes
docker-compose down -v

# Restart specific service
docker-compose restart app

# View real-time logs
docker-compose logs -f app
```

### Data Management
```bash
# Enter database container
docker-compose exec db mysql -u root -p

# Connect to database externally (if needed)
mysql -h localhost -P 3307 -u root -p

# Backup database
docker-compose exec db mysqldump -u root -plab_web_root_123 lab_web > backup.sql

# Restore database
docker-compose exec -T db mysql -u root -plab_web_root_123 lab_web < backup.sql
```

### Application Container Operations
```bash
# Enter application container
docker-compose exec app bash

# Manually initialize database
docker-compose exec app python scripts/init_db.py

# View media files
docker-compose exec app ls -la /app/media/
```

## 📊 API Testing

### Basic Testing
```bash
# Health check
curl http://localhost:8000/health

# API information
curl http://localhost:8000/api-info

# Get laboratory information
curl http://localhost:8000/api/lab
```

### Admin Login Testing
```bash
# Login to get Token
curl -X POST http://localhost:8000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"admin_name":"admin","admin_pass":"admin123"}'

# Use Token to access admin interfaces (replace with actual token)
curl -X GET http://localhost:8000/api/admin/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🗄️ Data Initialization

### Automatic Initialization Process
The system uses the project's existing `scripts/init_db.py` script for database initialization:

**Startup Sequence**:
```
MySQL container starts → Wait for database service → Run init_db.py → Start Flask application
```

**Automatically created sample data**:
- ✅ **Admin Account**: `admin/admin123`
- ✅ **Laboratory Info**: Intelligent Computing Laboratory
- ✅ **Research Groups**: Computer Vision, Natural Language Processing
- ✅ **Members**: Prof. Zhang, Assoc. Prof. Li, Dr. Wang
- ✅ **Papers**: 2 papers (CVPR 2024, AAAI 2024)
- ✅ **News**: 3 news items (paper accepted, award, academic seminar)
- ✅ **Projects**: 2 projects (surveillance system, dialogue robot)

## 📁 Data Persistence

### Volume Description
- `mysql_data`: MySQL data persistence
- `media_data`: Uploaded files persistence
- `./logs`: Application log files

### Data Directory Structure
```
media_data/
├── lab_logo/          # Laboratory Logo
├── member_avatar/     # Member Avatars
├── paper/            # Paper Files
└── other/            # Other Files
```

## 🔒 Security Configuration

### Production Environment Configuration
In production environment, please modify the following sensitive information:
1. Edit `.env.docker` file:
```bash
# Change secrets
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret

# Change database password
MYSQL_PASSWORD=your-secure-password
```

2. Update database password in `docker-compose.yml`

### Network Security
- Remove unnecessary port mappings
- Use custom networks
- Configure firewall rules

## 🐛 Troubleshooting

### Common Issues

**1. Database Connection Failed**
```bash
# Check database service status
docker-compose ps db
docker-compose logs db

# Restart database service
docker-compose restart db
```

**2. Application Startup Failed**
```bash
# View application startup logs
docker-compose logs app

# Check dependent services
docker-compose ps
```

**3. File Upload Failed**
```bash
# Check media directory permissions
docker-compose exec app ls -la /app/media/

# Reset permissions
docker-compose exec app chmod -R 755 /app/media/
```

**4. Port Conflict**
```bash
# If port 3307 is also occupied, modify to other port
# Edit docker-compose.yml
ports:
  - "3308:3306"  # Change to other available port

# Check port usage
netstat -tlnp | grep :3306
lsof -i :3306
```

**5. Local MySQL Service Conflict**
```bash
# Stop local MySQL service (if not needed)
sudo systemctl stop mysql        # Linux
brew services stop mysql         # macOS
net stop mysql                  # Windows

# Or use different port (already modified to 3307 in configuration)
```

### Environment Cleanup
```bash
# Stop and remove all containers
docker-compose down

# Remove all related images
docker rmi $(docker images "*lab_web*" -q)

# Clean unused data volumes
docker volume prune

# Complete reset (use with caution)
docker-compose down -v --rmi all
```

## 🔧 Development Mode

For development mode deployment:
```bash
# Modify docker-compose.yml
environment:
  FLASK_ENV: development

# Add code volume mount
volumes:
  - .:/app
  - media_data:/app/media
```

## 📝 Log Management

```bash
# View all service logs
docker-compose logs

# Real-time tracking of application logs
docker-compose logs -f app

# Export logs to file
docker-compose logs app > app.log
```

---

## 🎉 Deployment Complete

After successful deployment, you can:
- Visit [http://localhost:8000](http://localhost:8000) to view API documentation
- Use [http://localhost:8080](http://localhost:8080) to manage the database
- Manage laboratory data through API interfaces

If you encounter issues, please refer to the troubleshooting section or check container logs for diagnosis.