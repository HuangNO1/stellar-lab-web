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
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || '/api',
  BACKEND_URL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000',
  APP_TITLE: import.meta.env.VITE_APP_TITLE || 'Lab Website Framework',
  APP_DESCRIPTION: import.meta.env.VITE_APP_DESCRIPTION || 'Modern laboratory website framework'
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
  const runtimeConfig = window.APP_CONFIG || {};
  
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
    // Try to load runtime config from nginx
    const script = document.createElement('script');
    script.src = '/config.js';
    script.onload = () => {
      resolve(getConfig());
    };
    script.onerror = () => {
      console.warn('Runtime config not available, using environment/default config');
      resolve(getConfig());
    };
    
    document.head.appendChild(script);
    
    // Fallback timeout
    setTimeout(() => {
      resolve(getConfig());
    }, 2000);
  });
}