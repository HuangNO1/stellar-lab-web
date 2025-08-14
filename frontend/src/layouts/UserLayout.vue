<template>
  <n-config-provider :theme="currentTheme">
    <n-message-provider>
      <n-notification-provider>
        <div id="user-app" :class="{ 'dark-mode': isDarkMode }">
          <!-- Fixed Header Navigation for User Frontend -->
          <n-layout-header 
            class="header-nav" 
            :class="{ 'dark-theme': isDarkMode }"
          >
            <div class="nav-container">
              <!-- Left side: Logo and Name -->
              <div class="nav-left">
                <div class="logo-container" @click="router.push('/')">
                  <img v-if="lab?.lab_logo_path" :src="getLabLogoUrl(lab.lab_logo_path)" :alt="$t('defaults.labName')" class="lab-logo" />
                  <n-icon v-else size="26" color="#1890ff">
                    <svg viewBox="0 0 24 24">
                      <path fill="currentColor" d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                    </svg>
                  </n-icon>
                  <span class="lab-name">{{ getLabName() }}</span>
                </div>
              </div>
              
              <!-- Right side: Menu, Language, Theme Toggle -->
              <div class="nav-right">
                <!-- Mobile Menu Button (hidden on desktop) -->
                <n-button 
                  text 
                  class="mobile-menu-btn" 
                  @click="showMobileMenu = !showMobileMenu"
                >
                  <n-icon size="20">
                    <svg viewBox="0 0 24 24">
                      <path fill="currentColor" d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"/>
                    </svg>
                  </n-icon>
                </n-button>
                
                <!-- Navigation Menu (hidden on mobile) -->
                <n-menu
                  v-model:value="activeKey"
                  mode="horizontal"
                  :options="menuOptions"
                  class="nav-menu desktop-menu"
                  @update:value="handleMenuSelect"
                />
                
                <!-- Language Selector -->
                <n-dropdown :options="languageOptions" @select="handleLanguageSelect" class="desktop-lang-selector">
                  <n-button text>
                    <template #icon>
                      <n-icon size="18">
                        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M12.87,15.07L10.33,12.56L10.36,12.53C12.1,10.59 13.34,8.36 14.07,6H17V4H10V2H8V4H1V6H12.17C11.5,7.92 10.44,9.75 9,11.35C8.07,10.32 7.3,9.19 6.69,8H4.69C5.42,9.63 6.42,11.17 7.67,12.56L2.58,17.58L4,19L9,14L12.11,17.11L12.87,15.07Z"/></svg>
                      </n-icon>
                    </template>
                    {{ currentLanguage }}
                  </n-button>
                </n-dropdown>
                
                <!-- Theme Toggle -->
                <n-button text @click="toggleTheme" class="theme-btn desktop-theme-btn">
                  <template #icon>
                    <n-icon size="18">
                      <component :is="isDarkMode ? SunnyOutline : MoonOutline" />
                    </n-icon>
                  </template>
                </n-button>
              </div>
            </div>
          </n-layout-header>
          
          <!-- Mobile Menu Overlay -->
          <n-drawer
            v-model:show="showMobileMenu"
            :width="280"
            placement="right"
            class="mobile-drawer"
          >
            <n-drawer-content :title="$t('nav.menu')">
              <div class="mobile-nav-content">
                <n-menu
                  v-model:value="activeKey"
                  :options="menuOptions"
                  class="mobile-nav-menu"
                  @update:value="handleMobileMenuSelect"
                />
                
                <n-divider />
                
                <div class="mobile-settings">
                  <!-- Language Selector -->
                  <div class="setting-item">
                    <span class="setting-label">{{ $t('common.language') }}</span>
                    <n-select
                      :value="locale"
                      :options="languageSelectOptions"
                      size="small"
                      @update:value="handleLanguageSelect"
                    />
                  </div>
                  
                  <!-- Theme Toggle -->
                  <div class="setting-item">
                    <span class="setting-label">{{ $t('common.theme') }}</span>
                    <n-switch
                      :value="isDarkMode"
                      @update:value="toggleTheme"
                    >
                      <template #checked>
                        {{ $t('common.dark') }}
                      </template>
                      <template #unchecked>
                        {{ $t('common.light') }}
                      </template>
                    </n-switch>
                  </div>
                </div>
              </div>
            </n-drawer-content>
          </n-drawer>
          
          <!-- Main Content Area -->
          <n-layout 
            class="main-layout" 
            :class="{ 
              'dark-theme': isDarkMode, 
              'is-home': route.name === 'home'
            }"
          >
            <n-layout-content 
              class="main-content" 
              :class="{ 
                'home-content': route.name === 'home'
              }"
            >
              <router-view />
            </n-layout-content>
          </n-layout>
        </div>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref, onMounted, h, computed, provide, watch, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { NIcon, darkTheme } from 'naive-ui'
import type { GlobalTheme } from 'naive-ui'
import {
  HomeOutline,
  PeopleOutline,
  FolderOpenOutline,
  DocumentTextOutline,
  NewspaperOutline,
  SunnyOutline,
  MoonOutline
} from '@vicons/ionicons5'
import { setLanguage, getTheme, setTheme } from '@/locales'
import { useLabWithAutoFetch } from '@/composables/useLab'
import { getLabLogoUrl } from '@/utils/media'

const router = useRouter()
const { t, locale } = useI18n()
const route = useRoute()

// 獲取實驗室數據
const { lab } = useLabWithAutoFetch()

// Theme management
const isDarkMode = ref(getTheme() === 'dark')
const currentTheme = computed<GlobalTheme | null>(() => {
  return isDarkMode.value ? darkTheme : null
})

// Provide theme state and lab data to child components
provide('isDarkMode', isDarkMode)
provide('lab', lab)

// Navigation menu
const activeKey = ref<string>('home')
const showMobileMenu = ref(false)

const menuOptions = computed(() => [
  {
    label: t('nav.home'),
    key: 'home',
    icon: () => h(NIcon, { size: 16, component: HomeOutline })
  },
  {
    label: t('nav.members'),
    key: 'members',
    icon: () => h(NIcon, { size: 16, component: PeopleOutline })
  },
  {
    label: t('nav.projects'),
    key: 'projects',
    icon: () => h(NIcon, { size: 16, component: FolderOpenOutline })
  },
  {
    label: t('nav.papers'),
    key: 'papers',
    icon: () => h(NIcon, { size: 16, component: DocumentTextOutline })
  },
  {
    label: t('nav.news'),
    key: 'news',
    icon: () => h(NIcon, { size: 14, component: NewspaperOutline })
  }
])

// Language selector
const currentLanguage = computed(() => {
  return locale.value === 'zh' ? t('language.chinese') : t('language.english')
})

const languageOptions = [
  {
    label: t('language.chinese'),
    key: 'zh',
  },
  {
    label: t('language.english'),
    key: 'en',
  }
]

const languageSelectOptions = computed(() => [
  {
    label: t('language.chinese'),
    value: 'zh',
  },
  {
    label: t('language.english'),
    value: 'en',
  }
])

const handleLanguageSelect = (key: string) => {
  locale.value = key
  setLanguage(key)
  console.log('Language changed to:', key)
}

// Handle menu selection
const handleMenuSelect = (key: string) => {
  console.log('Menu selected:', key)
  showMobileMenu.value = false // Close mobile menu when item selected
  switch (key) {
    case 'home':
      router.push('/')
      break
    case 'members':
      router.push('/members')
      break
    case 'projects':
      router.push('/projects')
      break
    case 'papers':
      router.push('/papers')
      break
    case 'news':
      router.push('/news')
      break
  }
}

// Handle mobile menu selection
const handleMobileMenuSelect = (key: string) => {
  handleMenuSelect(key)
}

// Theme toggle
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const themeValue = isDarkMode.value ? 'dark' : 'light'
  setTheme(themeValue)
  
  // Update body and html background immediately
  const bgColor = isDarkMode.value ? 'rgb(16, 16, 20)' : '#fff'
  document.body.style.background = bgColor
  document.documentElement.style.background = bgColor
  
  console.log('Theme toggled to:', themeValue)
}

// 獲取實驗室名稱（根據當前語言）
const getLabName = () => {
  if (!lab.value) return t('defaults.labName');
  return locale.value === 'zh' 
    ? (lab.value.lab_zh || t('defaults.labName'))
    : (lab.value.lab_en || t('defaults.labName'));
};

// Update active menu based on route
const updateActiveKey = (path: string) => {
  if (path === '/') {
    activeKey.value = 'home'
  } else if (path.startsWith('/members')) {
    activeKey.value = 'members'
  } else if (path.startsWith('/projects')) {
    activeKey.value = 'projects'
  } else if (path.startsWith('/papers')) {
    activeKey.value = 'papers'
  } else if (path.startsWith('/news')) {
    activeKey.value = 'news'
  }
}

// Watch route changes
watch(() => route.path, (newPath) => {
  updateActiveKey(newPath)
})

// Initialize

onMounted(() => {
  // Set initial background based on theme
  const bgColor = isDarkMode.value ? 'rgb(16, 16, 20)' : '#fff'
  document.body.style.background = bgColor
  document.documentElement.style.background = bgColor
  
  // Set active menu based on current route
  updateActiveKey(route.path)
})

// 組件卸載時清理
onUnmounted(() => {
  // cleanup if needed
})
</script>

<style>
#user-app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
  background: #fff;
  transition: all 0.3s ease;
}

/* Dark mode for app */
#user-app.dark-mode {
  background: rgb(16, 16, 20) !important;
  color: #ffffff !important;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  background: #fff;
  transition: all 0.3s ease;
  min-height: 100vh;
}

html {
  background: #fff;
  transition: all 0.3s ease;
  min-height: 100vh;
}

/* Global dark mode styles */
body:has(#user-app.dark-mode) {
  background: rgb(16, 16, 20) !important;
}

html:has(#user-app.dark-mode) {
  background: rgb(16, 16, 20) !important;
}

/* Fallback for browsers that don't support :has() */
.dark-mode-global body,
.dark-mode-global html {
  background: rgb(16, 16, 20) !important;
}
</style>

<style scoped>
/* Fixed Header Navigation */
.header-nav {
  position: fixed !important;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1001;
  padding: 0 !important;
  height: 0;
  background: transparent;
}

/* iPhone-like notch design */
.nav-container {
  position: relative;
  width: 70vw;
  margin: 0 auto;
  height: 4.5rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 0 0 2.25rem 2.25rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  transition: all 0.3s ease;
}

/* Dark theme for notch */
.header-nav.dark-theme .nav-container {
  background: rgba(16, 16, 20, 0.95) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}

/* Left side - Logo and Name */
.nav-left {
  display: flex;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.logo-container:hover {
  opacity: 0.8;
}

.lab-name {
  font-size: 18px;
  font-weight: 600;
  color: #1890ff;
  white-space: nowrap;
}

.lab-logo {
  width: 26px;
  height: 26px;
  object-fit: contain;
  border-radius: 4px;
}

/* Dark theme styles for lab name */
.header-nav.dark-theme .lab-name {
  color: #70a1ff !important;
}

/* Right side - Menu, Language, Theme */
.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 100%;
}

.nav-menu.desktop-menu {
  background: transparent !important;
  border: none !important;
  margin-right: 8px;
}

.mobile-menu-btn {
  display: none;
}

.desktop-lang-selector,
.desktop-theme-btn {
  display: flex;
  align-items: center;
  height: 2.5rem;
}

.desktop-lang-selector .n-button,
.desktop-theme-btn {
  height: 2.5rem;
  min-height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 1.25rem;
  padding: 0 12px;
  transition: all 0.2s ease;
}

.desktop-lang-selector .n-button:hover,
.desktop-theme-btn:hover {
  background-color: rgba(24, 144, 255, 0.1);
}

/* Dark theme styles for buttons */
.header-nav.dark-theme .desktop-lang-selector .n-button:hover,
.header-nav.dark-theme .desktop-theme-btn:hover {
  background-color: rgba(112, 161, 255, 0.15);
}

/* Mobile Navigation Styles */
.mobile-nav-content {
  padding: 1rem 0;
}

.mobile-nav-menu {
  background: transparent !important;
  border: none !important;
}

/* 移動端菜單項樣式 */
:deep(.mobile-nav-menu .n-menu-item) {
  border-radius: 8px;
  margin-bottom: 4px;
}

:deep(.mobile-nav-menu .n-menu-item .n-menu-item-content) {
  padding: 12px 16px;
}

/* 暗色主題下的移動端菜單 */
.dark-mode :deep(.mobile-nav-menu .n-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.1);
}

.mobile-settings {
  margin-top: 1rem;
  padding: 1rem 0;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-label {
  font-weight: 500;
  color: #666;
  font-size: 1rem;
  flex-shrink: 0;
  min-width: 60px;
}

/* Dark mode for mobile settings */
.dark-mode .setting-label {
  color: #ccc;
}

.dark-mode .setting-item {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

/* 語言選擇器樣式調整 */
.setting-item .n-select {
  min-width: 120px;
}

/* 主題開關樣式調整 */
.setting-item .n-switch {
  flex-shrink: 0;
}

/* Better aligned menu styling */
:deep(.n-menu--horizontal .n-menu-item) {
  padding: 0 12px !important;
  margin: 0 3px !important;
  height: 2.5rem !important;
  border-radius: 1.25rem !important;
  font-size: 15px !important;
  line-height: 1.4 !important;
  display: flex !important;
  align-items: center !important;
}

:deep(.n-menu--horizontal .n-menu-item .n-menu-item-content) {
  padding: 0 !important;
  min-height: 2.5rem !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

:deep(.n-menu--horizontal .n-menu-item .n-menu-item-content .n-menu-item-content__icon) {
  margin-right: 8px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

/* Main Layout */
.main-layout {
  margin-top: 4.5rem;
  min-height: calc(100vh - 4.5rem);
  width: 100%;
}

.main-content {
  padding: 1.5rem;
  min-height: calc(100vh - 4.5rem);
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  background: transparent;
}

/* Home page specific styles - remove constraints */
.main-content.home-content {
  padding: 0 !important;
  max-width: none !important;
  margin: 0 !important;
  width: 100% !important;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .main-content:not(.home-content) {
    max-width: 100%;
    padding: 1.25rem;
  }
}

@media (max-width: 1024px) {
  .nav-container {
    width: 85vw;
    padding: 0 1.5rem;
  }
  
  .nav-right {
    gap: 10px;
  }
  
  .lab-name {
    font-size: 16px;
  }
  
  .desktop-lang-selector .n-button,
  .desktop-theme-btn {
    padding: 0 10px;
  }
}

@media (max-width: 768px) {
  .nav-container {
    width: 90vw;
    padding: 0 1rem;
    height: 4rem;
    border-radius: 0 0 2rem 2rem;
  }
  
  .lab-name {
    font-size: 15px;
  }
  
  .nav-right {
    gap: 4px;
  }
  
  .desktop-menu {
    display: none;
  }
  
  .mobile-menu-btn {
    display: block !important;
  }
  
  .desktop-lang-selector,
  .desktop-theme-btn {
    display: none !important;
  }
  
  .main-layout {
    margin-top: 4rem;
  }
  
  .main-content:not(.home-content) {
    padding: 1rem;
    min-height: calc(100vh - 4rem);
  }
}

@media (max-width: 640px) {
  .nav-container {
    width: 95vw;
    padding: 0 0.75rem;
    height: 3.5rem;
    border-radius: 0 0 1.75rem 1.75rem;
  }
  
  .lab-name {
    font-size: 14px;
  }
  
  .main-layout {
    margin-top: 3.5rem;
  }
  
  .main-content:not(.home-content) {
    padding: 0.75rem;
    min-height: calc(100vh - 3.5rem);
  }
}

@media (max-width: 480px) {
  .nav-container {
    width: 98vw;
    padding: 0 0.5rem;
    height: 3rem;
    border-radius: 0 0 1.5rem 1.5rem;
  }
  
  .lab-name {
    font-size: 12px;
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .main-layout {
    margin-top: 3rem;
  }
  
  .main-content:not(.home-content) {
    padding: 0.5rem;
    min-height: calc(100vh - 3rem);
  }
}
</style>