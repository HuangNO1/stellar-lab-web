<template>
  <div class="admin-dashboard">
    <!-- 概覽卡片 -->
    <div class="overview-cards">
      <n-card class="overview-card">
        <div class="card-content">
          <div class="card-icon members">
            <n-icon size="24">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M16,4C18.2,4 20,5.8 20,8A4,4 0 0,1 16,12A4,4 0 0,1 12,8A4,4 0 0,1 16,4M16,14C18.25,14 22,15.13 22,17.25V20H10V17.25C10,15.13 13.75,14 16,14Z"/>
              </svg>
            </n-icon>
          </div>
          <div class="card-info">
            <div class="card-number">{{ stats.members }}</div>
            <div class="card-title">{{ $t('admin.dashboard.totalMembers') }}</div>
          </div>
        </div>
      </n-card>

      <n-card class="overview-card">
        <div class="card-content">
          <div class="card-icon papers">
            <n-icon size="24">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
            </n-icon>
          </div>
          <div class="card-info">
            <div class="card-number">{{ stats.papers }}</div>
            <div class="card-title">{{ $t('admin.dashboard.totalPapers') }}</div>
          </div>
        </div>
      </n-card>

      <n-card class="overview-card">
        <div class="card-content">
          <div class="card-icon projects">
            <n-icon size="24">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,3H5C3.9,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.9 20.1,3 19,3M19,19H5V8H19V19Z"/>
              </svg>
            </n-icon>
          </div>
          <div class="card-info">
            <div class="card-number">{{ stats.projects }}</div>
            <div class="card-title">{{ $t('admin.dashboard.totalProjects') }}</div>
          </div>
        </div>
      </n-card>

      <n-card class="overview-card">
        <div class="card-content">
          <div class="card-icon news">
            <n-icon size="24">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M20,11H23V13H20V11M1,11H4V13H1V11M13,1V4H11V1H13M4.92,3.5L7.05,5.64L5.63,7.05L3.5,4.93L4.92,3.5Z"/>
              </svg>
            </n-icon>
          </div>
          <div class="card-info">
            <div class="card-number">{{ stats.news }}</div>
            <div class="card-title">{{ $t('admin.dashboard.totalNews') }}</div>
          </div>
        </div>
      </n-card>
    </div>

    <!-- 快速操作和最近活動 -->
    <div class="dashboard-content">
      <div class="left-panel">
        <!-- 快速操作 -->
        <n-card :title="$t('admin.dashboard.quickActions')" class="quick-actions">
          <div class="action-buttons">
            <n-button type="primary" @click="openModal('members', 'create')">
              <template #icon>
                <n-icon>
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M15,14C17.67,14 23,15.33 23,18V20H7V18C7,15.33 12.33,14 15,14M15,12A4,4 0 0,1 11,8A4,4 0 0,1 15,4A4,4 0 0,1 19,8A4,4 0 0,1 15,12M5,9.59L7.12,7.46L8.54,8.88L5,12.41L2.88,10.29L4.29,8.88L5,9.59Z"/>
                  </svg>
                </n-icon>
              </template>
              {{ $t('admin.dashboard.addMember') }}
            </n-button>

            <n-button type="info" @click="openModal('papers', 'create')">
              <template #icon>
                <n-icon>
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                  </svg>
                </n-icon>
              </template>
              {{ $t('admin.dashboard.addPaper') }}
            </n-button>

            <n-button type="success" @click="openModal('projects', 'create')">
              <template #icon>
                <n-icon>
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                  </svg>
                </n-icon>
              </template>
              {{ $t('admin.dashboard.addProject') }}
            </n-button>

            <n-button type="warning" @click="openModal('news', 'create')">
              <template #icon>
                <n-icon>
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                  </svg>
                </n-icon>
              </template>
              {{ $t('admin.dashboard.addNews') }}
            </n-button>

            <n-button type="default" @click="openModal('research-groups', 'create')">
              <template #icon>
                <n-icon>
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M12,5.5A3.5,3.5 0 0,1 15.5,9A3.5,3.5 0 0,1 12,12.5A3.5,3.5 0 0,1 8.5,9A3.5,3.5 0 0,1 12,5.5M5,8C5.56,8 6.08,8.15 6.53,8.42C6.38,9.85 6.8,11.27 7.66,12.38C7.16,13.34 6.16,14 5,14A3,3 0 0,1 2,11A3,3 0 0,1 5,8M19,8A3,3 0 0,1 22,11A3,3 0 0,1 19,14C17.84,14 16.84,13.34 16.34,12.38C17.2,11.27 17.62,9.85 17.47,8.42C17.92,8.15 18.44,8 19,8M5.5,18.25C5.5,16.18 8.41,14.5 12,14.5C15.59,14.5 18.5,16.18 18.5,18.25V20H5.5V18.25Z"/>
                  </svg>
                </n-icon>
              </template>
              新增課題組
            </n-button>
          </div>
        </n-card>

        <!-- 系統狀態 -->
        <n-card :title="$t('admin.dashboard.systemStatus')" class="system-status">
          <div class="status-items">
            <div class="status-item">
              <div class="status-icon success">
                <n-icon size="16">
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
                  </svg>
                </n-icon>
              </div>
              <div class="status-info">
                <div class="status-title">{{ $t('admin.dashboard.apiStatus') }}</div>
                <div class="status-value">{{ $t('admin.dashboard.online') }}</div>
              </div>
            </div>

            <div class="status-item">
              <div class="status-icon success">
                <n-icon size="16">
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
                  </svg>
                </n-icon>
              </div>
              <div class="status-info">
                <div class="status-title">{{ $t('admin.dashboard.databaseStatus') }}</div>
                <div class="status-value">{{ $t('admin.dashboard.normal') }}</div>
              </div>
            </div>

            <div class="status-item">
              <div class="status-icon success">
                <n-icon size="16">
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
                  </svg>
                </n-icon>
              </div>
              <div class="status-info">
                <div class="status-title">{{ $t('admin.dashboard.mediaStatus') }}</div>
                <div class="status-value">{{ $t('admin.dashboard.normal') }}</div>
              </div>
            </div>
          </div>
        </n-card>
      </div>

      <div class="right-panel">
        <!-- 最近活動 -->
        <n-card :title="$t('admin.dashboard.recentActivities')" class="recent-activities">
          <n-list>
            <n-list-item v-for="activity in recentActivities" :key="activity.id">
              <div class="activity-item">
                <div class="activity-icon">
                  <n-icon size="16" :color="getActivityColor(activity.type)">
                    <component :is="getActivityIcon(activity.type)" />
                  </n-icon>
                </div>
                <div class="activity-content">
                  <div class="activity-title">{{ activity.title }}</div>
                  <div class="activity-time">{{ formatTime(activity.time) }}</div>
                </div>
              </div>
            </n-list-item>
          </n-list>

          <div v-if="recentActivities.length === 0" class="empty-activities">
            <n-empty :description="$t('admin.dashboard.noActivities')" />
          </div>
        </n-card>

        <!-- 待辦事項 -->
        <n-card :title="$t('admin.dashboard.todoList')" class="todo-list">
          <div class="todo-items">
            <div class="todo-item">
              <n-checkbox>
                {{ $t('admin.dashboard.reviewPapers') }}
              </n-checkbox>
            </div>
            <div class="todo-item">
              <n-checkbox>
                {{ $t('admin.dashboard.updateLabInfo') }}
              </n-checkbox>
            </div>
            <div class="todo-item">
              <n-checkbox>
                {{ $t('admin.dashboard.checkNews') }}
              </n-checkbox>
            </div>
          </div>
        </n-card>
      </div>
    </div>

    <!-- 快速操作 Modal -->
    <QuickActionModal
      v-model="showModal"
      :module-type="modalConfig.moduleType"
      :action-type="modalConfig.actionType"
      :edit-data="modalConfig.editData"
      @success="handleModalSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, h } from 'vue';
import { memberApi, paperApi, projectApi, newsApi } from '@/services/api';
import QuickActionModal from '@/components/QuickActionModal.vue';

// 統計數據
const stats = reactive({
  members: 0,
  papers: 0,
  projects: 0,
  news: 0
});

// 最近活動
const recentActivities = ref<Array<{
  id: string;
  type: 'create' | 'update' | 'delete';
  title: string;
  time: Date;
}>>([]);

// Modal 狀態
const showModal = ref(false);
const modalConfig = reactive({
  moduleType: 'members' as 'members' | 'papers' | 'projects' | 'news' | 'research-groups',
  actionType: 'create' as 'create' | 'edit',
  editData: {}
});

// 獲取統計數據
const fetchStats = async () => {
  try {
    const [membersRes, papersRes, projectsRes, newsRes] = await Promise.all([
      memberApi.getMembers({ all: 'true' }),
      paperApi.getPapers({ all: 'true' }),
      projectApi.getProjects({ all: 'true' }),
      newsApi.getNews({ all: 'true' })
    ]);

    if (membersRes.code === 0) {
      stats.members = membersRes.data.total || membersRes.data.items?.length || 0;
    }
    if (papersRes.code === 0) {
      stats.papers = papersRes.data.total || papersRes.data.items?.length || 0;
    }
    if (projectsRes.code === 0) {
      stats.projects = projectsRes.data.total || projectsRes.data.items?.length || 0;
    }
    if (newsRes.code === 0) {
      stats.news = newsRes.data.total || newsRes.data.items?.length || 0;
    }
  } catch (error) {
    console.error('獲取統計數據失敗:', error);
  }
};

// 獲取活動類型對應的顏色
const getActivityColor = (type: string) => {
  const colors = {
    create: '#52c41a',
    update: '#1890ff',
    delete: '#ff4d4f'
  };
  return colors[type as keyof typeof colors] || '#666';
};

// 獲取活動類型對應的圖標
const getActivityIcon = (type: string) => {
  const icons = {
    create: () => h('svg', { viewBox: '0 0 24 24' }, [
      h('path', { fill: 'currentColor', d: 'M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z' })
    ]),
    update: () => h('svg', { viewBox: '0 0 24 24' }, [
      h('path', { fill: 'currentColor', d: 'M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z' })
    ]),
    delete: () => h('svg', { viewBox: '0 0 24 24' }, [
      h('path', { fill: 'currentColor', d: 'M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z' })
    ])
  };
  return icons[type as keyof typeof icons] || icons.create;
};

// 格式化時間
const formatTime = (time: Date) => {
  const now = new Date();
  const diff = now.getTime() - time.getTime();
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) {
    return `${days}天前`;
  } else if (hours > 0) {
    return `${hours}小時前`;
  } else if (minutes > 0) {
    return `${minutes}分鐘前`;
  } else {
    return '剛剛';
  }
};

// 打開 Modal
const openModal = (
  moduleType: 'members' | 'papers' | 'projects' | 'news' | 'research-groups',
  actionType: 'create' | 'edit',
  editData: any = {}
) => {
  modalConfig.moduleType = moduleType;
  modalConfig.actionType = actionType;
  modalConfig.editData = editData;
  showModal.value = true;
};

// 處理 Modal 成功
const handleModalSuccess = () => {
  // 刷新統計數據
  fetchStats();
  
  // 添加活動記錄
  const moduleNames = {
    members: '成員',
    papers: '論文',
    projects: '項目',
    news: '新聞',
    'research-groups': '課題組'
  };
  
  const actionNames = {
    create: '新增',
    edit: '編輯'
  };
  
  const activity = {
    id: Date.now().toString(),
    type: modalConfig.actionType === 'create' ? 'create' as const : 'update' as const,
    title: `${actionNames[modalConfig.actionType]}了${moduleNames[modalConfig.moduleType]}`,
    time: new Date()
  };
  
  recentActivities.value.unshift(activity);
  // 只保留最近 10 條記錄
  if (recentActivities.value.length > 10) {
    recentActivities.value = recentActivities.value.slice(0, 10);
  }
};

onMounted(() => {
  fetchStats();
});
</script>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.overview-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.overview-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.card-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-icon.members {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon.papers {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-icon.projects {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.card-icon.news {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.card-info {
  flex: 1;
}

.card-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.card-title {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.5rem;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.left-panel,
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.action-buttons .n-button:nth-child(5) {
  grid-column: 1 / -1;
}

.status-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.status-icon.success {
  background-color: #52c41a;
}

.status-info {
  flex: 1;
}

.status-title {
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

.status-value {
  font-size: 0.75rem;
  color: #6b7280;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

.activity-time {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.empty-activities {
  padding: 2rem 0;
  text-align: center;
}

.todo-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.todo-item {
  padding: 0.5rem 0;
}

/* 暗色主題 */
[data-theme="dark"] .card-number,
.dark .card-number {
  color: #f9fafb;
}

[data-theme="dark"] .card-title,
.dark .card-title {
  color: #9ca3af;
}

[data-theme="dark"] .status-title,
.dark .status-title {
  color: #f3f4f6;
}

[data-theme="dark"] .status-value,
.dark .status-value {
  color: #9ca3af;
}

[data-theme="dark"] .activity-title,
.dark .activity-title {
  color: #f3f4f6;
}

[data-theme="dark"] .activity-time,
.dark .activity-time {
  color: #9ca3af;
}

[data-theme="dark"] .activity-icon,
.dark .activity-icon {
  background-color: rgba(255, 255, 255, 0.1);
}

/* 響應式設計 */
@media (max-width: 768px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
  }
  
  .overview-cards {
    grid-template-columns: 1fr;
  }
}
</style>