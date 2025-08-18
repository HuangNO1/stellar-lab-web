<template>
  <div class="admin-not-found-view">
    <div class="admin-not-found-container">
      <!-- 404 圖標 -->
      <div class="error-icon">
        <svg viewBox="0 0 24 24" class="icon">
          <path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M13,7H11V13H13V7M11,15V17H13V15H11Z"/>
        </svg>
      </div>
      
      <!-- 錯誤碼 -->
      <div class="error-code">404</div>
      
      <!-- 錯誤標題 -->
      <h1 class="error-title">{{ $t('admin.error.pageNotFound') }}</h1>
      
      <!-- 錯誤描述 -->
      <p class="error-description">{{ $t('admin.error.adminPageNotFoundDescription') }}</p>
      
      <!-- 操作按鈕 -->
      <div class="error-actions">
        <n-button 
          type="primary" 
          size="large"
          @click="goToDashboard"
          class="action-button"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M13,3V9H21V3M13,21H21V11H13M3,21H11V15H3M3,13H11V3H3V13Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.error.backToDashboard') }}
        </n-button>
        
        <n-button 
          size="large"
          @click="goBack"
          class="action-button"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('common.goBack') }}
        </n-button>
      </div>
      
      <!-- 快速導航 -->
      <div class="quick-nav">
        <h3 class="quick-nav-title">{{ $t('admin.error.quickNavigation') }}</h3>
        <div class="quick-nav-buttons">
          <n-button 
            type="info" 
            dashed
            size="small"
            @click="$router.push('/admin/members')"
            class="quick-nav-button"
          >
            {{ $t('admin.menu.members') }}
          </n-button>
          <n-button 
            type="info" 
            dashed
            size="small"
            @click="$router.push('/admin/groups')"
            class="quick-nav-button"
          >
            {{ $t('admin.menu.groups') }}
          </n-button>
          <n-button 
            type="info" 
            dashed
            size="small"
            @click="$router.push('/admin/papers')"
            class="quick-nav-button"
          >
            {{ $t('admin.menu.papers') }}
          </n-button>
          <n-button 
            type="info" 
            dashed
            size="small"
            @click="$router.push('/admin/projects')"
            class="quick-nav-button"
          >
            {{ $t('admin.menu.projects') }}
          </n-button>
          <n-button 
            type="info" 
            dashed
            size="small"
            @click="$router.push('/admin/news')"
            class="quick-nav-button"
          >
            {{ $t('admin.menu.news') }}
          </n-button>
          <n-button 
            type="info" 
            dashed
            size="small"
            @click="$router.push('/admin/resources')"
            class="quick-nav-button"
          >
            {{ $t('admin.menu.resources') }}
          </n-button>
          <n-button 
            type="info" 
            dashed
            size="small"
            @click="$router.push('/admin/lab')"
            class="quick-nav-button"
          >
            {{ $t('admin.menu.lab') }}
          </n-button>
          <n-button 
            v-if="authStore.isSuperAdmin"
            type="info" 
            dashed
            size="small"
            @click="$router.push('/admin/admins')"
            class="quick-nav-button"
          >
            {{ $t('admin.menu.admins') }}
          </n-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const goToDashboard = () => {
  router.push('/admin/dashboard');
};

const goBack = () => {
  // 如果有歷史記錄，返回上一頁；否則回到管理員儀表板
  if (window.history.length > 1) {
    router.go(-1);
  } else {
    router.push('/admin/dashboard');
  }
};
</script>

<style scoped>
.admin-not-found-view {
  min-height: calc(100vh - 60px); /* 考慮到管理員頂部導航欄 */
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--n-body-color);
  padding: 2rem;
}

.admin-not-found-container {
  text-align: center;
  max-width: 600px;
  background: var(--n-card-color);
  border: 1px solid var(--n-border-color);
  border-radius: 12px;
  padding: 3rem 2rem;
  box-shadow: var(--n-box-shadow);
}

.error-icon {
  margin-bottom: 2rem;
}

.error-icon .icon {
  width: 100px;
  height: 100px;
  color: var(--n-color-target);
  opacity: 0.8;
}

.error-code {
  font-size: 6rem;
  font-weight: 900;
  color: var(--n-color-target);
  line-height: 1;
  margin-bottom: 1rem;
}

.error-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--n-text-color);
  margin: 0 0 1rem 0;
  line-height: 1.2;
}

.error-description {
  font-size: 1.125rem;
  color: var(--n-text-color-placeholder);
  margin: 0 0 2.5rem 0;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
}

.action-button {
  min-width: 140px;
  height: 40px;
}

.quick-nav {
  border-top: 1px solid var(--n-border-color);
  padding-top: 2rem;
}

.quick-nav-title {
  font-size: 1rem;
  font-weight: 500;
  color: var(--n-text-color);
  margin: 0 0 1rem 0;
}

.quick-nav-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.quick-nav-button {
  color: var(--n-color-target);
  font-size: 0.875rem;
}

.quick-nav-button:hover {
  background: var(--n-color-target-hover);
}

/* 響應式設計 */
@media (max-width: 768px) {
  .admin-not-found-view {
    padding: 1rem;
    min-height: calc(100vh - 120px);
  }
  
  .admin-not-found-container {
    padding: 2rem 1.5rem;
  }
  
  .error-code {
    font-size: 4.5rem;
  }
  
  .error-title {
    font-size: 1.75rem;
  }
  
  .error-description {
    font-size: 1rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .action-button {
    width: 100%;
    max-width: 280px;
  }
  
  .error-icon .icon {
    width: 80px;
    height: 80px;
  }
  
  .quick-nav-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .quick-nav-button {
    width: 100%;
    max-width: 200px;
  }
}

@media (max-width: 480px) {
  .admin-not-found-container {
    padding: 1.5rem 1rem;
  }
  
  .error-code {
    font-size: 3.5rem;
  }
  
  .error-title {
    font-size: 1.5rem;
  }
  
  .error-description {
    font-size: 0.9375rem;
  }
}
</style>