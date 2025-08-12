# Frontend Environment Configuration Guide

This guide explains the environment configuration system for the Lab Website Frontend.

## 📁 Environment Files

### Available Environment Files

| File | Purpose | Committed to Git | Used in Docker |
|------|---------|------------------|----------------|
| `.env.development` | Local development | ✅ Yes | ❌ No |
| `.env.production` | Production builds | ✅ Yes | ✅ Yes |
| `.env.docker` | Docker-specific | ✅ Yes | ✅ Yes |
| `.env.example` | Template/documentation | ✅ Yes | ❌ No |
| `.env.local` | Personal overrides | ❌ No | ❌ No |

### Loading Priority

Vue.js loads environment files in this order (highest priority first):
1. `.env.local` - Personal development overrides (highest priority)
2. `.env.production` / `.env.development` - Mode-specific
3. `.env` - General fallback (lowest priority)

## 🔧 Configuration Details

### Development Environment (`.env.development`)

```env
NODE_ENV=development
VUE_APP_API_BASE_URL=http://127.0.0.1:8000/api
```

**Use Case**: Local development with direct backend connection
- Frontend dev server connects directly to Flask backend
- Suitable for debugging and local testing
- Backend must be running on localhost:8000

### Production Environment (`.env.production`)

```env
NODE_ENV=production
VUE_APP_API_BASE_URL=/api
```

**Use Case**: Production deployments with reverse proxy
- Uses relative paths for API calls
- Works with nginx reverse proxy or similar
- Scalable for different domains

### Docker Environment (`.env.docker`)

```env
NODE_ENV=production
VUE_APP_API_BASE_URL=/api
```

**Use Case**: Docker container builds
- Specifically for containerized deployments
- Uses nginx proxy within Docker network
- Allows docker-specific optimizations

### Custom Local Environment (`.env.local`)

Create this file for personal overrides (not tracked by git):

```env
# Custom API endpoint
NODE_ENV=development
VUE_APP_API_BASE_URL=https://api.yourdomain.com/api

# Or local backend on different port
VUE_APP_API_BASE_URL=http://127.0.0.1:5000/api
```

## 🏗️ Build Process Integration

### Docker Build Process

1. **Copy environment files**: `COPY . .` includes all env files
2. **Override for Docker**: `COPY .env.docker .env.production`
3. **Build with mode**: `npm run build -- --mode production`
4. **Compile variables**: Vue CLI injects `VUE_APP_*` variables into build

### Local Development Build

```bash
# Development build (uses .env.development)
npm run serve

# Production build locally (uses .env.production)
npm run build
```

## 🔗 API Configuration Patterns

### Development Pattern
```
Frontend (localhost:8080) 
    ↓ HTTP Request
Backend (localhost:8000/api)
```

### Docker Pattern
```
Browser → Nginx (port 3000) → API Proxy (/api) → Backend Container (lab_web_app:8000)
                            ↘ Static Files (/*)    → Nginx HTML
```

### Production Pattern
```
Browser → Load Balancer → Frontend Container(s) → Nginx Proxy → Backend Service(s)
```

## 🚀 Deployment Scenarios

### Scenario 1: Local Development
```bash
# Backend
cd backend && flask run

# Frontend (new terminal)
cd frontend && npm run serve
# Accesses http://127.0.0.1:8000/api directly
```

### Scenario 2: Full Docker Stack
```bash
# Start backend first (creates network)
cd backend && docker-compose up -d

# Start frontend (joins existing network)
cd frontend && docker-compose up -d
# Uses nginx proxy to reach lab_web_app:8000
```

### Scenario 3: Custom Domain Production
```bash
# Modify .env.local or .env.production
VUE_APP_API_BASE_URL=https://api.mylab.edu/v1

# Build and deploy
npm run build
# Deploy dist/ to web server
```

### Scenario 4: CDN + API Gateway
```bash
# Frontend served from CDN
VUE_APP_API_BASE_URL=https://api-gateway.mylab.edu/api

# Static files served from CDN
# API calls routed through API Gateway
```

## 🛠️ Troubleshooting

### Issue 1: API Calls Failing

**Symptoms**: 
- Console errors: "Failed to fetch"
- Network tab shows failed API requests

**Diagnosis**:
```bash
# Check compiled API base URL
docker run --rm your-frontend-image grep -r "VUE_APP_API_BASE_URL" /usr/share/nginx/html/

# Should show the correct URL for your environment
```

**Solutions**:
1. Verify correct environment file is loaded
2. Check if backend service is accessible
3. Verify nginx proxy configuration

### Issue 2: Environment Variables Not Loading

**Symptoms**:
- Variables showing as `undefined` in browser
- Development/production differences

**Diagnosis**:
```javascript
// In browser console
console.log(process.env.NODE_ENV);
console.log(process.env.VUE_APP_API_BASE_URL);
```

**Solutions**:
1. Ensure variables start with `VUE_APP_`
2. Restart development server after env changes
3. Check file naming (`.env.development` not `.env.dev`)

### Issue 3: Docker Network Issues

**Symptoms**:
- API proxy returns 502 Bad Gateway
- nginx logs show "host not found in upstream"

**Diagnosis**:
```bash
# Check network connectivity
docker exec frontend-container ping lab_web_app

# Check nginx configuration
docker exec frontend-container nginx -t
```

**Solutions**:
1. Verify backend container name (`lab_web_app`)
2. Ensure containers are on same network
3. Check nginx proxy configuration

## 📝 Best Practices

### 1. Environment Naming
- Use descriptive, environment-specific names
- Follow Vue.js conventions (`.env.production`, `.env.development`)
- Never commit `.env.local` to version control

### 2. Variable Naming
- Prefix all frontend variables with `VUE_APP_`
- Use uppercase with underscores: `VUE_APP_API_BASE_URL`
- Be descriptive: `VUE_APP_API_BASE_URL` not `VUE_APP_API`

### 3. Security
- Never put secrets in frontend environment variables
- All `VUE_APP_*` variables are publicly visible in compiled code
- Use backend environment variables for sensitive configuration

### 4. Documentation
- Document all environment variables in `.env.example`
- Include comments explaining usage
- Keep examples realistic but non-sensitive

### 5. Testing
- Test in multiple environments before deployment
- Verify API connectivity in each environment
- Use health check endpoints to validate configuration

## 🔄 Migration Guide

### From Old Configuration
If you had previous environment setup:

1. **Remove old files**:
   ```bash
   rm .env.prod .env.test  # These were empty
   ```

2. **Update build scripts**:
   - Docker now uses `.env.docker` → `.env.production`
   - Local development uses `.env.development`

3. **Update nginx configuration**:
   - Backend hostname changed from `backend` to `lab_web_app`
   - API proxy routes `/api` to `lab_web_app:8000`

4. **Test new configuration**:
   ```bash
   # Test local development
   npm run serve
   
   # Test Docker build
   docker build -t frontend-test .
   docker run -p 3000:80 frontend-test
   ```

---

**Related Documentation:**
- [Docker Deployment](./DOCKER.md)
- [Main Project README](../README.md)
- [Backend Environment Configuration](../backend/README.md#environment-configuration)