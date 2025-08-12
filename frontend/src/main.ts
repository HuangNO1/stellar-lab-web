import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import i18n from './locales'
// 通用字体
import 'vfonts/Lato.css'
// 等宽字体
import 'vfonts/FiraCode.css'

const pinia = createPinia()

createApp(App)
  .use(pinia)
  .use(router)
  .use(naive)
  .use(i18n)
  .mount('#app')
