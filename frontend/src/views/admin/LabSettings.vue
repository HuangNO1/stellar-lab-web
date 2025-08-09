<template>
  <div class="lab-settings">
    <n-card :title="t('admin.labSettings')">
      <n-empty description="待開發" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.lab-settings {
  padding: 20px;
}
</style>