<template>
  <div class="paper-edit">
    <div class="page-header">
      <h2>{{ isEdit ? $t('admin.papers.editPaper') : $t('admin.papers.addPaper') }}</h2>
    </div>
    
    <n-card>
      <n-result
        status="info"
        :title="$t('admin.common.comingSoon')"
        :description="$t('admin.common.comingSoonDesc')"
      >
        <template #footer>
          <n-button @click="router.back()">{{ $t('common.goBack') }}</n-button>
        </template>
      </n-result>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const isEdit = computed(() => !!route.params.id);
</script>

<style scoped>
.paper-edit {
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