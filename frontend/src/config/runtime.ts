/**
 * Runtime configuration loader
 * Allows dynamic configuration of API endpoints and app settings
 */

interface AppConfig {
  API_BASE_URL: string;
  BACKEND_URL: string;
  APP_TITLE: string;
  APP_DESCRIPTION: string;
}

// Default fallback configuration
const defaultConfig: AppConfig = {
  API_BASE_URL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api',
  BACKEND_URL: process.env.VUE_APP_BACKEND_URL || 'http://localhost:8000',
  APP_TITLE: process.env.VUE_APP_TITLE || 'Laboratory Website',
  APP_DESCRIPTION: process.env.VUE_APP_DESCRIPTION || 'Modern laboratory website'
};

// Runtime configuration from nginx-generated config.js
declare global {
  interface Window {
    APP_CONFIG?: AppConfig;
  }
}

/**
 * Get runtime configuration with fallbacks
 */
export function getConfig(): AppConfig {
  // Priority: Runtime config (nginx) > Environment variables > Default values
  const runtimeConfig: Partial<AppConfig> = window.APP_CONFIG || {};
  
  return {
    API_BASE_URL: runtimeConfig.API_BASE_URL || defaultConfig.API_BASE_URL,
    BACKEND_URL: runtimeConfig.BACKEND_URL || defaultConfig.BACKEND_URL,
    APP_TITLE: runtimeConfig.APP_TITLE || defaultConfig.APP_TITLE,
    APP_DESCRIPTION: runtimeConfig.APP_DESCRIPTION || defaultConfig.APP_DESCRIPTION
  };
}

/**
 * Initialize app configuration
 */
export function initConfig(): Promise<AppConfig> {
  return new Promise((resolve) => {
    let resolved = false;
    
    const resolveOnce = () => {
      if (!resolved) {
        resolved = true;
        resolve(getConfig());
      }
    };
    
    // Try to load runtime config from nginx
    const script = document.createElement('script');
    script.src = '/config.js';
    script.onload = resolveOnce;
    script.onerror = () => {
      console.warn('Runtime config not available, using environment/default config');
      resolveOnce();
    };
    
    document.head.appendChild(script);
    
    // Fallback timeout (reduced to 1 second for better UX)
    setTimeout(resolveOnce, 1000);
  });
}

/**
 * Debug function to log current configuration
 */
export function logConfig(): void {
  const config = getConfig();
  console.log('=== Runtime Configuration ===');
  console.log('API_BASE_URL:', config.API_BASE_URL);
  console.log('BACKEND_URL:', config.BACKEND_URL);
  console.log('APP_TITLE:', config.APP_TITLE);
  console.log('APP_DESCRIPTION:', config.APP_DESCRIPTION);
  console.log('Runtime config available:', !!window.APP_CONFIG);
  console.log('===============================');
}