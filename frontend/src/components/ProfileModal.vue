<template>
  <n-modal v-model:show="show" @update:show="handleModalClose" class="profile-modal">
    <n-card
      :style="{ width: isMobile ? '95vw' : '600px', maxWidth: isMobile ? '95vw' : '600px' }"
      :title="modalTitle"
      :bordered="false"
      :size="isMobile ? 'medium' : 'huge'"
      role="dialog"
      aria-modal="true"
      class="modal-card"
    >
      <template #header-extra>
        <n-button
          quaternary
          circle
          @click="show = false"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
              </svg>
            </n-icon>
          </template>
        </n-button>
      </template>

      <!-- 查看模式 -->
      <div v-if="!editMode" class="profile-view">
        <div class="profile-info">
          <n-descriptions 
            :column="1" 
            :label-placement="isMobile ? 'top' : 'left'"
            :label-width="isMobile ? 'auto' : '140px'"
          >
            <n-descriptions-item :label="t('admin.admins.form.adminName')">
              {{ authStore.admin?.admin_name }}
            </n-descriptions-item>
            <n-descriptions-item :label="t('admin.admins.form.isSuper')">
              <n-tag :type="authStore.admin?.is_super ? 'success' : 'default'">
                {{ authStore.admin?.is_super ? t('admin.admins.superAdmin') : t('admin.admins.normalAdmin') }}
              </n-tag>
            </n-descriptions-item>
            <n-descriptions-item :label="t('admin.common.status')">
              <n-tag :type="authStore.admin?.enable ? 'success' : 'error'">
                {{ authStore.admin?.enable ? t('admin.common.enabled') : t('admin.common.disabled') }}
              </n-tag>
            </n-descriptions-item>
            <n-descriptions-item :label="t('admin.admins.createdAt')">
              {{ formatDate(authStore.admin?.created_at) }}
            </n-descriptions-item>
          </n-descriptions>
        </div>
      </div>

      <!-- 编辑模式 -->
      <div v-else class="profile-edit">
        <n-form
          ref="formRef"
          :model="formData"
          :rules="formRules"
          :label-placement="isMobile ? 'top' : 'left'"
          :label-width="isMobile ? 'auto' : '140'"
          require-mark-placement="right-hanging"
        >
          <n-form-item :label="t('admin.admins.form.adminName')" path="admin_name">
            <n-input
              v-model:value="formData.admin_name"
              :placeholder="t('admin.admins.form.placeholders.adminName')"
              style="width: 100%"
            />
          </n-form-item>

          <!-- 修改密码选项 -->
          <n-form-item>
            <n-checkbox v-model:checked="changePassword" @update:checked="handlePasswordToggle">
              {{ t('admin.user.changePassword') }}
            </n-checkbox>
          </n-form-item>

          <!-- 密码字段 -->
          <template v-if="changePassword">
            <n-form-item :label="t('admin.profile.currentPassword')" path="old_password">
              <n-input
                v-model:value="formData.old_password"
                type="password"
                :placeholder="t('admin.profile.placeholders.currentPassword')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.profile.newPassword')" path="new_password">
              <n-input
                v-model:value="formData.new_password"
                type="password"
                :placeholder="t('admin.profile.placeholders.newPassword')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.profile.confirmPassword')" path="confirm_password">
              <n-input
                v-model:value="formData.confirm_password"
                type="password"
                :placeholder="t('admin.profile.placeholders.confirmPassword')"
                style="width: 100%"
              />
            </n-form-item>
          </template>
        </n-form>
      </div>

      <template #footer>
        <div class="modal-footer">
          <n-button v-if="!editMode" @click="show = false">
            {{ t('admin.common.cancel') }}
          </n-button>
          <n-button v-if="!editMode" type="primary" @click="enterEditMode">
            {{ t('admin.common.edit') }}
          </n-button>

          <n-button v-if="editMode" @click="cancelEdit">
            {{ t('admin.common.cancel') }}
          </n-button>
          <n-button
            v-if="editMode"
            type="primary"
            :loading="submitting"
            @click="handleSubmit"
          >
            {{ t('admin.common.update') }}
          </n-button>
        </div>
      </template>
    </n-card>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick, onMounted, onUnmounted } from 'vue';
import { useMessage } from 'naive-ui';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/stores/auth';
import { authApi } from '@/services/api';
import type { ApiError } from '@/types/api';

const { t } = useI18n();
const message = useMessage();
const authStore = useAuthStore();

// Props
interface Props {
  modelValue: boolean;
}

const props = defineProps<Props>();

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean];
  'success': [data: Record<string, unknown>];
}>();

// Reactive data
const show = ref(props.modelValue);
const editMode = ref(false);
const changePassword = ref(false);
const formRef = ref<{ validate: () => Promise<void>; restoreValidation: () => void } | null>(null);
const submitting = ref(false);
const isMobile = ref(window.innerWidth <= 768);

// Form data
const formData = reactive<{
  admin_name: string;
  old_password: string;
  new_password: string;
  confirm_password: string;
}>({
  admin_name: '',
  old_password: '',
  new_password: '',
  confirm_password: ''
});

// Computed
const modalTitle = computed(() => {
  if (editMode.value) {
    return t('admin.profile.editProfile');
  }
  return t('admin.user.profile');
});

// Form rules
const formRules = computed(() => {
  const rules: Record<string, { required?: boolean; message: string; trigger: string | string[]; min?: number; validator?: (rule: unknown, value: string) => boolean | Error }[]> = {
    admin_name: [{ required: true, message: t('admin.admins.form.validation.adminNameRequired'), trigger: 'blur' }]
  };

  if (changePassword.value) {
    rules.old_password = [{ required: true, message: t('admin.profile.validation.currentPasswordRequired'), trigger: 'blur' }];
    rules.new_password = [
      { required: true, message: t('admin.profile.validation.newPasswordRequired'), trigger: 'blur' },
      { min: 8, message: t('admin.profile.validation.passwordMinLength'), trigger: 'blur' }
    ];
    rules.confirm_password = [
      { required: true, message: t('admin.profile.validation.confirmPasswordRequired'), trigger: 'blur' },
      {
        message: t('admin.profile.validation.passwordNotMatch'),
        validator: (rule: unknown, value: string) => {
          if (value !== formData.new_password) {
            return new Error(t('admin.profile.validation.passwordNotMatch'));
          }
          return true;
        },
        trigger: ['blur', 'change']
      }
    ];
  }

  return rules;
});

// Watchers
watch(
  () => props.modelValue,
  (newValue) => {
    show.value = newValue;
    if (newValue) {
      resetForm();
    }
  }
);

watch(show, (newValue) => {
  emit('update:modelValue', newValue);
});

// 检查屏幕尺寸
const checkScreenSize = () => {
  isMobile.value = window.innerWidth <= 768;
};

// 监听窗口大小变化
onMounted(() => {
  window.addEventListener('resize', checkScreenSize);
  checkScreenSize();
});

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize);
});

// Methods
const formatDate = (dateString?: string) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleString();
};

const resetForm = () => {
  editMode.value = false;
  changePassword.value = false;
  formData.admin_name = authStore.admin?.admin_name || '';
  formData.old_password = '';
  formData.new_password = '';
  formData.confirm_password = '';
  formRef.value?.restoreValidation();
};

const handleModalClose = (value: boolean) => {
  if (!value) {
    resetForm();
  }
};

const enterEditMode = () => {
  editMode.value = true;
  formData.admin_name = authStore.admin?.admin_name || '';
};

const cancelEdit = () => {
  editMode.value = false;
  changePassword.value = false;
  resetForm();
};

const handlePasswordToggle = (checked: boolean) => {
  if (!checked) {
    formData.old_password = '';
    formData.new_password = '';
    formData.confirm_password = '';
  }
  nextTick(() => {
    formRef.value?.restoreValidation();
  });
};

const handleSubmit = async () => {
  try {
    await formRef.value?.validate();
    submitting.value = true;

    // 构建请求数据
    const updateData: Record<string, unknown> = {};
    let needsProfileUpdate = false;
    let needsPasswordChange = false;

    // 检查是否需要更新用户名
    if (formData.admin_name !== authStore.admin?.admin_name) {
      updateData.admin_name = formData.admin_name;
      needsProfileUpdate = true;
    }

    // 处理密码更新
    if (changePassword.value) {
      needsPasswordChange = true;
    }

    // 先更新个人资料（如果需要）
    if (needsProfileUpdate) {
      try {
        await authApi.updateProfile(updateData);
        
        // 更新本地存储的管理员信息
        if (authStore.admin) {
          authStore.admin.admin_name = formData.admin_name;
        }
        
        message.success(t('admin.profile.messages.profileUpdateSuccess'));
      } catch (error: unknown) {
        const apiError = error as ApiError;
        const errorMessage = apiError?.message || t('admin.profile.messages.updateFailed');
        message.error(errorMessage);
        return;
      }
    }

    // 然后更改密码（如果需要）
    if (needsPasswordChange) {
      try {
        await authApi.changePassword(formData.old_password, formData.new_password);
        message.success(t('admin.profile.messages.passwordChangeSuccess'));
      } catch (error: unknown) {
        const apiError = error as ApiError;
        const errorMessage = apiError?.message || t('admin.profile.messages.passwordChangeFailed');
        message.error(errorMessage);
        return;
      }
    }

    // 如果没有任何更新
    if (!needsProfileUpdate && !needsPasswordChange) {
      message.info(t('admin.profile.messages.noChanges'));
      return;
    }

    emit('success', authStore.admin as Record<string, unknown>);
    show.value = false;
    resetForm();

  } catch (error) {
    if (error instanceof Error && error.message) {
      message.error(error.message);
    } else {
      message.error(t('admin.profile.messages.updateFailed'));
    }
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.profile-modal :deep(.n-modal) {
  padding: 1rem;
}

.modal-card {
  margin: 0 auto;
}

.profile-view {
  padding: 1rem 0;
}

.profile-info {
  max-width: 100%;
}

.profile-info :deep(.n-descriptions-item-label) {
  font-weight: 600;
  min-width: 120px;
}

.profile-info :deep(.n-descriptions-item-content) {
  text-align: left;
}

/* 確保標籤和內容對齊 */
.profile-info :deep(.n-descriptions) {
  width: 100%;
}

.profile-info :deep(.n-descriptions-item) {
  margin-bottom: 20px;
  align-items: flex-start;
}

.profile-info :deep(.n-descriptions-item-label) {
  font-weight: 600;
  min-width: 140px;
  padding-right: 16px;
  text-align: left;
  white-space: nowrap;
  flex-shrink: 0;
}

.profile-info :deep(.n-descriptions-item-content) {
  text-align: left;
  flex: 1;
}

/* 編輯模式表單對齊 */
.profile-edit :deep(.n-form-item-label) {
  min-width: 140px;
  text-align: left;
  padding-right: 16px;
  white-space: nowrap;
  flex-shrink: 0;
}

.profile-edit :deep(.n-form-item-blank) {
  flex: 1;
}

.profile-edit {
  padding: 0.5rem 0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 1rem;
}

/* 移动端样式调整 */
@media (max-width: 768px) {
  .profile-modal :deep(.n-modal) {
    padding: 0.5rem;
  }
  
  .modal-card :deep(.n-card__header) {
    padding: 1rem 1rem 0.75rem 1rem;
    font-size: 1.125rem;
  }
  
  .modal-card :deep(.n-card__content) {
    padding: 0.75rem 1rem;
  }
  
  .modal-card :deep(.n-card__footer) {
    padding: 0.75rem 1rem 1rem 1rem;
  }
  
  .modal-footer {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }
  
  .modal-footer .n-button {
    width: 100%;
    justify-content: center;
  }

  .profile-view {
    padding: 0.5rem 0;
  }
  
  .profile-info :deep(.n-descriptions-item-label) {
    font-weight: 600;
    margin-bottom: 0.5rem;
    min-width: auto;
    padding-right: 0;
  }
  
  .profile-info :deep(.n-descriptions-item) {
    margin-bottom: 1rem;
  }
  
  /* 編輯模式移動端對齊 */
  .profile-edit :deep(.n-form-item-label) {
    min-width: auto;
    padding-right: 0;
    margin-bottom: 0.5rem;
  }
}

@media (max-width: 480px) {
  .profile-modal :deep(.n-modal) {
    padding: 0.25rem;
  }
  
  .modal-card :deep(.n-card__header) {
    padding: 0.75rem 0.75rem 0.5rem 0.75rem;
  }
  
  .modal-card :deep(.n-card__content) {
    padding: 0.5rem 0.75rem;
  }
  
  .modal-card :deep(.n-card__footer) {
    padding: 0.5rem 0.75rem 0.75rem 0.75rem;
  }
}
</style>