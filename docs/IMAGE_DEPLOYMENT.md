# Local Build + Image Deployment Guide

Fast deployment solution: Build Docker images locally and upload to server, avoiding time-consuming builds on the server.

## 🚀 Advantages

- **⚡ Fast**: Server deployment time reduced from 10-15 minutes to 2-3 minutes
- **📦 Offline Deployment**: Supports offline environments without server internet access
- **🔄 Version Control**: Support for multi-version image management
- **🛠️ Flexibility**: Selective frontend or backend updates
- **💾 Resource Efficient**: Reduces server CPU and network usage

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

### Step 2: Package and Upload to Server

```bash
# Package and upload to server
./package-images.sh --server 192.168.1.100

# Specify user and path
./package-images.sh --server example.com --user ubuntu --path /home/ubuntu/lab_web

# Package only, no upload
./package-images.sh --package-only

# Upload only (existing packages)
./package-images.sh --upload-only --server 192.168.1.100
```

### Step 3: Deploy on Server

```bash
# SSH into server
ssh root@192.168.1.100

# Navigate to project directory
cd /opt/lab_web

# Execute fast deployment
./server-deploy.sh

# Deploy specific version
./server-deploy.sh v1.0.0
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