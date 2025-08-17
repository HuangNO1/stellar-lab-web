<template>
  <div class="papers-list-container">
    <span class="papers-list-label">{{ $t('members.relatedPapers', '相關論文') }}：</span>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="papers-list-loading">
      <div class="loading-spinner"></div>
      <span>{{ $t('common.loading', '載入論文資訊中...') }}</span>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="papers-list-error">
      <span>{{ error }}</span>
    </div>
    
    <!-- 论文列表 -->
    <div v-else-if="papers.length > 0" class="papers-list-content">
      <div 
        v-for="paper in papers" 
        :key="paper.paper_id"
        class="papers-list-item"
        @click="handlePaperClick(paper)"
      >
        <div class="papers-list-item-title">{{ getPaperTitle(paper) }}</div>
        <div v-if="paper.paper_venue" class="papers-list-item-venue">{{ paper.paper_venue }}</div>
        <div v-if="paper.paper_date" class="papers-list-item-date">{{ getPaperYear(paper.paper_date) }}</div>
      </div>
    </div>
    
    <!-- 无数据状态 -->
    <div v-else class="papers-list-empty">
      <span>{{ $t('members.noPapersAvailable', '無可用論文資訊') }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { paperApi } from '@/services/api';
import type { Paper } from '@/types/api';

// Props
interface Props {
  paperIds: number[];
}

const props = defineProps<Props>();
const { locale, t } = useI18n();
const router = useRouter();

// 响应式数据
const papers = ref<Paper[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// 计算属性
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

const getPaperTitle = (paper: Paper) => {
  return getCurrentLocale() === 'zh' ? paper.paper_title_zh : paper.paper_title_en;
};

const getPaperYear = (dateStr: string) => {
  return new Date(dateStr).getFullYear();
};

// 方法
const handlePaperClick = (paper: Paper) => {
  router.push(`/paper/${paper.paper_id}`);
};

const loadPapers = async () => {
  if (props.paperIds.length === 0) return;
  
  try {
    loading.value = true;
    error.value = null;
    
    const paperPromises = props.paperIds.map(async (id) => {
      try {
        const response = await paperApi.getPaper(id);
        return response.code === 0 ? response.data : null;
      } catch (err) {
        console.warn(`Failed to load paper ${id}:`, err);
        return null;
      }
    });
    
    const results = await Promise.all(paperPromises);
    papers.value = results.filter(paper => paper !== null) as Paper[];
    
  } catch (err) {
    console.error('Failed to load papers:', err);
    error.value = t('common.loadError', '載入論文時發生錯誤');
  } finally {
    loading.value = false;
  }
};

// 生命周期
onMounted(() => {
  loadPapers();
});
</script>

<style scoped>
.papers-list-container {
  margin: 1.5rem 0;
  padding: 1rem;
  background: linear-gradient(135deg, #fefce8, #fef3c7);
  border-radius: 0.75rem;
  border: 1px solid #fbbf24;
  transition: all 0.3s ease;
}

.papers-list-container:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.papers-list-label {
  display: inline-block;
  font-weight: 600;
  color: #92400e;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.papers-list-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #92400e;
  font-size: 0.9rem;
}

.loading-spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid #fbbf24;
  border-top: 2px solid #92400e;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.papers-list-error,
.papers-list-empty {
  color: #92400e;
  font-size: 0.9rem;
  font-style: italic;
}

.papers-list-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.papers-list-item {
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 0.5rem;
  border: 1px solid rgba(251, 191, 36, 0.3);
  transition: all 0.3s ease;
  cursor: pointer;
}

.papers-list-item:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: #fbbf24;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.papers-list-item-title {
  font-weight: 600;
  color: #92400e;
  margin-bottom: 0.25rem;
  font-size: 0.95rem;
  line-height: 1.4;
}

.papers-list-item-venue {
  font-size: 0.8rem;
  color: #d97706;
  margin-bottom: 0.25rem;
}

.papers-list-item-date {
  font-size: 0.75rem;
  color: #a16207;
}

/* 暗色主题支持 */
[data-theme="dark"] .papers-list-container,
.dark .papers-list-container {
  background: linear-gradient(135deg, #292524, #1c1917);
  border-color: #78716c;
}

[data-theme="dark"] .papers-list-label,
.dark .papers-list-label {
  color: #fbbf24;
}

[data-theme="dark"] .papers-list-loading,
[data-theme="dark"] .papers-list-error,
[data-theme="dark"] .papers-list-empty,
.dark .papers-list-loading,
.dark .papers-list-error,
.dark .papers-list-empty {
  color: #fbbf24;
}

[data-theme="dark"] .loading-spinner,
.dark .loading-spinner {
  border-color: #78716c;
  border-top-color: #fbbf24;
}

[data-theme="dark"] .papers-list-item,
.dark .papers-list-item {
  background: rgba(41, 37, 36, 0.8);
  border-color: rgba(120, 113, 108, 0.3);
}

[data-theme="dark"] .papers-list-item:hover,
.dark .papers-list-item:hover {
  background: rgba(41, 37, 36, 0.95);
  border-color: #78716c;
}

[data-theme="dark"] .papers-list-item-title,
.dark .papers-list-item-title {
  color: #fbbf24;
}

[data-theme="dark"] .papers-list-item-venue,
.dark .papers-list-item-venue {
  color: #f59e0b;
}

[data-theme="dark"] .papers-list-item-date,
.dark .papers-list-item-date {
  color: #d97706;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .papers-list-container {
    margin: 1rem 0;
    padding: 0.75rem;
  }

  .papers-list-label {
    font-size: 0.9rem;
  }

  .papers-list-item {
    padding: 0.65rem;
  }

  .papers-list-item-title {
    font-size: 0.9rem;
  }

  .papers-list-item-venue {
    font-size: 0.75rem;
  }

  .papers-list-item-date {
    font-size: 0.7rem;
  }
}
</style>