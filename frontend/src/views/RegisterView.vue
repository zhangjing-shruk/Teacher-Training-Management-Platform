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
        <p class="mt-2 text-sm text-gray-600">创建您的账户</p>
      </div>

      <!-- 注册表单 -->
      <div class="bg-white rounded-lg shadow-lg p-8">
        <form @submit.prevent="handleRegister" class="space-y-6">
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
            {{ error }}
          </div>
          
          <div v-if="success" class="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-md">
            {{ success }}
          </div>
          
          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700 mb-2">姓名</label>
            <input
              id="full_name"
              v-model="form.full_name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-400 focus:border-blue-400"
              placeholder="请输入您的姓名"
            />
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">邮箱地址</label>
            <input
              id="email"
              v-model="form.email"
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
              v-model="form.password"
              type="password"
              required
              minlength="6"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-400 focus:border-blue-400"
              placeholder="请输入密码（至少6位）"
            />
          </div>
          
          <div>
            <label for="role" class="block text-sm font-medium text-gray-700 mb-2">角色</label>
            <select
              id="role"
              v-model="form.role"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-400 focus:border-blue-400"
            >
              <option value="">请选择角色</option>
              <option value="teacher">教师</option>
              <option value="manager">管理员</option>
            </select>
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-400 disabled:opacity-50"
          >
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>
        
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            已有账户？
            <router-link to="/login" class="font-medium text-blue-500 hover:text-blue-600">
              立即登录
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'
import type { RegisterData } from '@/stores/supabaseAuth'

const router = useRouter()
const authStore = useSupabaseAuthStore()

const form = ref<RegisterData>({
  email: '',
  password: '',
  full_name: '',
  role: 'teacher'
})

const loading = ref(false)
const error = ref<string | null>(null)
const success = ref<string | null>(null)

const handleRegister = async () => {
  loading.value = true
  error.value = null
  success.value = null

  try {
    await authStore.register(form.value)
    success.value = '注册成功！请检查您的邮箱以验证账户。'
    
    // 3秒后跳转到登录页面
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (err: any) {
    error.value = err.message || '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>