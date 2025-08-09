<template>
  <n-config-provider :theme="currentTheme">
    <div id="app" :class="{ 'dark-mode': isDarkMode }">
      <!-- Fixed Header Navigation -->
      <n-layout-header class="header-nav" :class="{ 'dark-theme': isDarkMode }">
        <div class="nav-container">
          <!-- Left side: Logo and Name -->
          <div class="nav-left">
            <div class="logo-container">
              <n-icon size="26" color="#1890ff">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
              </n-icon>
              <span class="lab-name">實驗室名稱</span>
            </div>
          </div>
          
          <!-- Right side: Menu, Language, Theme Toggle -->
          <div class="nav-right">
            <!-- Navigation Menu -->
            <n-menu
              v-model:value="activeKey"
              mode="horizontal"
              :options="menuOptions"
              class="nav-menu"
            />
            
            <!-- Language Selector -->
            <n-dropdown :options="languageOptions" @select="handleLanguageSelect">
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
            <n-button text @click="toggleTheme" class="theme-btn">
              <template #icon>
                <n-icon size="18">
                  <component :is="isDarkMode ? SunnyOutline : MoonOutline" />
                </n-icon>
              </template>
            </n-button>
          </div>
        </div>
      </n-layout-header>
      
      <!-- Main Content Area -->
      <n-layout class="main-layout" :class="{ 'dark-theme': isDarkMode }">
        <n-layout-content class="main-content">
          <router-view />
        </n-layout-content>
      </n-layout>
    </div>
  </n-config-provider>
</template>
<script setup lang="ts">
import { ref, onMounted, h, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { NIcon, darkTheme } from 'naive-ui'
import type { GlobalTheme } from 'naive-ui'
import {
  HomeOutline,
  PeopleOutline,
  LibraryOutline,
  FolderOpenOutline,
  DocumentTextOutline,
  NewspaperOutline,
  InformationCircleOutline,
  SunnyOutline,
  MoonOutline
} from '@vicons/ionicons5'
import { setLanguage, getTheme, setTheme } from './locales'

const router = useRouter()
const { t, locale } = useI18n()

// Theme management
const isDarkMode = ref(getTheme() === 'dark')
const currentTheme = computed<GlobalTheme | null>(() => {
  return isDarkMode.value ? darkTheme : null
})

// Navigation menu
const activeKey = ref<string>('home')

const menuOptions = computed(() => [
  {
    label: t('nav.home'),
    key: 'home',
    icon: () => h(NIcon, { size: 16, component: HomeOutline }),
    onClick: () => router.push('/')
  },
  {
    label: t('nav.members'),
    key: 'members',
    icon: () => h(NIcon, { size: 16, component: PeopleOutline }),
    onClick: () => router.push('/members')
  },
  {
    label: t('nav.research'),
    key: 'research',
    icon: () => h(NIcon, { size: 16, component: LibraryOutline }),
    children: [
      {
        label: t('nav.projects'),
        key: 'projects',
        icon: () => h(NIcon, { size: 16, component: FolderOpenOutline }),
        onClick: () => router.push('/projects')
      },
      {
        label: t('nav.papers'),
        key: 'papers',
        icon: () => h(NIcon, { size: 16, component: DocumentTextOutline }),
        onClick: () => router.push('/papers')
      }
    ]
  },
  {
    label: t('nav.news'),
    key: 'news',
    icon: () => h(NIcon, { size: 14, component: NewspaperOutline }),
    onClick: () => router.push('/news')
  },
  {
    label: t('nav.about'),
    key: 'about',
    icon: () => h(NIcon, { size: 16, component: InformationCircleOutline }),
    onClick: () => router.push('/about')
  }
])

// Language selector
const currentLanguage = computed(() => {
  return locale.value === 'zh' ? '中文' : 'English'
})

const languageOptions = [
  {
    label: '中文',
    key: 'zh',
  },
  {
    label: 'English',
    key: 'en',
  }
]

const handleLanguageSelect = (key: string) => {
  locale.value = key
  setLanguage(key)
  console.log('Language changed to:', key)
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

// Initialize
onMounted(() => {
  // Set initial background based on theme
  const bgColor = isDarkMode.value ? 'rgb(16, 16, 20)' : '#fff'
  document.body.style.background = bgColor
  document.documentElement.style.background = bgColor
  
  // Set active menu based on current route
  const currentPath = router.currentRoute.value.path
  if (currentPath === '/') {
    activeKey.value = 'home'
  } else if (currentPath.startsWith('/members')) {
    activeKey.value = 'members'
  } else if (currentPath.startsWith('/projects')) {
    activeKey.value = 'projects'
  } else if (currentPath.startsWith('/papers')) {
    activeKey.value = 'papers'
  } else if (currentPath.startsWith('/news')) {
    activeKey.value = 'news'
  } else if (currentPath.startsWith('/about')) {
    activeKey.value = 'about'
  }
})
</script>

<style>
#app {
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
#app.dark-mode {
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
body:has(#app.dark-mode) {
  background: rgb(16, 16, 20) !important;
}

html:has(#app.dark-mode) {
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
  z-index: 1000;
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

/* Remove problematic side curves */
.nav-container::before,
.nav-container::after {
  display: none;
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

/* Dark theme styles for lab name */
.header-nav.dark-theme .lab-name {
  color: #70a1ff !important;
}

/* Right side - Menu, Language, Theme */
.nav-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-menu {
  background: transparent !important;
  border: none !important;
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

/* Fix submenu/dropdown alignment specifically */
:deep(.n-submenu) {
  display: flex !important;
  align-items: center !important;
}

:deep(.n-submenu .n-menu-item-content) {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  height: 2.5rem !important;
}

:deep(.n-submenu .n-menu-item-content .n-menu-item-content__icon) {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin-right: 8px !important;
}

:deep(.n-submenu .n-menu-item-content .n-menu-item-content__arrow) {
  display: flex !important;
  align-items: center !important;
  margin-left: 8px !important;
}

/* Main Layout */
.main-layout {
  margin-top: 4.5rem;
  min-height: calc(100vh - 4.5rem);
  display: flex;
  justify-content: center;
}

.main-content {
  padding: 24px;
  min-height: calc(100vh - 4.5rem);
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  background: transparent;
}

/* Responsive Design */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 16px;
  }
  
  .lab-name {
    font-size: 16px;
  }
  
  .nav-right {
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .lab-name {
    display: none;
  }
  
  .nav-container {
    padding: 0 12px;
  }
}
</style>