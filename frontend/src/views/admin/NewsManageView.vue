<template>
  <div class="news-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.news') }}</h2>
      <n-space>
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.news.addNews') }}
        </n-button>
      </n-space>
    </div>

    <!-- 搜索和篩選 -->
    <n-card class="search-card">
      <n-space>
        <n-input
          v-model:value="searchQuery"
          :placeholder="$t('admin.news.searchPlaceholder')"
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
          :placeholder="$t('admin.news.filterByType')"
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
            :data="newsList"
            :pagination="pagination"
            :loading="loading"
            :remote="true"
            :row-key="(row: News) => row.news_id"
            @update:page="handlePageChange"
            @update:page-size="handlePageSizeChange"
          />
        </n-config-provider>
      </div>
    </n-card>

    <!-- 新增/編輯 Modal -->
    <QuickActionModal
      v-model="showCreateModal"
      :module-type="'news'"
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
        <p>{{ $t('admin.news.deleteConfirmText') }}</p>
        <div v-if="deleteTarget" class="delete-news-info">
          <div class="news-details">
            <div class="news-type">
              <n-tag :type="getNewsTypeTagType(deleteTarget.news_type)">
                {{ getNewsTypeLabel(deleteTarget.news_type) }}
              </n-tag>
            </div>
            <div class="news-content">{{ deleteTarget.news_content_zh?.slice(0, 100) }}{{ deleteTarget.news_content_zh && deleteTarget.news_content_zh.length > 100 ? '...' : '' }}</div>
            <div class="news-date">
              {{ $t('admin.news.form.date') }}: {{ formatDate(deleteTarget.news_date) }}
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
import { newsApi } from '@/services/api';
import QuickActionModal from '@/components/QuickActionModal.vue';
import type { News, ApiError } from '@/types/api';
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
const newsList = ref<News[]>([]);
const loading = ref(false);
const deleteLoading = ref(false);
const showDeleteModal = ref(false);
const deleteTarget = ref<News | null>(null);

// Modal 狀態
const showCreateModal = ref(false);
const modalActionType = ref<'create' | 'edit'>('create');
const editData = ref<Partial<News>>({});

// 搜索和篩選
const searchQuery = ref('');
const filterType = ref<number | null>(null);

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
  { label: t('admin.common.newsTypes.publication'), value: 0 },
  { label: t('admin.common.newsTypes.award'), value: 1 },
  { label: t('admin.common.newsTypes.activity'), value: 2 }
]);

// 工具函數
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString();
};

const getNewsTypeLabel = (type: number) => {
  const typeMap = {
    0: t('admin.common.newsTypes.publication'),
    1: t('admin.common.newsTypes.award'),
    2: t('admin.common.newsTypes.activity')
  };
  return typeMap[type as keyof typeof typeMap] || '-';
};

const getNewsTypeTagType = (type: number) => {
  const typeMap = {
    0: 'success' as const,
    1: 'warning' as const,
    2: 'info' as const
  };
  return typeMap[type as keyof typeof typeMap] || 'default' as const;
};

// 表格列定義
const columns: DataTableColumns<News> = [
  {
    title: t('admin.news.form.type'),
    key: 'news_type',
    width: 120,
    render(row) {
      return h(NTag, { 
        type: getNewsTypeTagType(row.news_type) 
      }, { 
        default: () => getNewsTypeLabel(row.news_type) 
      });
    }
  },
  {
    title: t('admin.news.form.contentZh'),
    key: 'news_content_zh',
    ellipsis: {
      tooltip: true
    },
    render(row) {
      const displayText = row.news_title_zh || row.news_content_zh;
      return h('div', [
        h('div', { style: { fontWeight: 'bold', maxWidth: '400px' } }, 
          displayText ? 
            displayText.slice(0, 100) + (displayText.length > 100 ? '...' : '') :
            '-'
        ),
        row.news_title_en && h('div', { style: { fontSize: '0.875rem', color: '#666', maxWidth: '400px' } }, 
          row.news_title_en.slice(0, 80) + (row.news_title_en.length > 80 ? '...' : '')
        )
      ]);
    }
  },
  {
    title: t('admin.news.form.date'),
    key: 'news_date',
    width: 120,
    render(row) {
      return formatDate(row.news_date);
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
      return h(NSpace, {}, {
        default: () => [
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
        ]
      });
    }
  }
];

// 獲取新聞列表
const fetchNews = async () => {
  try {
    loading.value = true;
    const params = {
      page: pagination.page,
      per_page: pagination.pageSize,
      q: searchQuery.value || undefined,
      news_type: filterType.value ?? undefined
    };

    const response = await newsApi.getNews(params);
    if (response.code === 0) {
      newsList.value = response.data.items;
      pagination.itemCount = response.data.total;
    } else {
      message.error(response.message || t('admin.news.fetchError'));
    }
  } catch (error: unknown) {
    console.error('獲取新聞列表失敗:', error);
    const apiError = error as ApiError;
    const errorMessage = apiError?.message || t('admin.news.fetchError');
    message.error(errorMessage);
  } finally {
    loading.value = false;
  }
};

// 搜索處理
const handleSearch = () => {
  pagination.page = 1;
  fetchNews();
};

// 頁面變化處理
const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchNews();
};

// 每頁數量變化處理
const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize;
  pagination.page = 1;
  fetchNews();
};

// Modal 處理
const handleCreate = () => {
  modalActionType.value = 'create';
  editData.value = {};
  showCreateModal.value = true;
};

const handleEdit = (news: News) => {
  modalActionType.value = 'edit';
  editData.value = { ...news };
  showCreateModal.value = true;
};

const handleModalSuccess = () => {
  fetchNews();
};

// 處理刪除
const handleDelete = (news: News) => {
  deleteTarget.value = news;
  showDeleteModal.value = true;
};

// 確認刪除
const confirmDelete = async () => {
  if (!deleteTarget.value) return;

  try {
    deleteLoading.value = true;
    const response = await newsApi.deleteNews(deleteTarget.value.news_id);
    
    if (response.code === 0) {
      message.success(t('admin.news.deleteSuccess'));
      showDeleteModal.value = false;
      fetchNews();
    } else {
      message.error(response.message || t('admin.news.deleteError'));
    }
  } catch (error: unknown) {
    console.error('刪除新聞失敗:', error);
    const apiError = error as ApiError;
    const errorMessage = apiError?.message || t('admin.news.deleteError');
    message.error(errorMessage);
  } finally {
    deleteLoading.value = false;
  }
};

// 生命週期
onMounted(() => {
  fetchNews();
});
</script>

<style scoped>
.news-manage {
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

.delete-news-info {
  margin: 16px 0;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.news-details {
  flex: 1;
}

.news-type {
  margin-bottom: 8px;
}

.news-content {
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 8px;
  color: #333;
}

.news-date {
  color: #888;
  font-size: 13px;
}

/* 暗色主題 */
[data-theme="dark"] .page-header h2,
.dark .page-header h2 {
  color: #f9fafb;
}

[data-theme="dark"] .delete-news-info,
.dark .delete-news-info {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .news-content,
.dark .news-content {
  color: #e5e7eb;
}

[data-theme="dark"] .news-date,
.dark .news-date {
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
    min-width: 1000px;
  }
}
</style>