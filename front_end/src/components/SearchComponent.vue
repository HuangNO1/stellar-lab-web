<template>
  <div class="search-component">
    <!-- 基礎搜索 -->
    <div class="basic-search">
      <n-input
        v-model:value="localFilters.q"
        :placeholder="$t('search.placeholder')"
        clearable
        @keyup.enter="handleSearch"
        @clear="handleSearch"
      >
        <template #prefix>
          <n-icon size="16">
            <svg viewBox="0 0 24 24">
              <path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
            </svg>
          </n-icon>
        </template>
        <template #suffix>
          <n-button
            text
            @click="toggleAdvanced"
            :class="{ 'text-primary': showAdvanced }"
          >
            <n-icon size="16">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M3,17V19H9V17H3M3,5V7H13V5H3M13,21V19H21V17H13V15H11V21H13M7,9V11H3V13H7V15H9V9H7M21,13V11H11V13H21M15,9H13V7H21V5H13V3H11V9H15Z"/>
              </svg>
            </n-icon>
            {{ $t('search.advanced') }}
          </n-button>
        </template>
      </n-input>
    </div>

    <!-- 高級搜索 -->
    <n-collapse-transition :show="showAdvanced">
      <div class="advanced-search">
        <n-form label-placement="left" label-width="80" label-align="left">
          <!-- 日期範圍 -->
          <n-form-item :label="$t('search.dateRange')" v-if="config.dateRange">
            <n-date-picker
              v-model:value="dateRange"
              type="daterange"
              :placeholder="[$t('search.startDate'), $t('search.endDate')]"
              @update:value="handleDateChange"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              clearable
              style="width: 300px"
            />
          </n-form-item>

          <!-- 論文特定篩選 -->
          <template v-if="config.type === 'papers'">
            <n-form-item :label="$t('papers.type')">
              <n-select
                v-model:value="localFilters.paper_type"
                :options="paperTypeOptions"
                :placeholder="$t('search.all')"
                clearable
                style="width: 200px"
                @update:value="handleSearch"
              />
            </n-form-item>
            <n-form-item :label="$t('papers.status')">
              <n-select
                v-model:value="localFilters.paper_accept"
                :options="paperStatusOptions"
                :placeholder="$t('search.all')"
                clearable
                style="width: 200px"
                @update:value="handleSearch"
              />
            </n-form-item>
          </template>

          <!-- 新聞特定篩選 -->
          <template v-if="config.type === 'news'">
            <n-form-item :label="$t('news.type')">
              <n-select
                v-model:value="localFilters.news_type"
                :options="newsTypeOptions"
                :placeholder="$t('search.all')"
                clearable
                style="width: 200px"
                @update:value="handleSearch"
              />
            </n-form-item>
          </template>

          <!-- 項目特定篩選 -->
          <template v-if="config.type === 'projects'">
            <n-form-item :label="$t('projects.status')">
              <n-select
                v-model:value="localFilters.is_end"
                :options="projectStatusOptions"
                :placeholder="$t('search.all')"
                clearable
                style="width: 200px"
                @update:value="handleSearch"
              />
            </n-form-item>
          </template>

          <!-- 排序 -->
          <template v-if="config.sorting">
            <n-form-item :label="$t('search.sortBy')">
              <n-space>
                <n-select
                  v-model:value="localFilters.sort_by"
                  :options="sortOptions"
                  :placeholder="$t('search.default')"
                  clearable
                  style="width: 200px"
                  @update:value="handleSearch"
                />
                <n-select
                  v-model:value="localFilters.order"
                  :options="orderOptions"
                  :placeholder="$t('search.desc')"
                  clearable
                  style="width: 120px"
                  @update:value="handleSearch"
                />
              </n-space>
            </n-form-item>
          </template>
        </n-form>
      </div>
    </n-collapse-transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import type { SearchFilters } from '@/types/api';

interface SearchConfig {
  type: 'papers' | 'news' | 'projects';
  dateRange?: boolean;
  sorting?: boolean;
  sortFields?: { value: string; label: string }[];
}

// eslint-disable-next-line no-undef
const props = defineProps<{
  config: SearchConfig;
  filters?: SearchFilters;
}>();

// eslint-disable-next-line no-undef
const emit = defineEmits<{
  search: [filters: SearchFilters];
}>();

const { t } = useI18n();
const showAdvanced = ref(false);
const dateRange = ref<[string, string] | null>(null);

// 本地篩選狀態
const localFilters = ref<SearchFilters>({
  q: '',
  sort_by: '',
  order: 'desc',
  ...props.filters
});

// 論文類型選項
const paperTypeOptions = computed(() => [
  { label: t('papers.conference'), value: 0 },
  { label: t('papers.journal'), value: 1 },
  { label: t('papers.patent'), value: 2 },
  { label: t('papers.book'), value: 3 },
  { label: t('papers.other'), value: 4 }
]);

// 論文狀態選項
const paperStatusOptions = computed(() => [
  { label: t('papers.submitted'), value: 0 },
  { label: t('papers.accepted'), value: 1 }
]);

// 新聞類型選項
const newsTypeOptions = computed(() => [
  { label: t('news.paperPublished'), value: 0 },
  { label: t('news.award'), value: 1 },
  { label: t('news.academic'), value: 2 }
]);

// 項目狀態選項
const projectStatusOptions = computed(() => [
  { label: t('projects.ongoing'), value: 0 },
  { label: t('projects.completed'), value: 1 }
]);

// 排序選項
const sortOptions = computed(() => {
  if (props.config.sortFields) {
    return props.config.sortFields.map(field => ({
      label: t(field.label),
      value: field.value
    }));
  }

  const commonOptions = [];
  if (props.config.type === 'papers') {
    commonOptions.push(
      { label: t('papers.title'), value: 'title' },
      { label: t('papers.venue'), value: 'venue' },
      { label: t('papers.date'), value: 'paper_date' }
    );
  } else if (props.config.type === 'news') {
    commonOptions.push(
      { label: t('news.date'), value: 'news_date' }
    );
  } else if (props.config.type === 'projects') {
    commonOptions.push(
      { label: t('projects.name'), value: 'name' },
      { label: t('projects.startDate'), value: 'project_date_start' }
    );
  }
  return commonOptions;
});

// 排序順序選項
const orderOptions = computed(() => [
  { label: t('search.asc'), value: 'asc' },
  { label: t('search.desc'), value: 'desc' }
]);

// 處理搜索
const handleSearch = () => {
  emit('search', { ...localFilters.value });
};

// 處理日期變化
const handleDateChange = (value: [string, string] | null) => {
  if (value) {
    localFilters.value.start_date = value[0];
    localFilters.value.end_date = value[1];
  } else {
    localFilters.value.start_date = undefined;
    localFilters.value.end_date = undefined;
  }
  handleSearch();
};

// 切換高級搜索
const toggleAdvanced = () => {
  showAdvanced.value = !showAdvanced.value;
};

// 監聽外部篩選變化
watch(() => props.filters, (newFilters) => {
  if (newFilters) {
    localFilters.value = { ...localFilters.value, ...newFilters };
    if (newFilters.start_date && newFilters.end_date) {
      dateRange.value = [newFilters.start_date, newFilters.end_date];
    }
  }
}, { deep: true });

// 初始設置日期範圍
if (localFilters.value.start_date && localFilters.value.end_date) {
  dateRange.value = [localFilters.value.start_date, localFilters.value.end_date];
}
</script>

<style scoped>
.search-component {
  width: 100%;
  margin-bottom: 1.5rem;
}

.basic-search {
  width: 100%;
}

.advanced-search {
  background: rgba(24, 144, 255, 0.05);
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
  border: 0.0625rem solid rgba(24, 144, 255, 0.1);
}

.text-primary {
  color: #1890ff !important;
}

/* 暗色主題支持 */
[data-theme="dark"] .advanced-search,
.dark .advanced-search {
  background: rgba(112, 161, 255, 0.1);
  border-color: rgba(112, 161, 255, 0.2);
}

/* 表單項樣式 */
:deep(.n-form-item) {
  margin-bottom: 1rem;
}

:deep(.n-form-item:last-child) {
  margin-bottom: 0;
}

:deep(.n-form-item-label) {
  color: #666;
  font-weight: 500;
  padding-right: 0.75rem !important;
}

/* 暗色主題下的標籤顏色 */
[data-theme="dark"] :deep(.n-form-item-label),
.dark :deep(.n-form-item-label) {
  color: #ccc !important;
}

/* 響應式設計 */
@media (max-width: 48rem) {
  .advanced-search {
    padding: 1rem;
  }

  :deep(.n-form) {
    --n-label-width: 70px;
  }

  :deep(.n-form-item-label) {
    font-size: 0.875rem;
  }
}

@media (max-width: 36rem) {
  :deep(.n-form) {
    --n-label-placement: top;
  }

  :deep(.n-form-item-label) {
    padding-bottom: 0.5rem !important;
    padding-right: 0 !important;
  }

  .advanced-search {
    padding: 0.75rem;
  }
}
</style>