<template>
  <div class="home">
    <!-- Full Screen Carousel -->
    <div class="carousel-container">
      <n-carousel autoplay class="full-carousel">
        <img
            class="carousel-img"
            src="https://naive-ui.oss-cn-beijing.aliyuncs.com/carousel-img/carousel1.jpeg"
        >
        <img
            class="carousel-img"
            src="https://naive-ui.oss-cn-beijing.aliyuncs.com/carousel-img/carousel2.jpeg"
        >
        <img
            class="carousel-img"
            src="https://naive-ui.oss-cn-beijing.aliyuncs.com/carousel-img/carousel3.jpeg"
        >
        <img
            class="carousel-img"
            src="https://naive-ui.oss-cn-beijing.aliyuncs.com/carousel-img/carousel4.jpeg"
        >
      </n-carousel>
    </div>
    
    <!-- Page Content -->
    <div class="page-content" :class="{ 'dark-theme': isDarkMode }">
      <div class="content-wrapper">
        <h1 style="text-align: center; margin-bottom: 32px; font-size: 28px; font-weight: bold;">{{ $t('researchGroups.title') }}</h1>
        
        <!-- 加載狀態 -->
        <div v-if="loading" style="text-align: center; padding: 40px;">
          <n-spin size="large" />
          <p style="margin-top: 16px;">{{ $t('common.loading') }}</p>
        </div>
        
        <!-- 錯誤狀態 -->
        <div v-else-if="error" style="text-align: center; padding: 40px;">
          <n-alert type="warning" :title="$t('common.error')" style="margin-bottom: 16px;">
            {{ error }}
          </n-alert>
          <n-button @click="fetchResearchGroups" type="primary" ghost>
            重試
          </n-button>
        </div>
        
        <!-- 課題組列表 -->
        <n-grid v-else :x-gap="12" :y-gap="8" :cols="3">
          <n-grid-item v-for="group in researchGroups" :key="group.research_group_id">
            <div class="card-container">
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
                  {{ getCurrentLocale() === 'zh' ? group.research_group_desc_zh : group.research_group_desc_en }}
                </div>
                <template #action>
                  <n-button size="small" type="primary" ghost>
                    {{ $t('researchGroups.viewDetails') }}
                  </n-button>
                </template>
              </n-card>
            </div>
          </n-grid-item>
        </n-grid>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue';
import { useRouter } from "vue-router";
import { useI18n } from 'vue-i18n';
import { useResearchGroupsWithAutoFetch } from '@/composables/useResearchGroups';
import type { ResearchGroup } from '@/types/api';

const router = useRouter();
const { locale } = useI18n();

// 從全域狀態獲取主題
const isDarkMode = inject('isDarkMode', false);

// 使用 composable 獲取課題組數據
const { researchGroups, loading, error, fetchResearchGroups } = useResearchGroupsWithAutoFetch();

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value;
};

// 跳轉到研究組詳情頁面
const toResearchGroup = (group: ResearchGroup) => {
  router.push(`/members?group=${group.research_group_id}`);
};
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
  padding: 40px 24px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

/* 確保導覽欄在輪播上方 */
:deep(.header-nav) {
  z-index: 1001 !important;
}

/* 卡片容器 - 統一高度 */
.card-container {
  height: 100%;
}

/* 研究組卡片樣式 */
.research-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

:deep(.research-card .n-card__content) {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 卡片描述 - 固定高度和文字溢出處理 */
.card-description {
  flex: 1;
  min-height: 60px;
  max-height: 80px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
  line-height: 1.4;
  margin-bottom: 12px;
}

/* 統一卡片最小高度 */
:deep(.research-card) {
  min-height: 200px;
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
</style>