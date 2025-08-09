<template>
  <div class="project-management">
    <n-card :title="t('admin.projectManagement')">
      <n-empty description="待開發" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.project-management {
  padding: 20px;
}
</style>