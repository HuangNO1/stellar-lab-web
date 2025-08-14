<template>
  <div class="news-detail-view">
    <!-- 加載狀態 -->
    <template v-if="loading">
      <div class="news-detail-skeleton">
        <div class="detail-header-skeleton">
          <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
            <n-skeleton text height="1.5rem" width="4rem" />
            <n-skeleton text height="1.5rem" width="6rem" />
          </div>
          <n-skeleton text height="2rem" width="90%" style="margin-bottom: 1rem" />
        </div>
        <div class="detail-content-skeleton">
          <n-skeleton text height="1rem" width="100%" :repeat="8" />
        </div>
        <div class="detail-actions-skeleton" style="margin-top: 2rem;">
          <n-skeleton text height="2rem" width="5rem" />
        </div>
      </div>
    </template>

    <!-- 錯誤狀態 -->
    <div v-else-if="error" class="error-state">
      <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 16px;">
        {{ error }}
      </n-alert>
      <n-button @click="fetchNewsDetail" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 新聞詳情 -->
    <div v-else-if="news" class="news-detail-content">
      <!-- 返回按鈕 -->
      <div class="back-button-section">
        <n-button @click="goBack" ghost size="large">
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('common.back') }}
        </n-button>
      </div>
      
      <div class="news-header">
        <!-- 新聞標題 -->
        <h1 v-if="news.news_title_zh || news.news_title_en" class="news-title">
          {{ getCurrentLocale() === 'zh' ? (news.news_title_zh || news.news_title_en) : (news.news_title_en || news.news_title_zh) }}
        </h1>
        
        <div class="news-meta">
          <n-tag :type="getNewsTypeColor(news.news_type)" size="medium">
            {{ getNewsTypeText(news.news_type) }}
          </n-tag>
          <span class="news-date">
            <n-icon size="16" style="margin-right: 0.5rem;">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,3H18V1H16V3H8V1H6V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3M19,19H5V8H19V19Z"/>
              </svg>
            </n-icon>
            {{ formatDate(news.news_date) }}
          </span>
        </div>
      </div>

      <!-- 新聞內容 -->
      <div class="news-content">
        <markdown-it :source="getNewsContent()" :plugins="markdownPlugins"></markdown-it>
      </div>
    </div>

    <!-- 沒有找到新聞 -->
    <div v-else class="not-found-state">
      <n-empty :description="$t('news.notFound')" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { newsApi } from '@/services/api';
import { processMarkdownImageUrls } from '@/utils/media';
import { createMarkdownPlugins } from '@/utils/markdown';
import type { News, ApiError } from '@/types/api';
import MarkdownIt from 'vue3-markdown-it';

const route = useRoute();
const router = useRouter();
const { t, locale } = useI18n();

// 響應式數據
const news = ref<News | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

// 計算屬性
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

const getNewsContent = () => {
  if (!news.value) return '';
  const content = getCurrentLocale() === 'zh' ? news.value.news_content_zh : news.value.news_content_en;
  return content ? processMarkdownImageUrls(content) : '';
};

// Markdown插件配置
const markdownPlugins = createMarkdownPlugins();

// 方法
const fetchNewsDetail = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const newsId = parseInt(route.params.id as string);
    if (isNaN(newsId)) {
      error.value = t('news.invalidId');
      return;
    }

    const response = await newsApi.getNewsItem(newsId);
    if (response.code === 0) {
      news.value = response.data;
    } else {
      error.value = response.message;
    }
  } catch (err: unknown) {
    console.error('Failed to fetch news detail:', err);
    const apiError = err as ApiError;
    error.value = apiError?.message || t('news.fetchError');
  } finally {
    loading.value = false;
  }
};

const getNewsTypeColor = (type: number) => {
  const colors = ['info', 'success', 'warning'];
  return colors[type] || 'default';
};

const getNewsTypeText = (type: number) => {
  const types = [
    'news.types.publication',
    'news.types.award',
    'news.types.activity'
  ];
  return t(types[type] || types[0]);
};

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString(getCurrentLocale() === 'zh' ? 'zh-CN' : 'en-US');
};

const goBack = () => {
  router.back();
};

// 生命週期
onMounted(() => {
  fetchNewsDetail();
});
</script>

<style scoped>
.news-detail-view {
  padding: 0.5rem 1rem;
  max-width: 160rem;
  min-width: 20rem;
  margin: 0 auto;
  width: 100%;
}

.news-detail-skeleton,
.news-detail-content {
  width: 100%;
}

.error-state,
.not-found-state {
  text-align: center;
  padding: 5rem 1.25rem;
}

/* 返回按鈕區域 */
.back-button-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.news-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e0e0e0;
}

.news-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}

.news-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.news-date {
  display: flex;
  align-items: center;
  font-size: 1rem;
  color: #666;
}

.news-content {
  margin-bottom: 2rem;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 0.75rem;
  border-left: 4px solid #1890ff;
  font-size: 1.1rem;
  line-height: 1.8;
}

/* 暗色主題支持 */
[data-theme="dark"] .back-button-section,
.dark .back-button-section {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .news-detail-view,
.dark .news-detail-view {
  color: #fff;
}

[data-theme="dark"] .news-header,
.dark .news-header {
  border-bottom-color: #3c3c41;
}

[data-theme="dark"] .news-date,
.dark .news-date {
  color: #ccc;
}

[data-theme="dark"] .news-content,
.dark .news-content {
  background: rgba(255, 255, 255, 0.08);
  border-left-color: #70a1ff;
  color: #fff;
}

/* 響應式設計 */
@media (max-width: 48rem) {
  .news-detail-view {
    padding: 1rem;
    min-width: auto;
  }
  
  .news-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .news-content {
    padding: 1.5rem;
    font-size: 1rem;
  }
}
</style>