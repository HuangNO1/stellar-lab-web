<template>
  <div class="group-view">
    <!-- 加載狀態 -->
    <template v-if="loading">
      <div class="group-header-skeleton">
        <n-skeleton text height="36px" width="60%" style="margin-bottom: 16px" />
        <n-skeleton text height="20px" width="40%" style="margin-bottom: 16px" />
        <n-skeleton text height="16px" width="100%" :repeat="3" />
      </div>
      
      <div class="members-skeleton" style="margin-top: 32px">
        <n-skeleton text height="24px" width="20%" style="margin-bottom: 16px" />
        <n-grid :x-gap="16" :y-gap="16" cols="2 600:4 800:6 1000:8 1200:10">
          <n-grid-item v-for="i in 8" :key="i">
            <div class="member-card skeleton-card">
              <n-skeleton height="60px" width="60px" circle />
              <div class="member-info">
                <n-skeleton text height="16px" width="80%" style="margin-bottom: 8px" />
                <n-skeleton text height="14px" width="60%" />
              </div>
            </div>
          </n-grid-item>
        </n-grid>
      </div>
    </template>

    <!-- 錯誤狀態 -->
    <div v-else-if="error" class="error-state">
      <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 16px;">
        {{ error }}
      </n-alert>
      <n-button @click="fetchGroupDetail" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 課題組詳情 -->
    <div v-else-if="researchGroup" class="group-content">
      <!-- 課題組信息 -->
      <div class="group-header">
        <h1 class="group-name">
          {{ getCurrentLocale() === 'zh' ? researchGroup.research_group_name_zh : researchGroup.research_group_name_en }}
        </h1>
        
        <!-- 課題組負責人 -->
        <div v-if="researchGroup.leader" class="group-leader">
          <div class="leader-label">{{ $t('groups.leader') }}:</div>
          <div class="leader-info" @click="toMember(researchGroup.leader.mem_id)">
            <n-avatar
              :size="32"
              :src="getMemberAvatar(researchGroup.leader) || '/default-avatar.svg'"
              :fallback-src="'/default-avatar.svg'"
              class="leader-avatar"
            />
            <span class="leader-name">
              {{ getCurrentLocale() === 'zh' ? researchGroup.leader.mem_name_zh : researchGroup.leader.mem_name_en }}
            </span>
          </div>
        </div>

        <!-- 課題組描述 -->
        <div v-if="researchGroup.research_group_desc_zh || researchGroup.research_group_desc_en" class="group-description">
          <h3>{{ $t('groups.description') }}</h3>
          <div class="description-content" v-html="getGroupDescription()"></div>
        </div>
      </div>

      <!-- 課題組成員 -->
      <div v-if="groupMembers.length > 0" class="group-members-section">
        <h2 class="section-title">{{ $t('groups.members') }} ({{ groupMembers.length }})</h2>
        <n-grid :x-gap="16" :y-gap="16" cols="2 600:4 800:6 1000:8 1200:10">
          <n-grid-item v-for="member in groupMembers" :key="member.mem_id">
            <div class="member-card" @click="toMember(member.mem_id)">
              <n-avatar
                :round="true"
                :size="60"
                :src="getMemberAvatar(member) || '/default-avatar.svg'"
                :fallback-src="'/default-avatar.svg'"
              />
              <div class="member-info">
                <div class="member-name">
                  {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
                </div>
                <div class="member-position">
                  {{ getMemberPosition(member, getCurrentLocale()) }}
                </div>
              </div>
            </div>
          </n-grid-item>
        </n-grid>
      </div>

      <!-- 沒有成員 -->
      <div v-else class="empty-members">
        <n-empty description="該課題組暫無成員" />
      </div>
    </div>

    <!-- 沒有找到課題組 -->
    <div v-else class="not-found-state">
      <n-empty description="未找到該課題組" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { researchGroupApi, memberApi } from '@/services/api';
import { useMembers } from '@/composables/useMembers';
import type { ResearchGroup, Member } from '@/types/api';

const route = useRoute();
const router = useRouter();
const { locale } = useI18n();
const { getMemberAvatar, getMemberPosition } = useMembers();

// 響應式數據
const researchGroup = ref<ResearchGroup | null>(null);
const groupMembers = ref<Member[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// 計算屬性
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

const getGroupDescription = () => {
  if (!researchGroup.value) return '';
  const desc = getCurrentLocale() === 'zh' ? researchGroup.value.research_group_desc_zh : researchGroup.value.research_group_desc_en;
  // 簡單的 Markdown 渲染 (基本支持段落和換行)
  return desc?.replace(/\n/g, '<br>') || '';
};

// 方法
const fetchGroupDetail = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const groupId = parseInt(route.params.id as string);
    if (isNaN(groupId)) {
      error.value = '無效的課題組ID';
      return;
    }

    // 獲取課題組詳情
    const groupResponse = await researchGroupApi.getResearchGroup(groupId);
    if (groupResponse.code === 0) {
      researchGroup.value = groupResponse.data;
      
      // 獲取課題組成員
      try {
        const membersResponse = await memberApi.getMembers({ 
          all: 'true',
          research_group_id: groupId,
          sort_by: 'name',
          order: 'asc'
        });
        if (membersResponse.code === 0) {
          groupMembers.value = membersResponse.data.items;
        }
      } catch (err) {
        console.warn('Failed to fetch group members:', err);
        // 成員獲取失敗不阻止課題組信息顯示
      }
      
    } else {
      error.value = groupResponse.message;
    }
  } catch (err) {
    console.error('Failed to fetch group detail:', err);
    error.value = '獲取課題組詳情失敗';
  } finally {
    loading.value = false;
  }
};

const toMember = (memberId: number) => {
  router.push(`/member/${memberId}`);
};

// 生命週期
onMounted(() => {
  fetchGroupDetail();
});

// 監聽路由參數變化
watch(() => route.params.id, () => {
  fetchGroupDetail();
});
</script>

<style scoped>
.group-view {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.group-header-skeleton,
.group-content {
  width: 100%;
}

.error-state,
.not-found-state {
  text-align: center;
  padding: 80px 20px;
}

/* 課題組頭部 */
.group-header {
  margin-bottom: 48px;
}

.group-name {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 24px 0;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
  text-align: center;
}

.group-leader {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  gap: 12px;
}

.leader-label {
  font-size: 1.125rem;
  color: #666;
  font-weight: 500;
}

.leader-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(24, 144, 255, 0.05);
}

.leader-info:hover {
  background: rgba(24, 144, 255, 0.1);
  transform: translateY(-1px);
}

.leader-avatar {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.leader-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1890ff;
}

.group-description {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.group-description h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #333;
}

.description-content {
  font-size: 1.125rem;
  line-height: 1.6;
  color: #666;
}

/* 成員區域 */
.group-members-section {
  margin-top: 48px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 24px;
  color: #1890ff;
  border-bottom: 2px solid #1890ff;
  padding-bottom: 8px;
}

.member-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
}

.member-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  border-color: #1890ff;
}

.member-info {
  text-align: center;
  margin-top: 12px;
  width: 100%;
}

.member-name {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 4px;
  color: #333;
  word-wrap: break-word;
}

.member-position {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.4;
  word-wrap: break-word;
}

.empty-members {
  text-align: center;
  padding: 80px 20px;
}

/* 骨架屏樣式 */
.skeleton-card {
  opacity: 0.7;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 0.8;
  }
}

/* 暗色主題支持 */
[data-theme="dark"] .group-view,
.dark .group-view {
  color: #fff;
}

[data-theme="dark"] .leader-label,
.dark .leader-label {
  color: #ccc;
}

[data-theme="dark"] .leader-info,
.dark .leader-info {
  background: rgba(112, 161, 255, 0.1);
}

[data-theme="dark"] .leader-info:hover,
.dark .leader-info:hover {
  background: rgba(112, 161, 255, 0.15);
}

[data-theme="dark"] .leader-name,
.dark .leader-name {
  color: #70a1ff;
}

[data-theme="dark"] .group-description h3,
.dark .group-description h3 {
  color: #fff;
}

[data-theme="dark"] .description-content,
.dark .description-content {
  color: #ccc;
}

[data-theme="dark"] .section-title,
.dark .section-title {
  color: #70a1ff;
  border-bottom-color: #70a1ff;
}

[data-theme="dark"] .member-card,
.dark .member-card {
  background: rgba(255, 255, 255, 0.08);
  border-color: transparent;
}

[data-theme="dark"] .member-card:hover,
.dark .member-card:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: #70a1ff;
}

[data-theme="dark"] .member-name,
.dark .member-name {
  color: #fff;
}

[data-theme="dark"] .member-position,
.dark .member-position {
  color: #ccc;
}

/* 響應式設計 */
@media (max-width: 800px) {
  .group-view {
    padding: 16px;
  }
  
  .group-name {
    font-size: 2rem;
  }
  
  .group-leader {
    flex-direction: column;
    gap: 8px;
  }
  
  .leader-label {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .group-name {
    font-size: 1.75rem;
  }
  
  .member-card {
    padding: 12px;
  }
  
  .member-name {
    font-size: 0.9rem;
  }
  
  .member-position {
    font-size: 0.8rem;
  }
}
</style>