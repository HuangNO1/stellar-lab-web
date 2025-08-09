import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginCredentials } from '@/types'
import { authAPI } from '@/utils/api'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  
  const isLoggedIn = computed(() => !!user.value && !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  
  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await authAPI.login(credentials)
      const { access_token, admin } = response.data
      // 將 admin 信息轉換為 User 格式
      user.value = {
        id: admin.admin_id,
        username: admin.admin_name,
        role: admin.is_super ? 'admin' : 'user',
        created_at: new Date().toISOString(),
        enable: true
      }
      token.value = access_token
      localStorage.setItem('token', access_token)
      return response
    } catch (error) {
      throw error
    }
  }
  
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }
  
  const fetchUserProfile = async () => {
    if (!token.value) return
    try {
      const response = await authAPI.getProfile()
      user.value = response.data
    } catch (error) {
      logout()
      throw error
    }
  }
  
  // 初始化時檢查token
  if (token.value) {
    fetchUserProfile()
  }
  
  return {
    user,
    token,
    isLoggedIn,
    isAdmin,
    login,
    logout,
    fetchUserProfile
  }
})