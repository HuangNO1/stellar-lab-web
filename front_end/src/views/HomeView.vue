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
        <img alt="Vue logo" src="../assets/logo.png">
        <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, inject } from 'vue';
import HelloWorld from '@/components/HelloWorld.vue';

export default defineComponent({
  name: 'HomeView',
  components: {
    HelloWorld,
  },
  setup() {
    // 從全域狀態獲取主題
    const isDarkMode = inject('isDarkMode', false);
    
    return {
      isDarkMode
    };
  }
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
  padding: 40px 24px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

/* 確保導覽欄在輪播上方 */
:deep(.header-nav) {
  z-index: 1001 !important;
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