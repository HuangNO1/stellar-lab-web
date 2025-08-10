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
        <n-grid :x-gap="16" :y-gap="16" cols="8 600:4 800:6 1000:8 1200:10">
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
      <n-button @click="fetchMembers" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 成員列表 -->
    <div v-else class="members-content">
      <!-- 教師 -->
      <div v-if="groupedMembers.teachers.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.professor') }}</h2>
        <n-grid :x-gap="16" :y-gap="16" cols="8 600:4 800:6 1000:8 1200:10">
          <n-grid-item v-for="member in groupedMembers.teachers" :key="member.mem_id">
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

      <!-- 博士生 -->
      <div v-if="groupedMembers.phd.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.phd') }}</h2>
        <n-grid :x-gap="16" :y-gap="16" cols="8 600:4 800:6 1000:8 1200:10">
          <n-grid-item v-for="member in groupedMembers.phd" :key="member.mem_id">
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

      <!-- 碩士生 -->
      <div v-if="groupedMembers.master.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.master') }}</h2>
        <n-grid :x-gap="16" :y-gap="16" cols="8 600:4 800:6 1000:8 1200:10">
          <n-grid-item v-for="member in groupedMembers.master" :key="member.mem_id">
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

      <!-- 本科生 -->
      <div v-if="groupedMembers.undergraduate.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.undergraduate') }}</h2>
        <n-grid :x-gap="16" :y-gap="16" cols="8 600:4 800:6 1000:8 1200:10">
          <n-grid-item v-for="member in groupedMembers.undergraduate" :key="member.mem_id">
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

      <!-- 校友 -->
      <div v-if="groupedMembers.alumni.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.alumni') }}</h2>
        <n-grid :x-gap="16" :y-gap="16" cols="8 600:4 800:6 1000:8 1200:10">
          <n-grid-item v-for="member in groupedMembers.alumni" :key="member.mem_id">
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

      <!-- 其他 -->
      <div v-if="groupedMembers.others.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.others') }}</h2>
        <n-grid :x-gap="16" :y-gap="16" cols="8 600:4 800:6 1000:8 1200:10">
          <n-grid-item v-for="member in groupedMembers.others" :key="member.mem_id">
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

      <!-- 沒有數據 -->
      <div v-if="total === 0" class="empty-state">
        <n-empty description="暫無成員數據" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { useRouter, useRoute } from 'vue-router';
import { useMembersWithAutoFetch } from '@/composables/useMembers';

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

// 跳轉到成員詳情頁面
const toMember = (memberId: number) => {
  router.push(`/member/${memberId}`);
};
</script>

<style scoped>
.member-view {
  padding: 24px;
  max-width: 1400px; /* 增加最大寬度 */
  margin: 0 auto;
  width: 100%; /* 確保占滿可用寬度 */
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
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
  margin-bottom: 48px;
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

.error-state {
  text-align: center;
  padding: 40px;
}

.empty-state {
  text-align: center;
  padding: 80px 0;
}

/* 暗色主題支持 */
[data-theme="dark"] .member-card {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: transparent !important;
}

[data-theme="dark"] .member-card:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  border-color: #70a1ff !important;
}

[data-theme="dark"] .member-name {
  color: #fff !important;
}

[data-theme="dark"] .member-position {
  color: #ccc !important;
}

[data-theme="dark"] .section-title {
  color: #70a1ff !important;
  border-bottom-color: #70a1ff !important;
}

/* 另一種暗色主題支持方式 */
.dark .member-card {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: transparent !important;
}

.dark .member-card:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  border-color: #70a1ff !important;
}

.dark .member-name {
  color: #fff !important;
}

.dark .member-position {
  color: #ccc !important;
}

.dark .section-title {
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

/* 響應式設計 */
@media (max-width: 768px) {
  .member-view {
    padding: 16px;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .section-title {
    font-size: 1.25rem;
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