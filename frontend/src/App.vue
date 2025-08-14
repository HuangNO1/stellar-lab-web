<template>
  <n-message-provider>
    <router-view/>
    <n-back-top :right="40" :bottom="40" />
  </n-message-provider>
</template>

<script setup lang="ts">
import { watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { NMessageProvider, NBackTop } from 'naive-ui'
import { useLabWithAutoFetch } from '@/composables/useLab'
import { getMediaUrl } from '@/utils/media'

const { t, locale } = useI18n()
const { lab } = useLabWithAutoFetch()

// 設置網頁標題和圖標
const updatePageTitleAndFavicon = () => {
  // 設置網頁標題
  document.title = getLabTitle()
  
  // 設置 favicon
  if (lab.value?.lab_logo_path) {
    updateFavicon(getMediaUrl(lab.value.lab_logo_path))
  } else {
    // 如果沒有 logo，使用默認的 favicon
    resetFavicon()
  }
}

// 獲取實驗室標題（參考 HomeView.vue 的實作方式）
const getLabTitle = () => {
  if (!lab.value) return t('defaults.labName')
  
  return locale.value === 'zh' 
    ? (lab.value.lab_zh || t('defaults.labName'))
    : (lab.value.lab_en || t('defaults.labName'))
}

// 更新 favicon
const updateFavicon = (iconUrl: string) => {
  // 創建一個圖片元素來檢測圖片是否能正常載入
  const img = new Image()
  
  img.onload = () => {
    // 圖片載入成功，更新 favicon
    updateFaviconLinks(iconUrl)
  }
  
  img.onerror = () => {
    // 圖片載入失敗，使用默認 favicon
    console.warn('Failed to load favicon image:', iconUrl)
    resetFavicon()
  }
  
  img.src = iconUrl
}

// 更新 favicon 連結
const updateFaviconLinks = (iconUrl: string) => {
  // 移除現有的 favicon
  const existingFavicons = document.querySelectorAll('link[rel*="icon"]')
  existingFavicons.forEach(favicon => favicon.remove())
  
  // 添加新的 favicon
  const link = document.createElement('link')
  link.rel = 'icon'
  link.type = 'image/x-icon'
  link.href = iconUrl
  document.head.appendChild(link)
  
  // 也設置 apple-touch-icon 用於移動設備
  const appleTouchIcon = document.createElement('link')
  appleTouchIcon.rel = 'apple-touch-icon'
  appleTouchIcon.href = iconUrl
  document.head.appendChild(appleTouchIcon)
}

// 重置為默認 favicon
const resetFavicon = () => {
  const existingFavicons = document.querySelectorAll('link[rel*="icon"]')
  existingFavicons.forEach(favicon => favicon.remove())
  
  // 添加默認 favicon（如果存在 /favicon.ico）
  const link = document.createElement('link')
  link.rel = 'icon'
  link.type = 'image/x-icon'
  link.href = '/favicon.ico'
  document.head.appendChild(link)
}

// 監聽實驗室數據變化
watch(() => lab.value, () => {
  updatePageTitleAndFavicon()
}, { immediate: true })

// 監聽語言變化
watch(() => locale.value, () => {
  updatePageTitleAndFavicon()
})

// 組件掛載時設置
onMounted(() => {
  updatePageTitleAndFavicon()
})
</script>

<style>
/* 全局基礎樣式重置 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  width: 100%;
  height: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>