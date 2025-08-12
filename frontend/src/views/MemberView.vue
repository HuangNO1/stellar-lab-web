<template>
  <div class="member-view">
    <!-- 頁面標題 -->
    <div class="page-header">
      <h1 class="page-title">{{ $t('members.title') }}</h1>
    </div>

    <!-- 加載狀態 -->
    <template v-if="loading">
      <div class="member-section">
        <h2 class="section-title">
          <n-skeleton text width="150px" />
        </h2>
        <div class="members-grid">
          <div v-for="i in 8" :key="i" class="member-card skeleton-card">
            <n-skeleton height="60px" width="60px" circle />
            <div class="member-info">
              <n-skeleton text height="16px" width="80%" style="margin-bottom: 8px" />
              <n-skeleton text height="14px" width="60%" />
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
      <n-button @click="fetchMembers" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 成員列表 -->
    <div v-else class="members-content">
      <!-- 教師 -->
      <div v-if="groupedMembers.teachers.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.professor') }}</h2>
        <div class="members-grid">
          <div v-for="member in groupedMembers.teachers" :key="member.mem_id" class="member-card" @click="toMember(member.mem_id)">
            <n-avatar
              :round="true"
              :size="60"
              :src="getMemberAvatar(member) || '/default-avatar.svg'"
              :fallback-src="'/default-avatar.svg'"
              class="member-avatar"
            />
            <div class="member-info">
              <n-tooltip trigger="hover" :disabled="!isNameTruncated(member)">
                <template #trigger>
                  <div class="member-name">
                    {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
                  </div>
                </template>
                {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
              </n-tooltip>
              <n-tooltip trigger="hover" :disabled="!isPositionTruncated(member)">
                <template #trigger>
                  <div class="member-position">
                    {{ getMemberPosition(member, getCurrentLocale()) }}
                  </div>
                </template>
                {{ getMemberPosition(member, getCurrentLocale()) }}
              </n-tooltip>
            </div>
          </div>
        </div>
      </div>

      <!-- 博士生 -->
      <div v-if="groupedMembers.phd.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.phd') }}</h2>
        <div class="members-grid">
          <div v-for="member in groupedMembers.phd" :key="member.mem_id" class="member-card" @click="toMember(member.mem_id)">
            <n-avatar
              :round="true"
              :size="60"
              :src="getMemberAvatar(member) || '/default-avatar.svg'"
              :fallback-src="'/default-avatar.svg'"
              class="member-avatar"
            />
            <div class="member-info">
              <n-tooltip trigger="hover" :disabled="!isNameTruncated(member)">
                <template #trigger>
                  <div class="member-name">
                    {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
                  </div>
                </template>
                {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
              </n-tooltip>
              <n-tooltip trigger="hover" :disabled="!isPositionTruncated(member)">
                <template #trigger>
                  <div class="member-position">
                    {{ getMemberPosition(member, getCurrentLocale()) }}
                  </div>
                </template>
                {{ getMemberPosition(member, getCurrentLocale()) }}
              </n-tooltip>
            </div>
          </div>
        </div>
      </div>

      <!-- 碩士生 -->
      <div v-if="groupedMembers.master.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.master') }}</h2>
        <div class="members-grid">
          <div v-for="member in groupedMembers.master" :key="member.mem_id" class="member-card" @click="toMember(member.mem_id)">
            <n-avatar
              :round="true"
              :size="60"
              :src="getMemberAvatar(member) || '/default-avatar.svg'"
              :fallback-src="'/default-avatar.svg'"
              class="member-avatar"
            />
            <div class="member-info">
              <n-tooltip trigger="hover" :disabled="!isNameTruncated(member)">
                <template #trigger>
                  <div class="member-name">
                    {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
                  </div>
                </template>
                {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
              </n-tooltip>
              <n-tooltip trigger="hover" :disabled="!isPositionTruncated(member)">
                <template #trigger>
                  <div class="member-position">
                    {{ getMemberPosition(member, getCurrentLocale()) }}
                  </div>
                </template>
                {{ getMemberPosition(member, getCurrentLocale()) }}
              </n-tooltip>
            </div>
          </div>
        </div>
      </div>

      <!-- 本科生 -->
      <div v-if="groupedMembers.undergraduate.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.undergraduate') }}</h2>
        <div class="members-grid">
          <div v-for="member in groupedMembers.undergraduate" :key="member.mem_id" class="member-card" @click="toMember(member.mem_id)">
            <n-avatar
              :round="true"
              :size="60"
              :src="getMemberAvatar(member) || '/default-avatar.svg'"
              :fallback-src="'/default-avatar.svg'"
              class="member-avatar"
            />
            <div class="member-info">
              <n-tooltip trigger="hover" :disabled="!isNameTruncated(member)">
                <template #trigger>
                  <div class="member-name">
                    {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
                  </div>
                </template>
                {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
              </n-tooltip>
              <n-tooltip trigger="hover" :disabled="!isPositionTruncated(member)">
                <template #trigger>
                  <div class="member-position">
                    {{ getMemberPosition(member, getCurrentLocale()) }}
                  </div>
                </template>
                {{ getMemberPosition(member, getCurrentLocale()) }}
              </n-tooltip>
            </div>
          </div>
        </div>
      </div>

      <!-- 校友 -->
      <div v-if="groupedMembers.alumni.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.alumni') }}</h2>
        <div class="members-grid">
          <div v-for="member in groupedMembers.alumni" :key="member.mem_id" class="member-card" @click="toMember(member.mem_id)">
            <n-avatar
              :round="true"
              :size="60"
              :src="getMemberAvatar(member) || '/default-avatar.svg'"
              :fallback-src="'/default-avatar.svg'"
              class="member-avatar"
            />
            <div class="member-info">
              <n-tooltip trigger="hover" :disabled="!isNameTruncated(member)">
                <template #trigger>
                  <div class="member-name">
                    {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
                  </div>
                </template>
                {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
              </n-tooltip>
              <n-tooltip trigger="hover" :disabled="!isPositionTruncated(member)">
                <template #trigger>
                  <div class="member-position">
                    {{ getMemberPosition(member, getCurrentLocale()) }}
                  </div>
                </template>
                {{ getMemberPosition(member, getCurrentLocale()) }}
              </n-tooltip>
            </div>
          </div>
        </div>
      </div>

      <!-- 其他 -->
      <div v-if="groupedMembers.others.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.others') }}</h2>
        <div class="members-grid">
          <div v-for="member in groupedMembers.others" :key="member.mem_id" class="member-card" @click="toMember(member.mem_id)">
            <n-avatar
              :round="true"
              :size="60"
              :src="getMemberAvatar(member) || '/default-avatar.svg'"
              :fallback-src="'/default-avatar.svg'"
              class="member-avatar"
            />
            <div class="member-info">
              <n-tooltip trigger="hover" :disabled="!isNameTruncated(member)">
                <template #trigger>
                  <div class="member-name">
                    {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
                  </div>
                </template>
                {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
              </n-tooltip>
              <n-tooltip trigger="hover" :disabled="!isPositionTruncated(member)">
                <template #trigger>
                  <div class="member-position">
                    {{ getMemberPosition(member, getCurrentLocale()) }}
                  </div>
                </template>
                {{ getMemberPosition(member, getCurrentLocale()) }}
              </n-tooltip>
            </div>
          </div>
        </div>
      </div>

      <!-- 沒有數據 -->
      <div v-if="total === 0" class="empty-state">
        <n-empty :description="$t('emptyStates.noMembers')" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { useRouter, useRoute } from 'vue-router';
import { useMembersWithAutoFetch } from '@/composables/useMembers';
import type { Member } from '@/types/api';

const { locale } = useI18n();
const router = useRouter();
const route = useRoute();

// 根據URL查詢參數決定是否篩選特定課題組
const queryParams = route.query.group ? 
  { all: 'true', research_group_id: parseInt(route.query.group as string), sort_by: 'name', order: 'asc' } :
  { all: 'true', sort_by: 'name', order: 'asc' };

// 使用 composable 獲取成員數據
const { 
  loading, 
  error, 
  total, 
  groupedMembers, 
  fetchMembers, 
  getMemberAvatar, 
  getMemberPosition 
} = useMembersWithAutoFetch(queryParams);

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

// 判断名字是否被截断
const isNameTruncated = (member: Member) => {
  const name = getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en;
  // 更新判断条件：英文名字超过15字符或中文超过7字符
  return getCurrentLocale() === 'zh' ? (name?.length || 0) > 7 : (name?.length || 0) > 15;
};

// 判断職位是否被截断
const isPositionTruncated = (member: Member) => {
  const position = getMemberPosition(member, getCurrentLocale());
  // 更新判断条件：英文職位超过18字符或中文超过8字符
  return getCurrentLocale() === 'zh' ? (position?.length || 0) > 8 : (position?.length || 0) > 18;
};

// 跳轉到成員詳情頁面
const toMember = (memberId: number) => {
  router.push(`/member/${memberId}`);
};
</script>

<style scoped>
.member-view {
  padding: 1.5rem;
  max-width: 87.5rem;
  margin: 0 auto;
  width: 100%;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.member-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1890ff;
  border-bottom: 0.125rem solid #1890ff;
  padding-bottom: 0.5rem;
}

/* Flex 網格布局 */
.members-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: flex-start; /* 左对齊而不是居中 */
}

.member-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border-radius: 0.75rem;
  background: #fff;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 0.125rem solid transparent;
  /* 增大寬度以適應英文名字 */
  width: 10rem;
  min-width: 10rem;
  max-width: 10rem;
  height: 9rem;
  min-height: 9rem;
  max-height: 9rem;
  flex-shrink: 0;
}

/* 小屏幕调整 */
@media (max-width: 30rem) {
  .members-grid {
    justify-content: center; /* 小屏幕才居中 */
  }
  
  .member-card {
    width: 8rem;
    min-width: 8rem;
    max-width: 8rem;
    height: 8rem;
    min-height: 8rem;
    max-height: 8rem;
  }
}

.member-card:hover {
  transform: translateY(-0.25rem);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.15);
  border-color: #1890ff;
}

.member-info {
  text-align: center;
  margin-top: 0.75rem;
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: visible;
  padding: 0 4px;
}

.member-name {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #333;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
  min-height: 1.26rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.member-position {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
  min-height: 1.12rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-state {
  text-align: center;
  padding: 2.5rem;
}

.empty-state {
  text-align: center;
  padding: 5rem 0;
}

/* 暗色主題支持 */
[data-theme="dark"] .member-card,
.dark .member-card,
.dark-mode .member-card {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: transparent !important;
}

[data-theme="dark"] .member-card:hover,
.dark .member-card:hover,
.dark-mode .member-card:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  border-color: #70a1ff !important;
}

[data-theme="dark"] .member-name,
.dark .member-name,
.dark-mode .member-name {
  color: #fff !important;
}

[data-theme="dark"] .member-position,
.dark .member-position,
.dark-mode .member-position {
  color: #ccc !important;
}

[data-theme="dark"] .section-title,
.dark .section-title,
.dark-mode .section-title {
  color: #70a1ff !important;
  border-bottom-color: #70a1ff !important;
}

/* 骨架屏卡片樣式 */
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

/* 成員頭像固定樣式 */
.member-avatar {
  flex-shrink: 0;
  width: 60px !important;
  height: 60px !important;
  border-radius: 50% !important;
  object-fit: cover;
}

/* 不同屏幕尺寸下的頭像調整 */
@media (max-width: 1024px) {
  .member-card .member-avatar {
    width: 50px !important;
    height: 50px !important;
  }
}

@media (max-width: 640px) {
  .member-card .member-avatar {
    width: 45px !important;
    height: 45px !important;
  }
}

@media (max-width: 30rem) {
  .member-card .member-avatar {
    width: 40px !important;
    height: 40px !important;
  }
}

/* 響應式設計 - 改善版 */
@media (max-width: 1024px) {
  .member-view {
    padding: 1.25rem;
  }
  
  .members-grid {
    gap: 0.875rem;
  }
  
  .member-card {
    width: 9rem;
    min-width: 9rem;
    max-width: 9rem;
    height: 8.5rem;
    min-height: 8.5rem;
    max-height: 8.5rem;
  }
  
  .member-name {
    font-size: 0.875rem;
  }
  
  .member-position {
    font-size: 0.75rem;
  }
}

@media (max-width: 768px) {
  .member-view {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.75rem;
  }
  
  .section-title {
    font-size: 1.375rem;
  }
  
  .members-grid {
    gap: 0.75rem;
    justify-content: center;
  }
  
  .member-card {
    width: 8.5rem;
    min-width: 8.5rem;
    max-width: 8.5rem;
    height: 8.5rem;
    min-height: 8.5rem;
    max-height: 8.5rem;
  }
  
  .member-info {
    margin-top: 0.5rem;
    padding: 0 3px;
  }
  
  .member-name {
    font-size: 0.85rem;
    line-height: 1.4;
    min-height: 1.19rem;
    margin-bottom: 0.2rem;
  }
  
  .member-position {
    font-size: 0.7rem;
    line-height: 1.4;
    min-height: 0.98rem;
  }
}

@media (max-width: 640px) {
  .members-grid {
    gap: 0.625rem;
  }
  
  .member-card {
    width: 8rem;
    min-width: 8rem;
    max-width: 8rem;
    height: 8rem;
    min-height: 8rem;
    max-height: 8rem;
    padding: 0.75rem;
  }
  
  .member-info {
    margin-top: 0.4rem;
    padding: 0 2px;
  }
  
  .member-name {
    font-size: 0.8rem;
    margin-bottom: 0.15rem;
    min-height: 1.12rem;
  }
  
  .member-position {
    font-size: 0.65rem;
    min-height: 0.91rem;
  }
}

@media (max-width: 48rem) {
  .member-view {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
  
  .members-grid {
    gap: 0.75rem;
  }
  
  .member-name {
    font-size: 0.85rem;
    line-height: 1.4;
    min-height: 1.19rem;
  }
  
  .member-position {
    font-size: 0.75rem;
    line-height: 1.4;
    min-height: 1.05rem;
  }
}

/* 小屏幕调整 - 優化版 */
@media (max-width: 30rem) {
  .members-grid {
    justify-content: center;
  }
  
  .member-card {
    width: 7.5rem;
    min-width: 7.5rem;
    max-width: 7.5rem;
    height: 7.5rem;
    min-height: 7.5rem;
    max-height: 7.5rem;
    padding: 0.6rem 0.4rem;
  }
  
  .member-info {
    margin-top: 0.3rem;
    padding: 0 2px;
  }
  
  .member-name {
    font-size: 0.75rem;
    min-height: 1.05rem;
    margin-bottom: 0.1rem;
  }
  
  .member-position {
    font-size: 0.6rem;
    min-height: 0.84rem;
  }
}

</style>