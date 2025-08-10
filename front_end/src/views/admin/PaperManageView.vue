<template>
  <div class="paper-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.papers') }}</h2>
      <n-button type="primary" @click="router.push('/admin/papers/create')">
        <template #icon>
          <n-icon>
            <svg viewBox="0 0 24 24">
              <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
            </svg>
          </n-icon>
        </template>
        {{ $t('admin.papers.addPaper') }}
      </n-button>
    </div>

    <n-card>
      <n-result
        status="info"
        :title="$t('admin.common.comingSoon')"
        :description="$t('admin.common.comingSoonDesc')"
      >
        <template #footer>
          <n-space>
            <n-button type="primary" @click="router.push('/admin/members')">
              {{ $t('admin.menu.members') }}
            </n-button>
            <n-button @click="router.push('/admin/dashboard')">
              {{ $t('admin.layout.dashboard') }}
            </n-button>
          </n-space>
        </template>
      </n-result>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<style scoped>
.paper-manage {
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
.dark .page-header h2 {
  color: #f9fafb;
}
</style>