<template>
  <div class="group-view">
    <!-- 加載狀態 -->
    <template v-if="loading">
      <div class="group-header-skeleton">
        <n-skeleton text height="36px" width="60%" style="margin-bottom: 16px" />
        <n-skeleton text height="20px" width="40%" style="margin-bottom: 16px" />
        <n-skeleton text height="16px" width="100%" :repeat="3" />
      </div>
      
      <div class="members-skeleton" style="margin-top: 2rem">
        <n-skeleton text height="1.5rem" width="20%" style="margin-bottom: 1rem" />
        <div class="members-grid">
          <div v-for="i in 8" :key="i" class="member-card skeleton-card">
            <n-skeleton height="3.75rem" width="3.75rem" circle />
            <div class="member-info">
              <n-skeleton text height="1rem" width="80%" style="margin-bottom: 0.5rem" />
              <n-skeleton text height="0.875rem" width="60%" />
            </div>
          </div>
        </div>
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
          <MarkdownRenderer :source="getGroupDescription()" />
        </div>
      </div>

      <!-- 課題組成員 -->
      <div v-if="groupMembers.length > 0" class="group-members-section">
        <h2 class="section-title">{{ $t('groups.members') }} ({{ groupMembers.length }})</h2>
        <div class="members-grid">
          <MemberCard 
            v-for="member in groupMembers" 
            :key="member.mem_id"
            :member="member"
            @click="toMember"
          />
        </div>
      </div>

      <!-- 沒有成員 -->
      <div v-else class="empty-members">
        <n-empty :description="$t('emptyStates.noGroupMembers')" />
      </div>
    </div>

    <!-- 沒有找到課題組 -->
    <div v-else class="not-found-state">
      <n-empty :description="$t('emptyStates.groupNotFound')" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { researchGroupApi, memberApi } from '@/services/api';
import { useMembers } from '@/composables/useMembers';
import { processMarkdownImageUrls } from '@/utils/media';
import MemberCard from '@/components/MemberCard.vue';
import MarkdownRenderer from '@/components/MarkdownRenderer.vue';
import type { ResearchGroup, Member, ApiError } from '@/types/api';

const route = useRoute();
const router = useRouter();
const { locale, t } = useI18n();
const { getMemberAvatar } = useMembers();

// 響應式數據
const researchGroup = ref<ResearchGroup | null>(null);
const groupMembers = ref<Member[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

const getGroupDescription = () => {
  if (!researchGroup.value) return '';
  const desc = getCurrentLocale() === 'zh' ? researchGroup.value.research_group_desc_zh : researchGroup.value.research_group_desc_en;
  return desc ? processMarkdownImageUrls(desc) : '';
};

// 方法
const fetchGroupDetail = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const groupId = parseInt(route.params.id as string);
    if (isNaN(groupId)) {
      error.value = t('errorMessages.invalidGroupId');
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
      } catch (err: unknown) {
        console.warn('Failed to fetch group members:', err);
        // 成員獲取失敗不阻止課題組信息顯示
      }
      
    } else {
      error.value = groupResponse.message;
    }
  } catch (err: unknown) {
    console.error('Failed to fetch group detail:', err);
    const apiError = err as ApiError;
    error.value = apiError?.message || t('errorMessages.fetchGroupDetail');
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
  padding: 0.5rem 1rem;
  max-width: 120rem;
  min-width: 20rem;
  margin: 0 auto;
}

.group-header-skeleton,
.group-content {
  width: 100%;
}

.error-state,
.not-found-state {
  text-align: center;
  padding: 5rem 1.25rem;
}

/* 課題組頭部 */
.group-header {
  margin-bottom: 3rem;
  background: linear-gradient(135deg, rgba(24, 144, 255, 0.05), rgba(114, 46, 209, 0.05));
  padding: 2rem;
  border-radius: 1rem;
  border: 0.0625rem solid rgba(24, 144, 255, 0.1);
}

.group-name {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1.5rem 0;
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
  margin-bottom: 1.5rem;
  gap: 0.75rem;
}

.leader-label {
  font-size: 1.125rem;
  color: #666;
  font-weight: 500;
}

.leader-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  background: rgba(24, 144, 255, 0.08);
  border: 0.0625rem solid rgba(24, 144, 255, 0.15);
}

.leader-info:hover {
  background: rgba(24, 144, 255, 0.12);
  border-color: rgba(24, 144, 255, 0.25);
  transform: translateY(-0.0625rem);
}

.leader-avatar {
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
}

.leader-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1890ff;
}

.group-description {
  text-align: left;
  max-width: 50rem;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.6);
  padding: 1.5rem;
  border-radius: 0.75rem;
  border-left: 0.25rem solid #1890ff;
}

.group-description h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #1890ff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.group-description h3::before {
  content: '📝';
  font-size: 1.125rem;
}

.description-content {
  font-size: 1rem;
  line-height: 1.7;
  color: #555;
  text-align: justify;
}

/* 成員區域 */
.group-members-section {
  margin-top: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1890ff;
  border-bottom: 0.125rem solid #1890ff;
  padding-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title::before {
  content: '👥';
  font-size: 1.25rem;
}

/* Flex 網格布局 */
.members-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: flex-start;
}


.empty-members {
  text-align: center;
  padding: 5rem 1.25rem;
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
.dark .group-view,
.dark-mode .group-view {
  color: #fff;
}

[data-theme="dark"] .group-description,
.dark .group-description,
.dark-mode .group-description {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .leader-label,
.dark .leader-label,
.dark-mode .leader-label {
  color: #ccc;
}

[data-theme="dark"] .leader-info,
.dark .leader-info,
.dark-mode .leader-info {
  background: rgba(112, 161, 255, 0.1);
}

[data-theme="dark"] .leader-info:hover,
.dark .leader-info:hover,
.dark-mode .leader-info:hover {
  background: rgba(112, 161, 255, 0.15);
}

[data-theme="dark"] .leader-name,
.dark .leader-name,
.dark-mode .leader-name {
  color: #70a1ff;
}

[data-theme="dark"] .group-description h3,
.dark .group-description h3,
.dark-mode .group-description h3 {
  color: #fff;
}

[data-theme="dark"] .description-content,
.dark .description-content,
.dark-mode .description-content {
  color: #ccc;
}

[data-theme="dark"] .section-title,
.dark .section-title,
.dark-mode .section-title {
  color: #70a1ff;
  border-bottom-color: #70a1ff;
}


/* 響應式設計 */
@media (max-width: 1024px) {
  .group-view {
    padding: 0.5rem 1rem;
  }
  
  .members-grid {
    gap: 0.875rem;
  }
}

@media (max-width: 768px) {
  .group-view {
    padding: 1rem;
  }
  
  .group-name {
    font-size: 2rem;
  }
  
  .group-header {
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .members-grid {
    gap: 0.75rem;
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .members-grid {
    gap: 0.625rem;
  }
}

@media (max-width: 50rem) {
  .group-view {
    padding: 1rem;
    min-width: auto;
  }
  
  .group-header {
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .group-name {
    font-size: 2rem;
  }
  
  .group-leader {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .leader-label {
    font-size: 1rem;
  }
  
  .group-description {
    padding: 1rem;
    text-align: center;
  }
  
  .members-grid {
    justify-content: center;
    gap: 0.75rem;
  }
}

@media (max-width: 30rem) {
  .group-name {
    font-size: 1.75rem;
  }
  
  .members-grid {
    justify-content: center;
  }
}
</style>