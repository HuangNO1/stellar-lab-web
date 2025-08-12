<template>
  <n-config-provider :theme="currentTheme">
    <n-layout class="admin-layout" :class="{ 'mobile-layout': isMobile, 'dark-theme': isDark }" :has-sider="!isMobile">
    <!-- 側邊欄 -->
    <n-layout-sider
      v-if="!isMobile"
      :collapsed="collapsed"
      :collapsed-width="64"
      :width="280"
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

    <!-- 移動端側邊欄抽屜 -->
    <n-drawer
      v-if="isMobile"
      v-model:show="showMobileSidebar"
      :width="280"
      placement="left"
      class="mobile-sidebar"
    >
      <n-drawer-content :title="$t('admin.layout.title')" :closable="true">
        <n-menu
          :options="menuOptions"
          :value="activeKey"
          @update:value="handleMobileMenuSelect"
        />
      </n-drawer-content>
    </n-drawer>

    <!-- 主內容區 -->
    <n-layout>
      <!-- 頂部欄 -->
      <n-layout-header class="header" bordered>
        <div class="header-left">
          <!-- 移動端菜單按鈕 -->
          <n-button
            v-if="isMobile"
            text
            class="mobile-menu-btn"
            @click="showMobileSidebar = true"
          >
            <n-icon size="20">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"/>
              </svg>
            </n-icon>
          </n-button>
          
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

    <!-- Profile Modal -->
    <ProfileModal
      v-model="showProfileModal"
      @success="handleProfileSuccess"
    />

    <!-- 修改密碼 Modal -->
    <QuickActionModal
      v-model="showPasswordModal"
      :module-type="'admins'"
      :action-type="'edit'"
      :edit-data="passwordEditData"
      :password-only="true"
      @success="handlePasswordSuccess"
    />
  </n-layout>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref, computed, h, onMounted, onUnmounted, provide } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useMessage, NIcon, darkTheme } from 'naive-ui';
import type { GlobalTheme } from 'naive-ui';
import { useAuthStore } from '@/stores/auth';
import { setLanguage, getTheme, setTheme } from '@/locales';
import ProfileModal from '@/components/ProfileModal.vue';
import QuickActionModal from '@/components/QuickActionModal.vue';
import type { MenuOption, DropdownOption } from 'naive-ui';

const router = useRouter();
const route = useRoute();
const { t, locale } = useI18n();
const message = useMessage();
const authStore = useAuthStore();

const collapsed = ref(false);
const isDark = ref(false);
const isMobile = ref(window.innerWidth <= 1024);
const showMobileSidebar = ref(false);
const showProfileModal = ref(false);
const showPasswordModal = ref(false);
const passwordEditData = ref<Record<string, unknown>>({});

// 當前語言
const currentLang = computed(() => locale.value);

// Theme management
const currentTheme = computed<GlobalTheme | null>(() => {
  return isDark.value ? darkTheme : null;
});

// Provide theme state to child components
provide('isDarkMode', isDark);

// 活躍菜單項
const activeKey = computed(() => {
  const path = route.path;
  if (path.startsWith('/admin/members')) return 'members';
  if (path.startsWith('/admin/papers')) return 'papers';
  if (path.startsWith('/admin/projects')) return 'projects';
  if (path.startsWith('/admin/news')) return 'news';
  if (path.startsWith('/admin/groups')) return 'groups';
  if (path.startsWith('/admin/lab')) return 'lab';
  if (path.startsWith('/admin/admins')) return 'admins';
  if (path.startsWith('/admin/system')) return 'system';
  if (path.startsWith('/admin/operation-logs')) return 'operation-logs';
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
    } else if (pathSegments.includes('admins')) {
      breadcrumbs.push({ title: t('admin.menu.admins'), path: '/admin/admins' });
    } else if (pathSegments.includes('system')) {
      breadcrumbs.push({ title: t('admin.menu.system'), path: '/admin/system' });
    } else if (pathSegments.includes('operation-logs')) {
      breadcrumbs.push({ title: t('admin.operationLogs.title'), path: '/admin/operation-logs' });
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
        icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>')
      },
      {
        label: t('admin.menu.groups'),
        key: 'groups',
        icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,12V20H16V22H8V20H5V12H7V20H9V18H15V20H17V12H19M2,16H4V18H2V16M20,16H22V18H20V16Z"/></svg>')
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
    label: t('admin.menu.admins'),
    key: 'admins',
    icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm9 7h-6v13h-2v-6h-2v6H9V9H3V7h18v2z"/></svg>')
  }] : []),
  ...(authStore.isSuperAdmin ? [{
    label: t('admin.menu.system'),
    key: 'system',
    icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/></svg>'),
    children: [
      {
        label: t('admin.operationLogs.title'),
        key: 'operation-logs',
        icon: renderIcon('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/></svg>')
      }
    ]
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
  } else if (key === 'operation-logs') {
    router.push('/admin/operation-logs');
  } else if (['members', 'papers', 'projects', 'news', 'groups', 'lab', 'admins', 'system'].includes(key)) {
    router.push(`/admin/${key}`);
  }
};

// 處理移動端菜單選擇
const handleMobileMenuSelect = (key: string) => {
  handleMenuSelect(key);
  showMobileSidebar.value = false; // 選擇後關閉抽屜
};

// 檢查屏幕尺寸
const checkScreenSize = () => {
  isMobile.value = window.innerWidth <= 1024;
  if (!isMobile.value) {
    showMobileSidebar.value = false;
  }
};

// 監聽窗口大小變化
onMounted(() => {
  window.addEventListener('resize', checkScreenSize);
  checkScreenSize();
});

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize);
});

// 處理語言切換
const handleLanguageChange = (key: string) => {
  locale.value = key;
  setLanguage(key); // 使用統一的 setLanguage 函數保存到 cookie
  message.success(t('admin.layout.languageChanged'));
};

// 切換主題
const toggleTheme = () => {
  isDark.value = !isDark.value;
  const newTheme = isDark.value ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', newTheme);
  setTheme(newTheme);
  
  // Update body and html background immediately for consistent theming
  const bgColor = isDark.value ? 'rgb(16, 16, 20)' : '#fff';
  document.body.style.background = bgColor;
  document.documentElement.style.background = bgColor;
};

// 處理用戶菜單選擇
const handleUserMenuSelect = async (key: string) => {
  if (key === 'logout') {
    await authStore.logout();
    message.success(t('admin.user.logoutSuccess'));
    router.push('/admin/login');
  } else if (key === 'profile') {
    // 顯示個人資料彈窗
    showProfileModal.value = true;
  } else if (key === 'changePassword') {
    // 直接彈出修改密碼的modal
    passwordEditData.value = { ...authStore.admin };
    showPasswordModal.value = true;
  }
};

// 處理個人資料更新成功
const handleProfileSuccess = () => {
  // 個人資料更新成功時的回調，可以在這裡做一些額外的處理
};

// 處理密碼修改成功
const handlePasswordSuccess = () => {
  message.success(t('admin.profile.messages.passwordChangeSuccess'));
};

// 初始化主題
const initTheme = () => {
  const savedTheme = getTheme();
  isDark.value = savedTheme === 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
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
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* 移動端頂部欄調整 */
@media (max-width: 768px) {
  .header {
    padding: 0 1rem;
    height: 56px;
  }
  
  .header-left {
    gap: 0.75rem;
  }
  
  .header-right {
    gap: 0.5rem;
  }
  
  .user-avatar span {
    display: none;
  }
}

@media (max-width: 640px) {
  .header {
    padding: 0 0.75rem;
    height: 52px;
  }
  
  .header-left {
    gap: 0.5rem;
  }
  
  .header-right {
    gap: 0.25rem;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 0 0.5rem;
    height: 48px;
  }
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
  min-height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
}

/* 移動端內容區調整 */
@media (max-width: 1024px) {
  .content {
    padding: 1rem;
    min-height: calc(100vh - 64px);
  }
}

@media (max-width: 768px) {
  .content {
    padding: 0.75rem;
    min-height: calc(100vh - 56px);
  }
}

@media (max-width: 480px) {
  .content {
    padding: 0.5rem;
    min-height: calc(100vh - 48px);
  }
}

/* 移動端布局 */
.mobile-layout {
  height: 100vh;
  overflow: hidden;
}

.mobile-layout .header {
  position: relative;
  z-index: 10;
}

.mobile-menu-btn {
  margin-right: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.375rem;
}

.mobile-menu-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.mobile-sidebar {
  z-index: 1000;
}

.mobile-sidebar :deep(.n-drawer-content) {
  padding: 0;
}

.mobile-sidebar :deep(.n-drawer-header) {
  border-bottom: 1px solid #e5e7eb;
  padding: 1rem 1.5rem;
}

.mobile-sidebar :deep(.n-drawer-body) {
  padding: 0;
}

.mobile-sidebar :deep(.n-menu) {
  padding: 1rem 0;
}

.mobile-sidebar :deep(.n-menu-item) {
  margin: 0 1rem 0.5rem 1rem;
  border-radius: 0.5rem;
  padding: 0;
}

.mobile-sidebar :deep(.n-menu-item .n-menu-item-content) {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
}

.mobile-sidebar :deep(.n-menu-item .n-menu-item-content__icon) {
  margin-right: 0.75rem;
}

/* 暗色主題下的抽屜樣式 */
[data-theme="dark"] .mobile-sidebar :deep(.n-drawer-header) {
  border-bottom-color: rgba(255, 255, 255, 0.1);
  background-color: #1f2937;
}

[data-theme="dark"] .mobile-sidebar :deep(.n-drawer-body) {
  background-color: #1f2937;
}

[data-theme="dark"] .mobile-sidebar :deep(.n-menu-item:hover .n-menu-item-content) {
  background-color: rgba(255, 255, 255, 0.1);
}

/* 全面的暗色主題 */
.admin-layout.dark-theme,
[data-theme="dark"] .admin-layout {
  background-color: #111827;
}

[data-theme="dark"] .sidebar-header,
.dark .sidebar-header {
  border-bottom-color: rgba(255, 255, 255, 0.1);
  background-color: #1f2937;
}

[data-theme="dark"] .logo-text,
.dark .logo-text {
  color: #f9fafb;
}

[data-theme="dark"] .header,
.dark .header {
  background: #1f2937;
  border-bottom-color: rgba(255, 255, 255, 0.1);
  color: #f9fafb;
}

[data-theme="dark"] .user-avatar:hover,
.dark .user-avatar:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .content,
.dark .content {
  background-color: #111827;
  color: #f9fafb;
}

[data-theme="dark"] .mobile-menu-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* N-Layout-Sider 暗色主題 */
[data-theme="dark"] :deep(.n-layout-sider),
.dark-theme :deep(.n-layout-sider) {
  background-color: #1f2937 !important;
  color: #f9fafb;
}

/* N-Menu 暗色主題 */
[data-theme="dark"] :deep(.n-menu),
.dark-theme :deep(.n-menu) {
  background-color: transparent !important;
  color: #f9fafb;
}

[data-theme="dark"] :deep(.n-menu .n-menu-item),
.dark-theme :deep(.n-menu .n-menu-item) {
  color: #d1d5db !important;
}

[data-theme="dark"] :deep(.n-menu .n-menu-item:hover),
.dark-theme :deep(.n-menu .n-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  color: #f9fafb !important;
}

[data-theme="dark"] :deep(.n-menu .n-menu-item.n-menu-item--selected),
.dark-theme :deep(.n-menu .n-menu-item.n-menu-item--selected) {
  background-color: rgba(99, 102, 241, 0.2) !important;
  color: #6366f1 !important;
}

/* 麵包屑暗色主題 */
[data-theme="dark"] :deep(.n-breadcrumb),
.dark-theme :deep(.n-breadcrumb) {
  color: #d1d5db;
}

[data-theme="dark"] :deep(.n-breadcrumb .n-breadcrumb-item),
.dark-theme :deep(.n-breadcrumb .n-breadcrumb-item) {
  color: #d1d5db;
}

/* 下拉菜單暗色主題 */
[data-theme="dark"] :deep(.n-dropdown-menu),
.dark-theme :deep(.n-dropdown-menu) {
  background-color: #1f2937 !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

[data-theme="dark"] :deep(.n-dropdown-option),
.dark-theme :deep(.n-dropdown-option) {
  color: #d1d5db !important;
}

[data-theme="dark"] :deep(.n-dropdown-option:hover),
.dark-theme :deep(.n-dropdown-option:hover) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  color: #f9fafb !important;
}

/* 按鈕暗色主題 */
[data-theme="dark"] :deep(.n-button--text),
.dark-theme :deep(.n-button--text) {
  color: #d1d5db;
}

[data-theme="dark"] :deep(.n-button--text:hover),
.dark-theme :deep(.n-button--text:hover) {
  background-color: rgba(255, 255, 255, 0.1);
  color: #f9fafb;
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

[data-theme="dark"] .mobile-menu-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>