import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Admin, ApiError } from '@/types/api';
import { authApi } from '@/services/api';

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref<boolean>(false);
  const admin = ref<Admin | null>(null);
  const token = ref<string | null>(localStorage.getItem('admin_token'));
  const loading = ref<boolean>(false);

  // 初始化認證狀態
  const initAuth = () => {
    const storedToken = localStorage.getItem('admin_token');
    const storedAdmin = localStorage.getItem('admin_info');
    
    if (storedToken && storedAdmin) {
      token.value = storedToken;
      admin.value = JSON.parse(storedAdmin);
      isAuthenticated.value = true;
    }
  };

  // 登錄
  const login = async (adminName: string, adminPass: string) => {
    try {
      loading.value = true;
      const response = await authApi.login(adminName, adminPass);
      
      if (response.code === 0) {
        const { access_token, admin: adminInfo } = response.data;
        
        // 存儲認證信息
        token.value = access_token;
        admin.value = adminInfo;
        isAuthenticated.value = true;
        
        // 持久化存儲
        localStorage.setItem('admin_token', access_token);
        localStorage.setItem('admin_info', JSON.stringify(adminInfo));
        
        return { success: true };
      } else {
        return { success: false, message: response.message };
      }
    } catch (error: unknown) {
      console.error('登錄失敗:', error);
      // 優先使用服務器返回的錯誤信息
      const apiError = error as ApiError;
      const errorMessage = apiError?.message || '登錄失敗，請檢查網絡連接';
      return { success: false, message: errorMessage };
    } finally {
      loading.value = false;
    }
  };

  // 登出
  const logout = async () => {
    try {
      if (token.value) {
        await authApi.logout();
      }
    } catch (error) {
      console.error('登出請求失敗:', error);
    } finally {
      // 清除本地狀態
      clearAuth();
    }
  };

  // 清除認證狀態
  const clearAuth = () => {
    isAuthenticated.value = false;
    admin.value = null;
    token.value = null;
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_info');
  };

  // 更新個人資訊
  const updateProfile = async (data: Partial<Admin>) => {
    try {
      const response = await authApi.updateProfile(data);
      if (response.code === 0) {
        admin.value = response.data;
        localStorage.setItem('admin_info', JSON.stringify(response.data));
        return { success: true };
      } else {
        return { success: false, message: response.message };
      }
    } catch (error) {
      console.error('更新個人資訊失敗:', error);
      return { success: false, message: '更新失敗，請重試' };
    }
  };

  // 修改密碼
  const changePassword = async (oldPassword: string, newPassword: string) => {
    try {
      const response = await authApi.changePassword(oldPassword, newPassword);
      if (response.code === 0) {
        return { success: true, message: '密碼修改成功' };
      } else {
        return { success: false, message: response.message };
      }
    } catch (error) {
      console.error('修改密碼失敗:', error);
      return { success: false, message: '修改失敗，請重試' };
    }
  };

  // 檢查是否為超級管理員
  const isSuperAdmin = computed(() => {
    return admin.value?.is_super === 1;
  });

  return {
    isAuthenticated,
    admin,
    token,
    loading,
    isSuperAdmin,
    initAuth,
    login,
    logout,
    clearAuth,
    updateProfile,
    changePassword
  };
});