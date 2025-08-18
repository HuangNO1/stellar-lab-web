<template>
  <div class="paper-detail-view">
    <!-- 加載狀態 -->
    <template v-if="loading">
      <div class="paper-detail-skeleton">
        <div class="detail-header-skeleton">
          <n-skeleton text height="2.5rem" width="90%" style="margin-bottom: 1rem" />
          <n-skeleton text height="1.5rem" width="60%" style="margin-bottom: 0.5rem" />
          <div style="display: flex; gap: 0.5rem; margin-bottom: 1.5rem;">
            <n-skeleton text height="1.5rem" width="4rem" />
            <n-skeleton text height="1.5rem" width="5rem" />
            <n-skeleton text height="1.5rem" width="6rem" />
          </div>
        </div>
        <div class="detail-content-skeleton">
          <n-skeleton text height="1rem" width="100%" :repeat="6" />
        </div>
        <div class="detail-actions-skeleton" style="margin-top: 2rem;">
          <n-skeleton text height="2rem" width="8rem" style="margin-right: 1rem" />
          <n-skeleton text height="2rem" width="6rem" style="margin-right: 1rem" />
          <n-skeleton text height="2rem" width="5rem" />
        </div>
      </div>
    </template>

    <!-- 錯誤狀態 -->
    <div v-else-if="error" class="error-state">
      <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 16px;">
        {{ error }}
      </n-alert>
      <n-button @click="fetchPaperDetail" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 論文詳情 -->
    <div v-else-if="paper" class="paper-detail-content">
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
      
      <div class="paper-header">
        <h1 class="paper-title">
          {{ getCurrentLocale() === 'zh' ? paper.paper_title_zh : (paper.paper_title_en || paper.paper_title_zh) }}
        </h1>
        
        <div v-if="paper.paper_venue" class="paper-venue">
          {{ paper.paper_venue }}
        </div>
        
        <div class="paper-meta">
          <n-tag :type="getPaperTypeColor(paper.paper_type)" size="medium">
            {{ getPaperTypeText(paper.paper_type) }}
          </n-tag>
          <n-tag :type="getPaperStatusColor(paper.paper_accept)" size="medium">
            {{ getPaperStatusText(paper.paper_accept) }}
          </n-tag>
          <span class="paper-date">
            <n-icon size="16" style="margin-right: 0.5rem;">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,3H18V1H16V3H8V1H6V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3M19,19H5V8H19V19Z"/>
              </svg>
            </n-icon>
            {{ formatDate(paper.paper_date) }}
          </span>
        </div>
      </div>

      <!-- 作者信息 -->
      <div class="paper-authors">
        <h3>{{ $t('papers.authors') }}</h3>
        
        <!-- 實驗室作者 -->
        <div v-if="hasLabAuthors()" class="authors-section">
          <h4 class="authors-subtitle">{{ $t('admin.papers.form.labAuthors') }}</h4>
          <div class="authors-list">
            <span 
              v-for="(author, index) in paper.authors" 
              :key="author.mem_id"
              class="author-item"
              :class="{ 'corresponding': author.is_corresponding }"
              @click="toMember(author.mem_id)"
            >
              {{ getCurrentLocale() === 'zh' ? author.member?.mem_name_zh : author.member?.mem_name_en }}
              <sup v-if="author.is_corresponding">*</sup>
              <span v-if="index < paper.authors.length - 1">, </span>
            </span>
          </div>
          <p class="corresponding-note" v-if="hasCorrespondingAuthor()">
            <sup>*</sup> {{ $t('papers.correspondingAuthor') }}
          </p>
        </div>

        <!-- 全部作者 -->
        <div v-if="hasAllAuthors()" class="authors-section">
          <h4 class="authors-subtitle">{{ $t('admin.papers.form.allAuthors') }}</h4>
          <div class="authors-text">
            {{ getCurrentLocale() === 'zh' ? (paper.all_authors_zh || paper.all_authors_en) : (paper.all_authors_en || paper.all_authors_zh) }}
          </div>
        </div>
        
        <!-- 無作者信息時顯示 -->
        <div v-if="!hasLabAuthors() && !hasAllAuthors()" class="authors-section">
          <div class="no-authors">{{ $t('common.none') }}</div>
        </div>
      </div>

      <!-- 論文描述 -->
      <div class="paper-description" v-if="paper.paper_desc_zh || paper.paper_desc_en">
        <h3>{{ $t('papers.abstract') }}</h3>
        <MarkdownRenderer :source="getPaperDescription()" />
      </div>

      <!-- 操作按鈕 -->
      <div class="paper-actions">
        <n-button 
          v-if="paper.paper_url" 
          type="primary" 
          @click="openPaperUrl(paper.paper_url)"
          size="large"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('papers.viewOnline') }}
        </n-button>
        
        <n-button 
          v-if="paper.paper_file_path" 
          type="info" 
          @click="downloadPaper()"
          size="large"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('papers.download') }}
        </n-button>
      </div>
    </div>

    <!-- 沒有找到論文 -->
    <div v-else class="not-found-state">
      <n-empty :description="$t('papers.notFound')" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { paperApi } from '@/services/api';
import { getMediaUrl, processMarkdownImageUrls } from '@/utils/media';
import MarkdownRenderer from '@/components/MarkdownRenderer.vue';
import type { Paper, ApiError } from '@/types/api';

const route = useRoute();
const router = useRouter();
const { t, locale } = useI18n();

// 響應式數據
const paper = ref<Paper | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

// 計算屬性
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

// 檢查是否有實驗室作者
const hasLabAuthors = () => {
  return paper.value?.authors && paper.value.authors.length > 0;
};

// 檢查是否有全部作者文本（非空）
const hasAllAuthors = () => {
  if (!paper.value) return false;
  
  // 檢查兩個字段是否都為 null 或 undefined
  const allAuthorsZh = paper.value.all_authors_zh;
  const allAuthorsEn = paper.value.all_authors_en;
  
  if (!allAuthorsZh && !allAuthorsEn) return false;
  
  // 選擇當前語言對應的文本
  const currentText = getCurrentLocale() === 'zh' ? allAuthorsZh : allAuthorsEn;
  const fallbackText = getCurrentLocale() === 'zh' ? allAuthorsEn : allAuthorsZh;
  const allAuthorsText = currentText || fallbackText;
  
  // 檢查文本是否存在且不為空
  return allAuthorsText && allAuthorsText.trim() !== '';
};

const getPaperDescription = () => {
  if (!paper.value) return '';
  const desc = getCurrentLocale() === 'zh' ? paper.value.paper_desc_zh : paper.value.paper_desc_en;
  return desc ? processMarkdownImageUrls(desc) : '';
};

// 方法
const fetchPaperDetail = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const paperId = parseInt(route.params.id as string);
    if (isNaN(paperId)) {
      error.value = t('papers.invalidId');
      return;
    }

    const response = await paperApi.getPaper(paperId);
    if (response.code === 0) {
      paper.value = response.data;
    } else {
      error.value = response.message;
    }
  } catch (err: unknown) {
    console.error('Failed to fetch paper detail:', err);
    const apiError = err as ApiError;
    error.value = apiError?.message || t('papers.fetchError');
  } finally {
    loading.value = false;
  }
};

const getPaperTypeColor = (type: number) => {
  const colors = ['info', 'success', 'warning', 'error', 'default'];
  return colors[type] || 'default';
};

const getPaperTypeText = (type: number) => {
  const types = [
    'papers.types.conference',
    'papers.types.journal', 
    'papers.types.patent',
    'papers.types.book',
    'papers.types.other'
  ];
  return t(types[type] || types[4]);
};

const getPaperStatusColor = (accept: number) => {
  return accept === 1 ? 'success' : 'warning';
};

const getPaperStatusText = (accept: number) => {
  return accept === 1 ? t('papers.accepted') : t('papers.submitted');
};

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString(getCurrentLocale() === 'zh' ? 'zh-CN' : 'en-US');
};

const hasCorrespondingAuthor = () => {
  return paper.value?.authors?.some(author => author.is_corresponding === 1) || false;
};

const openPaperUrl = (url: string) => {
  window.open(url, '_blank');
};

const downloadPaper = () => {
  if (paper.value?.paper_file_path) {
    const url = getMediaUrl(paper.value.paper_file_path);
    window.open(url, '_blank');
  }
};

const toMember = (memberId: number) => {
  router.push(`/member/${memberId}`);
};

const goBack = () => {
  router.back();
};

// 生命週期
onMounted(() => {
  fetchPaperDetail();
});
</script>

<style scoped>
.paper-detail-view {
  padding: 0.5rem 1rem;
  max-width: 160rem;
  min-width: 20rem;
  margin: 0 auto;
  width: 100%;
}

.paper-detail-skeleton,
.paper-detail-content {
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

.paper-header {
  margin-bottom: 2rem;
}

.paper-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}

.paper-venue {
  font-size: 1.25rem;
  color: #1890ff;
  font-weight: 600;
  margin-bottom: 1rem;
}

.paper-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.paper-date {
  display: flex;
  align-items: center;
  font-size: 1rem;
  color: #666;
}

.paper-authors {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f0f8ff;
  border-radius: 0.75rem;
  border-left: 4px solid #1890ff;
}

.paper-authors h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #333;
}

.authors-section {
  margin-bottom: 1.5rem;
}

.authors-section:last-child {
  margin-bottom: 0;
}

.authors-subtitle {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  color: #1890ff;
  border-bottom: 2px solid #e0f2ff;
  padding-bottom: 0.25rem;
}

.authors-list,
.authors-text {
  font-size: 1.1rem;
  line-height: 1.6;
}

.author-item {
  cursor: pointer;
  color: #1890ff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.author-item:hover {
  color: #40a9ff;
  text-decoration: underline;
}

.author-item.corresponding {
  font-weight: 600;
}

.corresponding-note {
  font-size: 0.875rem;
  color: #666;
  margin: 0.5rem 0 0 0;
  font-style: italic;
}

.no-authors {
  font-size: 1.1rem;
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}

.paper-description {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 0.75rem;
  border-left: 4px solid #1890ff;
}

.paper-description h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #333;
}

.paper-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* 暗色主題支持 */
[data-theme="dark"] .back-button-section,
.dark .back-button-section {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .paper-detail-view,
.dark .paper-detail-view {
  color: #fff;
}

[data-theme="dark"] .paper-venue,
.dark .paper-venue {
  color: #70a1ff;
}

[data-theme="dark"] .paper-date,
.dark .paper-date {
  color: #ccc;
}

[data-theme="dark"] .paper-authors,
.dark .paper-authors,
.dark-mode .paper-authors {
  background: rgb(24, 24, 28);
  border-left-color: #70a1ff;
  color: #fff;
}

[data-theme="dark"] .paper-description,
.dark .paper-description,
.dark-mode .paper-description {
  background: rgb(24, 24, 28);
  border-left-color: #70a1ff;
  color: #fff;
}

[data-theme="dark"] .paper-authors h3,
[data-theme="dark"] .paper-description h3,
.dark .paper-authors h3,
.dark .paper-description h3,
.dark-mode .paper-authors h3,
.dark-mode .paper-description h3 {
  color: #fff;
}

[data-theme="dark"] .authors-subtitle,
.dark .authors-subtitle,
.dark-mode .authors-subtitle {
  color: #70a1ff;
  border-bottom-color: rgba(112, 161, 255, 0.3);
}

[data-theme="dark"] .author-item,
.dark .author-item,
.dark-mode .author-item {
  color: #70a1ff;
}

[data-theme="dark"] .author-item:hover,
.dark .author-item:hover,
.dark-mode .author-item:hover {
  color: #91caff;
}

[data-theme="dark"] .corresponding-note,
.dark .corresponding-note,
.dark-mode .corresponding-note {
  color: #ccc;
}

[data-theme="dark"] .no-authors,
.dark .no-authors,
.dark-mode .no-authors {
  color: #aaa;
}

/* 響應式設計 */
@media (max-width: 48rem) {
  .paper-detail-view {
    padding: 1rem;
    min-width: auto;
  }
  
  .paper-title {
    font-size: 2rem;
  }
  
  .paper-venue {
    font-size: 1.125rem;
  }
  
  .paper-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .paper-actions {
    flex-direction: column;
  }
  
  .paper-actions .n-button {
    width: 100%;
    justify-content: center;
  }
}
</style>