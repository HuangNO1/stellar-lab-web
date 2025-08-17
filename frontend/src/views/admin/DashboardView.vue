<template>
  <div class="admin-dashboard">
    <!-- 概覽卡片 -->
    <div class="overview-cards">
      <n-card class="overview-card">
        <div class="card-content">
          <div class="card-icon members">
            <n-icon size="24">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
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
                <path fill="currentColor" d="M20,11H23V13H20V11M1,11H4V13H1V11M13,1V4H11V1H13M4.92,3.5L7.05,5.64L5.63,7.05L3.5,4.93L4.92,3.5M16.95,5.63L19.07,3.5L20.5,4.93L18.37,7.05L16.95,5.63M12,6A6,6 0 0,1 18,12C18,14.22 16.79,16.16 15,17.2V19A1,1 0 0,1 14,20H10A1,1 0 0,1 9,19V17.2C7.21,16.16 6,14.22 6,12A6,6 0 0,1 12,6M14,21V22A1,1 0 0,1 13,23H11A1,1 0 0,1 10,22V21H14M11,18H13V15.87C14.73,15.43 16,13.86 16,12A4,4 0 0,0 8,12C8,13.86 9.27,15.43 11,15.87V18Z"/>
              </svg>
            </n-icon>
          </div>
          <div class="card-info">
            <div class="card-number">{{ stats.news }}</div>
            <div class="card-title">{{ $t('admin.dashboard.totalNews') }}</div>
          </div>
        </div>
      </n-card>

      <n-card class="overview-card">
        <div class="card-content">
          <div class="card-icon resources">
            <n-icon size="24">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M20,6C20,4.89 19.11,4 18,4H12V2A2,2 0 0,0 10,0H4A2,2 0 0,0 2,2V18A2,2 0 0,0 4,20H18A2,2 0 0,0 20,18V6M18,18H4V2H10V6H18V18Z"/>
              </svg>
            </n-icon>
          </div>
          <div class="card-info">
            <div class="card-number">{{ stats.resources }}</div>
            <div class="card-title">{{ $t('admin.dashboard.totalResources') }}</div>
          </div>
        </div>
      </n-card>

      <n-card class="overview-card">
        <div class="card-content">
          <div class="card-icon groups">
            <n-icon size="24">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M12,5.5A3.5,3.5 0 0,1 15.5,9A3.5,3.5 0 0,1 12,12.5A3.5,3.5 0 0,1 8.5,9A3.5,3.5 0 0,1 12,5.5M5,8C5.56,8 6.08,8.15 6.53,8.42C6.38,9.85 6.8,11.27 7.66,12.38C7.16,13.34 6.16,14 5,14A3,3 0 0,1 2,11A3,3 0 0,1 5,8M19,8A3,3 0 0,1 22,11A3,3 0 0,1 19,14C17.84,14 16.84,13.34 16.34,12.38C17.2,11.27 17.62,9.85 17.47,8.42C17.92,8.15 18.44,8 19,8M5.5,18.25C5.5,16.18 8.41,14.5 12,14.5C15.59,14.5 18.5,16.18 18.5,18.25V20H5.5V18.25Z"/>
              </svg>
            </n-icon>
          </div>
          <div class="card-info">
            <div class="card-number">{{ stats.researchGroups }}</div>
            <div class="card-title">{{ $t('admin.dashboard.totalGroups') }}</div>
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
              {{ $t('admin.groups.addGroup') }}
            </n-button>

            <n-button type="tertiary" @click="openModal('resources', 'create')">
              <template #icon>
                <n-icon>
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M20,6C20,4.89 19.11,4 18,4H12V2A2,2 0 0,0 10,0H4A2,2 0 0,0 2,2V18A2,2 0 0,0 4,20H18A2,2 0 0,0 20,18V6M18,18H4V2H10V6H18V18Z"/>
                  </svg>
                </n-icon>
              </template>
              {{ $t('admin.dashboard.addResource') }}
            </n-button>
          </div>
        </n-card>

        <!-- 系統狀態 -->
        <n-card :title="$t('admin.dashboard.systemStatus')" class="system-status">
          <div class="status-items">
            <div class="status-item">
              <div class="status-icon" :class="getStatusIconClass(systemStatus.api.status)">
                <n-spin v-if="systemStatus.api.loading" size="small" />
                <n-icon v-else size="16">
                  <svg v-if="systemStatus.api.status === 'online'" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
                  </svg>
                </n-icon>
              </div>
              <div class="status-info">
                <div class="status-title">{{ $t('admin.dashboard.apiStatus') }}</div>
                <div class="status-value">{{ getStatusText(systemStatus.api.status, systemStatus.api.loading) }}</div>
              </div>
            </div>

            <div class="status-item">
              <div class="status-icon" :class="getStatusIconClass(systemStatus.database.status)">
                <n-spin v-if="systemStatus.database.loading" size="small" />
                <n-icon v-else size="16">
                  <svg v-if="systemStatus.database.status === 'normal'" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
                  </svg>
                </n-icon>
              </div>
              <div class="status-info">
                <div class="status-title">{{ $t('admin.dashboard.databaseStatus') }}</div>
                <div class="status-value">{{ getStatusText(systemStatus.database.status, systemStatus.database.loading) }}</div>
              </div>
            </div>

            <div class="status-item">
              <div class="status-icon" :class="getStatusIconClass(systemStatus.media.status)">
                <n-spin v-if="systemStatus.media.loading" size="small" />
                <n-icon v-else size="16">
                  <svg v-if="systemStatus.media.status === 'normal'" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
                  </svg>
                </n-icon>
              </div>
              <div class="status-info">
                <div class="status-title">{{ $t('admin.dashboard.mediaStatus') }}</div>
                <div class="status-value">{{ getStatusText(systemStatus.media.status, systemStatus.media.loading) }}</div>
              </div>
            </div>
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
import { useI18n } from 'vue-i18n';
import { memberApi, paperApi, projectApi, newsApi, editRecordApi, systemApi, resourceApi, researchGroupApi } from '@/services/api';
import type { EditRecord } from '@/types/api';
import QuickActionModal from '@/components/QuickActionModal.vue';
import { useTimeFormatter } from '@/utils/timezone';

const { t, locale } = useI18n();
const { formatRelativeTime } = useTimeFormatter();

// 統計數據
const stats = reactive({
  members: 0,
  papers: 0,
  projects: 0,
  news: 0,
  resources: 0,
  researchGroups: 0
});

// 最近活動
const recentActivities = ref<Array<{
  id: string;
  type: 'create' | 'update' | 'delete' | 'login' | 'logout' | 'change_password' | 'batch_delete' | 'batch_update' | 'upload';
  title: string;
  time: string; // 改為字符串類型存儲 UTC 時間
  admin: string;
}>>([]);

// 系統狀態
const systemStatus = reactive({
  api: {
    status: 'unknown' as 'online' | 'offline' | 'unknown',
    loading: true
  },
  database: {
    status: 'unknown' as 'normal' | 'error' | 'unknown',
    loading: true
  },
  media: {
    status: 'unknown' as 'normal' | 'error' | 'unknown',
    loading: true
  }
});

// Modal 狀態
const showModal = ref(false);
const modalConfig = reactive({
  moduleType: 'members' as 'members' | 'papers' | 'projects' | 'news' | 'research-groups' | 'resources',
  actionType: 'create' as 'create' | 'edit',
  editData: {}
});

// 獲取最近活動
const fetchRecentActivities = async () => {
  try {
    const response = await editRecordApi.getEditRecords({
      page: 1,
      per_page: 10
    });
    
    if (response.code === 0 && response.data.items) {
      recentActivities.value = response.data.items.map((log: EditRecord) => {
        const moduleNames = {
          0: t('admin.operationLogs.adminModule'),
          1: t('admin.operationLogs.labModule'),
          2: t('admin.operationLogs.groupModule'),
          3: t('admin.operationLogs.memberModule'),
          4: t('admin.operationLogs.paperModule'),
          5: t('admin.operationLogs.newsModule'),
          6: t('admin.operationLogs.projectModule'),
          7: t('admin.operationLogs.resourceModule')
        };
        
        const actionNames = {
          'CREATE': t('admin.operationLogs.create'),
          'UPDATE': t('admin.operationLogs.update'),
          'DELETE': t('admin.operationLogs.delete'),
          'LOGIN': t('admin.operationLogs.login'),
          'LOGOUT': t('admin.operationLogs.logout'),
          'CHANGE_PASSWORD': t('admin.operationLogs.changePassword'),
          'BATCH_DELETE': t('admin.operationLogs.batchDelete'),
          'BATCH_UPDATE': t('admin.operationLogs.batchUpdate'),
          'UPLOAD': t('admin.operationLogs.upload')
        };
        
        const moduleName = moduleNames[log.edit_module as keyof typeof moduleNames] || `模組 ${log.edit_module}`;
        const actionName = actionNames[log.edit_type as keyof typeof actionNames] || log.edit_type;
        
        return {
          id: log.edit_id.toString(),
          type: log.edit_type.toLowerCase().replace('_', '_') as 'create' | 'update' | 'delete' | 'login' | 'logout' | 'change_password' | 'batch_delete' | 'batch_update' | 'upload',
          title: `${log.admin?.admin_name || 'Unknown'} ${actionName}了${moduleName}`,
          time: log.edit_date, // 保持原始 UTC 時間字符串
          admin: log.admin?.admin_name || 'Unknown'
        };
      });
    }
  } catch (error) {
    console.error('獲取最近活動失敗:', error);
    // 發生錯誤時顯示空狀態
    recentActivities.value = [];
  }
};

// 獲取統計數據
const fetchStats = async () => {
  try {
    const [membersRes, papersRes, projectsRes, newsRes, resourcesRes, groupsRes] = await Promise.all([
      memberApi.getMembers({ all: 'true' }),
      paperApi.getPapers({ all: 'true' }),
      projectApi.getProjects({ all: 'true' }),
      newsApi.getNews({ all: 'true' }),
      resourceApi.getAdminResources({ all: 'true' }),
      researchGroupApi.getResearchGroups({ all: 'true' })
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
    if (resourcesRes.code === 0) {
      stats.resources = resourcesRes.data.total || resourcesRes.data.items?.length || 0;
    }
    if (groupsRes.code === 0) {
      stats.researchGroups = groupsRes.data.total || groupsRes.data.items?.length || 0;
    }
  } catch (error) {
    console.error('獲取統計數據失敗:', error);
  }
};

// 獲取系統健康狀態
const fetchSystemHealth = async () => {
  try {
    // 檢查API狀態
    systemStatus.api.loading = true;
    systemStatus.database.loading = true;
    systemStatus.media.loading = true;
    
    const response = await systemApi.healthCheck();
    console.log('Health check response:', response);
    
    // 健康檢查接口直接返回數據，不是標準的 { code: 0, data: {...} } 格式
    if (response && response.status) {
      const { status, message, timestamp, version } = response;
      console.log('Health check data:', { status, message, timestamp, version });
      
      if (status === 'healthy') {
        systemStatus.api.status = 'online';
        // 假設API正常表示數據庫也正常
        systemStatus.database.status = 'normal';
        // 假設API正常表示媒體服務也正常  
        systemStatus.media.status = 'normal';
        console.log('All systems set to healthy');
      } else {
        systemStatus.api.status = 'offline';
        systemStatus.database.status = 'error';
        systemStatus.media.status = 'error';
        console.log('Systems set to error, status:', status);
      }
    } else {
      console.log('Health check response invalid:', response);
      systemStatus.api.status = 'offline';
      systemStatus.database.status = 'error';
      systemStatus.media.status = 'error';
    }
  } catch (error) {
    console.error('獲取系統健康狀態失敗:', error);
    systemStatus.api.status = 'offline';
    systemStatus.database.status = 'error';
    systemStatus.media.status = 'error';
  } finally {
    systemStatus.api.loading = false;
    systemStatus.database.loading = false;
    systemStatus.media.loading = false;
  }
};

// 獲取活動類型對應的顏色
const getActivityColor = (type: string) => {
  const colors = {
    create: '#52c41a',
    update: '#1890ff',
    delete: '#ff4d4f',
    login: '#722ed1',
    logout: '#fa8c16',
    change_password: '#eb2f96',
    batch_delete: '#f5222d',
    batch_update: '#13c2c2',
    upload: '#52c41a'
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
    ]),
    login: () => h('svg', { viewBox: '0 0 24 24' }, [
      h('path', { fill: 'currentColor', d: 'M10,17V14H3V10H10V7L15,12L10,17M10,2H19A2,2 0 0,1 21,4V20A2,2 0 0,1 19,22H10A2,2 0 0,1 8,20V18H10V20H19V4H10V6H8V4A2,2 0 0,1 10,2Z' })
    ]),
    logout: () => h('svg', { viewBox: '0 0 24 24' }, [
      h('path', { fill: 'currentColor', d: 'M16,17V14H9V10H16V7L21,12L16,17M14,2A2,2 0 0,1 16,4V6H14V4H5V20H14V18H16V20A2,2 0 0,1 14,22H5A2,2 0 0,1 3,20V4A2,2 0 0,1 5,2H14Z' })
    ]),
    change_password: () => h('svg', { viewBox: '0 0 24 24' }, [
      h('path', { fill: 'currentColor', d: 'M6,14A3,3 0 0,1 9,11A3,3 0 0,1 12,14A3,3 0 0,1 9,17A3,3 0 0,1 6,14M12,20H2V18C2,15.79 4.69,14 8,14H10C13.31,14 16,15.79 16,18V20H14M22,15V9H20L19,10H17V15A2,2 0 0,0 19,17H21A2,2 0 0,0 23,15M19,15V10H21V15H19Z' })
    ]),
    batch_delete: () => h('svg', { viewBox: '0 0 24 24' }, [
      h('path', { fill: 'currentColor', d: 'M20.37,8.91L19.37,10.64L7.24,3.64L8.24,1.91L11.28,3.66L12.64,3.29L16.97,5.79L17.34,7.16L20.37,8.91M6,19V7H11.07L18,11V19A2,2 0 0,1 16,21H8A2,2 0 0,1 6,19Z' })
    ]),
    batch_update: () => h('svg', { viewBox: '0 0 24 24' }, [
      h('path', { fill: 'currentColor', d: 'M17,13H13V17H11V13H7V11H11V7H13V11H17M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z' })
    ]),
    upload: () => h('svg', { viewBox: '0 0 24 24' }, [
      h('path', { fill: 'currentColor', d: 'M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z' })
    ])
  };
  return icons[type as keyof typeof icons] || icons.create;
};

// 格式化時間 - 使用新的時區處理工具
const formatTime = (utcTimeString: string) => {
  return formatRelativeTime(utcTimeString);
};

// 獲取狀態圖標類
const getStatusIconClass = (status: string) => {
  if (status === 'online' || status === 'normal') {
    return 'success';
  } else if (status === 'offline' || status === 'error') {
    return 'error';
  } else {
    return 'warning';
  }
};

// 獲取狀態文字
const getStatusText = (status: string, loading: boolean) => {
  if (loading) {
    return t('admin.dashboard.checking');
  }
  
  switch (status) {
    case 'online':
      return t('admin.dashboard.online');
    case 'offline':
      return t('admin.dashboard.offline');
    case 'normal':
      return t('admin.dashboard.normal');
    case 'error':
      return t('admin.dashboard.error');
    default:
      return t('admin.dashboard.unknown');
  }
};

// 打開 Modal
const openModal = (
  moduleType: 'members' | 'papers' | 'projects' | 'news' | 'research-groups' | 'resources',
  actionType: 'create' | 'edit',
  editData: Record<string, unknown> = {}
) => {
  modalConfig.moduleType = moduleType;
  modalConfig.actionType = actionType;
  modalConfig.editData = editData;
  showModal.value = true;
};

// 處理 Modal 成功
const handleModalSuccess = () => {
  // 刷新統計數據和最近活動
  fetchStats();
  fetchRecentActivities();
  
  // 添加臨時活動記錄（實際的記錄會通過 fetchRecentActivities 獲取）
  const moduleNames = {
    members: t('admin.quickAction.activities.moduleNames.members'),
    papers: t('admin.quickAction.activities.moduleNames.papers'),
    projects: t('admin.quickAction.activities.moduleNames.projects'),
    news: t('admin.quickAction.activities.moduleNames.news'),
    'research-groups': t('admin.quickAction.activities.moduleNames.groups'),
    resources: t('admin.quickAction.activities.moduleNames.resources')
  };
  
  const actionNames = {
    create: t('admin.quickAction.activities.created'),
    edit: t('admin.quickAction.activities.updated')
  };
  
  const activity = {
    id: Date.now().toString(),
    type: modalConfig.actionType === 'create' ? 'create' as const : 'update' as const,
    title: `${actionNames[modalConfig.actionType]}${moduleNames[modalConfig.moduleType]}`,
    time: new Date().toISOString(), // 使用 ISO 字符串格式
    admin: 'Current Admin' // 臨時值，真實數據會從API獲取
  };
  
  // 臨時添加到列表開頭，真實數據會在 fetchRecentActivities 完成後替換
  recentActivities.value.unshift(activity);
  if (recentActivities.value.length > 10) {
    recentActivities.value = recentActivities.value.slice(0, 10);
  }
};

onMounted(() => {
  fetchStats();
  fetchRecentActivities();
  fetchSystemHealth();
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
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  position: relative;
}

.card-icon :deep(.n-icon) {
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon :deep(svg) {
  width: 24px;
  height: 24px;
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

.card-icon.resources {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.card-icon.groups {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
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

.status-icon.error {
  background-color: #ff4d4f;
}

.status-icon.warning {
  background-color: #faad14;
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

/* 暗色主題 - 改善文字可讀性 */
[data-theme="dark"] .card-number,
.dark .card-number,
.dark-theme .card-number {
  color: #f9fafb;
}

[data-theme="dark"] .card-title,
.dark .card-title,
.dark-theme .card-title {
  color: #e5e7eb;
}

[data-theme="dark"] .status-title,
.dark .status-title,
.dark-theme .status-title {
  color: #f9fafb;
}

[data-theme="dark"] .status-value,
.dark .status-value,
.dark-theme .status-value {
  color: #e5e7eb;
}

[data-theme="dark"] .activity-title,
.dark .activity-title,
.dark-theme .activity-title {
  color: #f9fafb;
}

[data-theme="dark"] .activity-time,
.dark .activity-time,
.dark-theme .activity-time {
  color: #e5e7eb;
}

[data-theme="dark"] .activity-icon,
.dark .activity-icon,
.dark-theme .activity-icon {
  background-color: rgba(255, 255, 255, 0.1);
}

/* 響應式設計 */
@media (max-width: 1024px) {
  .admin-dashboard {
    max-width: none;
    padding: 0 1rem;
  }
  
  .overview-cards {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .dashboard-content {
    gap: 1rem;
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 0 0.75rem;
  }
  
  .dashboard-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
  }
  
  .overview-cards {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .card-content {
    gap: 0.75rem;
  }
  
  .card-icon {
    width: 40px;
    height: 40px;
  }
  
  .card-number {
    font-size: 1.75rem;
  }
  
  .card-title {
    font-size: 0.8125rem;
  }
}

@media (max-width: 640px) {
  .admin-dashboard {
    padding: 0 0.5rem;
  }
  
  .overview-cards {
    margin-bottom: 1.5rem;
  }
  
  .dashboard-content {
    gap: 0.75rem;
  }
  
  .left-panel,
  .right-panel {
    gap: 1rem;
  }
  
  .card-content {
    gap: 0.5rem;
  }
  
  .card-icon {
    width: 36px;
    height: 36px;
  }
  
  .card-number {
    font-size: 1.5rem;
  }
  
  .status-item,
  .activity-item {
    gap: 0.5rem;
  }
  
  .status-icon,
  .activity-icon {
    width: 28px;
    height: 28px;
  }
}

@media (max-width: 480px) {
  .admin-dashboard {
    padding: 0 0.25rem;
  }
  
  .overview-cards {
    gap: 0.5rem;
  }
  
  .card-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .card-info {
    text-align: left;
  }
  
  .action-buttons {
    gap: 0.5rem;
  }
  
  .action-buttons .n-button {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }
}
</style>