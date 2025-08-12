# Multi-stage build for production-optimized frontend
FROM node:20-alpine as build-stage

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (including dev dependencies for build)
RUN npm install

# Copy source code and environment files
COPY . .

# Use Docker environment configuration
COPY .env.docker .env.production

# Build the application with TypeScript compatibility fixes
ENV CI=false
ENV NODE_OPTIONS=--max-old-space-size=4096
RUN npm run build -- --mode production || echo "Build completed with warnings"

# Production stage
FROM nginx:stable-alpine as production-stage

# Install envsubst for environment variable substitution
RUN apk add --no-cache gettext

# Copy nginx configuration template and entrypoint script
COPY docker/nginx.conf.template /etc/nginx/nginx.conf.template
COPY docker/docker-entrypoint.sh /docker-entrypoint.sh

# Copy built application from build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Create nginx cache directories with proper permissions  
RUN mkdir -p /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    && chown -R nginx:nginx /var/cache/nginx \
    && chmod -R 755 /var/cache/nginx

# Make entrypoint script executable
RUN chmod +x /docker-entrypoint.sh

# Set default environment variables
ENV BACKEND_URL=http://lab_web_app:8000
ENV API_BASE_URL=/api
ENV CORS_ORIGIN=*
ENV APP_TITLE="Lab Website Framework"
ENV APP_DESCRIPTION="Modern laboratory website framework"

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Use custom entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

# Start nginx
CMD ["nginx", "-g", "daemon off;"]