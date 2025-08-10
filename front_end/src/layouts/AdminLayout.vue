<template>
  <n-layout class="admin-layout" has-sider>
    <!-- 側邊欄 -->
    <n-layout-sider
      :collapsed="collapsed"
      :collapsed-width="64"
      :width="240"
      collapse-mode="width"
      bordered
      show-trigger
      @collapse="collapsed = true"
      @expand="collapsed = false"
    >
      <div class="sidebar-header">
        <div class="logo">
          <n-icon v-if="collapsed" size="28" color="#1890ff">
            <svg viewBox="0 0 24 24">
              <path fill="currentColor" d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1Z"/>
            </svg>
          </n-icon>
          <template v-else>
            <n-icon size="28" color="#1890ff" style="margin-right: 0.5rem;">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1Z"/>
              </svg>
            </n-icon>
            <span class="logo-text">{{ $t('admin.layout.title') }}</span>
          </template>
        </div>
      </div>
      
      <n-menu
        :collapsed="collapsed"
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="menuOptions"
        :value="activeKey"
        @update:value="handleMenuSelect"
      />
    </n-layout-sider>

    <!-- 主內容區 -->
    <n-layout>
      <!-- 頂部欄 -->
      <n-layout-header class="header" bordered>
        <div class="header-left">
          <n-breadcrumb>
            <n-breadcrumb-item v-for="item in breadcrumbs" :key="item.path">
              {{ item.title }}
            </n-breadcrumb-item>
          </n-breadcrumb>
        </div>
        
        <div class="header-right">
          <!-- 語言切換 -->
          <n-dropdown :options="languageOptions" @select="handleLanguageChange">
            <n-button text>
              <n-icon size="18" style="margin-right: 0.5rem;">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M12.87,15.07L10.33,12.56L10.36,12.53C12.1,10.59 13.34,8.36 14.07,6H17V4H10V2H8V4H1V6H12.17C11.5,7.92 10.44,9.75 9,11.35C8.07,10.32 7.3,9.19 6.69,8H4.69C5.42,9.63 6.42,11.17 7.67,12.56L2.58,17.58L4,19L9,14L12.11,17.11L12.87,15.07Z"/>
                </svg>
              </n-icon>
              {{ currentLang === 'zh' ? $t('language.chinese') : $t('language.english') }}
            </n-button>
          </n-dropdown>

          <!-- 主題切換 -->
          <n-button text @click="toggleTheme">
            <n-icon size="18">
              <svg v-if="isDark" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8M12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18M20,8.69V4H15.31L12,0.69L8.69,4H4V8.69L0.69,12L4,15.31V20H8.69L12,23.31L15.31,20H20V15.31L23.31,12L20,8.69Z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24">
                <path fill="currentColor" d="M17.75,4.09L15.22,6.03L16.13,9.09L13.5,7.28L10.87,9.09L11.78,6.03L9.25,4.09L12.44,4L13.5,1L14.56,4L17.75,4.09M21.25,11L19.61,12.25L20.2,14.23L18.5,13.06L16.8,14.23L17.39,12.25L15.75,11L17.81,10.95L18.5,9L19.19,10.95L21.25,11M18.97,15.95C19.8,15.87 20.69,17.05 20.16,17.8C19.84,18.25 19.5,18.67 19.08,19.07C15.17,23 8.84,23 4.94,19.07C1.03,15.17 1.03,8.83 4.94,4.93C5.34,4.53 5.76,4.17 6.21,3.85C6.96,3.32 8.14,4.21 8.06,5.04C7.79,7.9 8.75,10.87 10.95,13.06C13.14,15.26 16.1,16.22 18.97,15.95Z"/>
              </svg>
            </n-icon>
          </n-button>

          <!-- 用戶菜單 -->
          <n-dropdown :options="userMenuOptions" @select="handleUserMenuSelect">
            <div class="user-avatar">
              <n-avatar size="small" style="margin-right: 0.5rem;">
                <n-icon>
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
                  </svg>
                </n-icon>
              </n-avatar>
              <span>{{ authStore.admin?.admin_name }}</span>
              <n-icon size="14" style="margin-left: 0.5rem;">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M7,10L12,15L17,10H7Z"/>
                </svg>
              </n-icon>
            </div>
          </n-dropdown>
        </div>
      </n-layout-header>

      <!-- 內容區 -->
      <n-layout-content class="content">
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useMessage, NIcon } from 'naive-ui';
import { useAuthStore } from '@/stores/auth';
import type { MenuOption, DropdownOption } from 'naive-ui';

const router = useRouter();
const route = useRoute();
const { t, locale } = useI18n();
const message = useMessage();
const authStore = useAuthStore();

const collapsed = ref(false);
const isDark = ref(false);

// 當前語言
const currentLang = computed(() => locale.value);

// 活躍菜單項
const activeKey = computed(() => {
  const path = route.path;
  if (path.startsWith('/admin/members')) return 'members';
  if (path.startsWith('/admin/papers')) return 'papers';
  if (path.startsWith('/admin/projects')) return 'projects';
  if (path.startsWith('/admin/news')) return 'news';
  if (path.startsWith('/admin/groups')) return 'groups';
  if (path.startsWith('/admin/lab')) return 'lab';
  if (path.startsWith('/admin/system')) return 'system';
  return 'dashboard';
});

// 麵包屑導航
const breadcrumbs = computed(() => {
  const pathSegments = route.path.split('/').filter(Boolean);
  const breadcrumbs = [];
  
  if (pathSegments.includes('admin')) {
    breadcrumbs.push({ title: t('admin.layout.dashboard'), path: '/admin' });
    
    if (pathSegments.includes('members')) {
      breadcrumbs.push({ title: t('admin.menu.members'), path: '/admin/members' });
    } else if (pathSegments.includes('papers')) {
      breadcrumbs.push({ title: t('admin.menu.papers'), path: '/admin/papers' });
    } else if (pathSegments.includes('projects')) {
      breadcrumbs.push({ title: t('admin.menu.projects'), path: '/admin/projects' });
    } else if (pathSegments.includes('news')) {
      breadcrumbs.push({ title: t('admin.menu.news'), path: '/admin/news' });
    } else if (pathSegments.includes('groups')) {
      breadcrumbs.push({ title: t('admin.menu.groups'), path: '/admin/groups' });
    } else if (pathSegments.includes('lab')) {
      breadcrumbs.push({ title: t('admin.menu.lab'), path: '/admin/lab' });
    } else if (pathSegments.includes('system')) {
      breadcrumbs.push({ title: t('admin.menu.system'), path: '/admin/system' });
    }
  }
  
  return breadcrumbs;
});

// 創建菜單圖標
const renderIcon = (icon: string) => {
  return () => h(NIcon, null, { default: () => h('i', { innerHTML: icon }) });
};

// 菜單選項
const menuOptions = computed<MenuOption[]>(() => [
  {
    label: t('admin.menu.dashboard'),
    key: 'dashboard',
    icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M13,3V9H21V3M13,21H21V11H13M3,21H11V15H3M3,13H11V3H3V13Z"/></svg>')
  },
  {
    label: t('admin.menu.content'),
    key: 'content',
    icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M19,3H5C3.9,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.9 20.1,3 19,3M19,19H5V5H19V19Z"/></svg>'),
    children: [
      {
        label: t('admin.menu.members'),
        key: 'members',
        icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M16,4C18.2,4 20,5.8 20,8A4,4 0 0,1 16,12A4,4 0 0,1 12,8A4,4 0 0,1 16,4M16,14C18.25,14 22,15.13 22,17.25V20H10V17.25C10,15.13 13.75,14 16,14M8.5,14L7.5,16H6L4.5,12H6L7,14H8.5M15,7L14,9H13L11.5,5H13L14,7H15M1.5,5H3L4,7H5.5L4.5,9H3L1.5,5Z"/></svg>')
      },
      {
        label: t('admin.menu.groups'),
        key: 'groups',
        icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12,5.5A3.5,3.5 0 0,1 15.5,9A3.5,3.5 0 0,1 12,12.5A3.5,3.5 0 0,1 8.5,9A3.5,3.5 0 0,1 12,5.5M5,8C5.56,8 6.08,8.15 6.53,8.42C6.38,9.85 6.8,11.27 7.66,12.38C7.16,13.34 6.16,14 5,14A3,3 0 0,1 2,11A3,3 0 0,1 5,8M19,8A3,3 0 0,1 22,11A3,3 0 0,1 19,14C17.84,14 16.84,13.34 16.34,12.38C17.2,11.27 17.62,9.85 17.47,8.42C17.92,8.15 18.44,8 19,8M5.5,18.25C5.5,16.18 8.41,14.5 12,14.5C15.59,14.5 18.5,16.18 18.5,18.25V20H5.5V18.25M0,20V18.5C0,17.11 1.89,15.94 4.45,15.6C3.86,16.28 3.5,17.22 3.5,18.25V20H0M24,20H20.5V18.25C20.5,17.22 20.14,16.28 19.55,15.6C22.11,15.94 24,17.11 24,18.5V20Z"/></svg>')
      },
      {
        label: t('admin.menu.papers'),
        key: 'papers',
        icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/></svg>')
      },
      {
        label: t('admin.menu.projects'),
        key: 'projects',
        icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M19,3H5C3.9,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.9 20.1,3 19,3M19,19H5V8H19V19M10.5,17L15.5,12L10.5,7V10H6V14H10.5V17Z"/></svg>')
      },
      {
        label: t('admin.menu.news'),
        key: 'news',
        icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M20,11H23V13H20V11M1,11H4V13H1V11M13,1V4H11V1H13M4.92,3.5L7.05,5.64L5.63,7.05L3.5,4.93L4.92,3.5M16.95,5.63L19.07,3.5L20.5,4.93L18.37,7.05L16.95,5.63M12,6A6,6 0 0,1 18,12C18,14.22 16.79,16.16 15,17.2V19A1,1 0 0,1 14,20H10A1,1 0 0,1 9,19V17.2C7.21,16.16 6,14.22 6,12A6,6 0 0,1 12,6M14,21V22A1,1 0 0,1 13,23H11A1,1 0 0,1 10,22V21H14M11,18H13V15.87C14.73,15.43 16,13.86 16,12A4,4 0 0,0 8,12C8,13.86 9.27,15.43 11,15.87V18Z"/></svg>')
      }
    ]
  },
  {
    label: t('admin.menu.lab'),
    key: 'lab',
    icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/></svg>')
  },
  ...(authStore.isSuperAdmin ? [{
    label: t('admin.menu.system'),
    key: 'system',
    icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/></svg>')
  }] : [])
]);

// 語言選項
const languageOptions: DropdownOption[] = [
  {
    label: t('language.chinese'),
    key: 'zh'
  },
  {
    label: t('language.english'),
    key: 'en'
  }
];

// 用戶菜單選項
const userMenuOptions: DropdownOption[] = [
  {
    label: t('admin.user.profile'),
    key: 'profile'
  },
  {
    label: t('admin.user.changePassword'),
    key: 'changePassword'
  },
  {
    type: 'divider'
  },
  {
    label: t('admin.user.logout'),
    key: 'logout'
  }
];

// 處理菜單選擇
const handleMenuSelect = (key: string) => {
  if (key === 'dashboard') {
    router.push('/admin/dashboard');
  } else if (['members', 'papers', 'projects', 'news', 'groups', 'lab', 'system'].includes(key)) {
    router.push(`/admin/${key}`);
  }
};

// 處理語言切換
const handleLanguageChange = (key: string) => {
  locale.value = key;
  localStorage.setItem('language', key);
  message.success(t('admin.layout.languageChanged'));
};

// 切換主題
const toggleTheme = () => {
  isDark.value = !isDark.value;
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light');
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
};

// 處理用戶菜單選擇
const handleUserMenuSelect = async (key: string) => {
  if (key === 'logout') {
    await authStore.logout();
    message.success(t('admin.user.logoutSuccess'));
    router.push('/admin/login');
  } else if (key === 'profile') {
    // 跳轉到個人資料頁面
    router.push('/admin/profile');
  } else if (key === 'changePassword') {
    // 跳轉到修改密碼頁面
    router.push('/admin/change-password');
  }
};

// 初始化主題
const initTheme = () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    isDark.value = savedTheme === 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
  }
};

initTheme();
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.logo-text {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.header {
  height: 64px;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.user-avatar:hover {
  background-color: #f3f4f6;
}

.content {
  padding: 1.5rem;
  background-color: #f9fafb;
  overflow-y: auto;
}

/* 暗色主題 */
[data-theme="dark"] .sidebar-header,
.dark .sidebar-header {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .logo-text,
.dark .logo-text {
  color: #f9fafb;
}

[data-theme="dark"] .header,
.dark .header {
  background: #1f2937;
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .user-avatar:hover,
.dark .user-avatar:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .content,
.dark .content {
  background-color: #111827;
}
</style>