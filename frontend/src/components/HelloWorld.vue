<template>
  <div class="hello-world">
    <h2>{{ title }}</h2>
    <p>{{ message }}</p>
    <button @click="handleClick">點擊我</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  title?: string
  message?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Hello World',
  message: '這是一個 Vue 3 組件示例'
})

const emit = defineEmits<{
  clicked: []
}>()

const clickCount = ref(0)

function handleClick() {
  clickCount.value++
  emit('clicked')
}
</script>

<style scoped>
.hello-world {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  text-align: center;
}

h2 {
  color: #3498db;
  margin-bottom: 1rem;
}

p {
  color: #7f8c8d;
  margin-bottom: 1rem;
}

button {
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #27ae60;
}
</style>