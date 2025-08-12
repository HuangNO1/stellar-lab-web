<template>
  <div class="group-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.groups') }}</h2>
      <n-space>
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.groups.addGroup') }}
        </n-button>
      </n-space>
    </div>

    <!-- 搜索和篩選 -->
    <n-card class="search-card">
      <n-space>
        <n-input
          v-model:value="searchQuery"
          :placeholder="$t('admin.groups.searchPlaceholder')"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
          style="width: 300px"
        >
          <template #prefix>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
              </svg>
            </n-icon>
          </template>
        </n-input>

        <n-button @click="handleSearch">
          {{ $t('search.search') }}
        </n-button>
      </n-space>
    </n-card>

    <!-- 數據表格 -->
    <n-card>
      <n-config-provider :locale="naiveLocale" :date-locale="dateLocale">
        <n-data-table
          :columns="columns"
          :data="groupList"
          :pagination="pagination"
          :loading="loading"
          :remote="true"
          :row-key="(row: ResearchGroup) => row.research_group_id"
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </n-config-provider>
    </n-card>

    <!-- 新增/編輯 Modal -->
    <QuickActionModal
      v-model="showCreateModal"
      :module-type="'research-groups'"
      :action-type="modalActionType"
      :edit-data="editData"
      @success="handleModalSuccess"
    />

    <!-- 刪除確認對話框 -->
    <n-modal v-model:show="showDeleteModal">
      <n-card
        style="width: 450px;"
        :title="$t('admin.common.confirmDelete')"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
      >
        <p>{{ $t('admin.groups.deleteConfirmText') }}</p>
        <div v-if="deleteTarget" class="delete-group-info">
          <div class="group-details">
            <div class="group-name">{{ deleteTarget.research_group_name_zh }}</div>
            <div class="group-name-en">{{ deleteTarget.research_group_name_en }}</div>
            <div class="group-leader" v-if="deleteTarget.leader">
              {{ $t('admin.groups.leader') }}: {{ deleteTarget.leader.mem_name_zh }}
            </div>
          </div>
        </div>
        <template #footer>
          <n-space justify="end">
            <n-button @click="showDeleteModal = false">
              {{ $t('common.cancel') }}
            </n-button>
            <n-button type="error" @click="confirmDelete" :loading="deleteLoading">
              {{ $t('common.confirm') }}
            </n-button>
          </n-space>
        </template>
      </n-card>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, h, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessage, NButton, NTag, NSpace, zhCN, enUS, dateZhCN, dateEnUS } from 'naive-ui';
import { researchGroupApi } from '@/services/api';
import QuickActionModal from '@/components/QuickActionModal.vue';
import type { ResearchGroup } from '@/types/api';
import type { DataTableColumns } from 'naive-ui';

const { t, locale } = useI18n();
const message = useMessage();

// 當前語言環境
const currentLocale = computed(() => locale.value);

// Naive UI 語言包配置
const naiveLocale = computed(() => {
  return locale.value === 'zh' ? zhCN : enUS;
});

// 日期選擇器的國際化配置
const dateLocale = computed(() => {
  return locale.value === 'zh' ? dateZhCN : dateEnUS;
});

// 響應式數據
const groupList = ref<ResearchGroup[]>([]);
const loading = ref(false);
const deleteLoading = ref(false);
const showDeleteModal = ref(false);
const deleteTarget = ref<ResearchGroup | null>(null);

// Modal 狀態
const showCreateModal = ref(false);
const modalActionType = ref<'create' | 'edit'>('create');
const editData = ref<any>({});

// 搜索和篩選
const searchQuery = ref('');

// 分頁
const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100]
});

// 表格列定義
const columns: DataTableColumns<ResearchGroup> = [
  {
    title: t('admin.groups.form.nameZh'),
    key: 'research_group_name_zh',
    render(row) {
      return h('div', [
        h('div', { style: { fontWeight: 'bold' } }, row.research_group_name_zh),
        h('div', { style: { fontSize: '0.875rem', color: '#666' } }, row.research_group_name_en)
      ]);
    }
  },
  {
    title: t('admin.groups.leader'),
    key: 'leader',
    width: 150,
    render(row) {
      if (!row.leader) return '-';
      
      return h('div', [
        h('div', { style: { fontSize: '0.875rem' } }, row.leader.mem_name_zh),
        h('div', { style: { fontSize: '0.8rem', color: '#666', fontStyle: 'italic' } }, row.leader.mem_name_en)
      ].filter(item => item.children));
    }
  },
  {
    title: t('admin.groups.description'),
    key: 'research_group_desc_zh',
    ellipsis: {
      tooltip: true
    },
    render(row) {
      if (!row.research_group_desc_zh && !row.research_group_desc_en) {
        return '-';
      }
      
      const zhDesc = row.research_group_desc_zh || '';
      const enDesc = row.research_group_desc_en || '';
      
      return h('div', { style: { maxWidth: '300px' } }, [
        zhDesc ? h('div', { style: { fontSize: '0.875rem', marginBottom: '4px' } }, zhDesc.slice(0, 60) + (zhDesc.length > 60 ? '...' : '')) : null,
        enDesc ? h('div', { style: { fontSize: '0.8rem', color: '#666', fontStyle: 'italic' } }, enDesc.slice(0, 60) + (enDesc.length > 60 ? '...' : '')) : null
      ].filter(Boolean));
    }
  },
  {
    title: t('admin.common.status'),
    key: 'enable',
    width: 100,
    render(row) {
      return h(NTag, {
        type: row.enable ? 'success' : 'error'
      }, {
        default: () => row.enable ? t('admin.common.enabled') : t('admin.common.disabled')
      });
    }
  },
  {
    title: t('admin.common.actions'),
    key: 'actions',
    width: 180,
    render(row) {
      return h(NSpace, {}, {
        default: () => [
          h(NButton, {
            size: 'small',
            type: 'primary',
            onClick: () => handleEdit(row)
          }, { default: () => t('admin.common.edit') }),
          h(NButton, {
            size: 'small',
            type: 'error',
            onClick: () => handleDelete(row)
          }, { default: () => t('admin.common.delete') })
        ]
      });
    }
  }
];

// 獲取課題組列表
const fetchGroups = async () => {
  try {
    loading.value = true;
    const params = {
      page: pagination.page,
      per_page: pagination.pageSize,
      q: searchQuery.value || undefined
    };

    const response = await researchGroupApi.getResearchGroups(params);
    if (response.code === 0) {
      groupList.value = response.data.items;
      pagination.itemCount = response.data.total;
    } else {
      message.error(response.message || t('admin.groups.fetchError'));
    }
  } catch (error) {
    console.error('獲取課題組列表失敗:', error);
    message.error(t('admin.groups.fetchError'));
  } finally {
    loading.value = false;
  }
};

// 搜索處理
const handleSearch = () => {
  pagination.page = 1;
  fetchGroups();
};

// 頁面變化處理
const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchGroups();
};

// 每頁數量變化處理
const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize;
  pagination.page = 1;
  fetchGroups();
};

// Modal 處理
const handleCreate = () => {
  modalActionType.value = 'create';
  editData.value = {};
  showCreateModal.value = true;
};

const handleEdit = (group: ResearchGroup) => {
  modalActionType.value = 'edit';
  editData.value = { ...group };
  showCreateModal.value = true;
};

const handleModalSuccess = () => {
  fetchGroups();
};

// 處理刪除
const handleDelete = (group: ResearchGroup) => {
  deleteTarget.value = group;
  showDeleteModal.value = true;
};

// 確認刪除
const confirmDelete = async () => {
  if (!deleteTarget.value) return;

  try {
    deleteLoading.value = true;
    const response = await researchGroupApi.deleteResearchGroup(deleteTarget.value.research_group_id);
    
    if (response.code === 0) {
      message.success(t('admin.groups.deleteSuccess'));
      showDeleteModal.value = false;
      fetchGroups();
    } else {
      message.error(response.message || t('admin.groups.deleteError'));
    }
  } catch (error) {
    console.error('刪除課題組失敗:', error);
    message.error(t('admin.groups.deleteError'));
  } finally {
    deleteLoading.value = false;
  }
};

// 生命週期
onMounted(() => {
  fetchGroups();
});
</script>

<style scoped>
.group-manage {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.search-card {
  margin-bottom: 0;
}

.delete-group-info {
  margin: 16px 0;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.group-details {
  flex: 1;
}

.group-name {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
}

.group-name-en {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.group-leader {
  color: #888;
  font-size: 13px;
}

/* 暗色主題 */
[data-theme="dark"] .page-header h2,
.dark .page-header h2 {
  color: #f9fafb;
}

[data-theme="dark"] .delete-group-info,
.dark .delete-group-info {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .group-name-en,
.dark .group-name-en {
  color: #ccc;
}

[data-theme="dark"] .group-leader,
.dark .group-leader {
  color: #aaa;
}
</style>