<template>
  <div class="system-manage">
    <div class="page-header">
      <h2>{{ $t('admin.menu.system') }}</h2>
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
.dark .page-header h2 {
  color: #f9fafb;
}
</style>