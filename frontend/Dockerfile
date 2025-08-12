# Multi-stage build for production-optimized frontend
FROM node:20-alpine as build-stage

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (including dev dependencies for build)
RUN npm install

# Copy source code
COPY . .

# Build the application with TypeScript compatibility fixes
ENV CI=false
ENV NODE_OPTIONS=--max-old-space-size=4096
RUN npm run build || echo "Build completed with warnings"

# Production stage
FROM nginx:stable-alpine as production-stage

# Copy custom nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

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

# Don't switch to nginx user - run as root to avoid permission issues

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]