<template>
  <div class="resource-view">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">{{ $t('resources.title') }}</h1>
        <p class="page-description">{{ $t('resources.description') }}</p>
      </div>
    </div>

    <!-- 搜索組件 -->
    <SearchComponent
      :config="searchConfig"
      :filters="currentFilters"
      @search="handleSearch"
    />

    <!-- Resources Grid -->
    <div class="resources-section">
      <!-- 加載狀態 -->
      <div v-if="loading" class="resource-skeleton">
        <div v-for="i in 6" :key="i" class="resource-item-skeleton">
          <div class="card-content">
            <!-- 圖片骨架 -->
            <div class="resource-image-skeleton">
              <n-skeleton height="100px" width="150px" />
            </div>
            
            <!-- 信息骨架 -->
            <div class="resource-info-skeleton">
              <div class="skeleton-header">
                <n-skeleton text height="1.25rem" width="70%" />
                <n-skeleton text height="0.875rem" width="100%" :repeat="2" style="margin-top: 0.5rem" />
              </div>
              <div class="skeleton-meta" style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.5rem;">
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                  <n-skeleton text height="0.75rem" width="15%" />
                  <n-skeleton text height="1.5rem" width="20%" />
                </div>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                  <n-skeleton text height="0.75rem" width="15%" />
                  <n-skeleton text height="1.5rem" width="20%" />
                </div>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                  <n-skeleton text height="0.75rem" width="15%" />
                  <n-skeleton text height="0.75rem" width="30%" />
                </div>
              </div>
              <div class="skeleton-actions" style="margin-top: 1rem;">
                <n-skeleton text height="2rem" width="25%" />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="resources.length === 0" class="empty-container">
        <n-empty :description="$t('resources.empty')" />
      </div>
      
      <div v-else class="resources-list">
        <div
          v-for="resource in resources"
          :key="resource.resource_id"
          class="resource-item"
        >
          <div class="card-content">
            <!-- Resource Image -->
            <div class="resource-image">
              <img
                v-if="resource.resource_image"
                :src="getResourceImageUrl(resource.resource_image)"
                :alt="getResourceName(resource)"
                class="resource-img"
              />
              <div v-else class="resource-placeholder">
                <n-icon size="48" color="#ccc">
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M20,6C20,4.89 19.11,4 18,4H12V2A2,2 0 0,0 10,0H4A2,2 0 0,0 2,2V18A2,2 0 0,0 4,20H18A2,2 0 0,0 20,18V6M18,18H4V2H10V6H18V18Z"/>
                  </svg>
                </n-icon>
              </div>
            </div>
            
            <!-- Resource Info -->
            <div class="resource-info">
              <h3 class="resource-name">{{ getResourceName(resource) }}</h3>
              <p v-if="getResourceDescription(resource)" class="resource-description">
                {{ getResourceDescription(resource) }}
              </p>
              
              <!-- Resource Meta -->
              <div class="resource-meta">
                <div class="meta-row">
                  <span class="meta-label">{{ $t('resources.resourceType') }}:</span>
                  <n-tag :type="getTypeTagType(resource.resource_type)" size="small">
                    {{ getResourceTypeText(resource.resource_type) }}
                  </n-tag>
                </div>
                
                <div class="meta-row">
                  <span class="meta-label">{{ $t('resources.availabilityStatus') }}:</span>
                  <n-tag :type="getStatusTagType(resource.availability_status)" size="small">
                    {{ getResourceStatusText(resource.availability_status) }}
                  </n-tag>
                </div>
                
                <div v-if="getResourceLocation(resource)" class="meta-row">
                  <span class="meta-label">{{ $t('resources.location') }}:</span>
                  <span class="meta-value">{{ getResourceLocation(resource) }}</span>
                </div>
                
                <div v-if="resource.contact_info" class="meta-row">
                  <span class="meta-label">{{ $t('resources.contact') }}:</span>
                  <span class="meta-value">{{ resource.contact_info }}</span>
                </div>
              </div>
              
              <!-- Actions -->
              <div v-if="resource.resource_url" class="resource-actions">
                <n-button
                  type="primary"
                  size="small"
                  @click="openResourceUrl(resource.resource_url)"
                  class="action-btn"
                >
                  <template #icon>
                    <n-icon>
                      <svg viewBox="0 0 24 24">
                        <path fill="currentColor" d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"/>
                      </svg>
                    </n-icon>
                  </template>
                  {{ $t('resources.url') }}
                </n-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="!loading && resources.length > 0 && pagination.itemCount > pagination.pageSize" class="pagination-section">
      <n-config-provider :locale="naiveLocale" :date-locale="dateLocale">
        <n-pagination
          v-model:page="pagination.page"
          :page-size="pagination.pageSize"
          :item-count="pagination.itemCount"
          :show-size-picker="pagination.showSizePicker"
          :page-sizes="pagination.pageSizes"
          show-quick-jumper
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </n-config-provider>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessage, NConfigProvider, zhCN, enUS, dateZhCN, dateEnUS } from 'naive-ui';
import SearchComponent from '@/components/SearchComponent.vue';
import { resourceApi } from '@/services/api';
import { getMediaUrl } from '@/utils/media';
import type { Resource, ApiError, SearchFilters } from '@/types/api';

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

// Reactive data
const resources = ref<Resource[]>([]);
const loading = ref(false);
const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  showSizePicker: true,
  pageSizes: [10, 20, 50]
});

// 搜索配置
const searchConfig = {
  type: 'resources' as const,
  sorting: true,
  sortFields: [
    { value: 'resource_name_zh', label: 'resources.name' },
    { value: 'resource_type', label: 'resources.resourceType' }
  ]
};

// 當前搜索過濾器
const currentFilters = ref<SearchFilters>({
  q: '',
  sort_by: 'resource_name_zh',
  order: 'asc'
});

// Computed properties
const getResourceName = (resource: Resource) => {
  return locale.value === 'zh' 
    ? (resource.resource_name_zh || resource.resource_name_en || '')
    : (resource.resource_name_en || resource.resource_name_zh || '');
};

const getResourceDescription = (resource: Resource) => {
  const desc = locale.value === 'zh' 
    ? (resource.resource_description_zh || resource.resource_description_en || '')
    : (resource.resource_description_en || resource.resource_description_zh || '');
  
  // 截取描述的前100个字符
  if (desc.length > 100) {
    return desc.substring(0, 100) + '...';
  }
  return desc;
};

const getResourceLocation = (resource: Resource) => {
  return locale.value === 'zh' 
    ? (resource.resource_location_zh || resource.resource_location_en || '')
    : (resource.resource_location_en || resource.resource_location_zh || '');
};

const getResourceTypeText = (type: number) => {
  const typeMap: Record<number, string> = {
    0: t('resources.types.equipment'),
    1: t('resources.types.software'),
    2: t('resources.types.database'),
    3: t('resources.types.dataset'),
    4: t('resources.types.other')
  };
  return typeMap[type] || t('resources.types.other');
};

const getResourceStatusText = (status: number) => {
  const statusMap: Record<number, string> = {
    0: t('resources.status.unavailable'),
    1: t('resources.status.available'),
    2: t('resources.status.maintenance')
  };
  return statusMap[status] || t('resources.status.unavailable');
};

const getTypeTagType = (type: number) => {
  const typeMap: Record<number, 'info' | 'success' | 'warning' | 'default'> = {
    0: 'info',
    1: 'success', 
    2: 'warning',
    3: 'default'
  };
  return typeMap[type] || 'default';
};

const getStatusTagType = (status: number) => {
  const statusMap: Record<number, 'error' | 'success' | 'warning'> = {
    0: 'error',
    1: 'success',
    2: 'warning'
  };
  return statusMap[status] || 'error';
};

const getResourceImageUrl = (imagePath: string) => {
  return getMediaUrl(imagePath);
};

// Methods
const fetchResources = async () => {
  try {
    loading.value = true;
    
    const params = {
      page: pagination.page,
      per_page: pagination.pageSize,
      q: currentFilters.value.q || undefined,
      resource_type: currentFilters.value.resource_type ?? undefined,
      availability_status: currentFilters.value.availability_status ?? undefined,
      sort_by: currentFilters.value.sort_by || undefined,
      order: currentFilters.value.order || undefined
    };

    const response = await resourceApi.getResources(params);
    if (response.code === 0) {
      resources.value = response.data.items;
      pagination.itemCount = response.data.total;
    } else {
      message.error(response.message || t('resources.fetchError'));
    }
  } catch (error: unknown) {
    console.error('獲取資源列表失敗:', error);
    const apiError = error as ApiError;
    const errorMessage = apiError?.message || t('resources.fetchError');
    message.error(errorMessage);
  } finally {
    loading.value = false;
  }
};

// 搜索處理
const handleSearch = (filters: SearchFilters) => {
  currentFilters.value = { ...filters };
  pagination.page = 1;
  fetchResources();
};

const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchResources();
  
  // 滾動到頁面頂部
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const handlePageSizeChange = (size: number) => {
  pagination.pageSize = size;
  pagination.page = 1;
  fetchResources();
};

const openResourceUrl = (url: string) => {
  window.open(url, '_blank', 'noopener,noreferrer');
};

// Watchers
watch(locale, () => {
  // 語言變化時重新獲取數據以更新顯示
  fetchResources();
});

// Lifecycle
onMounted(() => {
  fetchResources();
});
</script>

<style scoped>
.resource-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

/* Resources Grid */
.resources-section {
  margin-bottom: 2rem;
}

/* 骨架屏 */
.resource-skeleton {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.resource-item-skeleton {
  background: var(--n-card-color);
  border: 1px solid var(--n-border-color);
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.08);
}

/* 暗色主題支持 */
[data-theme="dark"] .resource-item-skeleton,
.dark .resource-item-skeleton,
.dark-mode .resource-item-skeleton {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.2);
}

.resource-item-skeleton .card-content {
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
}

.resource-image-skeleton {
  width: 150px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  order: 1;
}

.resource-info-skeleton {
  flex: 1;
  order: 2;
}

.skeleton-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.resources-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* Resource Item */
.resource-item {
  background: var(--n-card-color);
  border: 1px solid var(--n-border-color);
  border-radius: 0.75rem;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.08);
  margin-bottom: 1rem;
}

.resource-item:last-child {
  margin-bottom: 0;
}

.resource-item:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.12);
  border-color: var(--n-color-target);
}

.card-content {
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
}

.resource-image {
  width: 150px;
  height: 100px;
  margin-bottom: 0;
  border-radius: 8px;
  overflow: hidden;
  background: var(--n-color-neutral);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  order: 1;
}

.resource-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.resource-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #f0f0f0 25%, transparent 25%), 
              linear-gradient(-45deg, #f0f0f0 25%, transparent 25%), 
              linear-gradient(45deg, transparent 75%, #f0f0f0 75%), 
              linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
}

.resource-info {
  flex: 1;
  order: 2;
}

.resource-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--n-text-color);
  margin: 0 0 0.75rem 0;
  line-height: 1.3;
}

.resource-description {
  color: var(--n-text-color-placeholder);
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0 0 1rem 0;
}

.resource-meta {
  margin-bottom: 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.meta-row {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  margin-bottom: 0;
}

.meta-label {
  font-weight: 500;
  color: var(--n-text-color);
  margin-right: 0.5rem;
  flex-shrink: 0;
}

.meta-value {
  color: var(--n-text-color-placeholder);
}

.resource-actions {
  margin-top: 1rem;
}

.action-btn {
  min-width: 100px;
}

/* Pagination */
.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--n-border-color);
}

/* 響應式設計 */
@media (max-width: 768px) {
  .resource-view {
    padding: 1rem 0.5rem;
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
  
  .resources-list {
    gap: 0.75rem;
  }
  
  .resource-item-skeleton .card-content {
    padding: 1rem;
    flex-direction: row;
    align-items: flex-start;
  }
  
  .resource-image-skeleton {
    width: 100px;
    height: 70px;
    order: 1;
  }
  
  .resource-item {
    margin: 0 -0.5rem 0.75rem -0.5rem;
  }
  
  .card-content {
    padding: 1rem;
    flex-direction: row;
    align-items: flex-start;
  }
  
  .resource-image {
    width: 100px;
    height: 70px;
    order: 1;
  }
}

@media (max-width: 480px) {
  .resource-view {
    padding: 0.5rem 0.25rem;
  }
  
  .page-header {
    margin-bottom: 1.5rem;
    padding: 1rem 0.5rem;
    border-radius: 8px;
  }
  
  .page-title {
    font-size: 1.75rem;
  }
  
  .resource-item-skeleton .card-content {
    padding: 0.75rem;
  }
  
  .resource-image-skeleton {
    width: 90px;
    height: 60px;
  }
  
  .resource-item {
    border-radius: 8px;
  }
  
  .resource-image {
    width: 90px;
    height: 60px;
  }
  
  .meta-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}
</style>