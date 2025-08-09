<template>
  <div class="header-container">
    <div class="header-brand">
      <router-link to="/" style="text-decoration: none; color: inherit;">
        <n-space align="center">
          <n-icon size="24">
            <LogoIcon />
          </n-icon>
          <span class="brand-text">{{ $t('nav.home') }}</span>
        </n-space>
      </router-link>
    </div>
    
    <n-menu
      mode="horizontal"
      :options="menuOptions"
      :value="currentRoute"
      @update:value="handleMenuSelect"
      style="flex: 1; margin: 0 24px;"
    />
    
    <n-space>
      <n-select
        v-model:value="locale"
        :options="localeOptions"
        size="small"
        style="width: 100px"
        @update:value="handleLocaleChange"
      />
      <n-button
        v-if="!userStore.isLoggedIn"
        @click="$router.push('/login')"
        type="primary"
      >
        {{ $t('nav.login') }}
      </n-button>
      <n-dropdown
        v-else
        :options="userDropdownOptions"
        @select="handleUserAction"
      >
        <n-button quaternary circle>
          <n-avatar size="small">
            {{ userStore.user?.username?.charAt(0).toUpperCase() }}
          </n-avatar>
        </n-button>
      </n-dropdown>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { computed, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { NIcon } from 'naive-ui'
import { Home, Document, People, Briefcase, Newspaper, Settings } from '@vicons/ionicons5'
import { useUserStore } from '@/store/user'

const LogoIcon = Home

const router = useRouter()
const route = useRoute()
const { t, locale } = useI18n()
const userStore = useUserStore()

const currentRoute = computed(() => route.name as string)

const menuOptions = computed(() => [
  {
    label: t('nav.home'),
    key: 'home',
    icon: () => h(NIcon, null, { default: () => h(Home) })
  },
  {
    label: t('nav.papers'),
    key: 'papers',
    icon: () => h(NIcon, null, { default: () => h(Document) })
  },
  {
    label: t('nav.members'),
    key: 'members',
    icon: () => h(NIcon, null, { default: () => h(People) })
  },
  {
    label: t('nav.projects'),
    key: 'projects',
    icon: () => h(NIcon, null, { default: () => h(Briefcase) })
  },
  {
    label: t('nav.news'),
    key: 'news',
    icon: () => h(NIcon, null, { default: () => h(Newspaper) })
  },
  ...(userStore.isAdmin ? [{
    label: t('nav.admin'),
    key: 'admin',
    icon: () => h(NIcon, null, { default: () => h(Settings) })
  }] : [])
])

const localeOptions = [
  { label: '中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' }
]

const userDropdownOptions = computed(() => [
  {
    label: t('nav.admin'),
    key: 'admin',
    show: userStore.isAdmin
  },
  {
    label: t('nav.logout'),
    key: 'logout'
  }
])

const handleMenuSelect = (key: string) => {
  router.push({ name: key })
}

const handleLocaleChange = (value: string) => {
  locale.value = value
  localStorage.setItem('locale', value)
}

const handleUserAction = (key: string) => {
  if (key === 'logout') {
    userStore.logout()
    router.push('/')
  } else if (key === 'admin') {
    router.push('/admin')
  }
}

// 初始化語言設置
const savedLocale = localStorage.getItem('locale')
if (savedLocale) {
  locale.value = savedLocale
}
</script>

<style scoped>
.header-container {
  display: flex;
  align-items: center;
  height: 100%;
}

.brand-text {
  font-size: 18px;
  font-weight: 600;
}
</style>