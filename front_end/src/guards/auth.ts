import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

// 管理員認證守衛
export const adminAuthGuard = (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) => {
  const authStore = useAuthStore();
  
  // 初始化認證狀態
  authStore.initAuth();
  
  // 檢查是否已認證
  if (!authStore.isAuthenticated) {
    // 未認證，跳轉到登錄頁
    next('/admin/login');
    return;
  }
  
  // 檢查超級管理員權限（針對系統管理頁面和管理員管理）
  if ((to.path.startsWith('/admin/system') || to.path.includes('/admin/admins')) && !authStore.isSuperAdmin) {
    // 非超級管理員，跳轉到儀表板
    next('/admin/dashboard');
    return;
  }
  
  // 已認證，繼續導航
  next();
};

// 登錄頁面守衛（已登錄則重定向到儀表板）
export const loginGuard = (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) => {
  const authStore = useAuthStore();
  
  // 初始化認證狀態
  authStore.initAuth();
  
  // 如果已經登錄，跳轉到儀表板
  if (authStore.isAuthenticated) {
    next('/admin/dashboard');
    return;
  }
  
  // 未登錄，繼續到登錄頁
  next();
};