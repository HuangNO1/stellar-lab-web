<template>
  <div class="not-found-page">
    <n-result
      status="404"
      title="404 找不到頁面"
      description="您訪問的頁面不存在"
    >
      <template #footer>
        <n-button @click="$router.push('/')">
          回到首頁
        </n-button>
      </template>
    </n-result>
  </div>
</template>

<script setup lang="ts">
// 404 page
</script>

<style scoped>
.not-found-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
}
</style>