import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginCredentials } from '@/types/auth'
import { authApi } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const login = async (credentials: LoginCredentials) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await authApi.login(credentials)
      
      // 存储token
      localStorage.setItem('access_token', response.access_token)
      token.value = response.access_token
      user.value = response.user
    } catch (err: any) {
      error.value = err.message || '登录失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    error.value = null
    
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  const validateToken = async () => {
    if (!token.value) {
      return false
    }
    
    try {
      const currentUser = await authApi.getCurrentUser()
      user.value = currentUser
      return true
    } catch (error) {
      console.log('Token validation failed:', error)
      logout()
      return false
    }
  }

  const initializeAuth = async () => {
    const storedToken = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      try {
        user.value = JSON.parse(storedUser)
        // 验证token是否仍然有效
        await validateToken()
      } catch {
        logout()
      }
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    login,
    logout,
    validateToken,
    initializeAuth
  }
})