<template>
  <div class="not-found-view">
    <div class="not-found-container">
      <!-- 404 圖標 -->
      <div class="error-icon">
        <svg viewBox="0 0 24 24" class="icon">
          <path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M13,7H11V13H13V7M11,15V17H13V15H11Z"/>
        </svg>
      </div>
      
      <!-- 錯誤碼 -->
      <div class="error-code">404</div>
      
      <!-- 錯誤標題 -->
      <h1 class="error-title">{{ $t('admin.error.pageNotFound') }}</h1>
      
      <!-- 錯誤描述 -->
      <p class="error-description">{{ $t('admin.error.pageNotFoundDescription') }}</p>
      
      <!-- 操作按鈕 -->
      <div class="error-actions">
        <n-button 
          type="primary" 
          size="large"
          @click="goHome"
          class="action-button"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('admin.error.backToHome') }}
        </n-button>
        
        <n-button 
          size="large"
          @click="goBack"
          class="action-button"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"/>
              </svg>
            </n-icon>
          </template>
          {{ $t('common.goBack') }}
        </n-button>
      </div>
    </div>
    
    <!-- 背景裝飾 -->
    <div class="background-decoration">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const goHome = () => {
  router.push('/');
};

const goBack = () => {
  // 如果有歷史記錄，返回上一頁；否則回到首頁
  if (window.history.length > 1) {
    router.go(-1);
  } else {
    router.push('/');
  }
};
</script>

<style scoped>
.not-found-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  padding: 2rem;
}

.not-found-container {
  text-align: center;
  max-width: 70rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 3rem 5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 2;
}

.error-icon {
  margin-bottom: 2rem;
}

.error-icon .icon {
  width: 120px;
  height: 120px;
  color: #667eea;
  opacity: 0.8;
}

.error-code {
  font-size: 8rem;
  font-weight: 900;
  color: #667eea;
  line-height: 1;
  margin-bottom: 1rem;
  text-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.error-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 1.5rem 0;
  line-height: 1.2;
}

.error-description {
  font-size: 1.25rem;
  color: #6b7280;
  margin: 0 0 3rem 0;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.action-button {
  min-width: 150px;
  height: 48px;
}

/* 背景裝飾 */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.floating-shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 100px;
  height: 100px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 10%;
  animation-delay: 2s;
}

.shape-3 {
  width: 80px;
  height: 80px;
  bottom: 10%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-20px) rotate(120deg);
  }
  66% {
    transform: translateY(20px) rotate(240deg);
  }
}

/* 暗色主題支持 */
[data-theme="dark"] .not-found-container,
.dark .not-found-container {
  background: rgba(31, 41, 55, 0.95);
}

[data-theme="dark"] .error-title,
.dark .error-title {
  color: #f9fafb;
}

[data-theme="dark"] .error-description,
.dark .error-description {
  color: #d1d5db;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .not-found-view {
    padding: 1rem;
  }
  
  .not-found-container {
    padding: 2rem 1.5rem;
  }
  
  .error-code {
    font-size: 6rem;
  }
  
  .error-title {
    font-size: 2rem;
  }
  
  .error-description {
    font-size: 1.125rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .action-button {
    width: 100%;
    max-width: 280px;
  }
  
  .error-icon .icon {
    width: 80px;
    height: 80px;
  }
}

@media (max-width: 480px) {
  .not-found-container {
    padding: 1.5rem 1rem;
  }
  
  .error-code {
    font-size: 4.5rem;
  }
  
  .error-title {
    font-size: 1.75rem;
  }
  
  .error-description {
    font-size: 1rem;
  }
  
  .floating-shape {
    display: none; /* 在小屏幕上隱藏裝飾元素 */
  }
}
</style>