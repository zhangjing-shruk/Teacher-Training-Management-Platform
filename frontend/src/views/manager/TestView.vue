<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-3xl font-bold text-gray-900">测试页面</h1>
      <p class="mt-2 text-gray-600">这是一个测试页面，用于验证导航功能</p>
    </div>

    <div class="card">
      <h2 class="text-xl font-semibold mb-4">导航测试</h2>
      <p class="text-gray-600 mb-4">如果您能看到这个页面，说明导航功能正常工作。</p>
      
      <div class="space-y-2">
        <p><strong>当前路由:</strong> {{ $route.path }}</p>
        <p><strong>当前时间:</strong> {{ currentTime }}</p>
        <p><strong>用户信息:</strong> {{ authStore.user?.full_name || '未获取到用户信息' }}</p>
      </div>
    </div>

    <div class="card">
      <h2 class="text-xl font-semibold mb-4">快速导航</h2>
      <div class="grid grid-cols-2 gap-4">
        <router-link to="/manager/dashboard" class="btn-secondary">
          返回仪表板
        </router-link>
        <router-link to="/manager/teachers" class="btn-secondary">
          教师管理
        </router-link>
        <router-link to="/manager/materials" class="btn-secondary">
          培训资料
        </router-link>
        <router-link to="/manager/analytics" class="btn-secondary">
          数据分析
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'

const authStore = useSupabaseAuthStore()
const currentTime = ref('')

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
})

const updateTime = () => {
  currentTime.value = new Date().toLocaleString()
}
</script>