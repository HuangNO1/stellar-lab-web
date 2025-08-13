# Local Build + Image Deployment Guide

Fast deployment solution: Build Docker images locally, package and upload to server, avoiding time-consuming builds on the server.

## 🚀 Advantages

- **⚡ Fast**: Server deployment time reduced from 10-15 minutes to 2-3 minutes
- **📦 Offline Deployment**: Supports offline environments without server internet access
- **🔄 Version Control**: Support for multi-version image management
- **🛠️ Flexibility**: Selective frontend or backend updates
- **💾 Resource Efficient**: Reduces server CPU and network usage
- **🌏 China Optimized**: Built-in China mirror acceleration to solve network issues

## 📋 Deployment Workflow

### Step 1: Build Images Locally

```bash
# Build all service images
./build-images.sh

# Build specific version
./build-images.sh v1.0.0

# Build backend only
./build-images.sh --backend-only

# Build frontend only
./build-images.sh --frontend-only

# No-cache build
./build-images.sh --no-cache
```

### Step 2: Package Deployment Files

```bash
# Package deployment files (recommended for manual upload)
./package-images.sh latest --package-only

# Auto-upload to server (requires SSH configuration)
./package-images.sh --server 192.168.1.100

# Specify user and path
./package-images.sh --server example.com --user ubuntu --path /home/ubuntu/lab_web
```

After packaging, you'll get a `docker-images` directory containing all deployment files:

```
docker-images/
└── deploy/                              # Complete deployment package
    ├── deploy.sh                        # Project deployment script
    ├── docker-compose.yml              # Docker Compose configuration
    ├── .env                            # Environment variables
    ├── nginx.conf                      # Nginx configuration
    ├── server-deploy.sh                # Server quick deployment script
    ├── lab-website-backend-latest.tar.gz   # Backend image file
    └── lab-website-frontend-latest.tar.gz  # Frontend image file
```

### Step 3: Upload to Server

**Method 1: Manual Upload (Recommended)**
```bash
# Upload entire deployment directory using scp
scp -r docker-images/deploy/* root@your-server:/opt/lab_web/

# Or use rsync (supports incremental upload)
rsync -avz docker-images/deploy/ root@your-server:/opt/lab_web/
```

**Method 2: Auto Upload (requires SSH key configuration)**
```bash
./package-images.sh latest --server your-server
```

### Step 4: Deploy on Server

```bash
# SSH into server
ssh root@your-server

# Navigate to project directory
cd /opt/lab_web

# Execute fast deployment
./server-deploy.sh

# Use China mirror acceleration for China servers
./server-deploy.sh --china

# Deploy specific version
./server-deploy.sh latest --china
```

## 📝 Script Documentation

### build-images.sh - Local Build Script

**Purpose**: Build Docker images in local environment

**Parameters**:
- `version_tag`: Specify image version (default: latest)
- `--no-cache`: Build without cache
- `--backend-only`: Build backend image only
- `--frontend-only`: Build frontend image only

**Examples**:
```bash
./build-images.sh                    # Build latest version
./build-images.sh v1.0.0            # Build v1.0.0 version
./build-images.sh --no-cache        # No-cache build
./build-images.sh latest --backend-only  # Backend only
```

### package-images.sh - Image Packaging Script

**Purpose**: Package built images into deployment package, with optional server upload

**Parameters**:
- `version_tag`: Specify image version (default: latest)
- `--package-only`: Package only, no upload (recommended for manual upload)
- `--server HOST`: Server address (required for auto upload)
- `--user USER`: SSH username (default: root)
- `--path PATH`: Server path (default: /opt/lab_web)
- `--output-dir DIR`: Local output directory (default: ./docker-images)
- `--upload-only`: Upload only, no repackaging

**Examples**:
```bash
./package-images.sh --package-only                         # Package only (recommended)
./package-images.sh --server 192.168.1.100                 # Package and auto-upload
./package-images.sh v1.0.0 --server example.com --user ubuntu  # Specify version and user
./package-images.sh --upload-only --server 192.168.1.100   # Upload existing package
```

### server-deploy.sh - Server Fast Deployment Script

**Purpose**: Load images and deploy services quickly on server

**Parameters**:
- `version_tag`: Specify deployment version (default: latest)
- `--china`: Use China mirror acceleration (recommended for China servers)
- `--no-health-check`: Skip health checks
- `--keep-old`: Keep old images
- `--force-recreate`: Force container recreation

**Examples**:
```bash
./server-deploy.sh                   # Deploy latest version
./server-deploy.sh --china           # Deploy with China mirror acceleration
./server-deploy.sh v1.0.0 --china    # Deploy specific version with acceleration
./server-deploy.sh --no-health-check # Skip health checks
```

## 🕐 Time Comparison

| Deployment Method | Local Time | Upload Time | Server Time | Total Time | Server Resource Usage |
|-------------------|------------|-------------|-------------|------------|----------------------|
| **Traditional** | 0 min | 0 min | 10-15 min | 10-15 min | High (building) |
| **Image Deployment** | 8-12 min | 2-5 min | 2-3 min | 12-20 min | Low (loading) |
| **Incremental Update** | 2-5 min | 1-2 min | 1-2 min | 4-9 min | Minimal |

> 💡 **Note**: Although initial total time may be slightly longer, server resource usage is significantly reduced and supports offline deployment

## 💡 Use Cases

### Case 1: Initial Deployment (Recommended Flow)
```bash
# Local
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --package-only

# Manual upload
scp -r docker-images/deploy/* root@your-server:/opt/lab_web/

# Server (recommend --china for China servers)
ssh root@your-server
cd /opt/lab_web
./server-deploy.sh v1.0.0 --china
```

### Case 2: Code Update (Backend Only)
```bash
# Local - Build only changed services
./build-images.sh v1.0.1 --backend-only
./package-images.sh v1.0.1 --package-only

# Manual upload
scp docker-images/deploy/lab-website-backend-v1.0.1.tar.gz root@your-server:/opt/lab_web/
scp docker-images/deploy/server-deploy.sh root@your-server:/opt/lab_web/

# Server
./server-deploy.sh v1.0.1 --china
```

### Case 3: Emergency Fix
```bash
# Local - Quick hotfix build
./build-images.sh hotfix-001 --no-cache --backend-only
./package-images.sh hotfix-001 --package-only

# Quick upload critical files
scp docker-images/deploy/lab-website-backend-hotfix-001.tar.gz root@your-server:/opt/lab_web/

# Server - Fast deployment
./server-deploy.sh hotfix-001 --china
```

### Case 4: Multi-Environment Deployment
```bash
# Build once, deploy to multiple environments
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --package-only

# Upload to test environment
scp -r docker-images/deploy/* ubuntu@test.example.com:/home/ubuntu/lab_web/

# Upload to production environment
scp -r docker-images/deploy/* root@prod.example.com:/opt/lab_web/
```

## 🌏 China Server Optimization

### Network Issues Resolution
```bash
# Use China mirror acceleration (recommended)
./server-deploy.sh --china

# Manual Docker mirror configuration (if needed)
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn", 
    "https://reg-mirror.qiniu.com"
  ]
}
EOF
sudo systemctl restart docker
```

### Upload Acceleration Tips
```bash
# Use compressed transmission
scp -C -r docker-images/deploy/* root@your-server:/opt/lab_web/

# Use rsync incremental sync
rsync -avz --progress docker-images/deploy/ root@your-server:/opt/lab_web/
```

## 🔧 Advanced Tips

### 1. Batch Deployment Script
```bash
#!/bin/bash
# batch-deploy.sh
VERSION="$1"
SERVERS=("server1.com" "server2.com" "server3.com")

./build-images.sh "$VERSION"
./package-images.sh "$VERSION" --package-only

for server in "${SERVERS[@]}"; do
    echo "Deploying to $server..."
    scp -r docker-images/deploy/* "root@$server:/opt/lab_web/"
    ssh "root@$server" "cd /opt/lab_web && ./server-deploy.sh $VERSION --china"
done
```

### 2. CI/CD Automation Integration
```yaml
# .github/workflows/deploy.yml example
name: Deploy to Production
on:
  push:
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Images
      run: ./build-images.sh ${{ github.ref_name }}
      
    - name: Package Images
      run: ./package-images.sh ${{ github.ref_name }} --package-only
      
    - name: Deploy to Server
      run: |
        scp -r docker-images/deploy/* ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }}:/opt/lab_web/
        ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} "cd /opt/lab_web && ./server-deploy.sh ${{ github.ref_name }} --china"
```

### 3. Image Backup & Version Management
```bash
# Save image backups locally
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --package-only

# Create version backup directory
mkdir -p backups/v1.0.0
cp -r docker-images/deploy/* backups/v1.0.0/

# Version rollback
scp -r backups/v1.0.0/* root@your-server:/opt/lab_web/
ssh root@your-server "cd /opt/lab_web && ./server-deploy.sh v1.0.0 --china"
```

## 🛠️ Troubleshooting

### 1. Image Loading Failures
```bash
# Check image file integrity
ls -lh *.tar.gz
file lab-website-backend-latest.tar.gz

# Manual loading test
gunzip -c lab-website-backend-latest.tar.gz | docker load

# Check if images loaded successfully
docker images | grep lab-website
```

### 2. Service Startup Failures
```bash
# View container logs
docker-compose -p lab_web logs backend
docker-compose -p lab_web logs frontend

# Check container status
docker-compose -p lab_web ps

# Check port usage
netstat -tlnp | grep -E ':3000|:8000|:3307'
```

### 3. Network Connection Issues
```bash
# Test Docker Hub connection
docker pull hello-world

# Use China mirror sources
./server-deploy.sh --china

# Check DNS resolution
nslookup registry-1.docker.io
```

### 4. SSH Connection Issues
```bash
# Test SSH connection
ssh -o ConnectTimeout=10 user@server "echo 'Connection OK'"

# Configure SSH keys
ssh-keygen -t rsa -b 4096
ssh-copy-id user@server

# Check SSH configuration
ssh -v user@server
```

### 5. File Permission Issues
```bash
# Check file permissions
ls -la server-deploy.sh

# Fix execution permissions
chmod +x server-deploy.sh deploy.sh

# Check directory permissions
ls -ld /opt/lab_web
```

## 📚 Related Documentation

- [Main Deployment Guide](./DEPLOYMENT.md)
- [ECS Cloud Server Deployment](./ECS_DEPLOYMENT.md)
- [Docker Reference Documentation](./DOCKER_REFERENCE.md)
- [Flexible Deployment Guide](./FLEXIBLE_DEPLOYMENT.md)

## 📝 Script Documentation

### build-images.sh - Local Build Script

**Purpose**: Build Docker images in local environment

**Parameters**:
- `version_tag`: Specify image version (default: latest)
- `--no-cache`: Build without cache
- `--backend-only`: Build backend image only
- `--frontend-only`: Build frontend image only

**Examples**:
```bash
./build-images.sh                    # Build latest version
./build-images.sh v1.0.0            # Build v1.0.0 version
./build-images.sh --no-cache        # No-cache build
./build-images.sh latest --backend-only  # Backend only
```

### package-images.sh - Image Packaging & Upload Script

**Purpose**: Package built images and upload to server

**Parameters**:
- `version_tag`: Specify image version (default: latest)
- `--server HOST`: Server address (required)
- `--user USER`: SSH username (default: root)
- `--path PATH`: Server path (default: /opt/lab_web)
- `--output-dir DIR`: Local output directory (default: ./docker-images)
- `--package-only`: Package only, no upload
- `--upload-only`: Upload only, no repackaging

**Examples**:
```bash
./package-images.sh --server 192.168.1.100                    # Basic usage
./package-images.sh v1.0.0 --server example.com --user ubuntu  # Specify version and user
./package-images.sh --package-only                             # Package only
./package-images.sh --upload-only --server 192.168.1.100      # Upload only
```

### server-deploy.sh - Server Fast Deployment Script

**Purpose**: Load images and deploy services quickly on server

**Parameters**:
- `version_tag`: Specify deployment version (default: latest)
- `--no-health-check`: Skip health checks
- `--keep-old`: Keep old images
- `--force-recreate`: Force container recreation

**Examples**:
```bash
./server-deploy.sh                   # Deploy latest version
./server-deploy.sh v1.0.0           # Deploy v1.0.0 version
./server-deploy.sh --no-health-check # Skip health checks
```

## 🕐 Time Comparison

| Deployment Method | Local Time | Server Time | Total Time | Server Resource Usage |
|-------------------|------------|-------------|------------|----------------------|
| **Traditional** | 0 min | 10-15 min | 10-15 min | High (building) |
| **Image Deployment** | 8-12 min | 2-3 min | 10-15 min | Low (loading) |
| **Incremental Update** | 2-5 min | 1-2 min | 3-7 min | Minimal |

## 💡 Use Cases

### Case 1: Initial Deployment
```bash
# Local
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --server YOUR_SERVER

# Server
./server-deploy.sh v1.0.0
```

### Case 2: Code Update (Backend Only)
```bash
# Local - Build only changed services
./build-images.sh v1.0.1 --backend-only
./package-images.sh v1.0.1 --server YOUR_SERVER

# Server
./server-deploy.sh v1.0.1
```

### Case 3: Emergency Fix
```bash
# Local - Quick hotfix build
./build-images.sh hotfix-001 --no-cache --backend-only
./package-images.sh hotfix-001 --server YOUR_SERVER

# Server - Fast deployment
./server-deploy.sh hotfix-001
```

### Case 4: Multi-Environment Deployment
```bash
# Build once, deploy to multiple environments
./build-images.sh v1.0.0

# Deploy to test environment
./package-images.sh v1.0.0 --server test.example.com

# Deploy to production environment
./package-images.sh v1.0.0 --server prod.example.com
```

## 🔧 Advanced Tips

### 1. Batch Deployment Script
```bash
#!/bin/bash
# batch-deploy.sh
VERSION="$1"
SERVERS=("server1.com" "server2.com" "server3.com")

./build-images.sh "$VERSION"

for server in "${SERVERS[@]}"; do
    ./package-images.sh "$VERSION" --server "$server"
done
```

### 2. CI/CD Automation Integration
```bash
# .github/workflows/deploy.yml example
- name: Build Images
  run: ./build-images.sh ${{ github.sha }}
  
- name: Deploy to Production
  run: ./package-images.sh ${{ github.sha }} --server prod.example.com
```

### 3. Image Backup
```bash
# Save image backups locally
./build-images.sh v1.0.0
./package-images.sh v1.0.0 --package-only
# Package files saved in ./docker-images/ directory
```

## 🛠️ Troubleshooting

### 1. SSH Connection Issues
```bash
# Test SSH connection
ssh -o ConnectTimeout=10 user@server "echo 'Connection OK'"

# Configure SSH keys
ssh-keygen -t rsa -b 4096
ssh-copy-id user@server
```

### 2. Image Loading Failures
```bash
# Check image files
ls -lh *.tar.gz
file backend-image-latest.tar.gz

# Manual loading test
gunzip -c backend-image-latest.tar.gz | docker load
```

### 3. Service Startup Failures
```bash
# View container logs
docker-compose -p lab_web logs backend
docker-compose -p lab_web logs frontend

# Check container status
docker-compose -p lab_web ps
```

## 📚 Related Documentation

- [Main Deployment Guide](./DEPLOYMENT.md)
- [ECS Cloud Server Deployment](./ECS_DEPLOYMENT.md)
- [Docker Reference Documentation](./DOCKER_REFERENCE.md)