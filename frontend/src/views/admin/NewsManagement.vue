<template>
  <div class="news-management">
    <n-card :title="t('admin.newsManagement')">
      <n-empty description="待開發" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.news-management {
  padding: 20px;
}
</style>