<template>
  <div class="member-detail-view">
    <!-- 加載狀態 -->
    <template v-if="loading">
      <div class="member-detail-skeleton">
        <n-grid :x-gap="24" cols="1 800:2">
          <n-grid-item>
            <div class="member-avatar-section">
              <n-skeleton height="200px" width="200px" circle />
            </div>
          </n-grid-item>
          <n-grid-item>
            <div class="member-info-section">
              <n-skeleton text height="32px" width="60%" style="margin-bottom: 16px" />
              <n-skeleton text height="18px" width="40%" style="margin-bottom: 12px" />
              <n-skeleton text height="18px" width="50%" style="margin-bottom: 12px" />
              <n-skeleton text height="18px" width="45%" style="margin-bottom: 20px" />
              <n-skeleton text height="16px" width="100%" :repeat="3" />
            </div>
          </n-grid-item>
        </n-grid>
        
        <!-- 相關論文骨架屏 -->
        <div class="related-papers-section" style="margin-top: 32px">
          <n-skeleton text height="24px" width="20%" style="margin-bottom: 16px" />
          <div v-for="i in 3" :key="i" style="margin-bottom: 16px">
            <n-skeleton text height="20px" width="80%" style="margin-bottom: 8px" />
            <n-skeleton text height="16px" width="60%" />
          </div>
        </div>
      </div>
    </template>

    <!-- 錯誤狀態 -->
    <div v-else-if="error" class="error-state">
      <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 16px;">
        {{ error }}
      </n-alert>
      <n-button @click="fetchMemberDetail" type="primary" ghost>
        {{ $t('common.retry') }}
      </n-button>
    </div>

    <!-- 成員詳情 -->
    <div v-else-if="member" class="member-detail-content">
      <!-- 返回按鈕 -->
      <div class="back-button-section">
        <n-button @click="goBack" ghost size="large">
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('common.back') }}
        </n-button>
      </div>
      
      <div class="member-layout">
        <!-- 左側：頭像 -->
        <div class="avatar-section">
          <div class="member-avatar-container">
            <n-avatar
              :size="200"
              :src="getMemberAvatar(member) || '/default-avatar.svg'"
              :fallback-src="'/default-avatar.svg'"
              class="member-avatar"
            />
          </div>
        </div>

        <!-- 右側：詳細信息 -->
        <div class="info-section">
          <div class="member-info-container">
            <!-- 姓名和職位 -->
            <h1 class="member-name">
              {{ getCurrentLocale() === 'zh' ? member.mem_name_zh : member.mem_name_en }}
            </h1>
          
          <div class="member-position">
            {{ getMemberPosition(member) }}
          </div>

          <!-- 聯繫方式 -->
          <div v-if="member.mem_email" class="contact-info">
            <n-icon size="16" class="contact-icon">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
              </svg>
            </n-icon>
            <span>{{ member.mem_email }}</span>
          </div>

          <!-- 所屬課題組 -->
          <div v-if="researchGroup" class="research-group" @click="toResearchGroup">
            <n-icon size="16" class="contact-icon">
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M16 4c0-1.11.89-2 2-2s2 .89 2 2-.89 2-2 2-2-.89-2-2M4 1v6h6V5.5l6 6v-2.84c-.94-.18-2-.76-2-1.66s1.06-1.48 2-1.66V1H4zm14.5 17.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5"/>
              </svg>
            </n-icon>
            <span class="group-link">{{ getResearchGroupName() }}</span>
          </div>

          <!-- 個人描述 -->
          <div v-if="member.mem_desc_zh || member.mem_desc_en" class="member-description">
            <h3>{{ $t('members.description') }}</h3>
            <MarkdownRenderer :source="getMemberDescription()" />
          </div>
          </div>
        </div>
      </div>

      <!-- 相關論文 -->
      <div v-if="relatedPapers.length > 0" class="related-papers-section">
        <h2 class="section-title">{{ $t('members.relatedPapers') }}</h2>
        <div class="papers-list">
          <PaperCard 
            v-for="paper in relatedPapers" 
            :key="paper.paper_id" 
            :paper="paper"
            :show-actions="true"
            :show-preview-image="true"
            @click="toPaper"
            @open-url="openPaperUrl"
            @download="downloadPaper"
          />
        </div>
      </div>
    </div>

    <!-- 沒有找到成員 -->
    <div v-else class="not-found-state">
      <n-empty :description="$t('emptyStates.memberNotFound')" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { memberApi, researchGroupApi, paperApi } from '@/services/api';
import { useMembers } from '@/composables/useMembers';
import { getMediaUrl } from '@/utils/media';
import type { Member, ResearchGroup, Paper, ApiError } from '@/types/api';
import MarkdownRenderer from '@/components/MarkdownRenderer.vue';
import PaperCard from '@/components/PaperCard.vue';

const route = useRoute();
const router = useRouter();
const { locale, t } = useI18n();
const { getMemberAvatar, getMemberPosition } = useMembers();

// 響應式數據
const member = ref<Member | null>(null);
const researchGroup = ref<ResearchGroup | null>(null);
const relatedPapers = ref<Paper[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// 計算屬性
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

const getMemberDescription = () => {
  if (!member.value) return '';
  const desc = getCurrentLocale() === 'zh' ? member.value.mem_desc_zh : member.value.mem_desc_en;
  return desc || '';
};

const getResearchGroupName = () => {
  if (!researchGroup.value) return '';
  return getCurrentLocale() === 'zh' ? researchGroup.value.research_group_name_zh : researchGroup.value.research_group_name_en;
};

// 方法
const fetchMemberDetail = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const memberId = parseInt(route.params.id as string);
    if (isNaN(memberId)) {
      error.value = t('errorMessages.invalidMemberId');
      return;
    }

    // 獲取成員詳情
    const memberResponse = await memberApi.getMember(memberId);
    if (memberResponse.code === 0) {
      member.value = memberResponse.data;
      
      // 獲取所屬課題組信息
      if (member.value.research_group_id) {
        try {
          const groupResponse = await researchGroupApi.getResearchGroup(member.value.research_group_id);
          if (groupResponse.code === 0) {
            researchGroup.value = groupResponse.data;
          }
        } catch (err: unknown) {
          console.warn('Failed to fetch research group:', err);
        }
      }
      
      // 獲取相關論文 (作為作者的論文)
      try {
        const papersResponse = await paperApi.getPapers({ 
          all: 'true', 
          sort_by: 'paper_date', 
          order: 'desc' 
        });
        if (papersResponse.code === 0) {
          // 篩選出該成員參與的論文
          relatedPapers.value = papersResponse.data.items.filter(paper => 
            paper.authors && paper.authors.some(author => author.mem_id === memberId)
          );
        }
      } catch (err: unknown) {
        console.warn('Failed to fetch related papers:', err);
      }
      
    } else {
      error.value = memberResponse.message;
    }
  } catch (err: unknown) {
    console.error('Failed to fetch member detail:', err);
    const apiError = err as ApiError;
    error.value = apiError?.message || t('errorMessages.fetchMemberDetail');
  } finally {
    loading.value = false;
  }
};

const toResearchGroup = () => {
  if (member.value?.research_group_id) {
    router.push(`/group/${member.value.research_group_id}`);
  }
};

const toPaper = (paper: Paper) => {
  // 跳轉到論文詳情頁面
  router.push(`/paper/${paper.paper_id}`);
};

const openPaperUrl = (url: string) => {
  window.open(url, '_blank');
};

const downloadPaper = (paper: Paper) => {
  if (paper.paper_file_path) {
    const downloadUrl = getMediaUrl(paper.paper_file_path);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = `${paper.paper_title_zh || paper.paper_title_en || 'paper'}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};

const goBack = () => {
  router.back();
};

// 生命週期
onMounted(() => {
  fetchMemberDetail();
});

// 監聽路由參數變化
watch(() => route.params.id, () => {
  fetchMemberDetail();
});
</script>

<style scoped>
.member-detail-view {
  padding: 0.5rem 1rem;
  max-width: 160rem;
  min-width: 20rem;
  margin: 0 auto;
  width: 100%;
}

.member-detail-skeleton,
.member-detail-content {
  width: 100%;
}

.error-state,
.not-found-state {
  text-align: center;
  padding: 5rem 1.25rem;
}

/* 返回按鈕區域 */
.back-button-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

/* Flex 布局容器 */
.member-layout {
  display: flex;
  gap: 3rem;
  align-items: flex-start;
  min-height: 25rem;
}

/* 頭像區域 */
.avatar-section {
  flex: 0 0 auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-width: 15rem;
}

.member-avatar-container {
  text-align: center;
  position: sticky;
  top: 1.5rem;
}

.member-avatar {
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.member-avatar:hover {
  transform: scale(1.02);
  box-shadow: 0 0.75rem 3rem rgba(0, 0, 0, 0.15);
}

/* 信息區域 */
.info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 18.75rem;
}

.member-info-container {
  flex: 1;
  padding-left: 0;
}

.member-name {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}

.member-position {
  font-size: 1.25rem;
  color: #1890ff;
  font-weight: 600;
  margin-bottom: 1.25rem;
}

.contact-info,
.research-group {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
  font-size: 1rem;
  color: #666;
}

.contact-icon {
  margin-right: 0.5rem;
  color: #1890ff;
  flex-shrink: 0;
}

.research-group {
  cursor: pointer;
  transition: color 0.3s ease;
}

.research-group:hover {
  color: #1890ff;
}

.group-link {
  color: #1890ff;
  text-decoration: underline;
}

.member-description {
  margin-top: 1.5rem;
}

.member-description h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  color: #333;
}

.description-content {
  font-size: 1rem;
  line-height: 1.6;
  color: #666;
}

/* 相關論文區域 */
.related-papers-section {
  margin-top: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #333;
}

.papers-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1890ff;
  border-bottom: 0.125rem solid #1890ff;
  padding-bottom: 0.5rem;
}

.papers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.paper-item {
  padding: 1.25rem;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 0.125rem solid transparent;
}

.paper-item:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.15);
  border-color: #1890ff;
}

.paper-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.paper-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
  color: #333;
  flex: 1;
  margin-right: 0.75rem;
  line-height: 1.4;
}

.paper-venue {
  font-size: 0.9rem;
  color: #1890ff;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.paper-date {
  font-size: 0.875rem;
  color: #999;
  margin-bottom: 0.5rem;
}

.paper-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 暗色主題支持 */
[data-theme="dark"] .back-button-section,
.dark .back-button-section {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .member-detail-view,
.dark .member-detail-view,
.dark-mode .member-detail-view {
  color: #fff;
}

[data-theme="dark"] .member-position,
.dark .member-position,
.dark-mode .member-position {
  color: #70a1ff;
}

[data-theme="dark"] .contact-info,
[data-theme="dark"] .research-group,
.dark .contact-info,
.dark .research-group,
.dark-mode .contact-info,
.dark-mode .research-group {
  color: #ccc;
}

[data-theme="dark"] .member-description h3,
.dark .member-description h3,
.dark-mode .member-description h3 {
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

[data-theme="dark"] .paper-item,
.dark .paper-item,
.dark-mode .paper-item {
  background: rgb(24, 24, 28);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.2);
}

[data-theme="dark"] .paper-item:hover,
.dark .paper-item:hover,
.dark-mode .paper-item:hover {
  background: rgb(32, 32, 36);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.3);
  border-left-color: #70a1ff;
}

[data-theme="dark"] .paper-title,
.dark .paper-title,
.dark-mode .paper-title {
  color: #fff;
}

[data-theme="dark"] .paper-venue,
.dark .paper-venue,
.dark-mode .paper-venue {
  color: #70a1ff;
}

[data-theme="dark"] .paper-date,
.dark .paper-date,
.dark-mode .paper-date {
  color: #bbb;
}

[data-theme="dark"] .paper-description,
.dark .paper-description,
.dark-mode .paper-description {
  color: #ccc;
}

/* 響應式設計 */
@media (max-width: 48rem) {
  .member-detail-view {
    padding: 1rem;
    min-width: auto;
  }
  
  .member-layout {
    flex-direction: column;
    gap: 1.5rem;
    align-items: center;
    text-align: center;
  }
  
  .avatar-section {
    min-width: auto;
  }
  
  .member-avatar-container {
    position: static;
  }
  
  .info-section {
    min-height: auto;
    width: 100%;
  }
  
  .member-name {
    font-size: 2rem;
  }
  
  .member-position {
    font-size: 1.125rem;
  }
  
  .contact-info,
  .research-group {
    justify-content: center;
  }
  
  .paper-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .paper-title {
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
}

@media (max-width: 30rem) {
  .member-avatar {
    width: 9.375rem !important;
    height: 9.375rem !important;
  }
  
  .member-name {
    font-size: 1.75rem;
  }
}
</style>

<style>
/* KaTeX數學公式樣式 - 全局樣式，不使用scoped */
.math-display {
  margin: 1.5em 0;
  padding: 0.8em;
  background-color: #fafafa;
  border-left: 4px solid #007bff;
  border-radius: 4px;
  overflow-x: auto;
}

.math-error {
  color: #dc3545;
  background-color: #f8d7da;
  border-color: #f5c6cb;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-family: 'Courier New', monospace;
}

/* 研究領域TAG樣式 - 全局樣式，不使用scoped */
.research-tags-container {
  margin: 1.5rem 0;
  padding: 1rem;
  background: var(--research-tags-bg, linear-gradient(135deg, #f8f9fa, #e9ecef));
  border-radius: 0.75rem;
  border: 1px solid var(--research-tags-border, #dee2e6);
  transition: all 0.3s ease;
}

.research-tags-container:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.research-tags-label {
  display: inline-block;
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.research-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.research-tag {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  background: linear-gradient(135deg, #1890ff, #40a9ff);
  color: white;
  border-radius: 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  box-shadow: 0 2px 6px rgba(24, 144, 255, 0.3);
}

.research-tag:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.4);
  background: linear-gradient(135deg, #40a9ff, #69c0ff);
}

/* 個人主頁TAG樣式 - 全局樣式，不使用scoped */
.homepage-container {
  margin: 1.5rem 0;
  padding: 1rem;
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border-radius: 0.75rem;
  border: 1px solid #bae6fd;
  transition: all 0.3s ease;
}

.homepage-container:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.homepage-label {
  display: inline-block;
  font-weight: 600;
  color: #0369a1;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.homepage-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #0ea5e9, #38bdf8);
  color: white;
  text-decoration: none;
  border-radius: 0.75rem;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.3);
}

.homepage-link:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(14, 165, 233, 0.4);
  background: linear-gradient(135deg, #38bdf8, #7dd3fc);
  color: white;
  text-decoration: none;
}

.homepage-icon,
.homepage-external-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.homepage-text {
  flex: 1;
}

.homepage-external-icon {
  opacity: 0.8;
}

/* 論文列表TAG樣式 - 全局樣式，不使用scoped */
.papers-list-container {
  margin: 1.5rem 0;
  padding: 1rem;
  background: linear-gradient(135deg, #fefce8, #fef3c7);
  border-radius: 0.75rem;
  border: 1px solid #fbbf24;
  transition: all 0.3s ease;
}

.papers-list-container:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.papers-list-label {
  display: inline-block;
  font-weight: 600;
  color: #92400e;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.papers-list-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #92400e;
  font-size: 0.9rem;
}

.loading-spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid #fbbf24;
  border-top: 2px solid #92400e;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.papers-list-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.papers-list-item {
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 0.5rem;
  border: 1px solid rgba(251, 191, 36, 0.3);
  transition: all 0.3s ease;
  cursor: pointer;
}

.papers-list-item:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: #fbbf24;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.papers-list-item-title {
  font-weight: 600;
  color: #92400e;
  margin-bottom: 0.25rem;
  font-size: 0.95rem;
  line-height: 1.4;
}

.papers-list-item-venue {
  font-size: 0.8rem;
  color: #d97706;
  margin-bottom: 0.25rem;
}

.papers-list-item-date {
  font-size: 0.75rem;
  color: #a16207;
}

@media (prefers-color-scheme: dark) {
  .math-display {
    background-color: #2a2a2a;
    border-left-color: #4dabf7;
  }
  
  .math-error {
    color: #f8d7da;
    background-color: #721c24;
    border-color: #a94442;
  }

  .research-tags-container {
    background: var(--research-tags-bg, linear-gradient(135deg, #1f1f23, #2a2a2e));
    border-color: var(--research-tags-border, #3a3a3e);
  }

  .research-tags-label {
    color: #e9ecef;
  }

  .research-tag {
    background: linear-gradient(135deg, #4dabf7, #74c0fc);
    box-shadow: 0 2px 6px rgba(77, 171, 247, 0.3);
  }

  .research-tag:hover {
    background: linear-gradient(135deg, #74c0fc, #91d5ff);
    box-shadow: 0 4px 12px rgba(77, 171, 247, 0.4);
  }

  .homepage-container {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border-color: #334155;
  }

  .homepage-label {
    color: #7dd3fc;
  }

  .homepage-link {
    background: linear-gradient(135deg, #0284c7, #0ea5e9);
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.3);
  }

  .homepage-link:hover {
    background: linear-gradient(135deg, #0ea5e9, #38bdf8);
    box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4);
  }

  .papers-list-container {
    background: linear-gradient(135deg, #292524, #1c1917);
    border-color: #78716c;
  }

  .papers-list-label {
    color: #fbbf24;
  }

  .papers-list-loading {
    color: #fbbf24;
  }

  .loading-spinner {
    border-color: #78716c;
    border-top-color: #fbbf24;
  }

  .papers-list-item {
    background: rgba(41, 37, 36, 0.8);
    border-color: rgba(120, 113, 108, 0.3);
  }

  .papers-list-item:hover {
    background: rgba(41, 37, 36, 0.95);
    border-color: #78716c;
  }

  .papers-list-item-title {
    color: #fbbf24;
  }

  .papers-list-item-venue {
    color: #f59e0b;
  }

  .papers-list-item-date {
    color: #d97706;
  }
}

@media (max-width: 768px) {
  .math-display {
    padding: 0.5em;
    font-size: 0.9em;
  }

  .research-tags-container {
    margin: 1rem 0;
    padding: 0.75rem;
  }

  .research-tags-label {
    font-size: 0.9rem;
  }

  .research-tag {
    font-size: 0.8rem;
    padding: 0.3rem 0.6rem;
  }

  .homepage-container {
    margin: 1rem 0;
    padding: 0.75rem;
  }

  .homepage-label {
    font-size: 0.9rem;
  }

  .homepage-link {
    padding: 0.65rem 0.85rem;
    font-size: 0.85rem;
  }

  .homepage-icon,
  .homepage-external-icon {
    width: 1.1rem;
    height: 1.1rem;
  }

  .papers-list-container {
    margin: 1rem 0;
    padding: 0.75rem;
  }

  .papers-list-label {
    font-size: 0.9rem;
  }

  .papers-list-item {
    padding: 0.65rem;
  }

  .papers-list-item-title {
    font-size: 0.9rem;
  }

  .papers-list-item-venue {
    font-size: 0.75rem;
  }

  .papers-list-item-date {
    font-size: 0.7rem;
  }
}
</style>