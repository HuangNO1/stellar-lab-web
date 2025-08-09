<template>
  <div class="login-page">
    <n-card class="login-card">
      <template #header>
        <div class="login-header">
          <h2>{{ t('nav.login') }}</h2>
        </div>
      </template>
      
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        size="large"
        @submit.prevent="handleLogin"
      >
        <n-form-item path="admin_name">
          <n-input
            v-model:value="formData.admin_name"
            :placeholder="t('form.username')"
            clearable
          >
            <template #prefix>
              <n-icon :component="PersonOutlined" />
            </template>
          </n-input>
        </n-form-item>
        
        <n-form-item path="admin_pass">
          <n-input
            v-model:value="formData.admin_pass"
            type="password"
            :placeholder="t('form.password')"
            show-password-on="click"
          >
            <template #prefix>
              <n-icon :component="LockOutlined" />
            </template>
          </n-input>
        </n-form-item>
        
        <n-form-item>
          <n-button
            type="primary"
            size="large"
            :loading="loading"
            attr-type="submit"
            style="width: 100%"
          >
            {{ t('nav.login') }}
          </n-button>
        </n-form-item>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useI18n } from 'vue-i18n'
import { Person, LockClosed } from '@vicons/ionicons5'
import type { FormInst, FormRules } from 'naive-ui'
import { useUserStore } from '@/store/user'

const PersonOutlined = Person
const LockOutlined = LockClosed
const message = useMessage()
const router = useRouter()
const { t } = useI18n()
const userStore = useUserStore()

const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const formData = ref({
  admin_name: '',
  admin_pass: ''
})

const rules: FormRules = {
  admin_name: {
    required: true,
    message: '請輸入用戶名',
    trigger: 'blur'
  },
  admin_pass: {
    required: true,
    message: '請輸入密碼',
    trigger: 'blur'
  }
}

const handleLogin = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    await userStore.login(formData.value)
    message.success('登錄成功')
    router.push('/')
    
  } catch (error: any) {
    message.error(error.message || '登錄失敗')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.login-header {
  text-align: center;
}

.login-header h2 {
  margin: 0;
  color: #333;
}
</style>