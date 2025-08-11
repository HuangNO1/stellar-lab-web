<template>
  <div class="operation-logs">
    <div class="page-header">
      <h2>{{ $t('admin.operationLogs.title') }}</h2>
    </div>

    <!-- 搜索和篩選 -->
    <n-card class="search-section">
      <div class="search-controls">
        <n-space vertical size="large">
          <!-- 基礎搜索 -->
          <n-input
            v-model:value="searchQuery"
            :placeholder="$t('admin.operationLogs.searchPlaceholder')"
            clearable
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          >
            <template #prefix>
              <n-icon size="16">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                </svg>
              </n-icon>
            </template>
          </n-input>

          <!-- 高級篩選 -->
          <n-space>
            <!-- 管理員篩選 -->
            <n-select
              v-model:value="filters.admin_id"
              :options="adminOptions"
              :placeholder="$t('admin.operationLogs.selectAdmin')"
              clearable
              style="width: 200px"
              @update:value="handleSearch"
            />

            <!-- 操作類型篩選 -->
            <n-select
              v-model:value="filters.edit_type"
              :options="editTypeOptions"
              :placeholder="$t('admin.operationLogs.selectOperation')"
              clearable
              style="width: 200px"
              @update:value="handleSearch"
            />

            <!-- 模組篩選 -->
            <n-select
              v-model:value="filters.edit_module"
              :options="moduleOptions"
              :placeholder="$t('admin.operationLogs.selectModule')"
              clearable
              style="width: 200px"
              @update:value="handleSearch"
            />

            <!-- 日期範圍 -->
            <n-config-provider :locale="naiveLocale" :date-locale="dateLocale">
              <n-date-picker
                :key="`date-picker-${currentLocale}`"
                v-model:value="dateRange"
                type="daterange"
                :format="currentLocale === 'zh' ? 'yyyy年MM月dd日' : 'yyyy-MM-dd'"
                value-format="yyyy-MM-dd"
                clearable
                @update:value="handleDateChange"
                :style="{ width: currentLocale === 'zh' ? '350px' : '300px' }"
              />
            </n-config-provider>
          </n-space>
        </n-space>
      </div>
    </n-card>

    <!-- 操作日誌列表 -->
    <n-card>
      <n-data-table
        :columns="columns"
        :data="logs"
        :loading="loading"
        :row-key="(row: EditRecord) => row.edit_id"
        :pagination="false"
        :bordered="false"
      />
      
      <!-- 分頁組件 -->
      <div class="pagination-container">
        <n-pagination
          v-model:page="pagination.page"
          v-model:page-size="pagination.per_page"
          :page-count="Math.ceil(pagination.total / pagination.per_page)"
          :page-sizes="[10, 20, 50]"
          show-size-picker
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </div>
    </n-card>

    <!-- JSON 詳情 Modal -->
    <JsonDetailModal
      v-model:show="showJsonModal"
      :title="jsonModalTitle"
      :content="jsonModalContent"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessage, NButton } from 'naive-ui';
import { zhCN, enUS, dateZhCN, dateEnUS } from 'naive-ui';
import type { DataTableColumns } from 'naive-ui';
import { editRecordApi, adminApi } from '@/services/api';
import type { EditRecord, EditRecordQueryParams, Admin } from '@/types/api';
import JsonDetailModal from '@/components/JsonDetailModal.vue';

const { t, locale } = useI18n();
const message = useMessage();

// 響應式數據
const loading = ref(false);
const logs = ref<EditRecord[]>([]);
const searchQuery = ref('');
const dateRange = ref<[string, string] | null>(null);
const adminList = ref<Admin[]>([]);

// JSON 詳情 modal
const showJsonModal = ref(false);
const jsonModalTitle = ref('');
const jsonModalContent = ref<Record<string, any> | null>(null);

// 篩選條件
const filters = ref<EditRecordQueryParams>({
  admin_id: undefined,
  edit_module: undefined,
  edit_type: undefined,
  start_date: undefined,
  end_date: undefined,
  q: undefined,
  page: 1,
  per_page: 20
});

// 分頁信息
const pagination = ref({
  page: 1,
  per_page: 20,
  total: 0,
  pages: 0
});

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

// 管理員選項
const adminOptions = computed(() => [
  { label: t('admin.operationLogs.allAdmins'), value: undefined },
  ...adminList.value.map(admin => ({
    label: admin.admin_name,
    value: admin.admin_id
  }))
]);

// 操作類型選項
const editTypeOptions = computed(() => [
  { label: t('admin.operationLogs.allOperations'), value: undefined },
  { label: t('admin.operationLogs.create'), value: 'CREATE' },
  { label: t('admin.operationLogs.update'), value: 'UPDATE' },
  { label: t('admin.operationLogs.delete'), value: 'DELETE' },
  { label: t('admin.operationLogs.login'), value: 'LOGIN' },
  { label: t('admin.operationLogs.logout'), value: 'LOGOUT' },
  { label: t('admin.operationLogs.changePassword'), value: 'CHANGE_PASSWORD' },
  { label: t('admin.operationLogs.batchDelete'), value: 'BATCH_DELETE' },
  { label: t('admin.operationLogs.batchUpdate'), value: 'BATCH_UPDATE' },
  { label: t('admin.operationLogs.upload'), value: 'UPLOAD' }
]);

// 模組選項
const moduleOptions = computed(() => [
  { label: t('admin.operationLogs.allModules'), value: undefined },
  { label: t('admin.operationLogs.adminModule'), value: 0 },
  { label: t('admin.operationLogs.labModule'), value: 1 },
  { label: t('admin.operationLogs.groupModule'), value: 2 },
  { label: t('admin.operationLogs.memberModule'), value: 3 },
  { label: t('admin.operationLogs.paperModule'), value: 4 },
  { label: t('admin.operationLogs.newsModule'), value: 5 },
  { label: t('admin.operationLogs.projectModule'), value: 6 }
]);

// 顯示 JSON 詳情
const showJsonDetail = (content: Record<string, any> | undefined, title: string) => {
  if (!content || Object.keys(content).length === 0) return;
  
  jsonModalContent.value = content;
  jsonModalTitle.value = title;
  showJsonModal.value = true;
};

// 格式化模組名稱
const formatModuleName = (moduleId: number): string => {
  const moduleNames = [
    t('admin.operationLogs.adminModule'),
    t('admin.operationLogs.labModule'),
    t('admin.operationLogs.groupModule'),
    t('admin.operationLogs.memberModule'),
    t('admin.operationLogs.paperModule'),
    t('admin.operationLogs.newsModule'),
    t('admin.operationLogs.projectModule')
  ];
  return moduleNames[moduleId] || `模組 ${moduleId}`;
};

// 格式化操作類型
const formatEditType = (type: string): string => {
  const typeMap: Record<string, string> = {
    CREATE: t('admin.operationLogs.create'),
    UPDATE: t('admin.operationLogs.update'),
    DELETE: t('admin.operationLogs.delete'),
    LOGIN: t('admin.operationLogs.login'),
    LOGOUT: t('admin.operationLogs.logout'),
    CHANGE_PASSWORD: t('admin.operationLogs.changePassword'),
    BATCH_DELETE: t('admin.operationLogs.batchDelete'),
    BATCH_UPDATE: t('admin.operationLogs.batchUpdate'),
    UPLOAD: t('admin.operationLogs.upload')
  };
  return typeMap[type] || type;
};

// 表格列定義
const columns = computed<DataTableColumns<EditRecord>>(() => [
  {
    title: t('admin.operationLogs.time'),
    key: 'edit_date',
    width: 180,
    render: (row) => new Date(row.edit_date).toLocaleString(currentLocale.value === 'zh' ? 'zh-CN' : 'en-US')
  },
  {
    title: t('admin.operationLogs.admin'),
    key: 'admin',
    width: 120,
    render: (row) => row.admin?.admin_name || '-'
  },
  {
    title: t('admin.operationLogs.operation'),
    key: 'edit_type',
    width: 100,
    render: (row) => formatEditType(row.edit_type)
  },
  {
    title: t('admin.operationLogs.module'),
    key: 'edit_module',
    width: 120,
    render: (row) => formatModuleName(row.edit_module)
  },
  {
    title: t('admin.operationLogs.content'),
    key: 'edit_content',
    width: 160,
    render: (row) => {
      const hasContent = row.edit_content && Object.keys(row.edit_content).length > 0;
      
      if (!hasContent) {
        return '-';
      }
      
      return h(
        NButton,
        {
          size: 'small',
          type: 'primary',
          onClick: () => showJsonDetail(row.edit_content, `${formatEditType(row.edit_type)} - ${formatModuleName(row.edit_module)}`)
        },
        { default: () => t('common.viewDetails') }
      );
    }
  }
]);

// 載入操作日誌
const loadLogs = async () => {
  try {
    loading.value = true;
    const params: EditRecordQueryParams = {
      ...filters.value,
      q: searchQuery.value || undefined
    };

    const response = await editRecordApi.getEditRecords(params);
    if (response.code === 0) {
      logs.value = response.data.items;
      pagination.value = {
        page: response.data.page || 1,
        per_page: response.data.per_page || 20,
        total: response.data.total,
        pages: response.data.pages || 0
      };
    }
  } catch (error) {
    console.error('載入操作日誌失敗:', error);
    message.error(t('admin.operationLogs.loadError'));
  } finally {
    loading.value = false;
  }
};

// 載入管理員列表
const loadAdmins = async () => {
  try {
    const response = await adminApi.getAdmins({ all: 'true' });
    if (response.code === 0) {
      adminList.value = response.data.items;
    }
  } catch (error) {
    console.error('載入管理員列表失敗:', error);
  }
};

// 處理搜索
const handleSearch = () => {
  filters.value.page = 1;
  pagination.value.page = 1;
  loadLogs();
};

// 處理日期變化
const handleDateChange = (value: [string, string] | null) => {
  if (value) {
    filters.value.start_date = value[0];
    filters.value.end_date = value[1];
  } else {
    filters.value.start_date = undefined;
    filters.value.end_date = undefined;
  }
  handleSearch();
};

// 處理頁面變化
const handlePageChange = (page: number) => {
  filters.value.page = page;
  pagination.value.page = page;
  loadLogs();
};

// 處理每頁大小變化
const handlePageSizeChange = (pageSize: number) => {
  filters.value.per_page = pageSize;
  filters.value.page = 1;
  pagination.value.per_page = pageSize;
  pagination.value.page = 1;
  loadLogs();
};

// 頁面掛載時初始化
onMounted(() => {
  loadAdmins();
  loadLogs();
});
</script>

<style scoped>
.operation-logs {
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

[data-theme="dark"] .page-header h2,
.dark .page-header h2 {
  color: #f9fafb;
}

.search-section {
  background: #fafbfc;
  border: 1px solid #e5e7eb;
}

[data-theme="dark"] .search-section,
.dark .search-section {
  background: #1f2937;
  border-color: #374151;
}

.search-controls {
  width: 100%;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 響應式設計 */
@media (max-width: 48rem) {
  :deep(.n-space) {
    flex-direction: column;
    align-items: stretch;
  }

  :deep(.n-select),
  :deep(.n-date-picker) {
    width: 100% !important;
  }
}
</style>