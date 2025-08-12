# Docker Flexible Deployment Examples

<!-- Language Switcher -->

<div align="right">

[简体中文](README_zh-CN.md)

</div>

<!-- Content -->

This directory contains Docker Compose configuration examples for various deployment scenarios, demonstrating how to use published Docker images with flexible configuration.

## 📁 File Descriptions

### 1. `docker-compose.standalone.yml`
**Standalone Deployment Mode** - Complete deployment using published images
- Includes all services (frontend, backend, database)
- Best for quick setup and testing
- Uses published Docker images from GHCR

### 2. `docker-compose.external-db.yml`
**External Database Mode** - Connect to existing MySQL database
- Uses your existing database server
- Reduces resource usage
- Suitable for organizations with existing database infrastructure

### 3. `docker-compose.separate.yml`
**Frontend/Backend Separation Mode** - Independent deployment of frontend and backend
- Frontend and backend can be deployed independently
- Supports cross-domain deployment
- Ideal for microservices architecture

### 4. `.env.example`
**Environment Variables Template** - Comprehensive configuration template
- Contains all supported environment variables
- Includes security recommendations
- Production-ready configuration examples

## 🚀 Usage Instructions

### Quick Start

```bash
# Download configuration examples
curl -L https://github.com/your-repo/lab_web/archive/main.tar.gz | tar xz
cd lab_web-main/examples

# Copy and customize environment file
cp .env.example .env
# Edit .env with your configuration

# Deploy with published images
docker-compose -f docker-compose.standalone.yml up -d
```

### Using Specific Configuration

```bash
# Standalone deployment (recommended for beginners)
docker-compose -f docker-compose.standalone.yml up -d

# External database deployment
docker-compose -f docker-compose.external-db.yml up -d

# Separate frontend/backend deployment
docker-compose -f docker-compose.separate.yml up -d
```

### Copy to Root Directory

```bash
# Copy desired configuration to root directory
cp examples/docker-compose.standalone.yml docker-compose.yml
cp examples/.env.example .env

# Edit configuration
nano .env

# Deploy
docker-compose up -d
```

## 🔧 Environment Variables

All examples support configuration through environment variables. Key variables include:

### Frontend Configuration
- `BACKEND_URL` - Backend service address
- `API_BASE_URL` - API endpoint path
- `APP_TITLE` - Application title
- `CORS_ORIGIN` - CORS settings

### Backend Configuration
- `DATABASE_URL` - Complete database connection string
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT secret key
- `CORS_ORIGINS` - CORS whitelist

### Database Configuration
- `MYSQL_ROOT_PASSWORD` - MySQL root password
- `MYSQL_DATABASE` - Database name
- `MYSQL_USER` - Database user
- `MYSQL_PASSWORD` - Database user password

## 📊 Deployment Scenarios

### 1. Complete Lab Website Setup
Use `docker-compose.standalone.yml` for:
- New lab website deployment
- Testing and development
- Self-contained environment

### 2. Enterprise Integration
Use `docker-compose.external-db.yml` for:
- Integration with existing database infrastructure
- Enterprise security compliance
- Shared database resources

### 3. Scalable Architecture
Use `docker-compose.separate.yml` for:
- High-traffic websites
- Load balancing requirements
- Multi-server deployment

## 🔒 Security Recommendations

### Production Environment
1. **Change default passwords** in `.env` file
2. **Use strong secret keys** - generate with `openssl rand -hex 32`
3. **Configure CORS properly** - specify exact domains
4. **Use HTTPS** in production
5. **Regular updates** - pull latest image versions

### Example Production Configuration
```bash
# Generate secure keys
export SECRET_KEY=$(openssl rand -hex 32)
export JWT_SECRET_KEY=$(openssl rand -hex 32)
export MYSQL_ROOT_PASSWORD=$(openssl rand -base64 32)

# Set production CORS
export CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 🔍 Troubleshooting

### Common Issues

1. **Port conflicts**
   ```bash
   # Check port usage
   netstat -tlnp | grep :3000
   
   # Modify ports in .env file
   FRONTEND_PORT=3001
   BACKEND_PORT=8001
   ```

2. **Container connectivity**
   ```bash
   # Check container logs
   docker-compose -f docker-compose.standalone.yml logs frontend
   docker-compose -f docker-compose.standalone.yml logs backend
   ```

3. **Database connection**
   ```bash
   # Verify database status
   docker-compose -f docker-compose.standalone.yml exec db mysql -u root -p -e "SHOW DATABASES;"
   ```

## 📚 Additional Resources

- **[Complete Deployment Guide](../docs/FLEXIBLE_DEPLOYMENT.md)** - Detailed deployment instructions
- **[Main README](../README.md)** - Project overview and features
- **[Backend Documentation](../backend/README.md)** - Backend-specific configuration
- **[Frontend Documentation](../frontend/README.md)** - Frontend-specific configuration

## 🆘 Support

For questions or issues:
- Check the [troubleshooting guide](../docs/FLEXIBLE_DEPLOYMENT.md#故障排除)
- Review container logs: `docker-compose logs [service-name]`
- Open an [issue](../../issues) on GitHub

---

<div align="center">

**Ready to deploy your lab website in minutes!**

*Choose the deployment mode that best fits your needs.*

</div>