<template>
  <div class="resource-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.resources') }}</h2>
      <n-space>
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.resources.addResource') }}
        </n-button>
      </n-space>
    </div>

    <!-- 搜索和篩選 -->
    <n-card class="search-card">
      <n-space>
        <n-input
          v-model:value="searchQuery"
          :placeholder="$t('admin.resources.searchPlaceholder')"
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

        <n-select
          v-model:value="filterType"
          :options="typeOptions"
          :placeholder="$t('admin.resources.filterByType')"
          clearable
          style="width: 150px"
          @update:value="handleSearch"
        />

        <n-select
          v-model:value="filterStatus"
          :options="statusOptions"
          :placeholder="$t('admin.resources.filterByStatus')"
          clearable
          style="width: 150px"
          @update:value="handleSearch"
        />

        <n-button @click="handleSearch">
          {{ $t('search.search') }}
        </n-button>
      </n-space>
    </n-card>

    <!-- 數據表格 -->
    <n-card>
      <div class="table-container">
        <n-config-provider :locale="naiveLocale" :date-locale="dateLocale">
          <n-data-table
            :columns="columns"
            :data="resourceList"
            :pagination="pagination"
            :loading="loading"
            :remote="true"
            :row-key="(row: Resource) => row.resource_id"
            @update:page="handlePageChange"
            @update:page-size="handlePageSizeChange"
          />
        </n-config-provider>
      </div>
    </n-card>

    <!-- 新增/編輯 Modal -->
    <QuickActionModal
      v-model="showCreateModal"
      :module-type="'resources'"
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
        <p>{{ $t('admin.resources.deleteConfirmText') }}</p>
        <div v-if="deleteTarget" class="delete-resource-info">
          <div class="resource-details">
            <div class="resource-name">{{ deleteTarget.resource_name_zh }}</div>
            <div class="resource-name-en">{{ deleteTarget.resource_name_en }}</div>
            <div class="resource-type" v-if="deleteTarget.resource_type !== undefined">
              {{ $t('admin.resources.form.type') }}: 
              {{ getResourceTypeText(deleteTarget.resource_type) }}
            </div>
            <div class="resource-location" v-if="deleteTarget.resource_location_zh">
              {{ $t('admin.resources.form.locationZh') }}: {{ deleteTarget.resource_location_zh }}
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
import { resourceApi } from '@/services/api';
import QuickActionModal from '@/components/QuickActionModal.vue';
import type { Resource, ApiError } from '@/types/api';
import type { DataTableColumns } from 'naive-ui';

const { t, locale } = useI18n();
const message = useMessage();

// Naive UI 語言包配置
const naiveLocale = computed(() => {
  return locale.value === 'zh' ? zhCN : enUS;
});

// 日期選擇器的國際化配置
const dateLocale = computed(() => {
  return locale.value === 'zh' ? dateZhCN : dateEnUS;
});

// 響應式數據
const resourceList = ref<Resource[]>([]);
const loading = ref(false);
const deleteLoading = ref(false);
const showDeleteModal = ref(false);
const deleteTarget = ref<Resource | null>(null);

// Modal 狀態
const showCreateModal = ref(false);
const modalActionType = ref<'create' | 'edit'>('create');
const editData = ref<Partial<Resource>>({});

// 搜索和篩選
const searchQuery = ref('');
const filterType = ref<number | null>(null);
const filterStatus = ref<number | null>(null);

// 分頁
const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100]
});

// 選項數據
const typeOptions = computed(() => [
  { label: t('admin.common.resourceTypes.equipment'), value: 0 },
  { label: t('admin.common.resourceTypes.software'), value: 1 },
  { label: t('admin.common.resourceTypes.database'), value: 2 },
  { label: t('admin.common.resourceTypes.dataset'), value: 3 },
  { label: t('admin.common.resourceTypes.other'), value: 4 }
]);

const statusOptions = computed(() => [
  { label: t('admin.common.resourceStatus.unavailable'), value: 0 },
  { label: t('admin.common.resourceStatus.available'), value: 1 },
  { label: t('admin.common.resourceStatus.maintenance'), value: 2 }
]);

// 工具函數
const getResourceTypeText = (type: number) => {
  const typeMap: Record<number, string> = {
    0: t('admin.common.resourceTypes.equipment'),
    1: t('admin.common.resourceTypes.software'),
    2: t('admin.common.resourceTypes.database'),
    3: t('admin.common.resourceTypes.dataset'),
    4: t('admin.common.resourceTypes.other')
  };
  return typeMap[type] || t('admin.common.resourceTypes.other');
};

const getResourceStatusText = (status: number) => {
  const statusMap: Record<number, string> = {
    0: t('admin.common.resourceStatus.unavailable'),
    1: t('admin.common.resourceStatus.available'),
    2: t('admin.common.resourceStatus.maintenance')
  };
  return statusMap[status] || t('admin.common.resourceStatus.unavailable');
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString();
};

// 表格列定義
const columns: DataTableColumns<Resource> = [
  {
    title: t('admin.resources.form.nameZh'),
    key: 'resource_name_zh',
    ellipsis: {
      tooltip: true
    },
    render(row) {
      return h('div', [
        h('div', { style: { fontWeight: 'bold' } }, row.resource_name_zh),
        h('div', { style: { fontSize: '0.875rem', color: '#666' } }, row.resource_name_en)
      ]);
    }
  },
  {
    title: t('admin.resources.form.type'),
    key: 'resource_type',
    width: 120,
    render(row) {
      const typeMap = {
        0: { text: t('admin.common.resourceTypes.equipment'), type: 'info' as const },
        1: { text: t('admin.common.resourceTypes.software'), type: 'success' as const },
        2: { text: t('admin.common.resourceTypes.database'), type: 'warning' as const },
        3: { text: t('admin.common.resourceTypes.dataset'), type: 'primary' as const },
        4: { text: t('admin.common.resourceTypes.other'), type: 'default' as const }
      };
      const config = typeMap[row.resource_type as keyof typeof typeMap];
      return h(NTag, { type: config.type }, { default: () => config.text });
    }
  },
  {
    title: t('admin.resources.form.availabilityStatus'),
    key: 'availability_status',
    width: 120,
    render(row) {
      const statusMap = {
        0: { text: t('admin.common.resourceStatus.unavailable'), type: 'error' as const },
        1: { text: t('admin.common.resourceStatus.available'), type: 'success' as const },
        2: { text: t('admin.common.resourceStatus.maintenance'), type: 'warning' as const }
      };
      const config = statusMap[row.availability_status as keyof typeof statusMap];
      return h(NTag, { type: config.type }, { default: () => config.text });
    }
  },
  {
    title: t('admin.resources.form.locationZh'),
    key: 'resource_location_zh',
    ellipsis: {
      tooltip: true
    },
    render(row) {
      if (!row.resource_location_zh && !row.resource_location_en) {
        return '-';
      }
      
      return h('div', [
        row.resource_location_zh ? h('div', { style: { fontSize: '0.875rem' } }, row.resource_location_zh) : null,
        row.resource_location_en ? h('div', { style: { fontSize: '0.8rem', color: '#666', fontStyle: 'italic' } }, row.resource_location_en) : null
      ].filter(Boolean));
    }
  },
  {
    title: t('admin.resources.form.contactInfo'),
    key: 'contact_info',
    width: 150,
    ellipsis: {
      tooltip: true
    },
    render(row) {
      return row.contact_info || '-';
    }
  },
  {
    title: t('admin.common.actions'),
    key: 'actions',
    width: 220,
    render(row) {
      return h(NSpace, {}, {
        default: () => [
          row.resource_url ? h(NButton, {
            size: 'small',
            type: 'info',
            onClick: () => row.resource_url && window.open(row.resource_url, '_blank', 'noopener,noreferrer')
          }, { default: () => t('resources.url') }) : null,
          h(NButton, {
            size: 'small',
            type: 'primary',
            onClick: () => handleEdit(row)
          }, { default: () => t('admin.common.edit') }),
          h(NButton, {
            size: 'small',
            type: 'error',
            onClick: () => handleDelete(row)
          }, { default: () => t('admin.common.delete') })
        ].filter(Boolean)
      });
    }
  }
];

// 獲取資源列表
const fetchResources = async () => {
  try {
    loading.value = true;
    const params = {
      page: pagination.page,
      per_page: pagination.pageSize,
      q: searchQuery.value || undefined,
      resource_type: filterType.value ?? undefined,
      availability_status: filterStatus.value ?? undefined
    };

    const response = await resourceApi.getAdminResources(params);
    if (response.code === 0) {
      resourceList.value = response.data.items;
      pagination.itemCount = response.data.total;
    } else {
      message.error(response.message || t('admin.resources.fetchError'));
    }
  } catch (error: unknown) {
    console.error('獲取資源列表失敗:', error);
    const apiError = error as ApiError;
    const errorMessage = apiError?.message || t('admin.resources.fetchError');
    message.error(errorMessage);
  } finally {
    loading.value = false;
  }
};

// 搜索處理
const handleSearch = () => {
  pagination.page = 1;
  fetchResources();
};

// 頁面變化處理
const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchResources();
};

// 每頁數量變化處理
const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize;
  pagination.page = 1;
  fetchResources();
};

// Modal 處理
const handleCreate = () => {
  modalActionType.value = 'create';
  editData.value = {};
  showCreateModal.value = true;
};

const handleEdit = (resource: Resource) => {
  modalActionType.value = 'edit';
  editData.value = { ...resource };
  showCreateModal.value = true;
};

const handleModalSuccess = () => {
  fetchResources();
};

// 處理刪除
const handleDelete = (resource: Resource) => {
  deleteTarget.value = resource;
  showDeleteModal.value = true;
};

// 確認刪除
const confirmDelete = async () => {
  if (!deleteTarget.value) return;

  try {
    deleteLoading.value = true;
    const response = await resourceApi.deleteResource(deleteTarget.value.resource_id);
    
    if (response.code === 0) {
      message.success(t('admin.resources.deleteSuccess'));
      showDeleteModal.value = false;
      fetchResources();
    } else {
      message.error(response.message || t('admin.resources.deleteError'));
    }
  } catch (error: unknown) {
    console.error('刪除資源失敗:', error);
    const apiError = error as ApiError;
    const errorMessage = apiError?.message || t('admin.resources.deleteError');
    message.error(errorMessage);
  } finally {
    deleteLoading.value = false;
  }
};

// 生命週期
onMounted(() => {
  fetchResources();
});
</script>

<style scoped>
.resource-manage {
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

.delete-resource-info {
  margin: 16px 0;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.resource-details {
  flex: 1;
}

.resource-name {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
}

.resource-name-en {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.resource-type,
.resource-location {
  color: #888;
  font-size: 13px;
  margin-bottom: 4px;
}

/* 暗色主題 */
[data-theme="dark"] .page-header h2,
.dark .page-header h2,
.dark-theme .page-header h2 {
  color: #f9fafb !important;
}

[data-theme="dark"] .delete-resource-info,
.dark .delete-resource-info {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .resource-name-en,
.dark .resource-name-en {
  color: #ccc;
}

[data-theme="dark"] .resource-type,
.dark .resource-type,
[data-theme="dark"] .resource-location,
.dark .resource-location {
  color: #aaa;
}

.table-container {
  overflow-x: auto;
  min-width: 0;
  width: 100%;
}

/* 手機端響應式優化 */
@media (max-width: 768px) {
  .table-container {
    margin: -16px -20px;
    padding: 16px 20px;
    border-radius: 0;
  }
  
  /* 設置表格最小寬度以觸發滾動 */
  :deep(.n-data-table-wrapper) {
    min-width: 1200px;
  }
}
</style>