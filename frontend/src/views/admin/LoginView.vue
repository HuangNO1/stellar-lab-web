<template>
  <div class="admin-login">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <div class="logo">
            <n-icon size="48" color="#1890ff">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,7C13.1,7 14,7.9 14,9C14,10.1 13.1,11 12,11C10.9,11 10,10.1 10,9C10,7.9 10.9,7 12,7M12,13.5C13.67,13.5 15.23,14.04 16.5,14.95C16.5,16.23 14.5,17.5 12,17.5C9.5,17.5 7.5,16.23 7.5,14.95C8.77,14.04 10.33,13.5 12,13.5Z"/>
              </svg>
            </n-icon>
          </div>
          <h1 class="login-title">{{ $t('admin.login.title') }}</h1>
          <p class="login-subtitle">{{ $t('admin.login.subtitle') }}</p>
        </div>

        <n-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          @keyup.enter="handleLogin"
        >
          <n-form-item path="admin_name">
            <n-input
              v-model:value="loginForm.admin_name"
              :placeholder="$t('admin.login.usernamePlaceholder')"
              size="large"
              :disabled="loading"
            >
              <template #prefix>
                <n-icon size="18">
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
                  </svg>
                </n-icon>
              </template>
            </n-input>
          </n-form-item>

          <n-form-item path="admin_pass">
            <n-input
              v-model:value="loginForm.admin_pass"
              :placeholder="$t('admin.login.passwordPlaceholder')"
              type="password"
              size="large"
              show-password-on="click"
              :disabled="loading"
            >
              <template #prefix>
                <n-icon size="18">
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M12,17A2,2 0 0,0 14,15C14,13.89 13.1,13 12,13A2,2 0 0,0 10,15A2,2 0 0,0 12,17M18,8A2,2 0 0,1 20,10V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V10C4,8.89 4.9,8 6,8H7V6A5,5 0 0,1 12,1A5,5 0 0,1 17,6V8H18M12,3A3,3 0 0,0 9,6V8H15V6A3,3 0 0,0 12,3Z"/>
                  </svg>
                </n-icon>
              </template>
            </n-input>
          </n-form-item>

          <n-form-item>
            <n-button
              type="primary"
              size="large"
              :block="true"
              :loading="loading"
              @click="handleLogin"
            >
              {{ $t('admin.login.loginButton') }}
            </n-button>
          </n-form-item>
        </n-form>

        <div class="login-footer">
          <n-text depth="3" style="font-size: 0.875rem;">
            {{ $t('admin.login.footer') }}
          </n-text>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useMessage } from 'naive-ui';
import { useAuthStore } from '@/stores/auth';
import type { FormInst } from 'naive-ui';

const router = useRouter();
const { t } = useI18n();
const message = useMessage();
const authStore = useAuthStore();

const loginFormRef = ref<FormInst>();
const loading = ref(false);

// 登錄表單數據
const loginForm = reactive({
  admin_name: '',
  admin_pass: ''
});

// 表單驗證規則
const loginRules = {
  admin_name: [
    {
      required: true,
      message: t('admin.login.usernameRequired'),
      trigger: ['blur', 'input']
    }
  ],
  admin_pass: [
    {
      required: true,
      message: t('admin.login.passwordRequired'),
      trigger: ['blur', 'input']
    }
  ]
};

// 處理登錄
const handleLogin = async () => {
  try {
    await loginFormRef.value?.validate();
    loading.value = true;

    const result = await authStore.login(loginForm.admin_name, loginForm.admin_pass);
    
    if (result.success) {
      message.success(t('admin.login.loginSuccess'));
      await router.push('/admin/dashboard');
    } else {
      message.error(result.message || t('admin.login.loginFailed'));
    }
  } catch (error: any) {
    console.error('登錄驗證失敗:', error);
    message.error(error.message || t('admin.login.loginFailed'));
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.admin-login {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.admin-login::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100%" height="100%" fill="url(%23grid)"/></svg>');
  opacity: 0.3;
}

.login-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 40rem;
  padding: 0 2rem;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.login-title {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.login-subtitle {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.login-footer {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

/* 暗色主題支持 */
[data-theme="dark"] .login-card,
.dark .login-card {
  background: rgba(24, 24, 28, 0.95);
  border-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .login-title,
.dark .login-title {
  color: #f9fafb;
}

[data-theme="dark"] .login-subtitle,
.dark .login-subtitle {
  color: #9ca3af;
}

[data-theme="dark"] .login-footer,
.dark .login-footer {
  border-top-color: rgba(255, 255, 255, 0.1);
}

/* 響應式設計 */
@media (max-width: 640px) {
  .login-container {
    padding: 0 1rem;
  }
  
  .login-card {
    padding: 2rem 1.5rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
}
</style>