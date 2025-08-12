#!/bin/sh
set -e

# Default environment variables
export BACKEND_URL=${BACKEND_URL:-"http://lab_web_app:8000"}
export API_BASE_URL=${API_BASE_URL:-"/api"}
export CORS_ORIGIN=${CORS_ORIGIN:-"*"}
export APP_TITLE=${APP_TITLE:-"Lab Website Framework"}
export APP_DESCRIPTION=${APP_DESCRIPTION:-"Modern laboratory website framework"}

# Log configuration
echo "=== Frontend Configuration ==="
echo "BACKEND_URL: $BACKEND_URL"
echo "API_BASE_URL: $API_BASE_URL"  
echo "CORS_ORIGIN: $CORS_ORIGIN"
echo "APP_TITLE: $APP_TITLE"
echo "APP_DESCRIPTION: $APP_DESCRIPTION"
echo "================================"

# Replace environment variables in nginx template
envsubst '${BACKEND_URL} ${API_BASE_URL} ${CORS_ORIGIN} ${APP_TITLE} ${APP_DESCRIPTION}' \
    < /etc/nginx/nginx.conf.template \
    > /etc/nginx/nginx.conf

# Validate nginx configuration
nginx -t

# Create runtime configuration file for frontend JavaScript
cat > /usr/share/nginx/html/config.js << EOF
window.APP_CONFIG = {
    API_BASE_URL: '$API_BASE_URL',
    BACKEND_URL: '$BACKEND_URL',
    APP_TITLE: '$APP_TITLE',
    APP_DESCRIPTION: '$APP_DESCRIPTION'
};
EOF

echo "Frontend configuration completed successfully!"

# Start nginx
exec "$@"