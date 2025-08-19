<template>
  <div class="member-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.members') }}</h2>
      <n-space>
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.members.addMember') }}
        </n-button>
        <n-button 
          v-if="selectedRowKeys.length > 0" 
          type="warning" 
          @click="showBatchModal = true"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,5V7H15V5H19M9,5V11H7V9H5V7H7V5H9M11,7H13V9H11V7M15,9V7H19V9H15M7,11V13H5V11H7M9,11H11V13H9V11M13,11V13H15V11H13M17,11V13H19V11H17M7,15V17H5V15H7M9,15H11V17H9V15M13,15V17H15V13H17V15H19V17H17V19H15V17H13V15M5,19V17H7V19H5Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.common.batchEdit') }} ({{ selectedRowKeys.length }})
        </n-button>
        <n-button 
          v-if="selectedRowKeys.length > 0" 
          type="error" 
          @click="handleBatchDelete"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M9,3V4H4V6H5V19A2,2 0 0,0 7,21H17A2,2 0 0,0 19,19V6H20V4H15V3H9M7,6H17V19H7V6M9,8V17H11V8H9M13,8V17H15V8H13Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.common.batchDelete') }}
        </n-button>
      </n-space>
    </div>

    <!-- 搜索和篩選 -->
    <n-card class="search-card">
      <n-space>
        <n-input
          v-model:value="searchQuery"
          :placeholder="$t('admin.members.searchPlaceholder')"
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

        <n-select
          v-model:value="filterType"
          :options="typeOptions"
          :placeholder="$t('admin.members.filterByType')"
          clearable
          style="width: 150px"
          @update:value="handleSearch"
        />

        <n-select
          v-model:value="filterGroup"
          :options="groupOptions"
          :placeholder="$t('admin.members.filterByGroup')"
          clearable
          style="width: 200px"
          @update:value="handleSearch"
        />

        <n-button @click="handleSearch">
          {{ $t('search.search') }}
        </n-button>
      </n-space>
    </n-card>

    <!-- 數據表格 -->
    <n-card>
      <div class="table-container">
        <n-config-provider :locale="naiveLocale" :date-locale="dateLocale">
          <n-data-table
            v-model:checked-row-keys="selectedRowKeys"
            :columns="columns"
            :data="memberList"
            :pagination="pagination"
            :loading="loading"
            :remote="true"
            :row-key="(row: Member) => row.mem_id"
            @update:page="handlePageChange"
            @update:page-size="handlePageSizeChange"
          />
        </n-config-provider>
      </div>
    </n-card>

    <!-- 新增/編輯 Modal -->
    <QuickActionModal
      v-model="showCreateModal"
      :module-type="'members'"
      :action-type="modalActionType"
      :edit-data="editData"
      @success="handleModalSuccess"
    />

    <!-- 批量編輯 Modal -->
    <n-modal v-model:show="showBatchModal">
      <n-card
        style="width: 600px;"
        :title="$t('admin.members.batchEdit')"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
      >
        <n-form
          ref="batchFormRef"
          :model="batchFormData"
          label-placement="left"
          label-width="120"
        >
          <n-form-item :label="$t('admin.members.form.type')">
            <n-select
              v-model:value="batchFormData.mem_type"
              :options="typeOptions"
              :placeholder="$t('admin.members.form.placeholders.type')"
              clearable
            />
          </n-form-item>
          
          <n-form-item :label="$t('admin.members.form.group.label')">
            <n-select
              v-model:value="batchFormData.research_group_id"
              :options="groupOptionsWithNone"
              :placeholder="$t('admin.members.form.placeholders.group')"
              clearable
            />
          </n-form-item>
          
          <n-form-item :label="$t('admin.members.studentGrade')" v-if="batchFormData.mem_type === 1">
            <n-input-number
              v-model:value="batchFormData.student_grade"
              :placeholder="$t('admin.members.placeholders.studentGrade')"
              :min="1"
              :max="6"
              clearable
            />
          </n-form-item>
          
          <n-form-item :label="$t('admin.members.jobType')" v-if="batchFormData.mem_type === 0">
            <n-select
              v-model:value="batchFormData.job_type"
              :options="jobTypeOptions"
              :placeholder="$t('admin.members.placeholders.jobType')"
              clearable
            />
          </n-form-item>
          
          <n-form-item :label="$t('admin.members.studentType')" v-if="batchFormData.mem_type === 1">
            <n-select
              v-model:value="batchFormData.student_type"
              :options="studentTypeOptions"
              :placeholder="$t('admin.members.placeholders.studentType')"
              clearable
            />
          </n-form-item>

          <n-form-item :label="$t('admin.members.form.graduationYear')" v-if="batchFormData.mem_type === 2">
            <n-input-number
              v-model:value="batchFormData.graduation_year"
              :placeholder="$t('admin.members.form.placeholders.graduationYear')"
              :min="1900"
              :max="new Date().getFullYear()"
              clearable
            />
          </n-form-item>

          <n-form-item :label="$t('admin.members.form.alumniIdentity')" v-if="batchFormData.mem_type === 2">
            <n-select
              v-model:value="batchFormData.alumni_identity"
              :options="alumniIdentityOptions"
              :placeholder="$t('admin.members.form.placeholders.alumniIdentity')"
              clearable
            />
          </n-form-item>
          
          <n-form-item :label="$t('admin.common.status')">
            <n-select
              v-model:value="batchFormData.enable"
              :options="statusOptions"
              :placeholder="$t('admin.members.placeholders.status')"
              clearable
            />
          </n-form-item>
        </n-form>
        
        <n-alert type="info" style="margin-top: 16px;">
          {{ $t('admin.members.batchEditTip', { count: selectedRowKeys.length }) }}
        </n-alert>
        
        <template #footer>
          <n-space justify="end">
            <n-button @click="showBatchModal = false">
              {{ $t('admin.common.cancel') }}
            </n-button>
            <n-button type="primary" @click="handleBatchUpdate" :loading="batchLoading">
              {{ $t('admin.common.update') }}
            </n-button>
          </n-space>
        </template>
      </n-card>
    </n-modal>

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
        <div v-if="deleteType === 'single'">
          <p>{{ $t('admin.members.deleteConfirmText') }}</p>
          <div v-if="deleteTarget" class="delete-member-info">
            <n-avatar :src="deleteTarget.mem_avatar_path ? getMediaUrl(deleteTarget.mem_avatar_path) : undefined" />
            <div class="member-details">
              <div class="member-name">{{ deleteTarget.mem_name_zh }}</div>
              <div class="member-email">{{ deleteTarget.mem_email }}</div>
            </div>
          </div>
        </div>
        <div v-else>
          <p>{{ $t('admin.members.batchDeleteConfirmText', { count: selectedRowKeys.length }) }}</p>
          <n-alert type="warning">
            {{ $t('admin.members.batchDeleteWarning') }}
          </n-alert>
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
import { useMessage, NButton, NTag, NAvatar, NSpace, zhCN, enUS, dateZhCN, dateEnUS } from 'naive-ui';
import { memberApi, researchGroupApi } from '@/services/api';
import { getMediaUrl } from '@/utils/media';
import QuickActionModal from '@/components/QuickActionModal.vue';
import type { Member, ResearchGroup, ApiError } from '@/types/api';
import type { DataTableColumns } from 'naive-ui';

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

// 響應式數據
const memberList = ref<Member[]>([]);
const loading = ref(false);
const deleteLoading = ref(false);
const showDeleteModal = ref(false);
const deleteTarget = ref<Member | null>(null);
const deleteType = ref<'single' | 'batch'>('single');

// Modal 狀態
const showCreateModal = ref(false);
const showBatchModal = ref(false);
const modalActionType = ref<'create' | 'edit'>('create');
const editData = ref<Partial<Member>>({});

// 批量操作
const selectedRowKeys = ref<number[]>([]);
const batchLoading = ref(false);
const batchFormRef = ref();
const batchFormData = reactive<Record<string, unknown>>({});

// 搜索和篩選
const searchQuery = ref('');
const filterType = ref<number | null>(null);
const filterGroup = ref<number | null>(null);

// 分頁
const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100]
});

// 課題組選項
const groupOptions = ref<Array<{ label: string; value: number; nameEn?: string }>>([]);

// 包含「無」選項的課題組選擇列表
const groupOptionsWithNone = computed(() => {
  const noneOption = {
    label: t('admin.members.form.group.none'),
    value: -1
  };
  return [noneOption, ...groupOptions.value];
});

// 選項數據
const typeOptions = computed(() => [
  { label: t('admin.common.memberTypes.teacher'), value: 0 },
  { label: t('admin.common.memberTypes.student'), value: 1 },
  { label: t('admin.common.memberTypes.alumni'), value: 2 }
]);

const jobTypeOptions = computed(() => [
  { label: t('admin.members.jobTypes.professor'), value: 0 },
  { label: t('admin.members.jobTypes.assocProfessor'), value: 1 },
  { label: t('admin.members.jobTypes.lecturer'), value: 2 },
  { label: t('admin.members.jobTypes.assistantProfessor'), value: 3 },
  { label: t('admin.members.jobTypes.postdoc'), value: 4 }
]);

const studentTypeOptions = computed(() => [
  { label: t('admin.members.studentTypes.phd'), value: 0 },
  { label: t('admin.members.studentTypes.master'), value: 1 },
  { label: t('admin.members.studentTypes.undergraduate'), value: 2 }
]);

const alumniIdentityOptions = computed(() => [
  { label: t('admin.common.alumniIdentity.phd'), value: 0 },
  { label: t('admin.common.alumniIdentity.master'), value: 1 },
  { label: t('admin.common.alumniIdentity.undergraduate'), value: 2 },
  { label: t('admin.common.alumniIdentity.teacher'), value: 3 },
  { label: t('admin.common.alumniIdentity.other'), value: 4 }
]);

const statusOptions = computed(() => [
  { label: t('admin.common.enabled'), value: 1 },
  { label: t('admin.common.disabled'), value: 0 }
]);

// 表格列定義
const columns: DataTableColumns<Member> = [
  {
    type: 'selection',
    width: 50
  },
  {
    title: t('admin.members.avatar'),
    key: 'mem_avatar_path',
    width: 80,
    render(row) {
      return h(NAvatar, {
        size: 'medium',
        src: row.mem_avatar_path ? getMediaUrl(row.mem_avatar_path) : undefined,
        fallbackSrc: '/default-avatar.svg'
      });
    }
  },
  {
    title: t('admin.members.name'),
    key: 'mem_name_zh',
    render(row) {
      return h('div', [
        h('div', { style: { fontWeight: 'bold' } }, row.mem_name_zh),
        h('div', { style: { fontSize: '0.875rem', color: '#666' } }, row.mem_name_en)
      ]);
    }
  },
  {
    title: t('admin.members.email'),
    key: 'mem_email'
  },
  {
    title: t('admin.members.type'),
    key: 'mem_type',
    width: 120,
    render(row) {
      const typeMap = {
        0: { text: t('admin.common.memberTypes.teacher'), type: 'success' as const },
        1: { text: t('admin.common.memberTypes.student'), type: 'info' as const },
        2: { text: t('admin.common.memberTypes.alumni'), type: 'warning' as const }
      };
      const config = typeMap[row.mem_type as keyof typeof typeMap];
      return h(NTag, { type: config.type }, { default: () => config.text });
    }
  },
  {
    title: t('admin.members.details'),
    key: 'details',
    width: 150,
    render(row) {
      const details = [];
      if (row.mem_type === 0 && row.job_type !== null && row.job_type !== undefined) {
        details.push(jobTypeOptions.value.find(opt => opt.value === row.job_type)?.label || '');
      }
      if (row.mem_type === 1) {
        if (row.student_type !== null && row.student_type !== undefined) {
          details.push(studentTypeOptions.value.find(opt => opt.value === row.student_type)?.label || '');
        }
        if (row.student_grade) {
          details.push(`${row.student_grade}${t('admin.members.grade')}`);
        }
      }
      return details.join(', ') || '-';
    }
  },
  {
    title: t('admin.members.group'),
    key: 'research_group_id',
    render(row) {
      const group = groupOptions.value.find(g => g.value === row.research_group_id);
      if (!group) return '-';
      
      return h('div', [
        h('div', { style: { fontSize: '0.875rem' } }, group.label),
        group.nameEn ? h('div', { style: { fontSize: '0.8rem', color: '#666', fontStyle: 'italic' } }, group.nameEn) : null
      ].filter(Boolean));
    }
  },
  {
    title: t('admin.members.status'),
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

// 獲取成員列表
const fetchMembers = async () => {
  try {
    loading.value = true;
    const params = {
      page: pagination.page,
      per_page: pagination.pageSize,
      q: searchQuery.value || undefined,
      type: filterType.value ?? undefined,
      research_group_id: filterGroup.value ?? undefined
    };

    const response = await memberApi.getMembers(params);
    if (response.code === 0) {
      memberList.value = response.data.items;
      pagination.itemCount = response.data.total;
    } else {
      message.error(response.message || t('admin.members.fetchError'));
    }
  } catch (error: unknown) {
    console.error('獲取成員列表失敗:', error);
    const apiError = error as ApiError;
    const errorMessage = apiError?.message || t('admin.members.fetchError');
    message.error(errorMessage);
  } finally {
    loading.value = false;
  }
};

// 獲取課題組列表
const fetchGroups = async () => {
  try {
    const response = await researchGroupApi.getResearchGroups({ all: 'true' });
    if (response.code === 0) {
      groupOptions.value = response.data.items.map((group: ResearchGroup) => ({
        label: group.research_group_name_zh,
        value: group.research_group_id,
        nameEn: group.research_group_name_en // 保存英文名稱
      }));
    }
  } catch (error) {
    console.error('獲取課題組列表失敗:', error);
  }
};

// 搜索處理
const handleSearch = () => {
  pagination.page = 1;
  fetchMembers();
};

// 頁面變化處理
const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchMembers();
};

// 每頁數量變化處理
const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize;
  pagination.page = 1;
  fetchMembers();
};

// Modal 處理
const handleCreate = () => {
  modalActionType.value = 'create';
  editData.value = {};
  showCreateModal.value = true;
};

const handleEdit = (member: Member) => {
  modalActionType.value = 'edit';
  editData.value = { ...member };
  showCreateModal.value = true;
};

const handleModalSuccess = () => {
  fetchMembers();
  selectedRowKeys.value = [];
};

// 處理刪除
const handleDelete = (member: Member) => {
  deleteType.value = 'single';
  deleteTarget.value = member;
  showDeleteModal.value = true;
};

const handleBatchDelete = () => {
  deleteType.value = 'batch';
  showDeleteModal.value = true;
};

// 確認刪除
const confirmDelete = async () => {
  try {
    deleteLoading.value = true;
    
    if (deleteType.value === 'single' && deleteTarget.value) {
      const response = await memberApi.deleteMember(deleteTarget.value.mem_id);
      if (response.code === 0) {
        message.success(t('admin.members.deleteSuccess'));
      } else {
        message.error(response.message || t('admin.members.deleteError'));
      }
    } else if (deleteType.value === 'batch' && selectedRowKeys.value.length > 0) {
      const response = await memberApi.deleteMembersBatch(selectedRowKeys.value);
      if (response.code === 0) {
        message.success(t('admin.members.batchDeleteSuccess', { count: selectedRowKeys.value.length }));
        selectedRowKeys.value = [];
      } else {
        message.error(response.message || t('admin.members.deleteError'));
      }
    }
    
    showDeleteModal.value = false;
    fetchMembers();
  } catch (error: unknown) {
    console.error('刪除成員失敗:', error);
    const apiError = error as ApiError;
    const errorMessage = apiError?.message || t('admin.members.deleteError');
    message.error(errorMessage);
  } finally {
    deleteLoading.value = false;
  }
};

// 批量更新處理
const handleBatchUpdate = async () => {
  try {
    batchLoading.value = true;
    
    // 過濾掉空值和不適用的條件性字段
    const updates = Object.keys(batchFormData)
      .filter(key => {
        const value = batchFormData[key];
        // 排除 null, undefined
        if (value === null || value === undefined) {
          return false;
        }
        
        // 對批量更新的條件性字段進行檢查
        // 如果選擇了特定成員類型，只包含適用於該類型的字段
        if (batchFormData.mem_type !== null && batchFormData.mem_type !== undefined) {
          const memberType = batchFormData.mem_type as number;
          
          // 教師類型：排除學生和校友字段
          if (memberType === 0 && ['student_type', 'student_grade', 'graduation_year', 'alumni_identity'].includes(key)) {
            return false;
          }
          
          // 學生類型：排除教師和校友字段  
          if (memberType === 1 && ['job_type', 'graduation_year', 'alumni_identity'].includes(key)) {
            return false;
          }
          
          // 校友類型：排除教師和學生字段
          if (memberType === 2 && ['job_type', 'student_type', 'student_grade'].includes(key)) {
            return false;
          }
        }
        
        return true;
      })
      .reduce((acc, key) => {
        let value = batchFormData[key];
        
        // 特殊處理：research_group_id 為 -1 時轉換為 null（代表選擇了「無」）
        if (key === 'research_group_id' && value === -1) {
          value = null;
        }
        
        acc[key] = value;
        return acc;
      }, {} as Record<string, unknown>);
    
    if (Object.keys(updates).length === 0) {
      message.warning(t('admin.members.noUpdatesSelected'));
      return;
    }
    
    console.log('批量更新數據:', { member_ids: selectedRowKeys.value, updates });
    
    const response = await memberApi.updateMembersBatch(selectedRowKeys.value, updates);
    if (response.code === 0) {
      message.success(t('admin.members.batchUpdateSuccess', { count: selectedRowKeys.value.length }));
      showBatchModal.value = false;
      selectedRowKeys.value = [];
      Object.keys(batchFormData).forEach(key => {
        batchFormData[key] = undefined;
      });
      fetchMembers();
    } else {
      message.error(response.message || t('admin.members.updateError'));
    }
  } catch (error: unknown) {
    console.error('批量更新失敗:', error);
    const apiError = error as ApiError;
    const errorMessage = apiError?.message || t('admin.members.updateError');
    message.error(errorMessage);
  } finally {
    batchLoading.value = false;
  }
};

// 生命週期
onMounted(() => {
  fetchMembers();
  fetchGroups();
});
</script>

<style scoped>
.member-manage {
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

.delete-member-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 16px 0;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.member-details {
  flex: 1;
}

.member-name {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
}

.member-email {
  color: #666;
  font-size: 14px;
}

/* 暗色主題 */
[data-theme="dark"] .page-header h2,
.dark .page-header h2,
.dark-theme .page-header h2 {
  color: #f9fafb !important;
}

[data-theme="dark"] .delete-member-info,
.dark .delete-member-info {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .member-email,
.dark .member-email {
  color: #ccc;
}

.table-container {
  overflow-x: auto;
  min-width: 0;
  width: 100%;
}

/* 手機端響應式優化 */
@media (max-width: 768px) {
  .table-container {
    margin: -16px -20px;
    padding: 16px 20px;
    border-radius: 0;
  }
  
  /* 設置表格最小寬度以觸發滾動 */
  :deep(.n-data-table-wrapper) {
    min-width: 1200px;
  }
}
</style>