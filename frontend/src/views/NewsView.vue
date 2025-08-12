<template>
  <div class="news-view">
    <div class="news-header">
      <h1 class="page-title">{{ $t('nav.news') }}</h1>
      <p class="page-description">{{ $t('news.description') }}</p>
    </div>

    <!-- 搜索組件 -->
    <SearchComponent
      :config="searchConfig"
      :filters="currentFilters"
      @search="handleSearch"
    />

    <!-- 加載狀態 -->
    <div v-if="loading" class="news-skeleton">
      <div v-for="i in 6" :key="i" class="news-item-skeleton">
        <div class="skeleton-header">
          <n-skeleton text height="1.25rem" width="70%" />
          <n-skeleton text height="0.875rem" width="30%" style="margin-top: 0.5rem" />
        </div>
        <n-skeleton text height="1rem" width="100%" :repeat="3" style="margin-top: 1rem" />
      </div>
    </div>

    <!-- 錯誤狀態 -->
    <div v-else-if="error" class="error-state">
      <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 1rem;">
        {{ error }}
      </n-alert>
      <n-button @click="fetchNews" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 新聞列表 -->
    <div v-else class="news-content">
      <div v-if="newsList.length > 0" class="news-list">
        <div v-for="news in newsList" :key="news.news_id" class="news-item" @click="viewNewsDetail(news)">
          <div class="news-meta">
            <n-tag :type="getNewsTypeColor(news.news_type)" size="small">
              {{ getNewsTypeText(news.news_type) }}
            </n-tag>
            <span class="news-date">{{ formatDate(news.news_date) }}</span>
          </div>
          <div class="news-content-text">
            <h3 class="news-title">
              {{ stripMarkdown(getCurrentLocale() === 'zh' ? news.news_content_zh : (news.news_content_en || news.news_content_zh)) }}
            </h3>
          </div>
          <div class="news-actions">
            <n-button size="small" type="primary" ghost>
              {{ $t('common.viewDetails') }}
            </n-button>
          </div>
        </div>
      </div>

      <!-- 空狀態 -->
      <div v-else class="empty-state">
        <n-empty :description="$t('news.empty')" />
      </div>

      <!-- 分頁 -->
      <div v-if="pagination && pagination.pages > 1" class="pagination-wrapper">
        <n-config-provider :locale="naiveLocale" :date-locale="dateLocale">
          <n-pagination
            v-model:page="currentPage"
            :page-count="pagination.pages"
            :page-size="pagination.per_page"
            :item-count="pagination.total"
            show-size-picker
            :page-sizes="[10, 20, 50]"
            show-quick-jumper
            @update:page="handlePageChange"
            @update:page-size="handlePageSizeChange"
          />
        </n-config-provider>
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
import { newsApi } from '@/services/api';
import { stripMarkdown } from '@/utils/text';
import type { News, SearchFilters } from '@/types/api';

const { t, locale } = useI18n();
const router = useRouter();

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
const error = ref<string | null>(null);
const currentPage = ref(1);
const currentPageSize = ref(10);
const pagination = ref<{
  total: number;
  page: number;
  per_page: number;
  pages: number;
  has_prev: boolean;
  has_next: boolean;
} | null>(null);

// 搜索配置
const searchConfig = {
  type: 'news' as const,
  dateRange: true,
  sorting: true,
  sortFields: [
    { value: 'news_date', label: 'news.date' }
  ]
};

// 當前搜索過濾器
const currentFilters = ref<SearchFilters>({
  q: '',
  sort_by: 'news_date',
  order: 'desc'
});

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

// 獲取新聞類型顏色
const getNewsTypeColor = (type: number) => {
  const colorMap = {
    0: 'info',     // 論文發表
    1: 'success',  // 獲獎消息
    2: 'warning'   // 學術活動
  };
  return colorMap[type as keyof typeof colorMap] || 'default';
};

// 獲取新聞類型文本
const getNewsTypeText = (type: number) => {
  const textMap = {
    0: t('news.paperPublished'),
    1: t('news.award'),
    2: t('news.academic')
  };
  return textMap[type as keyof typeof textMap] || t('news.other');
};

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString(getCurrentLocale() === 'zh' ? 'zh-CN' : 'en-US');
};

// 獲取新聞數據
const fetchNews = async (resetPage = false) => {
  try {
    loading.value = true;
    error.value = null;

    if (resetPage) {
      currentPage.value = 1;
    }

    const params = {
      page: currentPage.value,
      per_page: currentPageSize.value,
      q: currentFilters.value.q,
      news_type: currentFilters.value.news_type,
      start_date: currentFilters.value.start_date,
      end_date: currentFilters.value.end_date
    };

    // 移除空值
    Object.keys(params).forEach(key => {
      if (params[key as keyof typeof params] === '' || params[key as keyof typeof params] === null || params[key as keyof typeof params] === undefined) {
        delete params[key as keyof typeof params];
      }
    });

    const response = await newsApi.getNews(params);
    if (response.code === 0) {
      newsList.value = response.data.items;
      
      // 處理分頁信息
      if ('total' in response.data) {
        pagination.value = {
          total: response.data.total,
          page: response.data.page || currentPage.value,
          per_page: response.data.per_page || currentPageSize.value,
          pages: response.data.pages || Math.ceil(response.data.total / (response.data.per_page || currentPageSize.value)),
          has_prev: response.data.has_prev || false,
          has_next: response.data.has_next || false
        };
      } else {
        // 獲取所有數據的情況
        pagination.value = null;
      }
    } else {
      error.value = response.message || t('common.fetchError');
    }
  } catch (err) {
    console.error('Failed to fetch news:', err);
    error.value = t('common.networkError');
  } finally {
    loading.value = false;
  }
};

// 搜索處理
const handleSearch = (filters: SearchFilters) => {
  currentFilters.value = { ...filters };
  fetchNews(true);
};

// 頁面變化處理
const handlePageChange = (page: number) => {
  currentPage.value = page;
  fetchNews();
};

// 每頁數量變化處理
const handlePageSizeChange = (pageSize: number) => {
  currentPageSize.value = pageSize;
  currentPage.value = 1;
  fetchNews();
};

// 查看新聞詳情
const viewNewsDetail = (news: News) => {
  router.push(`/news/${news.news_id}`);
};

// 生命週期
onMounted(() => {
  fetchNews();
});
</script>

<style scoped>
.news-view {
  padding: 1.5rem;
  min-width: 60rem;
  max-width: 87.5rem;
  margin: 0 auto;
}

/* 頁面頭部 */
.news-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-description {
  font-size: 1.125rem;
  color: #666;
  margin: 0;
  line-height: 1.6;
}

/* 骨架屏 */
.news-skeleton {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.news-item-skeleton {
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

/* 錯誤和空狀態 */
.error-state,
.empty-state {
  text-align: center;
  padding: 3rem 1.25rem;
}

/* 新聞列表 */
.news-content {
  margin-top: 1.5rem;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.news-item {
  padding: 1.5rem;
  border-radius: 0.75rem;
  background: #fff;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.08);
  border: 0.0625rem solid rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  cursor: pointer;
  border-left: 0.25rem solid transparent;
}

.news-item:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.12);
  border-left-color: #1890ff;
}

.news-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.news-date {
  font-size: 0.875rem;
  color: #888;
  font-weight: 500;
}

.news-content-text {
  margin-bottom: 1rem;
}

.news-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.news-actions {
  display: flex;
  justify-content: flex-end;
}

/* 分頁 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 0.0625rem solid rgba(0, 0, 0, 0.06);
}

/* 暗色主題 */
[data-theme="dark"] .news-view,
.dark .news-view,
.dark-mode .news-view {
  color: #fff;
}

[data-theme="dark"] .page-description,
.dark .page-description,
.dark-mode .page-description {
  color: #ccc;
}

[data-theme="dark"] .news-item,
[data-theme="dark"] .news-item-skeleton,
.dark .news-item,
.dark .news-item-skeleton,
.dark-mode .news-item,
.dark-mode .news-item-skeleton {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.2);
}

[data-theme="dark"] .news-item:hover,
.dark .news-item:hover,
.dark-mode .news-item:hover {
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.3);
  border-left-color: #70a1ff;
}

[data-theme="dark"] .news-title,
.dark .news-title,
.dark-mode .news-title {
  color: #fff;
}

[data-theme="dark"] .news-date,
.dark .news-date,
.dark-mode .news-date {
  color: #bbb;
}

[data-theme="dark"] .pagination-wrapper,
.dark .pagination-wrapper,
.dark-mode .pagination-wrapper {
  border-top-color: rgba(255, 255, 255, 0.1);
}

/* 響應式設計 */
@media (max-width: 48rem) {
  .news-view {
    padding: 1rem;
    min-width: unset;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-description {
    font-size: 1rem;
  }
  
  .news-item {
    padding: 1rem;
  }
  
  .news-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .news-title {
    font-size: 1rem;
  }
}
</style>