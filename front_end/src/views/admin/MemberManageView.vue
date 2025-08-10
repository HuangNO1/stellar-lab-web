<template>
  <div class="member-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.members') }}</h2>
      <n-button type="primary" @click="router.push('/admin/members/create')">
        <template #icon>
          <n-icon>
            <svg viewBox="0 0 24 24">
              <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
            </svg>
          </n-icon>
        </template>
        {{ $t('admin.members.addMember') }}
      </n-button>
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
      <n-data-table
        :columns="columns"
        :data="memberList"
        :pagination="pagination"
        :loading="loading"
        :remote="true"
        @update:page="handlePageChange"
        @update:page-size="handlePageSizeChange"
      />
    </n-card>

    <!-- 刪除確認對話框 -->
    <n-modal v-model:show="showDeleteModal">
      <n-card
        style="width: 400px;"
        :title="$t('admin.common.confirmDelete')"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
      >
        <p>{{ $t('admin.members.deleteConfirmText') }}</p>
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
import { ref, reactive, onMounted, h } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useMessage, NButton, NTag, NAvatar, NSpace } from 'naive-ui';
import { memberApi, researchGroupApi } from '@/services/api';
import { getMediaUrl } from '@/utils/media';
import type { Member, ResearchGroup } from '@/types/api';
import type { DataTableColumns } from 'naive-ui';

const router = useRouter();
const { t } = useI18n();
const message = useMessage();

// 響應式數據
const memberList = ref<Member[]>([]);
const loading = ref(false);
const deleteLoading = ref(false);
const showDeleteModal = ref(false);
const deleteTarget = ref<Member | null>(null);

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
const groupOptions = ref<Array<{ label: string; value: number }>>([]);

// 成員類型選項
const typeOptions = [
  { label: t('members.professor'), value: 0 },
  { label: t('members.student'), value: 1 },
  { label: t('members.others'), value: 2 }
];

// 表格列定義
const columns: DataTableColumns<Member> = [
  {
    title: t('admin.members.avatar'),
    key: 'mem_avatar_path',
    width: 80,
    render(row) {
      return h(NAvatar, {
        size: 'medium',
        src: row.mem_avatar_path ? getMediaUrl(row.mem_avatar_path) : undefined,
        fallbackSrc: '/default-avatar.png'
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
        0: { text: t('members.professor'), type: 'success' as const },
        1: { text: t('members.student'), type: 'info' as const },
        2: { text: t('members.others'), type: 'default' as const }
      };
      const config = typeMap[row.mem_type as keyof typeof typeMap];
      return h(NTag, { type: config.type }, { default: () => config.text });
    }
  },
  {
    title: t('admin.members.group'),
    key: 'research_group_id',
    render(row) {
      // 這裡需要從關聯數據獲取課題組名稱
      return row.research_group?.research_group_name_zh || '-';
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
    width: 200,
    render(row) {
      return h(NSpace, [
        h(NButton, {
          size: 'small',
          type: 'primary',
          onClick: () => router.push(`/admin/members/${row.mem_id}/edit`)
        }, { default: () => t('admin.common.edit') }),
        h(NButton, {
          size: 'small',
          type: 'error',
          onClick: () => handleDelete(row)
        }, { default: () => t('admin.common.delete') })
      ]);
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
  } catch (error) {
    console.error('獲取成員列表失敗:', error);
    message.error(t('admin.members.fetchError'));
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
        value: group.research_group_id
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

// 處理刪除
const handleDelete = (member: Member) => {
  deleteTarget.value = member;
  showDeleteModal.value = true;
};

// 確認刪除
const confirmDelete = async () => {
  if (!deleteTarget.value) return;

  try {
    deleteLoading.value = true;
    const response = await memberApi.deleteMember(deleteTarget.value.mem_id);
    
    if (response.code === 0) {
      message.success(t('admin.members.deleteSuccess'));
      showDeleteModal.value = false;
      fetchMembers();
    } else {
      message.error(response.message || t('admin.members.deleteError'));
    }
  } catch (error) {
    console.error('刪除成員失敗:', error);
    message.error(t('admin.members.deleteError'));
  } finally {
    deleteLoading.value = false;
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

/* 暗色主題 */
[data-theme="dark"] .page-header h2,
.dark .page-header h2 {
  color: #f9fafb;
}
</style>