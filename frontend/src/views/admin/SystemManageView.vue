<template>
  <div class="system-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.system') }}</h2>
    </div>

    <n-grid cols="1 s:2 m:3" responsive="screen" :x-gap="16" :y-gap="16">
      <!-- 操作日誌 -->
      <n-gi>
        <n-card class="system-card" hoverable @click="router.push('/admin/operation-logs')">
          <template #header>
            <n-space align="center">
              <n-icon size="24" color="#1890ff">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                </svg>
              </n-icon>
              <span class="card-title">{{ $t('admin.operationLogs.title') }}</span>
            </n-space>
          </template>
          <p class="card-description">{{ $t('admin.operationLogs.description') }}</p>
          <n-space justify="end">
            <n-button text type="primary">
              {{ $t('admin.common.viewDetails') }}
              <template #icon>
                <n-icon>
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"/>
                  </svg>
                </n-icon>
              </template>
            </n-button>
          </n-space>
        </n-card>
      </n-gi>

      <!-- 其他功能佔位 -->
      <n-gi>
        <n-card class="system-card coming-soon">
          <template #header>
            <n-space align="center">
              <n-icon size="24" color="#52c41a">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"/>
                </svg>
              </n-icon>
              <span class="card-title">{{ $t('admin.system.backup') }}</span>
            </n-space>
          </template>
          <p class="card-description">{{ $t('admin.system.backupDesc') }}</p>
          <n-tag type="info" size="small">{{ $t('admin.common.comingSoon') }}</n-tag>
        </n-card>
      </n-gi>

      <n-gi>
        <n-card class="system-card coming-soon">
          <template #header>
            <n-space align="center">
              <n-icon size="24" color="#faad14">
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
                </svg>
              </n-icon>
              <span class="card-title">{{ $t('admin.system.settings') }}</span>
            </n-space>
          </template>
          <p class="card-description">{{ $t('admin.system.settingsDesc') }}</p>
          <n-tag type="info" size="small">{{ $t('admin.common.comingSoon') }}</n-tag>
        </n-card>
      </n-gi>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<style scoped>
.system-manage {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

[data-theme="dark"] .page-header h2,
.dark .page-header h2,
.dark-theme .page-header h2 {
  color: #f9fafb !important;
}

.system-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
}

.system-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.system-card.coming-soon {
  cursor: default;
  opacity: 0.7;
}

.system-card.coming-soon:hover {
  transform: none;
  box-shadow: none;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

[data-theme="dark"] .card-title,
.dark .card-title {
  color: #f9fafb;
}

.card-description {
  margin: 0.75rem 0 1rem 0;
  color: #6b7280;
  line-height: 1.5;
}

[data-theme="dark"] .card-description,
.dark .card-description {
  color: #9ca3af;
}

/* 響應式設計 */
@media (max-width: 48rem) {
  :deep(.n-grid) {
    gap: 1rem;
  }
  
  .system-card {
    margin-bottom: 0;
  }
}
</style>