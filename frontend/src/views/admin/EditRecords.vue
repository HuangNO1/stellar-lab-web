<template>
  <div class="edit-records">
    <n-card :title="t('admin.editRecords')">
      <n-empty description="待開發" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.edit-records {
  padding: 20px;
}
</style>