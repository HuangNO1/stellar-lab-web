<template>
  <div class="admin-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.admins') }}</h2>
      <n-space>
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.admins.addAdmin') }}
        </n-button>
      </n-space>
    </div>

    <!-- 搜索 -->
    <n-card class="search-card">
      <n-space>
        <n-input
          v-model:value="searchQuery"
          :placeholder="$t('admin.admins.searchPlaceholder')"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
          style="width: 300px"
        >
          <template #prefix>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
              </svg>
            </n-icon>
          </template>
        </n-input>

        <n-button @click="handleSearch">
          {{ $t('search.search') }}
        </n-button>
      </n-space>
    </n-card>

    <!-- 數據表格 -->
    <n-card>
      <n-config-provider :locale="naiveLocale" :date-locale="dateLocale">
        <n-data-table
          :columns="columns"
          :data="adminList"
          :pagination="pagination"
          :loading="loading"
          :remote="true"
          :row-key="(row: Admin) => row.admin_id"
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </n-config-provider>
    </n-card>

    <!-- 新增/編輯 Modal -->
    <QuickActionModal
      v-model="showCreateModal"
      :module-type="'admins'"
      :action-type="modalActionType"
      :edit-data="editData"
      @success="handleModalSuccess"
    />

    <!-- 刪除確認對話框 -->
    <n-modal v-model:show="showDeleteModal">
      <n-card
        style="width: 450px;"
        :title="$t('admin.common.confirmDelete')"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
      >
        <p>{{ $t('admin.admins.deleteConfirmText') }}</p>
        <div v-if="deleteTarget" class="delete-admin-info">
          <div class="admin-details">
            <div class="admin-name">{{ deleteTarget.admin_name }}</div>
            <div class="admin-type">
              <n-tag :type="deleteTarget.is_super === 1 ? 'error' : 'info'">
                {{ deleteTarget.is_super === 1 ? $t('admin.admins.superAdmin') : $t('admin.admins.normalAdmin') }}
              </n-tag>
            </div>
            <div class="admin-created">
              {{ $t('admin.admins.createdAt') }}: {{ formatDate(deleteTarget.created_at) }}
            </div>
          </div>
        </div>
        <template #footer>
          <n-space justify="end">
            <n-button @click="showDeleteModal = false">
              {{ $t('common.cancel') }}
            </n-button>
            <n-button type="error" @click="confirmDelete" :loading="deleteLoading">
              {{ $t('common.confirm') }}
            </n-button>
          </n-space>
        </template>
      </n-card>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, h, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessage, NButton, NTag, NSpace, zhCN, enUS, dateZhCN, dateEnUS } from 'naive-ui';
import { adminApi } from '@/services/api';
import { useAuthStore } from '@/stores/auth';
import QuickActionModal from '@/components/QuickActionModal.vue';
import type { Admin } from '@/types/api';
import type { DataTableColumns } from 'naive-ui';

const { t, locale } = useI18n();
const message = useMessage();
const authStore = useAuthStore();

// 當前語言環境
const currentLocale = computed(() => locale.value);

// Naive UI 語言包配置
const naiveLocale = computed(() => {
  return locale.value === 'zh' ? zhCN : enUS;
});

// 日期選擇器的國際化配置
const dateLocale = computed(() => {
  return locale.value === 'zh' ? dateZhCN : dateEnUS;
});

// 響應式數據
const adminList = ref<Admin[]>([]);
const loading = ref(false);
const deleteLoading = ref(false);
const showDeleteModal = ref(false);
const deleteTarget = ref<Admin | null>(null);

// Modal 狀態
const showCreateModal = ref(false);
const modalActionType = ref<'create' | 'edit'>('create');
const editData = ref<any>({});

// 搜索
const searchQuery = ref('');

// 分頁
const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100]
});

// 工具函數
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString();
};

// 權限檢查函數
const canEditAdmin = (targetAdmin: Admin) => {
  // 只有超級管理員可以編輯管理員
  if (!authStore.isSuperAdmin) return false;
  
  // 超級管理員可以編輯自己的信息
  if (targetAdmin.admin_id === authStore.admin?.admin_id) return true;
  
  // 不能編輯其他超級管理員
  return targetAdmin.is_super !== 1;
};

const canDeleteAdmin = (targetAdmin: Admin) => {
  // 只有超級管理員可以刪除其他管理員
  if (!authStore.isSuperAdmin) return false;
  
  // 不能刪除自己
  if (targetAdmin.admin_id === authStore.admin?.admin_id) return false;
  
  // 不能刪除其他超級管理員
  return targetAdmin.is_super !== 1;
};

// 表格列定義
const columns: DataTableColumns<Admin> = [
  {
    title: t('admin.admins.adminName'),
    key: 'admin_name',
    render(row) {
      return h('div', { style: { fontWeight: 'bold' } }, row.admin_name);
    }
  },
  {
    title: t('admin.admins.adminType'),
    key: 'is_super',
    width: 120,
    render(row) {
      return h(NTag, {
        type: row.is_super === 1 ? 'error' : 'info'
      }, {
        default: () => row.is_super === 1 ? t('admin.admins.superAdmin') : t('admin.admins.normalAdmin')
      });
    }
  },
  {
    title: t('admin.admins.createdAt'),
    key: 'created_at',
    width: 150,
    render(row) {
      return formatDate(row.created_at);
    }
  },
  {
    title: t('admin.common.status'),
    key: 'enable',
    width: 100,
    render(row) {
      return h(NTag, {
        type: row.enable ? 'success' : 'error'
      }, {
        default: () => row.enable ? t('admin.common.enabled') : t('admin.common.disabled')
      });
    }
  },
  {
    title: t('admin.common.actions'),
    key: 'actions',
    width: 180,
    render(row) {
      const buttons = [];
      
      // 編輯按鈕 - 只有權限時才顯示
      if (canEditAdmin(row)) {
        buttons.push(
          h(NButton, {
            size: 'small',
            type: 'primary',
            onClick: () => handleEdit(row)
          }, { default: () => t('admin.common.edit') })
        );
      }
      
      // 刪除按鈕 - 只有權限時才顯示
      if (canDeleteAdmin(row)) {
        buttons.push(
          h(NButton, {
            size: 'small',
            type: 'error',
            onClick: () => handleDelete(row)
          }, { default: () => t('admin.common.delete') })
        );
      }
      
      // 如果沒有任何操作權限，顯示提示
      if (buttons.length === 0) {
        return h('span', { style: { color: '#999', fontSize: '12px' } }, t('admin.common.noPermission'));
      }
      
      return h(NSpace, {}, {
        default: () => buttons
      });
    }
  }
];

// 獲取管理員列表
const fetchAdmins = async () => {
  try {
    loading.value = true;
    const params = {
      page: pagination.page,
      per_page: pagination.pageSize,
      q: searchQuery.value || undefined
    };

    const response = await adminApi.getAdmins(params);
    if (response.code === 0) {
      let admins = response.data.items;
      
      // 將當前登錄的管理員排在最前面
      const currentAdminId = authStore.admin?.admin_id;
      if (currentAdminId) {
        admins = admins.sort((a: Admin, b: Admin) => {
          // 當前用戶排在最前
          if (a.admin_id === currentAdminId) return -1;
          if (b.admin_id === currentAdminId) return 1;
          
          // 其他按創建時間排序
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        });
      }
      
      adminList.value = admins;
      pagination.itemCount = response.data.total;
    } else {
      message.error(response.message || t('admin.admins.fetchError'));
    }
  } catch (error) {
    console.error('獲取管理員列表失敗:', error);
    message.error(t('admin.admins.fetchError'));
  } finally {
    loading.value = false;
  }
};

// 搜索處理
const handleSearch = () => {
  pagination.page = 1;
  fetchAdmins();
};

// 頁面變化處理
const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchAdmins();
};

// 每頁數量變化處理
const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize;
  pagination.page = 1;
  fetchAdmins();
};

// Modal 處理
const handleCreate = () => {
  modalActionType.value = 'create';
  editData.value = {};
  showCreateModal.value = true;
};

const handleEdit = (admin: Admin) => {
  // 雙重檢查權限
  if (!canEditAdmin(admin)) {
    message.error(t('admin.admins.noEditPermission'));
    return;
  }
  
  modalActionType.value = 'edit';
  editData.value = { ...admin };
  showCreateModal.value = true;
};

const handleModalSuccess = () => {
  fetchAdmins();
};

// 處理刪除
const handleDelete = (admin: Admin) => {
  // 雙重檢查權限
  if (!canDeleteAdmin(admin)) {
    message.error(t('admin.admins.noDeletePermission'));
    return;
  }
  
  deleteTarget.value = admin;
  showDeleteModal.value = true;
};

// 確認刪除
const confirmDelete = async () => {
  if (!deleteTarget.value) return;

  try {
    deleteLoading.value = true;
    const response = await adminApi.deleteAdmin(deleteTarget.value.admin_id);
    
    if (response.code === 0) {
      message.success(t('admin.admins.deleteSuccess'));
      showDeleteModal.value = false;
      fetchAdmins();
    } else {
      message.error(response.message || t('admin.admins.deleteError'));
    }
  } catch (error) {
    console.error('刪除管理員失敗:', error);
    message.error(t('admin.admins.deleteError'));
  } finally {
    deleteLoading.value = false;
  }
};

// 生命週期
onMounted(() => {
  fetchAdmins();
});
</script>

<style scoped>
.admin-manage {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.search-card {
  margin-bottom: 0;
}

.delete-admin-info {
  margin: 16px 0;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.admin-details {
  flex: 1;
}

.admin-name {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 8px;
}

.admin-type {
  margin-bottom: 8px;
}

.admin-created {
  color: #888;
  font-size: 13px;
}

/* 暗色主題 */
[data-theme="dark"] .page-header h2,
.dark .page-header h2 {
  color: #f9fafb;
}

[data-theme="dark"] .delete-admin-info,
.dark .delete-admin-info {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .admin-created,
.dark .admin-created {
  color: #aaa;
}
</style>