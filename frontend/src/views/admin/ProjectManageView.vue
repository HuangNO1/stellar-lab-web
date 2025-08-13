<template>
  <div class="project-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.projects') }}</h2>
      <n-space>
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.projects.addProject') }}
        </n-button>
      </n-space>
    </div>

    <!-- 搜索和篩選 -->
    <n-card class="search-card">
      <n-space>
        <n-input
          v-model:value="searchQuery"
          :placeholder="$t('admin.projects.searchPlaceholder')"
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
          v-model:value="filterStatus"
          :options="statusOptions"
          :placeholder="$t('admin.projects.filterByStatus')"
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
            :data="projectList"
            :pagination="pagination"
            :loading="loading"
            :remote="true"
            :row-key="(row: Project) => row.project_id"
            @update:page="handlePageChange"
            @update:page-size="handlePageSizeChange"
          />
        </n-config-provider>
      </div>
    </n-card>

    <!-- 新增/編輯 Modal -->
    <QuickActionModal
      v-model="showCreateModal"
      :module-type="'projects'"
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
        <p>{{ $t('admin.projects.deleteConfirmText') }}</p>
        <div v-if="deleteTarget" class="delete-project-info">
          <div class="project-details">
            <div class="project-name">{{ deleteTarget.project_name_zh }}</div>
            <div class="project-name-en">{{ deleteTarget.project_name_en }}</div>
            <div class="project-url" v-if="deleteTarget.project_url">
              {{ $t('admin.projects.form.url') }}: 
              <a :href="deleteTarget.project_url" target="_blank" rel="noopener noreferrer">
                {{ deleteTarget.project_url }}
              </a>
            </div>
            <div class="project-date" v-if="deleteTarget.project_date_start">
              {{ $t('admin.projects.form.startDate') }}: {{ formatDate(deleteTarget.project_date_start) }}
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
import { projectApi } from '@/services/api';
import QuickActionModal from '@/components/QuickActionModal.vue';
import type { Project } from '@/types/api';
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
const projectList = ref<Project[]>([]);
const loading = ref(false);
const deleteLoading = ref(false);
const showDeleteModal = ref(false);
const deleteTarget = ref<Project | null>(null);

// Modal 狀態
const showCreateModal = ref(false);
const modalActionType = ref<'create' | 'edit'>('create');
const editData = ref<Partial<Project>>({});

// 搜索和篩選
const searchQuery = ref('');
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
const statusOptions = computed(() => [
  { label: t('admin.common.projectStatus.ongoing'), value: 0 },
  { label: t('admin.common.projectStatus.completed'), value: 1 }
]);

// 表格列定義
const columns: DataTableColumns<Project> = [
  {
    title: t('admin.projects.form.nameZh'),
    key: 'project_name_zh',
    ellipsis: {
      tooltip: true
    },
    render(row) {
      return h('div', [
        h('div', { style: { fontWeight: 'bold' } }, row.project_name_zh),
        h('div', { style: { fontSize: '0.875rem', color: '#666' } }, row.project_name_en)
      ]);
    }
  },
  {
    title: t('admin.projects.form.description'),
    key: 'project_desc_zh',
    ellipsis: {
      tooltip: true
    },
    render(row) {
      if (!row.project_desc_zh && !row.project_desc_en) {
        return '-';
      }
      
      const zhDesc = row.project_desc_zh || '';
      const enDesc = row.project_desc_en || '';
      
      return h('div', { style: { maxWidth: '300px' } }, [
        zhDesc ? h('div', { style: { fontSize: '0.875rem', marginBottom: '4px' } }, zhDesc.slice(0, 60) + (zhDesc.length > 60 ? '...' : '')) : null,
        enDesc ? h('div', { style: { fontSize: '0.8rem', color: '#666', fontStyle: 'italic' } }, enDesc.slice(0, 60) + (enDesc.length > 60 ? '...' : '')) : null
      ].filter(Boolean));
    }
  },
  {
    title: t('admin.projects.form.startDate'),
    key: 'project_date_start',
    width: 120,
    render(row) {
      return formatDate(row.project_date_start);
    }
  },
  {
    title: t('admin.projects.form.status'),
    key: 'is_end',
    width: 120,
    render(row) {
      const statusMap = {
        0: { text: t('admin.common.projectStatus.ongoing'), type: 'info' as const },
        1: { text: t('admin.common.projectStatus.completed'), type: 'success' as const }
      };
      const config = statusMap[row.is_end as keyof typeof statusMap];
      return h(NTag, { type: config.type }, { default: () => config.text });
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
    width: 220,
    render(row) {
      return h(NSpace, {}, {
        default: () => [
          row.project_url ? h(NButton, {
            size: 'small',
            type: 'info',
            onClick: () => row.project_url && window.open(row.project_url, '_blank', 'noopener,noreferrer')
          }, { default: () => t('projects.viewRepository') }) : null,
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

// 工具函數
const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString();
};

// 獲取項目列表
const fetchProjects = async () => {
  try {
    loading.value = true;
    const params = {
      page: pagination.page,
      per_page: pagination.pageSize,
      q: searchQuery.value || undefined,
      is_end: filterStatus.value ?? undefined
    };

    const response = await projectApi.getProjects(params);
    if (response.code === 0) {
      projectList.value = response.data.items;
      pagination.itemCount = response.data.total;
    } else {
      message.error(response.message || t('admin.projects.fetchError'));
    }
  } catch (error: any) {
    console.error('獲取項目列表失敗:', error);
    const errorMessage = error?.message || t('admin.projects.fetchError');
    message.error(errorMessage);
  } finally {
    loading.value = false;
  }
};

// 搜索處理
const handleSearch = () => {
  pagination.page = 1;
  fetchProjects();
};

// 頁面變化處理
const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchProjects();
};

// 每頁數量變化處理
const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize;
  pagination.page = 1;
  fetchProjects();
};

// Modal 處理
const handleCreate = () => {
  modalActionType.value = 'create';
  editData.value = {};
  showCreateModal.value = true;
};

const handleEdit = (project: Project) => {
  modalActionType.value = 'edit';
  editData.value = { ...project };
  showCreateModal.value = true;
};

const handleModalSuccess = () => {
  fetchProjects();
};

// 處理刪除
const handleDelete = (project: Project) => {
  deleteTarget.value = project;
  showDeleteModal.value = true;
};

// 確認刪除
const confirmDelete = async () => {
  if (!deleteTarget.value) return;

  try {
    deleteLoading.value = true;
    const response = await projectApi.deleteProject(deleteTarget.value.project_id);
    
    if (response.code === 0) {
      message.success(t('admin.projects.deleteSuccess'));
      showDeleteModal.value = false;
      fetchProjects();
    } else {
      message.error(response.message || t('admin.projects.deleteError'));
    }
  } catch (error: any) {
    console.error('刪除項目失敗:', error);
    const errorMessage = error?.message || t('admin.projects.deleteError');
    message.error(errorMessage);
  } finally {
    deleteLoading.value = false;
  }
};

// 生命週期
onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
.project-manage {
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

.delete-project-info {
  margin: 16px 0;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.project-details {
  flex: 1;
}

.project-name {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
}

.project-name-en {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.project-url,
.project-date {
  color: #888;
  font-size: 13px;
  margin-bottom: 4px;
}

.project-url a {
  color: #1890ff;
  text-decoration: none;
}

.project-url a:hover {
  text-decoration: underline;
}

/* 暗色主題 */
[data-theme="dark"] .page-header h2,
.dark .page-header h2 {
  color: #f9fafb;
}

[data-theme="dark"] .delete-project-info,
.dark .delete-project-info {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .project-name-en,
.dark .project-name-en {
  color: #ccc;
}

[data-theme="dark"] .project-url,
.dark .project-url,
[data-theme="dark"] .project-date,
.dark .project-date {
  color: #aaa;
}

[data-theme="dark"] .project-url a,
.dark .project-url a {
  color: #52c41a;
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