<template>
  <div class="home">
    <h1>歡迎來到 Lab Web 應用程式</h1>
    <p class="description">
      這是一個使用 Vue 3 + TypeScript + Vite 構建的現代化 Web 應用程式
    </p>
    
    <div class="features">
      <div class="feature-card">
        <h3>🚀 現代技術棧</h3>
        <p>使用 Vue 3 Composition API、TypeScript 和 Vite</p>
      </div>
      
      <div class="feature-card">
        <h3>📱 響應式設計</h3>
        <p>適配各種設備和螢幕尺寸</p>
      </div>
      
      <div class="feature-card">
        <h3>⚡ 快速開發</h3>
        <p>熱重載和快速構建體驗</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 首頁組件邏輯
</script>

<style scoped>
.home {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.description {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 3rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}
</style>