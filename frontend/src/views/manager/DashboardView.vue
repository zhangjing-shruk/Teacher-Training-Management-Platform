<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-3xl font-bold text-gray-900">管理概览</h1>
      <p class="mt-2 text-gray-600">教师培训平台整体运营数据</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">总教师数</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalTeachers }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">已完成培训</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.completedTraining }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">进行中培训</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.inProgressTraining }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">待评审讲座</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.pendingReviews }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="card">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">最近活动</h2>
      <div class="space-y-4">
        <div v-for="activity in recentActivities" :key="activity.id" class="flex items-center space-x-4">
          <div class="flex-shrink-0">
            <div class="w-2 h-2 bg-blue-400 rounded-full"></div>
          </div>
          <div class="flex-1">
            <p class="text-sm text-gray-900">{{ activity.description }}</p>
            <p class="text-xs text-gray-500">{{ activity.time }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- API占位符标记 -->
    <div class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
      <h3 class="text-sm font-medium text-yellow-800">API占位符</h3>
      <div class="text-xs text-yellow-600 mt-1 space-y-1">
        <p>GET /api/manager/stats - 获取统计数据</p>
        <p>GET /api/manager/activities - 获取最近活动</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 统计数据接口
interface Stats {
  totalTeachers: number
  completedTraining: number
  inProgressTraining: number
  pendingReviews: number
}

// 活动数据接口
interface Activity {
  id: number
  description: string
  time: string
}

// 数据状态
const stats = ref<Stats>({
  totalTeachers: 0,
  completedTraining: 0,
  inProgressTraining: 0,
  pendingReviews: 0
})

const recentActivities = ref<Activity[]>([])

// 加载统计数据
const loadStats = async () => {
  try {
    // TODO: 调用API获取统计数据
    // const response = await fetch('/api/manager/stats')
    // const data = await response.json()
    // stats.value = data
    console.log('加载统计数据')
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载最近活动
const loadRecentActivities = async () => {
  try {
    // TODO: 调用API获取最近活动
    // const response = await fetch('/api/manager/activities')
    // const data = await response.json()
    // recentActivities.value = data
    console.log('加载最近活动')
  } catch (error) {
    console.error('加载最近活动失败:', error)
  }
}

// 生命周期
onMounted(() => {
  loadStats()
  loadRecentActivities()
})
</script>