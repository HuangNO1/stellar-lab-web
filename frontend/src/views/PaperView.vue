<template>
  <div class="paper-view">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">{{ $t('nav.papers') }}</h1>
        <p class="page-description">{{ $t('papers.description') }}</p>
      </div>
    </div>

    <!-- 搜索組件 -->
    <SearchComponent
      :config="searchConfig"
      :filters="currentFilters"
      @search="handleSearch"
    />

    <!-- 加載狀態 -->
    <div v-if="loading" class="paper-skeleton">
      <div v-for="i in 6" :key="i" class="paper-item-skeleton">
        <div class="skeleton-header">
          <n-skeleton text height="1.5rem" width="80%" />
          <n-skeleton text height="1rem" width="60%" style="margin-top: 0.5rem" />
        </div>
        <n-skeleton text height="0.875rem" width="100%" :repeat="2" style="margin-top: 1rem" />
        <div class="skeleton-meta" style="margin-top: 1rem; display: flex; gap: 1rem;">
          <n-skeleton text height="0.75rem" width="20%" />
          <n-skeleton text height="0.75rem" width="15%" />
        </div>
      </div>
    </div>

    <!-- 錯誤狀態 -->
    <div v-else-if="error" class="error-state">
      <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 1rem;">
        {{ error }}
      </n-alert>
      <n-button @click="fetchPapers" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 論文列表 -->
    <div v-else class="paper-content">
      <div v-if="paperList.length > 0" class="paper-list">
        <PaperCard 
          v-for="paper in paperList" 
          :key="paper.paper_id" 
          :paper="paper"
          :show-actions="true"
          :show-preview-image="true"
          @click="viewPaperDetail"
          @open-url="openPaperUrl"
          @download="downloadPaper"
        />
      </div>

      <!-- 空狀態 -->
      <div v-else class="empty-state">
        <n-empty :description="$t('papers.empty')" />
      </div>

      <!-- 分頁 -->
      <div v-if="pagination.total > 0" class="pagination-section">
        <n-pagination
          v-model:page="pagination.page"
          :page-count="pagination.pages"
          :page-size="pagination.per_page"
          :item-count="pagination.total"
          :show-size-picker="false"
          :show-quick-jumper="true"
          @update:page="onPageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { NConfigProvider, zhCN, enUS, dateZhCN, dateEnUS } from 'naive-ui';
import SearchComponent from '@/components/SearchComponent.vue';
import PaperCard from '@/components/PaperCard.vue';
import { paperApi } from '@/services/api';
import { getMediaUrl } from '@/utils/media';
import { stripMarkdown } from '@/utils/text';
import type { Paper, SearchFilters, PaperAuthor, ApiError } from '@/types/api';

const { t, locale } = useI18n();
const router = useRouter();

// 響應式數據
const paperList = ref<Paper[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const currentFilters = ref<SearchFilters>({});
const pagination = ref({
  page: 1,
  per_page: 12,
  total: 0,
  pages: 0
});

// 搜索配置
const searchConfig = computed(() => ({
  type: 'papers' as const,
  placeholder: t('papers.searchPlaceholder', 'Search papers...'),
  filters: [
    {
      key: 'paper_type',
      label: t('papers.filterByType', 'Filter by Type'),
      type: 'select',
      options: [
        { label: t('papers.types.conference'), value: 0 },
        { label: t('papers.types.journal'), value: 1 },
        { label: t('papers.types.patent'), value: 2 },
        { label: t('papers.types.book'), value: 3 },
        { label: t('papers.types.other'), value: 4 }
      ]
    },
    {
      key: 'paper_accept',
      label: t('papers.filterByStatus', 'Filter by Status'),
      type: 'select',
      options: [
        { label: t('papers.submitted'), value: 0 },
        { label: t('papers.accepted'), value: 1 }
      ]
    }
  ],
  dateRange: true,
  sorting: true,
  sortFields: [
    { value: 'paper_date', label: 'papers.date' },
    { value: 'paper_title_zh', label: 'papers.title' },
    { value: 'paper_venue', label: 'papers.venue' }
  ]
}));

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

// 方法
const fetchPapers = async (params: any = {}) => {
  try {
    loading.value = true;
    error.value = null;
    
    const queryParams = {
      page: pagination.value.page,
      per_page: pagination.value.per_page,
      sort_by: 'paper_date',
      order: 'desc',
      ...params
    };
    
    const response = await paperApi.getPapers(queryParams);
    if (response.code === 0) {
      paperList.value = response.data.items;
      pagination.value = {
        page: response.data.page || 1,
        per_page: response.data.per_page || 12,
        total: response.data.total || 0,
        pages: response.data.pages || 0
      };
    } else {
      error.value = response.message;
    }
  } catch (err: unknown) {
    console.error('Failed to fetch papers:', err);
    const apiError = err as ApiError;
    error.value = apiError?.message || t('papers.fetchError');
  } finally {
    loading.value = false;
  }
};

const handleSearch = (filters: SearchFilters) => {
  currentFilters.value = filters;
  pagination.value.page = 1;
  fetchPapers(filters);
};

const onPageChange = (page: number) => {
  pagination.value.page = page;
  fetchPapers(currentFilters.value);
};

const viewPaperDetail = (paper: Paper) => {
  router.push(`/paper/${paper.paper_id}`);
};

const openPaperUrl = (url: string) => {
  window.open(url, '_blank');
};

const downloadPaper = (paper: Paper) => {
  if (paper.paper_file_path) {
    const downloadUrl = getMediaUrl(paper.paper_file_path);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = `${paper.paper_title_zh || paper.paper_title_en || 'paper'}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};

// 生命週期
onMounted(() => {
  fetchPapers();
});
</script>

<style scoped>
.paper-view {
  padding: 1.5rem;
  min-width: 60rem;
  max-width: 87.5rem;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
  background: linear-gradient(135deg, #1890ff 0%, #722ed1 100%);
  border-radius: 12px;
  color: white;
}

.header-content {
  max-width: 600px;
  margin: 0 auto;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-description {
  font-size: 1.125rem;
  margin: 0;
  opacity: 0.9;
  line-height: 1.6;
}

/* 骨架屏 */
.paper-skeleton {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.paper-item-skeleton {
  padding: 1.5rem;
  border-radius: 0.75rem;
  background: #fff;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.08);
  border: 0.0625rem solid rgba(0, 0, 0, 0.06);
}

.skeleton-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* 錯誤狀態 */
.error-state {
  text-align: center;
  padding: 3rem 1.5rem;
}

/* 論文內容 */
.paper-content {
  margin-top: 1.5rem;
}

.paper-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* 分頁 */
.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 0.0625rem solid #f0f0f0;
}

/* 空狀態 */
.empty-state {
  text-align: center;
  padding: 5rem 1.5rem;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .paper-view {
    min-width: auto;
    padding: 1rem;
  }
  
  .page-header {
    margin-bottom: 2rem;
    padding: 1.5rem 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-description {
    font-size: 1rem;
  }
  
  .paper-list {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .page-header {
    margin-bottom: 1.5rem;
    padding: 1rem 0.5rem;
    border-radius: 8px;
  }
  
  .page-title {
    font-size: 1.75rem;
  }
  
  .page-description {
    font-size: 1rem;
  }
}
</style>