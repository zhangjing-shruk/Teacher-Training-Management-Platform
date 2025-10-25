<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900">重置密码</h3>
        <button 
          @click="closeModal"
          class="text-gray-400 hover:text-gray-600 focus:outline-none"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <form @submit.prevent="handleResetPassword" class="space-y-4">
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
          {{ error }}
        </div>

        <div v-if="success" class="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-md">
          {{ success }}
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
            邮箱地址
          </label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="请输入您的邮箱地址"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-1">
            新密码
          </label>
          <input
            id="newPassword"
            v-model="form.newPassword"
            type="password"
            required
            placeholder="请输入新密码"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
            确认新密码
          </label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            placeholder="请再次输入新密码"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div class="flex space-x-3 pt-4">
          <button
            type="button"
            @click="closeModal"
            class="flex-1 px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="flex-1 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {{ loading ? '重置中...' : '确认重置' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'

interface Props {
  show: boolean
}

interface Emits {
  (e: 'close'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const authStore = useSupabaseAuthStore()

const form = ref({
  email: '',
  newPassword: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref<string | null>(null)
const success = ref<string | null>(null)

const closeModal = () => {
  emit('close')
  resetForm()
}

const resetForm = () => {
  form.value = {
    email: '',
    newPassword: '',
    confirmPassword: ''
  }
  error.value = null
  success.value = null
  loading.value = false
}

const handleResetPassword = async () => {
  error.value = null
  success.value = null

  // 验证密码
  if (form.value.newPassword !== form.value.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }

  if (form.value.newPassword.length < 6) {
    error.value = '密码长度至少为6位'
    return
  }

  loading.value = true

  try {
    await authStore.resetPassword({
      email: form.value.email,
      newPassword: form.value.newPassword
    })
    
    success.value = '密码重置成功！请使用新密码登录'
    
    // 2秒后关闭弹窗
    setTimeout(() => {
      closeModal()
    }, 2000)
  } catch (err: any) {
    error.value = err.message || '重置密码失败，请重试'
  } finally {
    loading.value = false
  }
}

// 监听show属性变化，重置表单
watch(() => props.show, (newShow) => {
  if (!newShow) {
    resetForm()
  }
})
</script>