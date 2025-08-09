<template>
  <div class="research-groups">
    <n-card :title="t('admin.researchGroups')">
      <n-empty description="待開發" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.research-groups {
  padding: 20px;
}
</style>