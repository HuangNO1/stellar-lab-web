import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import naive from 'naive-ui'
import i18n from './locales'
// 通用字体
import 'vfonts/Lato.css'
// 等宽字体
import 'vfonts/FiraCode.css'

createApp(App).use(store).use(router).use(naive).use(i18n).mount('#app')
