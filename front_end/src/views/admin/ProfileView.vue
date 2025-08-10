<template>
  <div class="profile-view">
    <div class="page-header">
      <h2>{{ $t('admin.user.profile') }}</h2>
    </div>

    <n-card>
      <n-result
        status="info"
        :title="$t('admin.common.comingSoon')"
        :description="$t('admin.common.comingSoonDesc')"
      >
        <template #footer>
          <n-button @click="router.push('/admin/dashboard')">
            {{ $t('admin.layout.dashboard') }}
          </n-button>
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
.profile-view {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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