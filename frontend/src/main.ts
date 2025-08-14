import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import i18n from './locales'
import { initConfig, logConfig } from './config/runtime'
// 通用字体
import 'vfonts/Lato.css'
// 等宽字体
import 'vfonts/FiraCode.css'

const pinia = createPinia()

// Initialize runtime configuration first, then create app
initConfig().then(() => {
  // Log configuration for debugging (can be removed in production)
  if (process.env.NODE_ENV === 'development') {
    logConfig();
  }
  
  createApp(App)
    .use(pinia)
    .use(router)
    .use(naive)
    .use(i18n)
    .mount('#app')
}).catch(error => {
  console.error('Failed to initialize runtime config:', error)
  // Fallback: create app anyway with default config
  createApp(App)
    .use(pinia)
    .use(router)
    .use(naive)
    .use(i18n)
    .mount('#app')
})
