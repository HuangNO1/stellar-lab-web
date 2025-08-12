# Docker Quick Reference

Quick reference guide for Docker commands and troubleshooting for the Lab Website Framework.

## 🚀 Common Commands

### Using Deploy Script (Recommended)

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

### Using Make (Even Simpler)

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

## 📊 Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Main website |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/api/docs | Swagger documentation |
| phpMyAdmin | http://localhost:8081 | Database management |

**Default Login**: admin / admin123

## 🔧 Direct Docker Commands

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View container logs
docker logs lab_web_frontend -f
docker logs lab_web_backend -f
docker logs lab_web_db -f

# Execute commands in containers
docker exec -it lab_web_backend /bin/bash
docker exec -it lab_web_frontend /bin/sh
docker exec -it lab_web_db mysql -u root -plab_web_root_123 lab_web

# Restart individual containers
docker restart lab_web_frontend
docker restart lab_web_backend
docker restart lab_web_db
```

### Docker Compose Commands

```bash
# Start services
docker-compose up -d

# Start specific service
docker-compose up -d frontend

# Stop services
docker-compose down

# View logs
docker-compose logs -f
docker-compose logs -f backend

# Build and start
docker-compose up --build -d

# Scale services
docker-compose up --scale frontend=2 -d
```

## 🛠️ Troubleshooting Commands

### Health Checks

```bash
# Check if services are responding
curl http://localhost:3000/health    # Frontend
curl http://localhost:8000/health    # Backend

# Check database connection
docker exec lab_web_db mysqladmin ping -h localhost

# Check container health status
docker inspect lab_web_frontend --format='{{.State.Health.Status}}'
```

### Resource Usage

```bash
# Container resource usage
docker stats

# Disk usage
docker system df

# Volume usage
docker volume ls
docker volume inspect lab_web_mysql_data
```

### Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Full cleanup (CAREFUL!)
docker system prune -a --volumes
```

## 📂 Volume Management

### Volume Locations

```bash
# List volumes
docker volume ls | grep lab_web

# Inspect volume location
docker volume inspect lab_web_mysql_data
docker volume inspect lab_web_media_data

# Backup volumes
docker run --rm -v lab_web_mysql_data:/data -v $(pwd):/backup alpine tar czf /backup/mysql_backup.tar.gz -C /data .
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar czf /backup/media_backup.tar.gz -C /data .

# Restore volumes
docker run --rm -v lab_web_mysql_data:/data -v $(pwd):/backup alpine tar xzf /backup/mysql_backup.tar.gz -C /data
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar xzf /backup/media_backup.tar.gz -C /data
```

## 🔍 Debugging

### Container Issues

```bash
# Check why container failed to start
docker logs lab_web_backend

# Check container configuration
docker inspect lab_web_backend

# Check network connectivity
docker network ls
docker network inspect lab_web_default

# Test connectivity between containers
docker exec lab_web_backend ping db
docker exec lab_web_frontend ping backend
```

### Database Issues

```bash
# Check MySQL logs
docker logs lab_web_db

# Connect to MySQL
docker exec -it lab_web_db mysql -u root -plab_web_root_123

# Check database status
docker exec lab_web_db mysqladmin status -u root -plab_web_root_123

# Check database size
docker exec lab_web_db mysql -u root -plab_web_root_123 -e "SELECT table_schema 'Database', SUM(data_length + index_length) / 1024 / 1024 'Size (MB)' FROM information_schema.tables WHERE table_schema='lab_web' GROUP BY table_schema;"
```

### Performance Issues

```bash
# Monitor resource usage
docker stats --no-stream

# Check container processes
docker exec lab_web_backend ps aux
docker exec lab_web_frontend ps aux

# Check disk space in containers
docker exec lab_web_backend df -h
docker exec lab_web_db df -h
```

## 🚨 Emergency Procedures

### Complete Reset

```bash
# Stop all services
./deploy.sh prod stop

# Remove all containers and volumes (DESTRUCTIVE!)
./deploy.sh prod clean

# Start fresh
./deploy.sh prod start -d
./deploy.sh prod db-init
```

### Database Emergency Reset

```bash
# Stop backend to prevent connections
./deploy.sh prod stop --service=backend

# Reset database volume
docker volume rm lab_web_mysql_data

# Start database and reinitialize
./deploy.sh prod start --service=db -d
./deploy.sh prod db-init

# Start backend
./deploy.sh prod start --service=backend -d
```

### Backup Before Emergency Actions

```bash
# Always backup before destructive operations
./deploy.sh prod db-backup

# Backup media files
docker run --rm -v lab_web_media_data:/data -v $(pwd):/backup alpine tar czf /backup/media_emergency_backup.tar.gz -C /data .
```

## 📋 Maintenance Scripts

### Update Everything

```bash
#!/bin/bash
# update-lab-website.sh

echo "Stopping services..."
./deploy.sh prod stop

echo "Backing up database..."
./deploy.sh prod db-backup

echo "Pulling latest code..."
git pull origin main

echo "Rebuilding services..."
./deploy.sh prod build --no-cache --rebuild

echo "Starting services..."
./deploy.sh prod start -d

echo "Checking health..."
sleep 30
./deploy.sh prod health

echo "Update complete!"
```

### Daily Health Check

```bash
#!/bin/bash
# health-check.sh

DATE=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/var/log/lab-website-health.log"

echo "[$DATE] Starting health check..." >> "$LOG_FILE"

# Check services
if curl -sf http://localhost:3000/health > /dev/null; then
    echo "[$DATE] Frontend: OK" >> "$LOG_FILE"
else
    echo "[$DATE] Frontend: FAILED" >> "$LOG_FILE"
fi

if curl -sf http://localhost:8000/health > /dev/null; then
    echo "[$DATE] Backend: OK" >> "$LOG_FILE"
else
    echo "[$DATE] Backend: FAILED" >> "$LOG_FILE"
fi

# Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "[$DATE] Disk usage: WARNING - ${DISK_USAGE}%" >> "$LOG_FILE"
else
    echo "[$DATE] Disk usage: OK - ${DISK_USAGE}%" >> "$LOG_FILE"
fi

echo "[$DATE] Health check complete" >> "$LOG_FILE"
```

## 🔗 Useful Docker Commands

### Image Management

```bash
# List images
docker images

# Remove unused images
docker image prune

# Build without cache
docker build --no-cache -t lab-website-frontend ./frontend

# Tag images
docker tag lab-website-frontend:latest lab-website-frontend:v1.0.0
```

### Network Debugging

```bash
# List networks
docker network ls

# Inspect network
docker network inspect lab_web_default

# Test DNS resolution
docker exec lab_web_backend nslookup db
docker exec lab_web_frontend nslookup backend
```

### Environment Variables

```bash
# Show container environment
docker exec lab_web_backend env
docker exec lab_web_frontend env

# Check specific variable
docker exec lab_web_backend printenv DATABASE_URL
```

---

💡 **Pro Tips:**
- Always backup before making changes
- Use `./deploy.sh prod health` to check all services
- Monitor logs with `./deploy.sh prod logs -f`
- Use `make` commands for common operations
- Keep your `.env` file secure and backed up