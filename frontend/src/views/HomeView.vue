<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'
import type { LoginCredentials } from '@/stores/supabaseAuth'

const router = useRouter()
const authStore = useSupabaseAuthStore()

const loginForm = ref<LoginCredentials>({
  email: '',
  password: ''
})

const isLoading = ref(false)
const errorMessage = ref<string | null>(null)

const handleLogin = async () => {
  if (!loginForm.value.email || !loginForm.value.password) {
    errorMessage.value = '请填写邮箱和密码'
    return
  }

  try {
    isLoading.value = true
    errorMessage.value = ''
    
    await authStore.login(loginForm.value)
    
    // 根据用户角色重定向
    if (authStore.user?.role === 'manager') {
      await router.push('/manager')
    } else if (authStore.user?.role === 'teacher') {
      await router.push('/teacher')
    }
  } catch (error: any) {
    errorMessage.value = error.message || '登录失败，请重试'
  } finally {
    isLoading.value = false
  }
}


</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo 和标题 -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 bg-blue-500 rounded-lg flex items-center justify-center mb-4">
          <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-gray-900">AI 教师培训平台</h2>
        <p class="mt-2 text-sm text-gray-600">请登录您的账户</p>
      </div>

      <!-- 登录表单 -->
      <div class="bg-white rounded-lg shadow-lg p-8">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
            {{ errorMessage }}
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">邮箱地址</label>
            <input
              id="email"
              v-model="loginForm.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-400 focus:border-blue-400"
              placeholder="请输入邮箱地址"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">密码</label>
            <input
              id="password"
              v-model="loginForm.password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-400 focus:border-blue-400"
              placeholder="请输入密码"
            />
          </div>
          
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-400 disabled:opacity-50"
          >
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
        </form>
        
        <!-- 注册链接 -->
        <div class="text-center mt-4">
          <p class="text-sm text-gray-600">
            还没有账户？
            <router-link 
              to="/register" 
              class="font-medium text-blue-500 hover:text-blue-600 focus:outline-none focus:underline"
            >
              立即注册
            </router-link>
          </p>
        </div>
      </div>



      <!-- 功能介绍 -->
      <div class="text-center text-sm text-gray-600">
        <p>提供智能化的教师培训、试讲练习和专业评估服务</p>
      </div>
    </div>
  </div>
</template>
