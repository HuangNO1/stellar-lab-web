<template>
  <div class="project-view">
    <div class="project-header">
      <h1 class="page-title">{{ $t('nav.projects') }}</h1>
      <p class="page-description">{{ $t('projects.description') }}</p>
    </div>

    <!-- 搜索組件 -->
    <SearchComponent
      :config="searchConfig"
      :filters="currentFilters"
      @search="handleSearch"
    />

    <!-- 加載狀態 -->
    <div v-if="loading" class="project-skeleton">
      <div v-for="i in 6" :key="i" class="project-item-skeleton">
        <div class="skeleton-header">
          <n-skeleton text height="1.5rem" width="80%" />
          <n-skeleton text height="1rem" width="40%" style="margin-top: 0.5rem" />
        </div>
        <n-skeleton text height="0.875rem" width="100%" :repeat="2" style="margin-top: 1rem" />
        <div class="skeleton-footer" style="margin-top: 1rem; display: flex; justify-content: space-between;">
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
      <n-button @click="fetchProjects" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 項目列表 -->
    <div v-else class="project-content">
      <div v-if="projectList.length > 0" class="project-list">
        <div v-for="project in projectList" :key="project.project_id" class="project-item" @click="viewProjectDetail(project)">
          <div class="project-header-info">
            <h3 class="project-name">
              {{ getCurrentLocale() === 'zh' ? project.project_name_zh : (project.project_name_en || project.project_name_zh) }}
            </h3>
            <div class="project-status">
              <n-tag :type="getProjectStatusColor(project.is_end)" size="small">
                {{ getProjectStatusText(project.is_end) }}
              </n-tag>
            </div>
          </div>
          
          <div v-if="project.project_desc_zh || project.project_desc_en" class="project-description">
            {{ stripMarkdown(getCurrentLocale() === 'zh' ? project.project_desc_zh : (project.project_desc_en || project.project_desc_zh)) }}
          </div>
          
          <div class="project-meta">
            <div class="project-info">
              <span v-if="project.project_date_start" class="project-start-date">
                <n-icon size="14" style="margin-right: 0.25rem;">
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19,3H18V1H16V3H8V1H6V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3M19,19H5V8H19V19Z"/>
                  </svg>
                </n-icon>
                {{ $t('projects.startDate') }}: {{ formatDate(project.project_date_start) }}
              </span>
            </div>
          </div>

          <div class="project-actions">
            <n-button v-if="project.project_url" size="small" type="info" ghost @click.stop="openProjectUrl(project.project_url)">
              <template #icon>
                <n-icon size="14">
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M10.59,13.41C11,13.8 11,14.4 10.59,14.81C10.2,15.2 9.6,15.2 9.19,14.81L7.77,13.39L7.06,12.68L5.64,11.27C4.86,10.5 4.86,9.23 5.64,8.46L8.05,6.05C8.83,5.27 10.1,5.27 10.88,6.05L12.3,7.47C13.08,8.25 13.08,9.52 12.3,10.3L11.59,11L10.59,13.41M13.41,9.17C13.8,8.78 14.4,8.78 14.81,9.17L16.22,10.58L16.93,11.29L18.36,12.72C19.14,13.5 19.14,14.77 18.36,15.54L15.95,17.95C15.17,18.73 13.9,18.73 13.12,17.95L11.7,16.53C10.92,15.75 10.92,14.48 11.7,13.7L12.41,13L13.41,9.17M9.17,14.83L14.83,9.17C15.39,9.73 15.39,10.61 14.83,11.17L9.17,16.83C8.61,16.27 8.61,15.39 9.17,14.83Z"/>
                  </svg>
                </n-icon>
              </template>
              {{ $t('projects.viewRepository') }}
            </n-button>
            <n-button size="small" type="primary" ghost>
              {{ $t('common.viewDetails') }}
            </n-button>
          </div>
        </div>
      </div>

      <!-- 空狀態 -->
      <div v-else class="empty-state">
        <n-empty :description="$t('projects.empty')" />
      </div>

      <!-- 分頁 -->
      <div v-if="pagination && pagination.pages > 1" class="pagination-wrapper">
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
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import SearchComponent from '@/components/SearchComponent.vue';
import { projectApi } from '@/services/api';
import { stripMarkdown } from '@/utils/text';
import type { Project, SearchFilters } from '@/types/api';

const { t, locale } = useI18n();
const router = useRouter();

// 響應式數據
const projectList = ref<Project[]>([]);
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
  type: 'projects' as const,
  dateRange: true,
  sorting: true,
  sortFields: [
    { value: 'project_date_start', label: 'projects.startDate' },
    { value: 'project_name_zh', label: 'projects.name' }
  ]
};

// 當前搜索過濾器
const currentFilters = ref<SearchFilters>({
  q: '',
  sort_by: 'project_date_start',
  order: 'desc'
});

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

// 獲取項目狀態顏色
const getProjectStatusColor = (isEnd: number) => {
  return isEnd === 1 ? 'success' : 'info';
};

// 獲取項目狀態文本
const getProjectStatusText = (isEnd: number) => {
  return isEnd === 1 ? t('projects.completed') : t('projects.ongoing');
};

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString(getCurrentLocale() === 'zh' ? 'zh-CN' : 'en-US');
};

// 獲取項目數據
const fetchProjects = async (resetPage = false) => {
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
      is_end: currentFilters.value.is_end,
      start_date: currentFilters.value.start_date,
      end_date: currentFilters.value.end_date,
      sort_by: currentFilters.value.sort_by,
      order: currentFilters.value.order
    };

    // 移除空值
    Object.keys(params).forEach(key => {
      if (params[key as keyof typeof params] === '' || params[key as keyof typeof params] === null || params[key as keyof typeof params] === undefined) {
        delete params[key as keyof typeof params];
      }
    });

    const response = await projectApi.getProjects(params);
    if (response.code === 0) {
      projectList.value = response.data.items;
      
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
        pagination.value = null;
      }
    } else {
      error.value = response.message || t('common.fetchError');
    }
  } catch (err) {
    console.error('Failed to fetch projects:', err);
    error.value = t('common.networkError');
  } finally {
    loading.value = false;
  }
};

// 搜索處理
const handleSearch = (filters: SearchFilters) => {
  currentFilters.value = { ...filters };
  fetchProjects(true);
};

// 頁面變化處理
const handlePageChange = (page: number) => {
  currentPage.value = page;
  fetchProjects();
};

// 每頁數量變化處理
const handlePageSizeChange = (pageSize: number) => {
  currentPageSize.value = pageSize;
  currentPage.value = 1;
  fetchProjects();
};

// 查看項目詳情
const viewProjectDetail = (project: Project) => {
  router.push(`/project/${project.project_id}`);
};

// 打開項目URL
const openProjectUrl = (url: string) => {
  window.open(url, '_blank');
};

// 生命週期
onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
.project-view {
  padding: 1.5rem;
  min-width: 60rem;
  max-width: 87.5rem;
  margin: 0 auto;
}

/* 頁面頭部 */
.project-header {
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
.project-skeleton {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.project-item-skeleton {
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

/* 項目列表 */
.project-content {
  margin-top: 1.5rem;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.project-item {
  padding: 1.5rem;
  border-radius: 0.75rem;
  background: #fff;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.08);
  border: 0.0625rem solid rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  cursor: pointer;
  border-left: 0.25rem solid transparent;
}

.project-item:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.12);
  border-left-color: #1890ff;
}

.project-header-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.project-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  line-height: 1.5;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-status {
  flex-shrink: 0;
}

.project-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-meta {
  margin-bottom: 1rem;
}

.project-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.project-start-date {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #888;
  font-weight: 500;
}

.project-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  flex-wrap: wrap;
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
[data-theme="dark"] .project-view,
.dark .project-view,
.dark-mode .project-view {
  color: #fff;
}

[data-theme="dark"] .page-description,
.dark .page-description,
.dark-mode .page-description {
  color: #ccc;
}

[data-theme="dark"] .project-item,
[data-theme="dark"] .project-item-skeleton,
.dark .project-item,
.dark .project-item-skeleton,
.dark-mode .project-item,
.dark-mode .project-item-skeleton {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.2);
}

[data-theme="dark"] .project-item:hover,
.dark .project-item:hover,
.dark-mode .project-item:hover {
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.3);
  border-left-color: #70a1ff;
}

[data-theme="dark"] .project-name,
.dark .project-name,
.dark-mode .project-name {
  color: #fff;
}

[data-theme="dark"] .project-description,
.dark .project-description,
.dark-mode .project-description {
  color: #ccc;
}

[data-theme="dark"] .project-start-date,
.dark .project-start-date,
.dark-mode .project-start-date {
  color: #bbb;
}

[data-theme="dark"] .pagination-wrapper,
.dark .pagination-wrapper,
.dark-mode .pagination-wrapper {
  border-top-color: rgba(255, 255, 255, 0.1);
}

/* 響應式設計 */
@media (max-width: 48rem) {
  .project-view {
    padding: 1rem;
    min-width: unset;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-description {
    font-size: 1rem;
  }
  
  .project-item {
    padding: 1rem;
  }
  
  .project-header-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .project-name {
    font-size: 1.125rem;
  }
  
  .project-actions {
    justify-content: flex-start;
    gap: 0.25rem;
  }
  
  .project-actions .n-button {
    font-size: 0.8rem;
  }
}
</style>