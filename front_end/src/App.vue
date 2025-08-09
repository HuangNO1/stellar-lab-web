<template>
  <n-config-provider :theme="currentTheme">
    <div id="app">
      <!-- Fixed Header Navigation -->
      <n-layout-header class="header-nav" :class="{ 'dark-theme': isDarkMode }">
        <div class="nav-container">
          <!-- Left side: Logo and Name -->
          <div class="nav-left">
            <div class="logo-container">
              <n-icon size="32" color="#1890ff">
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
                  <n-icon><svg viewBox="0 0 24 24"><path fill="currentColor" d="M12.87,15.07L10.33,12.56L10.36,12.53C12.1,10.59 13.34,8.36 14.07,6H17V4H10V2H8V4H1V6H12.17C11.5,7.92 10.44,9.75 9,11.35C8.07,10.32 7.3,9.19 6.69,8H4.69C5.42,9.63 6.42,11.17 7.67,12.56L2.58,17.58L4,19L9,14L12.11,17.11L12.87,15.07Z"/></svg></n-icon>
                </template>
                {{ currentLanguage }}
              </n-button>
            </n-dropdown>
            
            <!-- Theme Toggle -->
            <n-button text @click="toggleTheme">
              <template #icon>
                <n-icon>
                  <svg v-if="isDarkMode" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8M12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18M20,8.69V4H15.31L12,0.69L8.69,4H4V8.69L0.69,12L4,15.31V20H8.69L12,23.31L15.31,20H20V15.31L23.31,12L20,8.69Z"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24">
                    <path fill="currentColor" d="M17.75,4.09L15.22,6.03L16.13,9.09L13.5,7.28L10.87,9.09L11.78,6.03L9.25,4.09L12.44,4L13.5,1L14.56,4L17.75,4.09M21.25,11L19.61,12.25L20.2,14.23L18.5,13.06L16.8,14.23L17.39,12.25L15.75,11L17.81,10.95L18.5,9L19.19,10.95L21.25,11M18.97,15.95C19.8,15.87 20.69,17.05 20.16,17.8C19.84,18.25 19.5,18.67 19.08,19.07C15.17,23 8.84,23 4.94,19.07C1.03,15.17 1.03,8.83 4.94,4.93C5.34,4.53 5.76,4.17 6.21,3.85C6.96,3.32 8.14,4.21 8.06,5.04C7.79,7.9 8.75,10.87 10.95,13.06C13.14,15.26 16.1,16.22 18.97,15.95M17.33,17.97C14.5,17.81 11.7,16.64 9.53,14.5C7.36,12.31 6.2,9.5 6.04,6.68C3.23,9.82 3.34,14.4 6.35,17.41C9.37,20.43 14,20.54 17.33,17.97Z"/>
                  </svg>
                </n-icon>
              </template>
            </n-button>
          </div>
        </div>
      </n-layout-header>
      
      <!-- Main Content Area -->
      <n-layout class="main-layout">
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
  InformationCircleOutline
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
    icon: () => h(NIcon, null, { default: () => h(HomeOutline) }),
    onClick: () => router.push('/')
  },
  {
    label: t('nav.members'),
    key: 'members',
    icon: () => h(NIcon, null, { default: () => h(PeopleOutline) }),
    onClick: () => router.push('/members')
  },
  {
    label: t('nav.research'),
    key: 'research',
    icon: () => h(NIcon, null, { default: () => h(LibraryOutline) }),
    children: [
      {
        label: t('nav.projects'),
        key: 'projects',
        icon: () => h(NIcon, null, { default: () => h(FolderOpenOutline) }),
        onClick: () => router.push('/projects')
      },
      {
        label: t('nav.papers'),
        key: 'papers',
        icon: () => h(NIcon, null, { default: () => h(DocumentTextOutline) }),
        onClick: () => router.push('/papers')
      }
    ]
  },
  {
    label: t('nav.news'),
    key: 'news',
    icon: () => h(NIcon, null, { default: () => h(NewspaperOutline) }),
    onClick: () => router.push('/news')
  },
  {
    label: t('nav.about'),
    key: 'about',
    icon: () => h(NIcon, null, { default: () => h(InformationCircleOutline) }),
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
  console.log('Theme toggled to:', themeValue)
}

// Initialize
onMounted(() => {
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
  height: 100vh;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
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
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  padding: 0 !important;
  height: 64px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

/* Dark theme styles for header */
.header-nav.dark-theme {
  background: rgba(24, 24, 28, 0.95) !important;
  border-bottom-color: rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

/* Dark theme styles for lab name */
.header-nav.dark-theme .lab-name {
  color: #70a1ff !important;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Left side - Logo and Name */
.nav-left {
  display: flex;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.logo-container:hover {
  opacity: 0.8;
}

.lab-name {
  font-size: 20px;
  font-weight: 600;
  color: #1890ff;
  white-space: nowrap;
}

/* Right side - Menu, Language, Theme */
.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-menu {
  background: transparent !important;
  border: none !important;
}

/* Main Layout */
.main-layout {
  margin-top: 64px;
  min-height: calc(100vh - 64px);
  display: flex;
  justify-content: center;
}

.main-content {
  padding: 24px;
  min-height: calc(100vh - 64px);
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
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