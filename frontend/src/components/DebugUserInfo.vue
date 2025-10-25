<template>
  <div class="fixed top-4 right-4 bg-white border border-gray-300 rounded-lg p-4 shadow-lg z-50 max-w-sm">
    <h3 class="text-lg font-semibold mb-2">调试信息</h3>
    <div class="space-y-2 text-sm">
      <div>
        <strong>认证状态:</strong> {{ authStore.isAuthenticated ? '已登录' : '未登录' }}
      </div>
      <div v-if="authStore.user">
        <strong>用户ID:</strong> {{ authStore.user.id }}
      </div>
      <div v-if="authStore.user">
        <strong>邮箱:</strong> {{ authStore.user.email }}
      </div>
      <div v-if="authStore.user">
        <strong>姓名:</strong> {{ authStore.user.full_name }}
      </div>
      <div v-if="authStore.user">
        <strong>角色:</strong> {{ authStore.user.role }}
      </div>
      <div>
        <strong>当前路由:</strong> {{ $route.path }}
      </div>
      <div v-if="authStore.error">
        <strong>错误:</strong> {{ authStore.error }}
      </div>
    </div>
    <button 
      @click="refreshUserInfo" 
      class="mt-2 px-3 py-1 bg-blue-500 text-white rounded text-xs"
    >
      刷新用户信息
    </button>
  </div>
</template>

<script setup lang="ts">
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'
import { useRoute } from 'vue-router'

const authStore = useSupabaseAuthStore()
const $route = useRoute()

const refreshUserInfo = async () => {
  if (authStore.session?.user?.id) {
    await authStore.fetchUserProfile(authStore.session.user.id)
  }
}
</script>