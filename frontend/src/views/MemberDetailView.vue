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
            {{ getMemberPosition(member, getCurrentLocale()) }}
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
            <markdown-it :source="getMemberDescription()" :plugins="markdownPlugins"></markdown-it>
          </div>
          </div>
        </div>
      </div>

      <!-- 相關論文 -->
      <div v-if="relatedPapers.length > 0" class="related-papers-section">
        <h2 class="section-title">{{ $t('members.relatedPapers') }}</h2>
        <div class="papers-list">
          <div v-for="paper in relatedPapers" :key="paper.paper_id" class="paper-item" @click="toPaper(paper.paper_id)">
            <div class="paper-header">
              <h4 class="paper-title">
                {{ getCurrentLocale() === 'zh' ? paper.paper_title_zh : paper.paper_title_en }}
              </h4>
              <n-tag v-if="paper.paper_accept === 1" type="success" size="small">
                {{ $t('papers.accepted') }}
              </n-tag>
              <n-tag v-else type="warning" size="small">
                {{ $t('papers.submitted') }}
              </n-tag>
            </div>
            <div class="paper-venue">{{ paper.paper_venue }}</div>
            <div class="paper-date">{{ formatDate(paper.paper_date) }}</div>
            <div v-if="paper.paper_desc_zh || paper.paper_desc_en" class="paper-description">
              {{ getCurrentLocale() === 'zh' ? paper.paper_desc_zh : paper.paper_desc_en }}
            </div>
          </div>
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
import type { Member, ResearchGroup, Paper } from '@/types/api';
import MarkdownIt from 'vue3-markdown-it';

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

// Markdown插件配置
const markdownPlugins = [
  {
    plugin: (md: Record<string, unknown>) => {
      // 修改链接渲染规则
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const defaultRender = (md as any).renderer.rules.link_open || function(tokens: Record<string, unknown>[], idx: number, options: Record<string, unknown>, env: Record<string, unknown>, renderer: Record<string, unknown>) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return (renderer as any).renderToken(tokens, idx, options);
      };

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (md as any).renderer.rules.link_open = function (tokens: Record<string, unknown>[], idx: number, options: Record<string, unknown>, env: Record<string, unknown>, renderer: Record<string, unknown>) {
        const token = tokens[idx];
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const href = (token as any).attrGet('href');
        
        // 检查是否为外部链接
        if (href && (href.startsWith('http://') || href.startsWith('https://') || href.startsWith('//') || href.includes('://'))) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          (token as any).attrSet('target', '_blank');
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          (token as any).attrSet('rel', 'noopener noreferrer');
        }
        
        return defaultRender(tokens, idx, options, env, renderer);
      };
    }
  }
];

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
        } catch (err) {
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
      } catch (err) {
        console.warn('Failed to fetch related papers:', err);
      }
      
    } else {
      error.value = memberResponse.message;
    }
  } catch (err) {
    console.error('Failed to fetch member detail:', err);
    error.value = t('errorMessages.fetchMemberDetail');
  } finally {
    loading.value = false;
  }
};

const toResearchGroup = () => {
  if (member.value?.research_group_id) {
    router.push(`/group/${member.value.research_group_id}`);
  }
};

const toPaper = (paperId: number) => {
  // 跳轉到論文詳情頁面 (假設存在)
  router.push(`/paper/${paperId}`);
};

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString(getCurrentLocale() === 'zh' ? 'zh-CN' : 'en-US');
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
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.2);
}

[data-theme="dark"] .paper-item:hover,
.dark .paper-item:hover,
.dark-mode .paper-item:hover {
  background: rgba(255, 255, 255, 0.12);
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