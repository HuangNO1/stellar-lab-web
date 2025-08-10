<template>
  <div class="member-view">
    <!-- 頁面標題 -->
    <div class="page-header">
      <h1 class="page-title">{{ $t('members.title') }}</h1>
    </div>

    <!-- 加載狀態 -->
    <div v-if="loading" class="loading-state">
      <n-spin size="large">
        <div class="loading-content">
          <div class="member-section">
            <div class="loading-title"></div>
            <n-grid :x-gap="16" :y-gap="16" cols="2 400:4 600:6 800:8">
              <n-grid-item v-for="i in 8" :key="i">
                <div class="member-card loading-card">
                  <div class="loading-avatar"></div>
                  <div class="member-info">
                    <div class="loading-name"></div>
                    <div class="loading-position"></div>
                  </div>
                </div>
              </n-grid-item>
            </n-grid>
          </div>
        </div>
      </n-spin>
    </div>

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
        <n-grid :x-gap="16" :y-gap="16" cols="2 400:4 600:6 800:8">
          <n-grid-item v-for="member in groupedMembers.teachers" :key="member.mem_id">
            <div class="member-card" @click="toMember(member.mem_id)">
              <n-avatar
                :round="true"
                :size="60"
                :src="getMemberAvatar(member)"
                :fallback-src="'/default-avatar.png'"
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
        <n-grid :x-gap="16" :y-gap="16" cols="2 400:4 600:6 800:8">
          <n-grid-item v-for="member in groupedMembers.phd" :key="member.mem_id">
            <div class="member-card" @click="toMember(member.mem_id)">
              <n-avatar
                :round="true"
                :size="60"
                :src="getMemberAvatar(member)"
                :fallback-src="'/default-avatar.png'"
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
        <n-grid :x-gap="16" :y-gap="16" cols="2 400:4 600:6 800:8">
          <n-grid-item v-for="member in groupedMembers.master" :key="member.mem_id">
            <div class="member-card" @click="toMember(member.mem_id)">
              <n-avatar
                :round="true"
                :size="60"
                :src="getMemberAvatar(member)"
                :fallback-src="'/default-avatar.png'"
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
        <n-grid :x-gap="16" :y-gap="16" cols="2 400:4 600:6 800:8">
          <n-grid-item v-for="member in groupedMembers.undergraduate" :key="member.mem_id">
            <div class="member-card" @click="toMember(member.mem_id)">
              <n-avatar
                :round="true"
                :size="60"
                :src="getMemberAvatar(member)"
                :fallback-src="'/default-avatar.png'"
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
        <n-grid :x-gap="16" :y-gap="16" cols="2 400:4 600:6 800:8">
          <n-grid-item v-for="member in groupedMembers.alumni" :key="member.mem_id">
            <div class="member-card" @click="toMember(member.mem_id)">
              <n-avatar
                :round="true"
                :size="60"
                :src="getMemberAvatar(member)"
                :fallback-src="'/default-avatar.png'"
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
        <n-grid :x-gap="16" :y-gap="16" cols="2 400:4 600:6 800:8">
          <n-grid-item v-for="member in groupedMembers.others" :key="member.mem_id">
            <div class="member-card" @click="toMember(member.mem_id)">
              <n-avatar
                :round="true"
                :size="60"
                :src="getMemberAvatar(member)"
                :fallback-src="'/default-avatar.png'"
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
import { useMembersWithAutoFetch } from '@/composables/useMembers';

const { locale } = useI18n();

// 使用 composable 獲取成員數據
const { 
  loading, 
  error, 
  total, 
  groupedMembers, 
  fetchMembers, 
  getMemberAvatar, 
  getMemberPosition 
} = useMembersWithAutoFetch();

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

// 跳轉到成員詳情頁面
const toMember = (memberId: number) => {
  // 可以跳轉到成員詳情頁面，例如 /member/:id
  console.log('Navigate to member:', memberId);
  // router.push(`/member/${memberId}`);
};
</script>

<style scoped>
.member-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
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
:global(.dark) .member-card {
  background: rgba(255, 255, 255, 0.08);
  border-color: transparent;
}

:global(.dark) .member-card:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: #70a1ff;
}

:global(.dark) .member-name {
  color: #fff;
}

:global(.dark) .member-position {
  color: #ccc;
}

:global(.dark) .section-title {
  color: #70a1ff;
  border-bottom-color: #70a1ff;
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

/* 骨架屏樣式 */
.skeleton-title {
  width: 100px;
}

/* 加載狀態樣式 */
.loading-state {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-content {
  width: 100%;
  max-width: 1200px;
  opacity: 0.6;
}

.loading-title {
  height: 32px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 24px;
  width: 150px;
}

.loading-card {
  animation: pulse 1.5s ease-in-out infinite;
}

.loading-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  margin-bottom: 12px;
}

.loading-name {
  height: 16px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 8px;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}

.loading-position {
  height: 14px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  width: 60%;
  margin-left: auto;
  margin-right: auto;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 0.8;
  }
}

/* 暗色主題下的加載狀態 */
:global(.dark) .loading-title,
:global(.dark) .loading-avatar,
:global(.dark) .loading-name,
:global(.dark) .loading-position {
  background: linear-gradient(90deg, #2a2a2a 25%, #3a3a3a 50%, #2a2a2a 75%);
  background-size: 200% 100%;
}
</style>