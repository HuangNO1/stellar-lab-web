import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useMainStore = defineStore('main', () => {
  // 狀態
  const count = ref(0)
  const user = ref<{ name: string; email: string } | null>(null)

  // 計算屬性
  const doubleCount = computed(() => count.value * 2)
  const isAuthenticated = computed(() => user.value !== null)

  // 動作
  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function setUser(userData: { name: string; email: string }) {
    user.value = userData
  }

  function logout() {
    user.value = null
  }

  return {
    count,
    user,
    doubleCount,
    isAuthenticated,
    increment,
    decrement,
    setUser,
    logout
  }
})