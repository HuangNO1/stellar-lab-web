<template>
  <div class="paper-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.papers') }}</h2>
      <n-space>
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.papers.addPaper') }}
        </n-button>
      </n-space>
    </div>

    <!-- 搜索和篩選 -->
    <n-card class="search-card">
      <n-space>
        <n-input
          v-model:value="searchQuery"
          :placeholder="$t('admin.papers.searchPlaceholder')"
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
          :placeholder="$t('admin.papers.filterByType')"
          clearable
          style="width: 150px"
          @update:value="handleSearch"
        />

        <n-select
          v-model:value="filterStatus"
          :options="statusOptions"
          :placeholder="$t('admin.papers.filterByStatus')"
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
      <n-config-provider :locale="naiveLocale" :date-locale="dateLocale">
        <n-data-table
          :columns="columns"
          :data="paperList"
          :pagination="pagination"
          :loading="loading"
          :remote="true"
          :row-key="(row: Paper) => row.paper_id"
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </n-config-provider>
    </n-card>

    <!-- 新增/編輯 Modal -->
    <QuickActionModal
      v-model="showCreateModal"
      :module-type="'papers'"
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
        <p>{{ $t('admin.papers.deleteConfirmText') }}</p>
        <div v-if="deleteTarget" class="delete-paper-info">
          <div class="paper-details">
            <div class="paper-title">{{ deleteTarget.paper_title_zh }}</div>
            <div class="paper-title-en">{{ deleteTarget.paper_title_en }}</div>
            <div class="paper-venue" v-if="deleteTarget.paper_venue">
              {{ $t('admin.papers.form.venue') }}: {{ deleteTarget.paper_venue }}
            </div>
            <div class="paper-date">
              {{ $t('admin.papers.form.date') }}: {{ formatDate(deleteTarget.paper_date) }}
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
import { paperApi } from '@/services/api';
import { getMediaUrl } from '@/utils/media';
import QuickActionModal from '@/components/QuickActionModal.vue';
import type { Paper } from '@/types/api';
import type { DataTableColumns } from 'naive-ui';

const { t, locale } = useI18n();
const message = useMessage();

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
const paperList = ref<Paper[]>([]);
const loading = ref(false);
const deleteLoading = ref(false);
const showDeleteModal = ref(false);
const deleteTarget = ref<Paper | null>(null);

// Modal 狀態
const showCreateModal = ref(false);
const modalActionType = ref<'create' | 'edit'>('create');
const editData = ref<any>({});

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
  { label: t('admin.common.paperTypes.conference'), value: 0 },
  { label: t('admin.common.paperTypes.journal'), value: 1 },
  { label: t('admin.common.paperTypes.patent'), value: 2 },
  { label: t('admin.common.paperTypes.book'), value: 3 },
  { label: t('admin.common.paperTypes.other'), value: 4 }
]);

const statusOptions = computed(() => [
  { label: t('admin.common.paperStatus.submitting'), value: 0 },
  { label: t('admin.common.paperStatus.accepted'), value: 1 }
]);

// 表格列定義
const columns: DataTableColumns<Paper> = [
  {
    title: t('admin.papers.form.titleZh'),
    key: 'paper_title_zh',
    ellipsis: {
      tooltip: true
    },
    render(row) {
      return h('div', [
        h('div', { style: { fontWeight: 'bold' } }, row.paper_title_zh),
        h('div', { style: { fontSize: '0.875rem', color: '#666' } }, row.paper_title_en)
      ]);
    }
  },
  {
    title: t('admin.papers.form.venue'),
    key: 'paper_venue',
    width: 150,
    ellipsis: {
      tooltip: true
    },
    render(row) {
      return row.paper_venue || '-';
    }
  },
  {
    title: t('admin.papers.form.type'),
    key: 'paper_type',
    width: 120,
    render(row) {
      const typeMap = {
        0: { text: t('admin.common.paperTypes.conference'), type: 'info' as const },
        1: { text: t('admin.common.paperTypes.journal'), type: 'success' as const },
        2: { text: t('admin.common.paperTypes.patent'), type: 'warning' as const },
        3: { text: t('admin.common.paperTypes.book'), type: 'default' as const },
        4: { text: t('admin.common.paperTypes.other'), type: 'default' as const }
      };
      const config = typeMap[row.paper_type as keyof typeof typeMap];
      return h(NTag, { type: config.type }, { default: () => config.text });
    }
  },
  {
    title: t('admin.papers.form.status'),
    key: 'paper_accept',
    width: 120,
    render(row) {
      const statusMap = {
        0: { text: t('admin.common.paperStatus.submitting'), type: 'warning' as const },
        1: { text: t('admin.common.paperStatus.accepted'), type: 'success' as const }
      };
      const config = statusMap[row.paper_accept as keyof typeof statusMap];
      return h(NTag, { type: config.type }, { default: () => config.text });
    }
  },
  {
    title: t('admin.papers.form.date'),
    key: 'paper_date',
    width: 120,
    render(row) {
      return formatDate(row.paper_date);
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
    width: 260,
    render(row) {
      return h(NSpace, [
        row.paper_url ? h(NButton, {
          size: 'small',
          type: 'info',
          onClick: () => window.open(row.paper_url!, '_blank')
        }, { default: () => t('papers.viewOnline') }) : null,
        row.paper_file_path ? h(NButton, {
          size: 'small',
          type: 'primary',
          ghost: true,
          onClick: () => window.open(getMediaUrl(row.paper_file_path!), '_blank')
        }, { default: () => t('papers.download') }) : null,
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
      ].filter(Boolean));
    }
  }
];

// 工具函數
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString();
};

// 獲取論文列表
const fetchPapers = async () => {
  try {
    loading.value = true;
    const params = {
      page: pagination.page,
      per_page: pagination.pageSize,
      q: searchQuery.value || undefined,
      paper_type: filterType.value ?? undefined,
      paper_accept: filterStatus.value ?? undefined
    };

    const response = await paperApi.getPapers(params);
    if (response.code === 0) {
      paperList.value = response.data.items;
      pagination.itemCount = response.data.total;
    } else {
      message.error(response.message || t('admin.papers.fetchError'));
    }
  } catch (error) {
    console.error('獲取論文列表失敗:', error);
    message.error(t('admin.papers.fetchError'));
  } finally {
    loading.value = false;
  }
};

// 搜索處理
const handleSearch = () => {
  pagination.page = 1;
  fetchPapers();
};

// 頁面變化處理
const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchPapers();
};

// 每頁數量變化處理
const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize;
  pagination.page = 1;
  fetchPapers();
};

// Modal 處理
const handleCreate = () => {
  modalActionType.value = 'create';
  editData.value = {};
  showCreateModal.value = true;
};

const handleEdit = (paper: Paper) => {
  modalActionType.value = 'edit';
  editData.value = { ...paper };
  showCreateModal.value = true;
};

const handleModalSuccess = () => {
  fetchPapers();
};

// 處理刪除
const handleDelete = (paper: Paper) => {
  deleteTarget.value = paper;
  showDeleteModal.value = true;
};

// 確認刪除
const confirmDelete = async () => {
  if (!deleteTarget.value) return;

  try {
    deleteLoading.value = true;
    const response = await paperApi.deletePaper(deleteTarget.value.paper_id);
    
    if (response.code === 0) {
      message.success(t('admin.papers.deleteSuccess'));
      showDeleteModal.value = false;
      fetchPapers();
    } else {
      message.error(response.message || t('admin.papers.deleteError'));
    }
  } catch (error) {
    console.error('刪除論文失敗:', error);
    message.error(t('admin.papers.deleteError'));
  } finally {
    deleteLoading.value = false;
  }
};

// 生命週期
onMounted(() => {
  fetchPapers();
});
</script>

<style scoped>
.paper-manage {
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

.delete-paper-info {
  margin: 16px 0;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.paper-details {
  flex: 1;
}

.paper-title {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
}

.paper-title-en {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.paper-venue,
.paper-date {
  color: #888;
  font-size: 13px;
  margin-bottom: 4px;
}

/* 暗色主題 */
[data-theme="dark"] .page-header h2,
.dark .page-header h2 {
  color: #f9fafb;
}

[data-theme="dark"] .delete-paper-info,
.dark .delete-paper-info {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .paper-title-en,
.dark .paper-title-en {
  color: #ccc;
}

[data-theme="dark"] .paper-venue,
.dark .paper-venue,
[data-theme="dark"] .paper-date,
.dark .paper-date {
  color: #aaa;
}
</style>