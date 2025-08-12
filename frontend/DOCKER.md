# Frontend Docker Deployment

This directory contains Docker configuration files for deploying the frontend application.

## Files Overview

- `Dockerfile` - Production-ready multi-stage build
- `Dockerfile.dev` - Development build with hot reloading
- `docker-compose.yml` - Production deployment configuration
- `docker-compose.dev.yml` - Development environment
- `deploy.sh` - Deployment automation script
- `docker/nginx.conf` - Nginx configuration for production
- `.dockerignore` - Files excluded from Docker build

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

The frontend container connects to the `lab_web_default` network to communicate with the backend. The Nginx configuration proxies API requests to the backend service.

## Environment Variables

- `NODE_ENV` - Set to 'production' or 'development'
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

1. **Container won't start**: Check Docker daemon and network
2. **Port conflicts**: Change port mapping in docker-compose.yml
3. **Build failures**: Check .dockerignore and build context
4. **API proxy issues**: Verify backend is running and network connectivity

## Production Considerations

1. Use a reverse proxy (like Traefik or nginx) in front of the container
2. Configure SSL/TLS certificates
3. Set up log rotation
4. Configure monitoring and alerts
5. Use Docker Swarm or Kubernetes for orchestration