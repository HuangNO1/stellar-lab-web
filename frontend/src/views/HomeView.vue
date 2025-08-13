<template>
  <div class="home">
    <!-- Full Screen Carousel -->
    <div class="carousel-container">
      <n-carousel autoplay class="full-carousel">
        <img v-if="lab?.carousel_img_1" class="carousel-img" :src="getMediaUrl(lab.carousel_img_1)" :alt="$t('defaults.carousel.alt1')" />
        <img v-if="lab?.carousel_img_2" class="carousel-img" :src="getMediaUrl(lab.carousel_img_2)" :alt="$t('defaults.carousel.alt2')" />
        <img v-if="lab?.carousel_img_3" class="carousel-img" :src="getMediaUrl(lab.carousel_img_3)" :alt="$t('defaults.carousel.alt3')" />
        <img v-if="lab?.carousel_img_4" class="carousel-img" :src="getMediaUrl(lab.carousel_img_4)" :alt="$t('defaults.carousel.alt4')" />
        <!-- 如果没有轮播图，显示默认图片 -->
        <img v-if="!hasCarouselImages" 
             class="carousel-img"
             src="../assets/engineering.jpg"
             :alt="$t('defaults.carousel.defaultAlt1')" />
        <img v-if="!hasCarouselImages" 
             class="carousel-img"
             src="../assets/laptop.jpg"
             :alt="$t('defaults.carousel.defaultAlt2')" />
      </n-carousel>
    </div>
    
    <!-- Page Content -->
    <div class="page-content" :class="{ 'dark-theme': isDarkMode }">
      <div class="content-wrapper">
        <!-- 實驗室介紹 -->
        <div class="lab-introduction">
          <h1 class="lab-title">{{ getLabName() }}</h1>
          <div class="lab-description">
            {{ getLabDescription() }}
          </div>
        </div>

        <h1 style="text-align: center; margin-bottom: 32px; font-size: 28px; font-weight: bold;">{{ $t('researchGroups.title') }}</h1>
        
        <!-- 加載狀態 -->
        <div v-if="loading" class="research-groups-section">
          <div class="research-groups-grid">
            <div v-for="i in 6" :key="i" class="research-card-skeleton">
              <n-card class="research-card">
                <template #header>
                  <n-skeleton text :repeat="1" />
                </template>
                <template #header-extra>
                  <n-skeleton text class="skeleton-header-tag" />
                </template>
                <div class="card-description">
                  <n-skeleton text :repeat="3" />
                </div>
                <template #action>
                  <n-skeleton text class="skeleton-action-button" />
                </template>
              </n-card>
            </div>
          </div>
        </div>
        
        <!-- 錯誤狀態 -->
        <div v-else-if="error" style="text-align: center; padding: 40px;">
          <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 16px;">
            {{ error }}
          </n-alert>
          <n-button @click="fetchResearchGroups" type="primary" ghost>
            {{ $t('common.retry') }}
          </n-button>
        </div>
        
        <!-- 課題組列表 -->
        <div v-else class="research-groups-section">
          <div class="research-groups-grid">
            <div v-for="group in researchGroups" :key="group.research_group_id" class="card-container">
              <n-card 
                :title="getCurrentLocale() === 'zh' ? group.research_group_name_zh : group.research_group_name_en" 
                @click="() => toResearchGroup(group)" 
                hoverable
                class="research-card"
              >
                <template #header-extra>
                  <n-tag size="small" type="info">
                    {{ getCurrentLocale() === 'zh' ? group.leader?.mem_name_zh : group.leader?.mem_name_en }}
                  </n-tag>
                </template>
                <div class="card-description">
                  {{ stripMarkdown(getCurrentLocale() === 'zh' ? group.research_group_desc_zh : group.research_group_desc_en) }}
                </div>
                <template #action>
                  <n-button size="small" type="primary" ghost>
                    {{ $t('researchGroups.viewDetails') }}
                  </n-button>
                </template>
              </n-card>
            </div>
          </div>
        </div>
        <!-- 新聞列表 -->
        <div class="news-section">
          <div class="section-header">
            <h2>{{ $t('nav.news') }}</h2>
            <n-button type="primary" ghost @click="toNewsPage">
              {{ $t('news.viewMore') }}
            </n-button>
          </div>

          <!-- 加載狀態 -->
          <div v-if="newsLoading" class="news-skeleton">
            <div v-for="i in 5" :key="i" class="news-item-skeleton">
              <div class="skeleton-tag">
                <n-skeleton text width="3rem" />
              </div>
              <div class="skeleton-content">
                <n-skeleton text width="70%" />
                <n-skeleton text width="40%" style="margin-top: 0.5rem" />
              </div>
            </div>
          </div>

          <!-- 錯誤狀態 -->
          <div v-else-if="newsError" class="error-state">
            <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 1rem;">
              {{ newsError }}
            </n-alert>
            <n-button @click="fetchLatestNews" type="primary" ghost size="small">
              {{ $t('common.retry') }}
            </n-button>
          </div>

          <!-- 新聞列表 -->
          <div v-else class="news-list">
            <div v-if="latestNews.length > 0">
              <div 
                v-for="news in latestNews" 
                :key="news.news_id" 
                class="news-item-compact" 
                @click="() => toNewsDetail(news)"
              >
                <div class="news-item-header">
                  <n-tag 
                    :type="getNewsTypeColor(news.news_type)" 
                    size="small"
                    class="news-tag"
                  >
                    {{ getNewsTypeText(news.news_type) }}
                  </n-tag>
                  <span class="news-date">{{ formatDate(news.news_date) }}</span>
                </div>
                <div class="news-content-compact">
                  <span class="news-title-compact">
                    {{ stripMarkdown(getCurrentLocale() === 'zh' ? news.news_content_zh : (news.news_content_en || news.news_content_zh)) }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- 空狀態 -->
            <div v-else class="empty-state-compact">
              <n-empty :description="$t('news.empty')" size="small" />
            </div>
          </div>
        </div>
        
        <!-- 聯繫我們 -->
        <div class="contact-section">
          <div class="contact-wrapper">
            <h2>{{ $t('common.contact') }}</h2>
            <div class="contact-info">
            <div v-if="lab?.lab_address_zh || lab?.lab_address_en" class="contact-item">
              <n-icon size="20" class="contact-icon">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
              </n-icon>
              <span>{{ getLabAddress() }}</span>
            </div>
            <div v-if="lab?.lab_email" class="contact-item">
              <n-icon size="20" class="contact-icon">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                </svg>
              </n-icon>
              <span>{{ lab?.lab_email }}</span>
            </div>
            <div v-if="lab?.lab_phone" class="contact-item">
              <n-icon size="20" class="contact-icon">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                </svg>
              </n-icon>
              <span>{{ lab?.lab_phone }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import { inject, computed, ref, onMounted } from 'vue';
import { useRouter } from "vue-router";
import { useI18n } from 'vue-i18n';
import { useResearchGroupsWithAutoFetch } from '@/composables/useResearchGroups';
import { getMediaUrl, hasCarouselImages as checkCarouselImages } from '@/utils/media';
import { stripMarkdown } from '@/utils/text';
import { newsApi } from '@/services/api';
import type { ResearchGroup, Lab, News, ApiError } from '@/types/api';

const router = useRouter();
const { t, locale } = useI18n();

// 從全域狀態獲取主題和實驗室數據
const isDarkMode = inject('isDarkMode', false);
const labRef = inject('lab');
const lab = computed(() => labRef && typeof labRef === 'object' && 'value' in labRef ? (labRef as { value: Lab | null }).value : null);

// 使用 composable 獲取課題組數據
const { researchGroups, loading, error, fetchResearchGroups } = useResearchGroupsWithAutoFetch();

// 新聞相關狀態
const latestNews = ref<News[]>([]);
const newsLoading = ref(false);
const newsError = ref<string | null>(null);

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value;
};

// 獲取實驗室名稱
const getLabName = () => {
  if (!lab.value) return t('defaults.labName');
  return locale.value === 'zh' 
    ? (lab.value.lab_zh || t('defaults.labName'))
    : (lab.value.lab_en || t('defaults.labName'));
};

// 獲取實驗室描述
const getLabDescription = () => {
  if (!lab.value) return t('defaults.labDescription');
  return locale.value === 'zh' 
    ? (lab.value.lab_desc_zh || t('defaults.labDescription'))
    : (lab.value.lab_desc_en || t('defaults.labDescription'));
};

// 獲取實驗室地址
const getLabAddress = () => {
  if (!lab.value) return '';
  return locale.value === 'zh' 
    ? (lab.value.lab_address_zh || '')
    : (lab.value.lab_address_en || '');
};


// 檢查是否有輪播圖
const hasCarouselImages = computed(() => {
  return checkCarouselImages(lab.value?.carousel_img_1, lab.value?.carousel_img_2, lab.value?.carousel_img_3, lab.value?.carousel_img_4);
});

// 跳轉到研究組詳情頁面
const toResearchGroup = (group: ResearchGroup) => {
  router.push(`/group/${group.research_group_id}`);
};

// 獲取新聞類型顏色
const getNewsTypeColor = (type: number) => {
  const colorMap = {
    0: 'info',     // 論文發表
    1: 'success',  // 獲獎消息
    2: 'warning'   // 學術活動
  };
  return colorMap[type as keyof typeof colorMap] || 'default';
};

// 獲取新聞類型文本
const getNewsTypeText = (type: number) => {
  const textMap = {
    0: t('news.paperPublished'),
    1: t('news.award'),
    2: t('news.academic')
  };
  return textMap[type as keyof typeof textMap] || t('news.other');
};

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString(getCurrentLocale() === 'zh' ? 'zh-CN' : 'en-US');
};

// 獲取最新新聞
const fetchLatestNews = async () => {
  try {
    newsLoading.value = true;
    newsError.value = null;

    const response = await newsApi.getNews({
      per_page: 10,
      page: 1
    });

    if (response.code === 0) {
      latestNews.value = response.data.items;
    } else {
      newsError.value = response.message || t('common.fetchError');
    }
  } catch (err: unknown) {
    console.error('Failed to fetch latest news:', err);
    const apiError = err as ApiError;
    newsError.value = apiError?.message || t('common.networkError');
  } finally {
    newsLoading.value = false;
  }
};

// 跳轉到新聞頁面
const toNewsPage = () => {
  router.push('/news');
};

// 跳轉到新聞詳情頁面
const toNewsDetail = (news: News) => {
  router.push(`/news/${news.news_id}`);
};

// 生命週期
onMounted(() => {
  fetchLatestNews();
});
</script>
<style scoped>
.home {
  padding: 0;
  margin: 0;
  position: relative;
}

/* Full Screen Carousel Container - 完全覆蓋包括導覽欄 */
.carousel-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1;
  overflow: hidden;
}

.full-carousel {
  width: 100%;
  height: 100%;
}

.carousel-img {
  width: 100%;
  height: 100vh;
  object-fit: cover;
  display: block;
}

/* Page Content - 在輪播下方，全寬度，不透明 */
.page-content {
  position: relative;
  z-index: 2;
  margin-top: 100vh; /* 在全屏輪播下方 */
  padding: 0; /* 移除所有padding */
  width: 100vw; /* 使用viewport width確保全屏寬度 */
  background-color: #fff; /* 預設白色背景 */
  min-height: 50vh; /* 確保有足夠高度 */
  transition: background-color 0.3s ease;
}

/* 深色主題 */
.page-content.dark-theme {
  background-color: rgb(16, 16, 20) !important;
}

/* 內容包裝器 - 控制內容間距 */
.content-wrapper {
  padding: 2.5rem 1.5rem 0;
  max-width: 75rem;
  margin: 0 auto;
  text-align: center;
}

/* 確保導覽欄在輪播上方 */
:deep(.header-nav) {
  z-index: 1001 !important;
}

/* Flex 網格布局 - 課題組卡片 */
.research-groups-section {
  margin-bottom: 3rem;
}

.research-groups-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
}

/* 卡片容器 - 統一高度 */
.card-container {
  flex: 0 0 auto;
  width: 100%;
  max-width: 22rem;
  min-width: 18rem;
}

/* 研究組卡片樣式 */
.research-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 16rem;
}

/* 黑夜模式下的研究組卡片樣式 */
.dark-theme :deep(.research-card.n-card) {
  background-color: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

.dark-theme :deep(.research-card .n-card__header) {
  color: #e6e6e6 !important;
}

.dark-theme :deep(.research-card .n-card__content) {
  color: #cccccc !important;
}

.research-card-skeleton {
  flex: 0 0 auto;
  width: 100%;
  max-width: 22rem;
  min-width: 18rem;
}

:deep(.research-card .n-card__content) {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 卡片描述 - 固定高度和文字溢出處理 */
.card-description {
  flex: 1;
  min-height: 3.75rem;
  max-height: 5rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
  line-height: 1.4;
  margin-bottom: 0.75rem;
  text-align: left;
  padding: 0 0.5rem;
}

/* 黑夜模式下的卡片描述 */
.dark-theme .card-description {
  color: #cccccc !important;
}

/* 黑夜模式下的標籤樣式 */
.dark-theme :deep(.research-card .n-tag) {
  background-color: rgba(24, 144, 255, 0.15) !important;
  color: #70a1ff !important;
  border: 1px solid rgba(24, 144, 255, 0.25) !important;
}

/* 黑夜模式下的按鈕樣式 */
.dark-theme :deep(.research-card .n-button.n-button--ghost) {
  color: #70a1ff !important;
  border-color: #70a1ff !important;
}

.dark-theme :deep(.research-card .n-button.n-button--ghost:hover) {
  background-color: rgba(112, 161, 255, 0.1) !important;
  border-color: #70a1ff !important;
}

/* 黑夜模式下的卡片懸停效果 */
.dark-theme :deep(.research-card.n-card:hover) {
  background-color: rgba(255, 255, 255, 0.12) !important;
  border-color: rgba(255, 255, 255, 0.18) !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* 統一卡片最小高度 */
:deep(.research-card) {
  min-height: 16rem;
}

/* 實驗室介紹樣式 */
.lab-introduction {
  text-align: left;
  margin-bottom: 2.5rem;
  padding: 2rem 0;
  max-width: 50rem;
  margin-left: auto;
  margin-right: auto;
}

.lab-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
}

.lab-description {
  font-size: 1.2rem;
  color: #666;
  line-height: 1.7;
  text-align: justify;
}

/* 暗色主題下的實驗室介紹 */
.dark-theme .lab-description {
  color: #ccc;
}

/* 聯繫我們樣式 - 全屏寬度 */
.contact-section {
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  background: rgba(24, 144, 255, 0.05);
  padding: 0;
  margin-top: 3rem;
}

.contact-wrapper {
  max-width: 75rem;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  text-align: center;
}

.contact-section h2 {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1890ff;
}

.contact-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
  max-width: 37.5rem;
  margin: 0 auto;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  color: #666;
  background: white;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.contact-item:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.15);
}

.contact-icon {
  color: #1890ff;
  flex-shrink: 0;
}

/* 暗色主題下的聯繫信息 */
.dark-theme .contact-section {
  background: rgba(24, 144, 255, 0.1);
}

.dark-theme .contact-section h2 {
  color: #70a1ff;
}

.dark-theme .contact-item {
  background: rgba(255, 255, 255, 0.1);
  color: #ccc;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.dark-theme .contact-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

.dark-theme .contact-icon {
  color: #70a1ff;
}

/* 響應式設計 */
@media (max-width: 1024px) {
  .content-wrapper {
    padding: 2rem 1.25rem 0;
  }
  
  .lab-title {
    font-size: 2.25rem;
  }
  
  .lab-description {
    font-size: 1.125rem;
  }
  
  .research-groups-grid {
    gap: 1.25rem;
  }
  
  .card-container {
    max-width: 20rem;
    min-width: 16rem;
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 2rem 1rem 0;
  }
  
  .lab-introduction {
    text-align: center;
    padding: 1.5rem 0;
  }
  
  .lab-title {
    font-size: 2rem;
  }
  
  .lab-description {
    font-size: 1rem;
    padding: 0 0.5rem;
    text-align: center;
  }
  
  .research-groups-grid {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .card-container,
  .research-card-skeleton {
    max-width: none;
    width: 100%;
    max-width: 28rem;
  }
  
  /* 卡片內字體調整 */
  :deep(.research-card .n-card__header .n-card__header__main) {
    font-size: 1rem !important;
  }
  
  .card-description {
    font-size: 0.9rem;
    line-height: 1.5;
  }
  
  :deep(.research-card .n-tag) {
    font-size: 0.75rem !important;
  }
  
  :deep(.research-card .n-button) {
    font-size: 0.875rem !important;
  }
}

@media (max-width: 640px) {
  .content-wrapper {
    padding: 1.5rem 0.75rem 0;
  }
  
  .lab-title {
    font-size: 1.75rem;
  }
  
  .lab-description {
    font-size: 0.9rem;
  }
  
  .card-container {
    max-width: 24rem;
  }
  
  /* 進一步縮小卡片字體 */
  :deep(.research-card .n-card__header .n-card__header__main) {
    font-size: 0.95rem !important;
  }
  
  .card-description {
    font-size: 0.85rem;
    line-height: 1.4;
  }
  
  :deep(.research-card .n-tag) {
    font-size: 0.7rem !important;
  }
  
  :deep(.research-card .n-button) {
    font-size: 0.8rem !important;
    padding: 0.25rem 0.75rem !important;
  }
}

@media (max-width: 48rem) {
  .content-wrapper {
    padding: 2rem 1rem 0;
  }
  
  .lab-introduction {
    text-align: center;
  }
  
  .lab-title {
    font-size: 2rem;
  }
  
  .lab-description {
    font-size: 1rem;
    padding: 0 1rem;
    text-align: center;
  }
  
  .research-groups-grid {
    flex-direction: column;
    align-items: center;
  }
  
  .card-container,
  .research-card-skeleton {
    max-width: none;
    width: 100%;
  }
  
  .contact-wrapper {
    padding: 1.5rem 1rem;
  }
  
  .contact-info {
    flex-direction: column;
    align-items: center;
  }
  
  .contact-item {
    width: 100%;
    max-width: 18.75rem;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 1.25rem 0.5rem 0;
  }
  
  .lab-title {
    font-size: 1.5rem;
  }
  
  .lab-description {
    font-size: 0.875rem;
  }
  
  .card-container {
    max-width: 20rem;
  }
  
  /* 最小屏幕的卡片字體 */
  :deep(.research-card .n-card__header .n-card__header__main) {
    font-size: 0.9rem !important;
  }
  
  .card-description {
    font-size: 0.8rem;
    line-height: 1.3;
  }
  
  :deep(.research-card .n-tag) {
    font-size: 0.65rem !important;
  }
  
  :deep(.research-card .n-button) {
    font-size: 0.75rem !important;
    padding: 0.2rem 0.6rem !important;
  }
  
  .contact-wrapper {
    padding: 1rem 0.75rem;
  }
  
  .contact-section h2 {
    font-size: 1.5rem;
  }
  
  .contact-item {
    font-size: 0.875rem;
    padding: 0.6rem 0.8rem;
  }
}

/* Carousel深度樣式覆蓋 */
:deep(.n-carousel) {
  width: 100% !important;
  height: 100% !important;
}

:deep(.n-carousel .n-carousel__slides) {
  height: 100% !important;
}

:deep(.n-carousel .n-carousel__slide) {
  height: 100% !important;
}

/* 確保輪播指示器在底部可見 */
:deep(.n-carousel .n-carousel__dots) {
  bottom: 30px !important;
  z-index: 10 !important;
}

:deep(.n-carousel .n-carousel__arrow) {
  background-color: rgba(255, 255, 255, 0.3) !important;
  z-index: 10 !important;
}

:deep(.n-carousel .n-carousel__arrow:hover) {
  background-color: rgba(255, 255, 255, 0.5) !important;
}

/* 骨架屏樣式 */
.skeleton-header-tag {
  width: 60px;
}

.skeleton-action-button {
  width: 80px;
}

/* =============== 新聞列表樣式 =============== */
.news-section {
  margin: 3rem 0;
  padding: 0 1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.section-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 暗色主題下的標題 */
.dark-theme .section-header {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

/* 新聞骨架屏 */
.news-skeleton {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.news-item-skeleton {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 0.5rem;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.skeleton-tag {
  flex-shrink: 0;
}

.skeleton-content {
  flex: 1;
}

/* 錯誤狀態 */
.error-state {
  text-align: center;
  padding: 1.5rem;
  background: rgba(255, 193, 7, 0.05);
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

/* 新聞列表 */
.news-list {
  background: #fff;
  border-radius: 0.75rem;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.dark-theme .news-list {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

/* 緊湊型新聞項 */
.news-item-compact {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.news-item-compact:hover {
  background: rgba(24, 144, 255, 0.04);
  border-color: rgba(24, 144, 255, 0.2);
  transform: translateX(4px);
}

.dark-theme .news-item-compact:hover {
  background: rgba(24, 144, 255, 0.08);
  border-color: rgba(112, 161, 255, 0.3);
}

.news-item-compact + .news-item-compact {
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.dark-theme .news-item-compact + .news-item-compact {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

/* 新聞項頭部 */
.news-item-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  flex-shrink: 0;
  min-width: 6rem;
}

.news-tag {
  font-size: 0.75rem !important;
  padding: 0.25rem 0.5rem !important;
  border-radius: 0.25rem !important;
  font-weight: 500;
}

.news-date {
  font-size: 0.75rem;
  color: #999;
  font-weight: 400;
}

.dark-theme .news-date {
  color: #999;
}

/* 新聞內容 */
.news-content-compact {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
}

.news-title-compact {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.9rem;
  line-height: 1.4;
  color: #333;
  font-weight: 500;
  cursor: pointer;
}

.dark-theme .news-title-compact {
  color: #e6e6e6;
}

.news-title-compact:hover {
  color: #1890ff;
}

.dark-theme .news-title-compact:hover {
  color: #70a1ff;
}

/* 空狀態 */
.empty-state-compact {
  text-align: center;
  padding: 2rem 1rem;
  color: #999;
}

.dark-theme .empty-state-compact {
  color: #666;
}

/* 響應式設計 - 新聞列表 */
@media (max-width: 768px) {
  .news-section {
    margin: 2rem 0;
    padding: 0 0.5rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 1rem;
  }
  
  .section-header h2 {
    font-size: 1.5rem;
    align-self: center;
  }
  
  .news-list {
    padding: 0.75rem;
  }
  
  .news-item-compact {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 1rem;
  }
  
  .news-item-header {
    flex-direction: row;
    width: 100%;
    justify-content: space-between;
    align-items: center;
    min-width: auto;
  }
  
  .news-content-compact {
    width: 100%;
  }
  
  .news-title-compact {
    font-size: 0.95rem;
    -webkit-line-clamp: 3;
  }
}

@media (max-width: 640px) {
  .section-header h2 {
    font-size: 1.375rem;
  }
  
  .news-item-compact {
    padding: 0.75rem;
  }
  
  .news-tag {
    font-size: 0.7rem !important;
    padding: 0.2rem 0.4rem !important;
  }
  
  .news-date {
    font-size: 0.7rem;
  }
  
  .news-title-compact {
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .section-header h2 {
    font-size: 1.25rem;
  }
  
  .news-item-compact {
    padding: 0.6rem;
  }
  
  .news-item-header {
    gap: 0.5rem;
  }
  
  .news-tag {
    font-size: 0.65rem !important;
  }
  
  .news-date {
    font-size: 0.65rem;
  }
  
  .news-title-compact {
    font-size: 0.8rem;
    line-height: 1.3;
  }
}
</style>