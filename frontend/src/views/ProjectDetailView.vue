<template>
  <div class="project-detail-view">
    <!-- 加載狀態 -->
    <template v-if="loading">
      <div class="project-detail-skeleton">
        <div class="detail-header-skeleton">
          <n-skeleton text height="2.5rem" width="80%" style="margin-bottom: 1rem" />
          <div style="display: flex; gap: 0.5rem; margin-bottom: 1.5rem;">
            <n-skeleton text height="1.5rem" width="5rem" />
            <n-skeleton text height="1.5rem" width="6rem" />
          </div>
        </div>
        <div class="detail-content-skeleton">
          <n-skeleton text height="1rem" width="100%" :repeat="5" />
        </div>
        <div class="detail-actions-skeleton" style="margin-top: 2rem;">
          <n-skeleton text height="2rem" width="8rem" style="margin-right: 1rem" />
          <n-skeleton text height="2rem" width="6rem" />
        </div>
      </div>
    </template>

    <!-- 錯誤狀態 -->
    <div v-else-if="error" class="error-state">
      <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 16px;">
        {{ error }}
      </n-alert>
      <n-button @click="fetchProjectDetail" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 項目詳情 -->
    <div v-else-if="project" class="project-detail-content">
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
      
      <div class="project-header">
        <h1 class="project-title">
          {{ getCurrentLocale() === 'zh' ? project.project_name_zh : (project.project_name_en || project.project_name_zh) }}
        </h1>
        
        <div class="project-meta">
          <n-tag :type="getProjectStatusColor(project.is_end)" size="medium">
            {{ getProjectStatusText(project.is_end) }}
          </n-tag>
          <span v-if="project.project_date_start" class="project-start-date">
            <n-icon size="16" style="margin-right: 0.5rem;">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,3H18V1H16V3H8V1H6V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3M19,19H5V8H19V19Z"/>
              </svg>
            </n-icon>
            {{ $t('projects.startDate') }}: {{ formatDate(project.project_date_start) }}
          </span>
        </div>
      </div>

      <div class="project-description" v-if="project.project_desc_zh || project.project_desc_en">
        <h3>{{ $t('projects.description') }}</h3>
        <markdown-it :source="getProjectDescription()" :plugins="markdownPlugins"></markdown-it>
      </div>

      <div class="project-actions">
        <n-button 
          v-if="project.project_url" 
          type="primary" 
          @click="openProjectUrl(project.project_url)"
          size="large"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M10.59,13.41C11,13.8 11,14.4 10.59,14.81C10.2,15.2 9.6,15.2 9.19,14.81L7.77,13.39L7.06,12.68L5.64,11.27C4.86,10.5 4.86,9.23 5.64,8.46L8.05,6.05C8.83,5.27 10.1,5.27 10.88,6.05L12.3,7.47C13.08,8.25 13.08,9.52 12.3,10.3L11.59,11L10.59,13.41M13.41,9.17C13.8,8.78 14.4,8.78 14.81,9.17L16.22,10.58L16.93,11.29L18.36,12.72C19.14,13.5 19.14,14.77 18.36,15.54L15.95,17.95C15.17,18.73 13.9,18.73 13.12,17.95L11.7,16.53C10.92,15.75 10.92,14.48 11.7,13.7L12.41,13L13.41,9.17M9.17,14.83L14.83,9.17C15.39,9.73 15.39,10.61 14.83,11.17L9.17,16.83C8.61,16.27 8.61,15.39 9.17,14.83Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('projects.viewRepository') }}
        </n-button>
      </div>
    </div>

    <!-- 沒有找到項目 -->
    <div v-else class="not-found-state">
      <n-empty :description="$t('projects.notFound')" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { projectApi } from '@/services/api';
import type { Project, ApiError } from '@/types/api';
import MarkdownIt from 'vue3-markdown-it';

const route = useRoute();
const router = useRouter();
const { t, locale } = useI18n();

// 響應式數據
const project = ref<Project | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

// 計算屬性
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

const getProjectDescription = () => {
  if (!project.value) return '';
  const desc = getCurrentLocale() === 'zh' ? project.value.project_desc_zh : project.value.project_desc_en;
  return desc || '';
};

// Markdown插件配置
const markdownPlugins = [
  {
    plugin: (md: Record<string, unknown>) => {
      // 修改链接渲染规则
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const defaultRender = (md as any).renderer.rules.link_open || function(tokens: Record<string, unknown>[], idx: number, options: Record<string, unknown>, env: Record<string, unknown>, renderer: Record<string, unknown>) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return (renderer as any).renderToken(tokens, idx, options);
      };

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (md as any).renderer.rules.link_open = function (tokens: Record<string, unknown>[], idx: number, options: Record<string, unknown>, env: Record<string, unknown>, renderer: Record<string, unknown>) {
        const token = tokens[idx];
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const href = (token as any).attrGet('href');
        
        // 检查是否为外部链接
        if (href && (href.startsWith('http://') || href.startsWith('https://') || href.startsWith('//') || href.includes('://'))) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          (token as any).attrSet('target', '_blank');
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          (token as any).attrSet('rel', 'noopener noreferrer');
        }
        
        return defaultRender(tokens, idx, options, env, renderer);
      };
    }
  }
];

// 方法
const fetchProjectDetail = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const projectId = parseInt(route.params.id as string);
    if (isNaN(projectId)) {
      error.value = t('projects.invalidId');
      return;
    }

    const response = await projectApi.getProject(projectId);
    if (response.code === 0) {
      project.value = response.data;
    } else {
      error.value = response.message;
    }
  } catch (err: unknown) {
    console.error('Failed to fetch project detail:', err);
    const apiError = err as ApiError;
    error.value = apiError?.message || t('projects.fetchError');
  } finally {
    loading.value = false;
  }
};

const getProjectStatusColor = (isEnd: number) => {
  return isEnd === 1 ? 'success' : 'info';
};

const getProjectStatusText = (isEnd: number) => {
  return isEnd === 1 ? t('projects.completed') : t('projects.ongoing');
};

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString(getCurrentLocale() === 'zh' ? 'zh-CN' : 'en-US');
};

const openProjectUrl = (url: string) => {
  window.open(url, '_blank');
};

const goBack = () => {
  router.back();
};

// 生命週期
onMounted(() => {
  fetchProjectDetail();
});
</script>

<style scoped>
.project-detail-view {
  padding: 0.5rem 1rem;
  max-width: 160rem;
  min-width: 20rem;
  margin: 0 auto;
  width: 100%;
}

.project-detail-skeleton,
.project-detail-content {
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

.project-header {
  margin-bottom: 2rem;
}

.project-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}

.project-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.project-start-date {
  display: flex;
  align-items: center;
  font-size: 1rem;
  color: #666;
}

.project-description {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 0.75rem;
  border-left: 4px solid #1890ff;
}

.project-description h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #333;
}

.project-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* 暗色主題支持 */
[data-theme="dark"] .back-button-section,
.dark .back-button-section {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .project-detail-view,
.dark .project-detail-view {
  color: #fff;
}

[data-theme="dark"] .project-start-date,
.dark .project-start-date {
  color: #ccc;
}

[data-theme="dark"] .project-description,
.dark .project-description {
  background: rgba(255, 255, 255, 0.08);
  border-left-color: #70a1ff;
}

[data-theme="dark"] .project-description h3,
.dark .project-description h3 {
  color: #fff;
}

/* 響應式設計 */
@media (max-width: 48rem) {
  .project-detail-view {
    padding: 1rem;
    min-width: auto;
  }
  
  .project-title {
    font-size: 2rem;
  }
  
  .project-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .project-actions {
    flex-direction: column;
  }
  
  .project-actions .n-button {
    width: 100%;
    justify-content: center;
  }
}
</style>