import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'

// Naive UI
import {
  // create naive ui
  create,
  // component
  NButton,
  NInput,
  NInputNumber,
  NSelect,
  NDatePicker,
  NTimePicker,
  NCheckbox,
  NCheckboxGroup,
  NRadio,
  NRadioGroup,
  NSwitch,
  NSlider,
  NRate,
  NUpload,
  NTransfer,
  NForm,
  NFormItem,
  NTable,
  NDataTable,
  NList,
  NListItem,
  NThing,
  NCard,
  NTabs,
  NTabPane,
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NLayoutFooter,
  NLayoutSider,
  NMenu,
  NBreadcrumb,
  NBreadcrumbItem,
  NDropdown,
  NPagination,
  NSpace,
  NDivider,
  NModal,
  NDrawer,
  NPopconfirm,
  NPopover,
  NTooltip,
  NAlert,
  NProgress,
  NSpin,
  NSkeleton,
  NAvatar,
  NBadge,
  NTag,
  NIcon,
  NEmpty,
  NResult,
  NDescriptions,
  NDescriptionsItem,
  NStatistic,
  NSteps,
  NStep,
  NLoadingBarProvider,
  NMessageProvider,
  NNotificationProvider,
  NDialogProvider,
  NConfigProvider,
  NGlobalStyle
} from 'naive-ui'

// 國際化配置
import zhCN from './locales/zh-CN.json'
import enUS from './locales/en-US.json'

const naive = create({
  components: [
    NButton,
    NInput,
    NInputNumber,
    NSelect,
    NDatePicker,
    NTimePicker,
    NCheckbox,
    NCheckboxGroup,
    NRadio,
    NRadioGroup,
    NSwitch,
    NSlider,
    NRate,
    NUpload,
    NTransfer,
    NForm,
    NFormItem,
    NTable,
    NDataTable,
    NList,
    NListItem,
    NThing,
    NCard,
    NTabs,
    NTabPane,
    NLayout,
    NLayoutHeader,
    NLayoutContent,
    NLayoutFooter,
    NLayoutSider,
    NMenu,
    NBreadcrumb,
    NBreadcrumbItem,
    NDropdown,
    NPagination,
    NSpace,
    NDivider,
    NModal,
    NDrawer,
    NPopconfirm,
    NPopover,
    NTooltip,
    NAlert,
    NProgress,
    NSpin,
    NSkeleton,
    NAvatar,
    NBadge,
    NTag,
    NIcon,
    NEmpty,
    NResult,
    NDescriptions,
    NDescriptionsItem,
    NStatistic,
    NSteps,
    NStep,
    NLoadingBarProvider,
    NMessageProvider,
    NNotificationProvider,
    NDialogProvider,
    NConfigProvider,
    NGlobalStyle
  ]
})

const i18n = createI18n({
  legacy: false,
  locale: 'zh-CN',
  fallbackLocale: 'en-US',
  messages: {
    'zh-CN': zhCN,
    'en-US': enUS
  }
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(naive)
app.use(i18n)

app.mount('#app')