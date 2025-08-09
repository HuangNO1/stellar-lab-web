<template>
  <div class="paper-management">
    <n-card :title="t('admin.paperManagement')">
      <n-empty description="待開發" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.paper-management {
  padding: 20px;
}
</style>