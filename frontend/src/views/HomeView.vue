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
  isLoading.value = true
  errorMessage.value = null

  try {
    await authStore.login(loginForm.value)
    
    // 等待用户资料加载
    let retries = 0
    while (!authStore.user && retries < 10) {
      await new Promise(resolve => setTimeout(resolve, 100))
      retries++
    }
    
    // 根据用户角色重定向
    if (authStore.user) {
      const redirectPath = authStore.user.role === 'manager' ? '/manager' : '/teacher'
      router.push(redirectPath)
    } else {
      // 如果没有用户信息，默认跳转到教师界面
      router.push('/teacher')
    }
  } catch (err: any) {
    errorMessage.value = err.message || '登录失败，请重试'
  } finally {
    isLoading.value = false
  }
}

const fillTestAccount = (email: string, password: string) => {
  loginForm.value.email = email
  loginForm.value.password = password
}


</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo 和标题 -->
      <div class="text-center">
        <div class="mx-auto mb-4">
          <img 
            src="/51talkACADEMY-logo.jpeg" 
            alt="51Talk Academy" 
            class="h-16 w-auto mx-auto rounded-lg shadow-sm"
          />
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

      <!-- 测试账号 -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4 text-center">测试账号</h3>
        <div class="grid grid-cols-2 gap-4">
          <div class="text-center">
            <h4 class="font-medium text-gray-700 mb-2">教师账号</h4>
            <button
              @click="fillTestAccount('teacher1@example.com', 'teacher123')"
              class="w-full px-3 py-2 text-sm bg-green-50 text-green-700 border border-green-200 rounded-md hover:bg-green-100 transition-colors"
            >
              使用教师账号
            </button>
            <p class="text-xs text-gray-500 mt-1">teacher1@example.com</p>
          </div>
          <div class="text-center">
            <h4 class="font-medium text-gray-700 mb-2">管理员账号</h4>
            <button
              @click="fillTestAccount('admin@example.com', 'admin123')"
              class="w-full px-3 py-2 text-sm bg-blue-50 text-blue-700 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
            >
              使用管理员账号
            </button>
            <p class="text-xs text-gray-500 mt-1">admin@example.com</p>
          </div>
        </div>
      </div>

      <!-- 功能介绍 -->
      <div class="text-center text-sm text-gray-600">
        <p>提供智能化的教师培训、试讲练习和专业评估服务</p>
      </div>
    </div>
  </div>
</template>
