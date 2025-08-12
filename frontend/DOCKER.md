# Frontend Docker Deployment

This directory contains Docker configuration files for deploying the frontend application.

## Files Overview

- `Dockerfile` - Production-ready multi-stage build with TypeScript compatibility fixes
- `Dockerfile.dev` - Development build with hot reloading
- `Dockerfile.simple` - Production build using pre-built dist directory
- `Dockerfile.test` - Test build with simplified configuration
- `docker-compose.yml` - Production deployment configuration
- `docker-compose.dev.yml` - Development environment
- `deploy.sh` - Deployment automation script (270+ lines)
- `docker/nginx.conf` - Nginx configuration with backend proxy setup
- `.dockerignore` - Files excluded from Docker build (updated for environment files)
- `.env.development` - Development environment configuration
- `.env.production` - Production environment configuration
- `.env.docker` - Docker build environment configuration
- `.env.example` - Template for environment variables

## Quick Start

### Production Deployment

```bash
# Build and start the frontend
./deploy.sh start

# Check status
./deploy.sh status

# View logs
./deploy.sh logs -f

# Stop the frontend
./deploy.sh stop
```

### Development Mode

```bash
# Start development server with hot reloading
docker-compose -f docker-compose.dev.yml up --build

# The app will be available at http://localhost:8080
```

## Deploy Script Usage

```bash
./deploy.sh [action] [options]

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
  --detach, -d    Run in background
  --follow, -f    Follow logs
  --help, -h      Show help message
```

## Network Configuration

The frontend container connects to the `backend_lab_web_network` network to communicate with backend services. 

### Backend Service Resolution
- **Container Name**: `lab_web_app` (not `backend`)
- **Network**: `backend_lab_web_network`
- **API Proxy**: Nginx routes `/api` → `http://lab_web_app:8000`
- **Media Proxy**: Nginx routes `/media` → `http://lab_web_app:8000`

### Network Setup
```bash
# The backend automatically creates the network
# Frontend joins this network for service discovery
docker network inspect backend_lab_web_network
```

## Environment Variables

### Frontend Environment Configuration
The frontend uses environment-specific configurations:

#### Development (`.env.development`)
```env
NODE_ENV=development
VUE_APP_API_BASE_URL=http://127.0.0.1:8000/api
```

#### Production/Docker (`.env.production`, `.env.docker`)
```env
NODE_ENV=production
VUE_APP_API_BASE_URL=/api  # Relative path through nginx proxy
```

#### Custom Local (`.env.local` - not committed)
```env
NODE_ENV=development
VUE_APP_API_BASE_URL=https://your-domain.com/api
```

### Build-time Variables
- `NODE_ENV` - Set to 'production' or 'development'
- `NODE_OPTIONS` - Set to `--max-old-space-size=4096` for large builds
- `CI` - Set to `false` to bypass TypeScript errors

### Development Variables
- `CHOKIDAR_USEPOLLING` - Enable file watching for development

## Health Checks

The production container includes health checks that verify:
- Nginx is responding
- The `/health` endpoint returns 200 OK

## Customization

### Nginx Configuration

Edit `docker/nginx.conf` to customize:
- Server settings
- Proxy configurations
- Security headers
- Cache settings

### Build Arguments

You can pass build arguments to customize the build:

```bash
docker build --build-arg NODE_ENV=production -t lab-website-frontend .
```

## Troubleshooting

### Common Issues

#### 1. TypeScript Build Errors
```bash
# Issue: @types/lodash compatibility with Node.js 20
# Solution: vue.config.js now disables TypeScript checking
# The build uses NODE_OPTIONS=--max-old-space-size=4096
docker build --no-cache -t frontend-fixed .
```

#### 2. Container Won't Start
```bash
# Check nginx configuration
docker logs [container-name]

# Common issue: Permission denied for nginx.pid
# Solution: Updated Dockerfile runs as root
docker run --rm frontend-image nginx -t  # Test config
```

#### 3. API Proxy Issues
```bash
# Issue: 'backend' host not found
# Solution: Use correct container name 'lab_web_app'
docker network inspect backend_lab_web_network
curl http://localhost:3000/api/health  # Test proxy
```

#### 4. Environment Variables Not Applied
```bash
# Check if variables are compiled into build
docker run --rm frontend-image grep -r "VUE_APP_API_BASE_URL" /usr/share/nginx/html/
# Should show /api for production builds
```

#### 5. Port Conflicts
```bash
# Change port mapping in docker-compose.yml
ports:
  - "3001:80"  # Use different port
```

#### 6. Build Cache Issues
```bash
# Clean build with no cache
./deploy.sh build --no-cache --rebuild

# Or manual cleanup
docker system prune -f
docker build --no-cache .
```

### Architecture Changes

Recent improvements address previous issues:
- ✅ **Removed duplicate state management** (Vuex → Pinia only)
- ✅ **Fixed Docker networking** (correct backend container name)
- ✅ **TypeScript compatibility** (disabled strict checking)
- ✅ **Environment configuration** (proper multi-environment setup)
- ✅ **Build optimization** (increased memory limit, better error handling)

## Production Considerations

1. Use a reverse proxy (like Traefik or nginx) in front of the container
2. Configure SSL/TLS certificates
3. Set up log rotation
4. Configure monitoring and alerts
5. Use Docker Swarm or Kubernetes for orchestration

---

**[中文文档](./DOCKER_zh-CN.md) | English**