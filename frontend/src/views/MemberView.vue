<template>
  <div class="member-view">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">{{ $t('members.title') }}</h1>
        <p class="page-description">{{ $t('members.description') }}</p>
      </div>
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
        <h2 class="section-title">{{ $t('members.teachers') }}</h2>
        <div class="members-grid">
          <MemberCard 
            v-for="member in groupedMembers.teachers" 
            :key="member.mem_id"
            :member="member"
            @click="toMember"
          />
        </div>
      </div>

      <!-- 博士生 -->
      <div v-if="groupedMembers.phd.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.phd') }}</h2>
        <div class="members-grid">
          <MemberCard 
            v-for="member in groupedMembers.phd" 
            :key="member.mem_id"
            :member="member"
            @click="toMember"
          />
        </div>
      </div>

      <!-- 碩士生 -->
      <div v-if="groupedMembers.master.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.master') }}</h2>
        <div class="members-grid">
          <MemberCard 
            v-for="member in groupedMembers.master" 
            :key="member.mem_id"
            :member="member"
            @click="toMember"
          />
        </div>
      </div>

      <!-- 本科生 -->
      <div v-if="groupedMembers.undergraduate.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.undergraduate') }}</h2>
        <div class="members-grid">
          <MemberCard 
            v-for="member in groupedMembers.undergraduate" 
            :key="member.mem_id"
            :member="member"
            @click="toMember"
          />
        </div>
      </div>

      <!-- 實習生 -->
      <div v-if="groupedMembers.intern.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.intern') }}</h2>
        <div class="members-grid">
          <MemberCard 
            v-for="member in groupedMembers.intern" 
            :key="member.mem_id"
            :member="member"
            @click="toMember"
          />
        </div>
      </div>

      <!-- 校友 -->
      <div v-if="groupedMembers.alumni.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.alumni') }}</h2>
        <div class="members-grid">
          <MemberCard 
            v-for="member in groupedMembers.alumni" 
            :key="member.mem_id"
            :member="member"
            @click="toMember"
          />
        </div>
      </div>

      <!-- 其他 -->
      <div v-if="groupedMembers.others.length > 0" class="member-section">
        <h2 class="section-title">{{ $t('members.others') }}</h2>
        <div class="members-grid">
          <MemberCard 
            v-for="member in groupedMembers.others" 
            :key="member.mem_id"
            :member="member"
            @click="toMember"
          />
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
import { useRouter, useRoute } from 'vue-router';
import { useMembersWithAutoFetch } from '@/composables/useMembers';
import MemberCard from '@/components/MemberCard.vue';

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
  fetchMembers
} = useMembersWithAutoFetch(queryParams);

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

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
  background: linear-gradient(135deg, #13c2c2 0%, #1890ff 100%);
  border-radius: 12px;
  color: white;
}

.header-content {
  max-width: 600px;
  margin: 0 auto;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-description {
  font-size: 1.125rem;
  margin: 0;
  opacity: 0.9;
  line-height: 1.6;
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

/* 小屏幕调整 */
@media (max-width: 30rem) {
  .members-grid {
    justify-content: center; /* 小屏幕才居中 */
  }
}

.error-state {
  text-align: center;
  padding: 2.5rem;
}

.empty-state {
  text-align: center;
  padding: 5rem 0;
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
@media (max-width: 1024px) {
  .member-view {
    padding: 1.25rem;
  }
  
  .page-header {
    margin-bottom: 2.5rem;
    padding: 1.75rem 1rem;
  }
  
  .members-grid {
    gap: 0.875rem;
  }
}

@media (max-width: 768px) {
  .member-view {
    padding: 1rem;
  }
  
  .page-header {
    margin-bottom: 2rem;
    padding: 1.5rem 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-description {
    font-size: 1rem;
  }
  
  .section-title {
    font-size: 1.375rem;
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

@media (max-width: 48rem) {
  .member-view {
    padding: 1rem;
  }
  
  .page-header {
    margin-bottom: 1.5rem;
    padding: 1rem 0.5rem;
    border-radius: 8px;
  }
  
  .page-title {
    font-size: 1.75rem;
  }
  
  .page-description {
    font-size: 1rem;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
  
  .members-grid {
    gap: 0.75rem;
  }
}

</style>