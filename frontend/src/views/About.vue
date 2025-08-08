<template>
  <div class="about">
    <h1>關於我們</h1>
    
    <div class="content">
      <section>
        <h2>項目介紹</h2>
        <p>
          這個 Lab Web 應用程式是一個全端開發項目，包含前端和後端兩個部分。
          前端使用 Vue 3 + TypeScript 構建，提供現代化的用戶界面體驗。
        </p>
      </section>
      
      <section>
        <h2>技術棧</h2>
        <div class="tech-stack">
          <div class="tech-item">
            <h3>前端</h3>
            <ul>
              <li>Vue 3</li>
              <li>TypeScript</li>
              <li>Vite</li>
              <li>Vue Router</li>
              <li>Pinia</li>
            </ul>
          </div>
          
          <div class="tech-item">
            <h3>工具</h3>
            <ul>
              <li>ESLint</li>
              <li>Git</li>
              <li>NPM</li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
// 關於頁面組件邏輯
</script>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 2rem;
}

.content {
  line-height: 1.6;
}

section {
  margin-bottom: 2rem;
}

h2 {
  color: #34495e;
  margin-bottom: 1rem;
}

.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 1rem;
}

.tech-item {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.tech-item h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.tech-item ul {
  list-style: none;
  padding: 0;
}

.tech-item li {
  padding: 0.25rem 0;
  color: #7f8c8d;
}

.tech-item li:before {
  content: "•";
  color: #3498db;
  font-weight: bold;
  display: inline-block;
  width: 1em;
  margin-left: -1em;
}
</style>