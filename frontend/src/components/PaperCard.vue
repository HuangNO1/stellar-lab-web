<template>
  <div class="paper-card" :class="{ compact }" @click="onCardClick">
    <div class="paper-content">
      <!-- 預覽圖片（左側顯示，如果有的話） -->
      <div v-if="showPreviewImage && paper.preview_img && !compact" class="paper-preview">
        <img 
          :src="getPreviewImageUrl(paper.preview_img)" 
          :alt="displayTitle"
          class="preview-image"
          @error="onImageError"
        />
      </div>
      
      <!-- 論文信息區域 -->
      <div class="paper-info">
        <!-- 論文頭部信息 -->
        <div class="paper-header">
          <div class="paper-title-section">
            <h3 class="paper-title">{{ displayTitle }}</h3>
            <div class="paper-meta-tags">
              <n-tag :type="getPaperTypeColor(paper.paper_type)" size="small">
                {{ getPaperTypeText(paper.paper_type) }}
              </n-tag>
              <n-tag :type="getPaperStatusColor(paper.paper_accept)" size="small">
                {{ getPaperStatusText(paper.paper_accept) }}
              </n-tag>
            </div>
          </div>
        </div>
      
      <!-- 論文詳細信息 -->
      <div class="paper-details">
        <!-- 發表場地 -->
        <div v-if="paper.paper_venue" class="paper-venue">
          <n-icon size="14" class="detail-icon">
            <svg viewBox="0 0 24 24">
              <path fill="currentColor" d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z"/>
            </svg>
          </n-icon>
          {{ paper.paper_venue }}
        </div>
        
        <!-- 發表日期 -->
        <div v-if="paper.paper_date" class="paper-date">
          <n-icon size="14" class="detail-icon">
            <svg viewBox="0 0 24 24">
              <path fill="currentColor" d="M19,3H18V1H16V3H8V1H6V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3M19,19H5V8H19V19Z"/>
            </svg>
          </n-icon>
          {{ formatDate(paper.paper_date) }}
        </div>
        
        <!-- 作者信息 -->
        <div class="paper-authors-section">
          <!-- 統一的作者顯示 -->
          <div class="paper-authors">
            <n-icon size="14" class="detail-icon">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M16,4C16.88,4 17.67,4.39 18.11,5.17L20.83,10.83C20.94,11.06 21,11.32 21,11.58V13A2,2 0 0,1 19,15H18V19A2,2 0 0,1 16,21H8A2,2 0 0,1 6,19V15H5A2,2 0 0,1 3,13V11.58C3,11.32 3.06,11.06 3.17,10.83L5.89,5.17C6.33,4.39 7.12,4 8,4H16M16,6H8L5.5,11H8.5V13H15.5V11H18.5L16,6M8,15V19H16V15H8Z"/>
              </svg>
            </n-icon>
            <span class="author-label">{{ getAuthorLabel() }}:</span>
            <span class="author-names">{{ getAuthorContent() }}</span>
          </div>
        </div>
        
        <!-- 論文描述 -->
        <div v-if="displayDescription" class="paper-description">
          {{ stripMarkdown(displayDescription) }}
        </div>
      </div>

      <!-- 操作按鈕 -->
      <div v-if="showActions && (paper.paper_url || paper.paper_file_path)" class="paper-actions">
        <n-button v-if="paper.paper_url" size="small" type="info" ghost @click.stop="openPaperUrl(paper.paper_url)">
          <template #icon>
            <n-icon size="14">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('papers.viewOnline') }}
        </n-button>
        <n-button v-if="paper.paper_file_path" size="small" type="primary" ghost @click.stop="downloadPaper(paper)">
          <template #icon>
            <n-icon size="14">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('papers.download') }}
        </n-button>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { getMediaUrl } from '@/utils/media';
import type { Paper } from '@/types/api';

interface Props {
  paper: Paper;
  showActions?: boolean;
  showPreviewImage?: boolean;
  compact?: boolean;
}

interface Emits {
  (e: 'click', paper: Paper): void;
  (e: 'openUrl', url: string): void;
  (e: 'download', paper: Paper): void;
}

const props = withDefaults(defineProps<Props>(), {
  showActions: false,
  showPreviewImage: true,
  compact: false
});

const emit = defineEmits<Emits>();

const { locale, t } = useI18n();
const imageError = ref(false);

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

// 顯示的標題
const displayTitle = computed(() => {
  return getCurrentLocale() === 'zh' ? 
    props.paper.paper_title_zh : 
    (props.paper.paper_title_en || props.paper.paper_title_zh);
});

// 顯示的描述
const displayDescription = computed(() => {
  if (!props.paper.paper_desc_zh && !props.paper.paper_desc_en) return '';
  return getCurrentLocale() === 'zh' ? 
    props.paper.paper_desc_zh : 
    (props.paper.paper_desc_en || props.paper.paper_desc_zh);
});

// 檢查是否有任何作者信息
const hasAnyAuthors = computed(() => {
  return hasLabAuthors.value || hasAllAuthors.value;
});

// 檢查是否有實驗室作者
const hasLabAuthors = computed(() => {
  return props.paper.authors && props.paper.authors.length > 0;
});

// 檢查是否有全部作者文本（非空）
const hasAllAuthors = computed(() => {
  const allAuthorsZh = props.paper.all_authors_zh;
  const allAuthorsEn = props.paper.all_authors_en;
  
  if (!allAuthorsZh && !allAuthorsEn) return false;
  
  const currentText = getCurrentLocale() === 'zh' ? allAuthorsZh : allAuthorsEn;
  const fallbackText = getCurrentLocale() === 'zh' ? allAuthorsEn : allAuthorsZh;
  const hasAllAuthorsText = currentText || fallbackText;
  
  return hasAllAuthorsText && hasAllAuthorsText.trim() !== '';
});

// 獲取作者標籤
const getAuthorLabel = () => {
  if (hasAllAuthors.value) {
    return t('papers.allAuthors');
  } else if (hasLabAuthors.value) {
    return t('papers.authors');
  } else {
    return t('papers.authors');
  }
};

// 獲取作者內容
const getAuthorContent = () => {
  if (hasAllAuthors.value) {
    return getAllAuthorsText();
  } else if (hasLabAuthors.value) {
    return getAuthorsText(props.paper.authors || []);
  } else {
    return t('common.none');
  }
};

// 獲取預覽圖片URL
const getPreviewImageUrl = (imagePath: string) => {
  if (imageError.value) return '';
  if (!imagePath) return '';
  return getMediaUrl(imagePath);
};

// 圖片加載錯誤處理
const onImageError = () => {
  imageError.value = true;
};

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString(getCurrentLocale() === 'zh' ? 'zh-CN' : 'en-US');
};

// 去除Markdown語法的簡單實現
const stripMarkdown = (text: string) => {
  if (!text) return '';
  return text
    .replace(/[#*_`~]/g, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .substring(0, props.compact ? 100 : 200) + (text.length > (props.compact ? 100 : 200) ? '...' : '');
};

// 獲取論文類型顏色
const getPaperTypeColor = (type: number) => {
  const colorMap: Record<number, string> = {
    0: 'info',     // conference
    1: 'success',  // journal
    2: 'warning',  // patent
    3: 'default',  // book
    4: 'default'   // other
  };
  return colorMap[type] || 'default';
};

// 獲取論文類型文本
const getPaperTypeText = (type: number) => {
  const typeMap: Record<number, string> = {
    0: 'conference',
    1: 'journal', 
    2: 'patent',
    3: 'book',
    4: 'other'
  };
  const typeKey = typeMap[type] || 'other';
  return t(`papers.types.${typeKey}`);
};

// 獲取論文狀態顏色
const getPaperStatusColor = (accept: number) => {
  return accept === 1 ? 'success' : 'warning';
};

// 獲取論文狀態文本
const getPaperStatusText = (accept: number) => {
  return accept === 1 ? t('papers.accepted') : t('papers.submitted');
};

// 獲取作者文本
const getAuthorsText = (authors: any[]) => {
  if (!authors || authors.length === 0) return '';
  const locale = getCurrentLocale();
  const authorNames = authors.map(author => 
    locale === 'zh' ? author.member?.mem_name_zh : author.member?.mem_name_en
  ).filter(Boolean);
  
  if (authorNames.length <= 3) {
    return authorNames.join(', ');
  } else {
    return authorNames.slice(0, 3).join(', ') + ' ' + t('papers.andOthers');
  }
};

// 獲取全部作者文本
const getAllAuthorsText = () => {
  return getCurrentLocale() === 'zh' ? 
    (props.paper.all_authors_zh || props.paper.all_authors_en) : 
    (props.paper.all_authors_en || props.paper.all_authors_zh);
};

// 事件處理
const onCardClick = () => {
  emit('click', props.paper);
};

const openPaperUrl = (url: string) => {
  emit('openUrl', url);
};

const downloadPaper = (paper: Paper) => {
  emit('download', paper);
};
</script>

<style scoped>
.paper-card {
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.08);
  border: 0.0625rem solid rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  cursor: pointer;
  margin-bottom: 1.5rem;
  border-left: 0.25rem solid transparent;
}

.paper-card:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.12);
  border-left-color: #1890ff;
}

.paper-content {
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
}

/* 頭部區域 */
.paper-header {
  margin-bottom: 1rem;
}

.paper-title-section {
}

.paper-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  color: #333;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.paper-meta-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* 預覽圖片 */
.paper-preview {
  width: 20rem;
  height: auto;
  border-radius: 0.5rem;
  overflow: hidden;
  background: #f5f5f5;
  flex-shrink: 0;
}

/* 論文信息區域 */
.paper-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.paper-card:hover .preview-image {
  transform: scale(1.05);
}

/* 詳細信息區域 */
.paper-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.paper-venue,
.paper-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  line-height: 1.5;
}

.paper-venue {
  color: #1890ff;
  font-weight: 500;
}

.detail-icon {
  color: #999;
  flex-shrink: 0;
}

/* 作者區域 */
.paper-authors-section {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.paper-authors {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.875rem;
  line-height: 1.5;
}

.paper-authors.lab-authors {
  color: #1890ff;
}

.paper-authors.all-authors {
  color: #666;
}

.author-label {
  font-weight: 500;
  flex-shrink: 0;
}

.author-names {
  flex: 1;
  min-width: 0;
}

/* 描述 */
.paper-description {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 操作按鈕 */
.paper-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  padding-top: 1rem;
  border-top: 0.0625rem solid #f0f0f0;
}

/* 緊湊模式 */
.paper-card.compact .paper-content {
  padding: 1rem;
}

.paper-card.compact .paper-title {
  font-size: 1rem;
  -webkit-line-clamp: 1;
}

.paper-card.compact .paper-description {
  -webkit-line-clamp: 1;
}

.paper-card.compact .paper-preview {
  width: 10rem;
  height: auto;
}

.paper-card.compact .paper-details {
  gap: 0.25rem;
}

/* 暗色主題支持 */
[data-theme="dark"] .paper-card,
.dark .paper-card,
.dark-mode .paper-card {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.2);
}

[data-theme="dark"] .paper-card:hover,
.dark .paper-card:hover,
.dark-mode .paper-card:hover {
  background: rgba(255, 255, 255, 0.12);
  border-left-color: #70a1ff;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .paper-title,
.dark .paper-title,
.dark-mode .paper-title {
  color: #fff;
}

[data-theme="dark"] .paper-venue,
.dark .paper-venue,
.dark-mode .paper-venue {
  color: #70a1ff;
}

[data-theme="dark"] .paper-date,
[data-theme="dark"] .paper-authors.all-authors,
[data-theme="dark"] .paper-description,
.dark .paper-date,
.dark .paper-authors.all-authors,
.dark .paper-description,
.dark-mode .paper-date,
.dark-mode .paper-authors.all-authors,
.dark-mode .paper-description {
  color: #ccc;
}

[data-theme="dark"] .paper-authors.lab-authors,
.dark .paper-authors.lab-authors,
.dark-mode .paper-authors.lab-authors {
  color: #70a1ff;
}

[data-theme="dark"] .detail-icon,
.dark .detail-icon,
.dark-mode .detail-icon {
  color: #aaa;
}

[data-theme="dark"] .paper-actions,
.dark .paper-actions,
.dark-mode .paper-actions {
  border-top-color: rgba(255, 255, 255, 0.1);
}

/* 響應式設計 */
@media (max-width: 768px) {
  .paper-content {
    padding: 1.25rem;
    flex-direction: row;
    align-items: flex-start;
  }
  
  .paper-preview {
    width: 15rem;
    height: auto;
  }
  
  .paper-title {
    font-size: 1.125rem;
  }
  
  .paper-authors {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .author-label {
    font-size: 0.75rem;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
}

@media (max-width: 640px) {
  .paper-content {
    padding: 1rem;
  }
  
  .paper-preview {
    width: 12rem;
    height: auto;
  }
  
  .paper-title {
    font-size: 1rem;
  }
  
  .paper-actions {
    flex-direction: column;
  }
}
</style>