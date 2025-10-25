<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">认证状态测试</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 用户状态 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">用户状态</h2>
          <div class="space-y-2">
            <div><strong>认证状态:</strong> {{ authStore.isAuthenticated ? '已登录' : '未登录' }}</div>
            <div><strong>加载中:</strong> {{ authStore.loading ? '是' : '否' }}</div>
            <div v-if="authStore.error"><strong>错误:</strong> {{ authStore.error }}</div>
          </div>
        </div>

        <!-- 会话信息 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">会话信息</h2>
          <div v-if="authStore.session">
            <div><strong>用户ID:</strong> {{ authStore.session.user?.id }}</div>
            <div><strong>邮箱:</strong> {{ authStore.session.user?.email }}</div>
            <div><strong>访问令牌:</strong> {{ authStore.session.access_token ? '存在' : '不存在' }}</div>
          </div>
          <div v-else>
            <p class="text-gray-500">无会话信息</p>
          </div>
        </div>

        <!-- 用户资料 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">用户资料</h2>
          <div v-if="authStore.user">
            <div><strong>ID:</strong> {{ authStore.user.id }}</div>
            <div><strong>邮箱:</strong> {{ authStore.user.email }}</div>
            <div><strong>姓名:</strong> {{ authStore.user.full_name }}</div>
            <div><strong>角色:</strong> {{ authStore.user.role }}</div>
            <div><strong>状态:</strong> {{ authStore.user.is_active ? '活跃' : '非活跃' }}</div>
            <div><strong>创建时间:</strong> {{ authStore.user.created_at }}</div>
          </div>
          <div v-else>
            <p class="text-gray-500">无用户资料</p>
          </div>
        </div>

        <!-- 角色检查 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">角色检查</h2>
          <div class="space-y-2">
            <div><strong>是教师:</strong> {{ authStore.isTeacher ? '是' : '否' }}</div>
            <div><strong>是管理员:</strong> {{ authStore.isManager ? '是' : '否' }}</div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="mt-8 space-x-4">
        <button 
          @click="refreshAuth" 
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          刷新认证状态
        </button>
        <button 
          @click="testLogin" 
          class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          测试登录
        </button>
        <button 
          @click="goToManager" 
          class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
        >
          跳转到管理员界面
        </button>
        <button 
          @click="goToTeacher" 
          class="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600"
        >
          跳转到教师界面
        </button>
      </div>

      <!-- 日志 -->
      <div class="mt-8 bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">操作日志</h2>
        <div class="bg-gray-100 p-4 rounded max-h-64 overflow-y-auto">
          <div v-for="(log, index) in logs" :key="index" class="text-sm mb-1">
            <span class="text-gray-500">{{ log.time }}</span> - {{ log.message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'

const router = useRouter()
const authStore = useSupabaseAuthStore()
const logs = ref<Array<{ time: string, message: string }>>([])

const addLog = (message: string) => {
  logs.value.push({
    time: new Date().toLocaleTimeString(),
    message
  })
}

const refreshAuth = async () => {
  addLog('开始刷新认证状态...')
  try {
    await authStore.initializeAuth()
    addLog('认证状态刷新完成')
  } catch (error: any) {
    addLog(`认证状态刷新失败: ${error.message}`)
  }
}

const testLogin = async () => {
  addLog('开始测试登录...')
  try {
    const result = await authStore.login({
      email: 'zhangjing32@51talk.com',
      password: 'admin123456'
    })
    addLog(`登录成功: ${JSON.stringify(result)}`)
  } catch (error: any) {
    addLog(`登录失败: ${error.message}`)
  }
}

const goToManager = () => {
  addLog('跳转到管理员界面...')
  router.push('/manager')
}

const goToTeacher = () => {
  addLog('跳转到教师界面...')
  router.push('/teacher')
}

onMounted(() => {
  addLog('页面加载完成')
  addLog(`当前认证状态: ${authStore.isAuthenticated}`)
  addLog(`当前用户角色: ${authStore.user?.role || '无'}`)
})
</script>