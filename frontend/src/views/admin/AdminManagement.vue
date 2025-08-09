<template>
  <div class="admin-management">
    <n-card :title="t('admin.adminManagement')">
      <n-empty description="待開發" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.admin-management {
  padding: 20px;
}
</style>