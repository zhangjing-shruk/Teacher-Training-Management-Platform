<template>
  <div class="space-y-8">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">数据分析</h1>
        <p class="mt-2 text-gray-600">查看平台使用情况和培训效果分析</p>
      </div>
      <div class="flex space-x-3">
        <select
          v-model="timeRange"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="7d">最近7天</option>
          <option value="30d">最近30天</option>
          <option value="90d">最近90天</option>
          <option value="1y">最近一年</option>
        </select>
        <button
          @click="exportData"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>导出报告</span>
        </button>
      </div>
    </div>

    <!-- 核心指标卡片 -->
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
            <p class="text-sm font-medium text-gray-600">活跃教师</p>
            <p class="text-2xl font-semibold text-gray-900">{{ analytics.activeTeachers }}</p>
            <p class="text-xs text-green-600">+12% 较上月</p>
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
            <p class="text-sm font-medium text-gray-600">完成讲座</p>
            <p class="text-2xl font-semibold text-gray-900">{{ analytics.completedLectures }}</p>
            <p class="text-xs text-green-600">+8% 较上月</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">平均评分</p>
            <p class="text-2xl font-semibold text-gray-900">{{ analytics.averageScore }}</p>
            <p class="text-xs text-green-600">+0.3 较上月</p>
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
            <p class="text-sm font-medium text-gray-600">平均时长</p>
            <p class="text-2xl font-semibold text-gray-900">{{ analytics.averageDuration }}分钟</p>
            <p class="text-xs text-red-600">-5% 较上月</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 讲座完成趋势 -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">讲座完成趋势</h3>
        <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <p class="mt-2 text-sm text-gray-500">图表组件占位符</p>
            <p class="text-xs text-gray-400">显示过去30天的讲座完成数量趋势</p>
          </div>
        </div>
      </div>

      <!-- 教师评分分布 -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">教师评分分布</h3>
        <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
            </svg>
            <p class="mt-2 text-sm text-gray-500">饼图组件占位符</p>
            <p class="text-xs text-gray-400">显示不同评分区间的教师分布</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 详细数据表格 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 教师排行榜 -->
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">教师排行榜</h3>
          <span class="text-sm text-gray-500">按评分排序</span>
        </div>
        <div class="space-y-3">
          <div v-for="(teacher, index) in topTeachers" :key="teacher.id" 
               class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold"
                   :class="getRankClass(index)">
                {{ index + 1 }}
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ teacher.name }}</p>
                <p class="text-sm text-gray-500">{{ teacher.subject }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="font-semibold text-gray-900">{{ teacher.score }}</p>
              <p class="text-sm text-gray-500">{{ teacher.lectureCount }}次讲座</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 最新活动 -->
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">最新活动</h3>
          <button class="text-sm text-blue-600 hover:text-blue-800">查看全部</button>
        </div>
        <div class="space-y-3">
          <div v-for="activity in recentActivities" :key="activity.id" 
               class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
            <div class="w-8 h-8 rounded-full flex items-center justify-center"
                 :class="getActivityIconClass(activity.type)">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getActivityIconPath(activity.type)" />
              </svg>
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
              <p class="text-xs text-gray-500">{{ activity.description }}</p>
              <p class="text-xs text-gray-400 mt-1">{{ formatTime(activity.timestamp) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 系统性能指标 -->
    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">系统性能指标</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="text-center">
          <div class="w-16 h-16 mx-auto bg-blue-100 rounded-full flex items-center justify-center mb-3">
            <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-gray-900">{{ performance.responseTime }}ms</p>
          <p class="text-sm text-gray-600">平均响应时间</p>
          <div class="mt-2 w-full bg-gray-200 rounded-full h-2">
            <div class="bg-blue-600 h-2 rounded-full" :style="`width: ${Math.min(performance.responseTime / 10, 100)}%`"></div>
          </div>
        </div>

        <div class="text-center">
          <div class="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-3">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-gray-900">{{ performance.uptime }}%</p>
          <p class="text-sm text-gray-600">系统可用性</p>
          <div class="mt-2 w-full bg-gray-200 rounded-full h-2">
            <div class="bg-green-600 h-2 rounded-full" :style="`width: ${performance.uptime}%`"></div>
          </div>
        </div>

        <div class="text-center">
          <div class="w-16 h-16 mx-auto bg-purple-100 rounded-full flex items-center justify-center mb-3">
            <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-gray-900">{{ performance.storageUsed }}GB</p>
          <p class="text-sm text-gray-600">存储使用量</p>
          <div class="mt-2 w-full bg-gray-200 rounded-full h-2">
            <div class="bg-purple-600 h-2 rounded-full" :style="`width: ${(performance.storageUsed / performance.storageTotal) * 100}%`"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Analytics {
  activeTeachers: number
  completedLectures: number
  averageScore: number
  averageDuration: number
}

interface Teacher {
  id: number
  name: string
  subject: string
  score: number
  lectureCount: number
}

interface Activity {
  id: number
  type: 'lecture' | 'review' | 'upload' | 'login'
  title: string
  description: string
  timestamp: string
}

interface Performance {
  responseTime: number
  uptime: number
  storageUsed: number
  storageTotal: number
}

// 虚拟数据
const analytics = ref<Analytics>({
  activeTeachers: 89,
  completedLectures: 234,
  averageScore: 8.7,
  averageDuration: 25
})

const topTeachers = ref<Teacher[]>([
  { id: 1, name: '张老师', subject: '英语', score: 9.5, lectureCount: 12 },
  { id: 2, name: '李老师', subject: '数学', score: 9.3, lectureCount: 8 },
  { id: 3, name: '王老师', subject: '语文', score: 9.1, lectureCount: 15 },
  { id: 4, name: '刘老师', subject: '物理', score: 8.9, lectureCount: 6 },
  { id: 5, name: '陈老师', subject: '化学', score: 8.7, lectureCount: 10 }
])

const recentActivities = ref<Activity[]>([
  {
    id: 1,
    type: 'lecture',
    title: '张老师完成讲座',
    description: '英语发音技巧训练',
    timestamp: '2024-01-15T10:30:00'
  },
  {
    id: 2,
    type: 'review',
    title: '李老师讲座已评审',
    description: '数学教学方法改进',
    timestamp: '2024-01-15T09:15:00'
  },
  {
    id: 3,
    type: 'upload',
    title: '新培训资料上传',
    description: '课堂互动技巧指南',
    timestamp: '2024-01-15T08:45:00'
  },
  {
    id: 4,
    type: 'login',
    title: '王老师登录系统',
    description: '开始新的培训课程',
    timestamp: '2024-01-15T08:00:00'
  }
])

const performance = ref<Performance>({
  responseTime: 245,
  uptime: 99.8,
  storageUsed: 156,
  storageTotal: 500
})

const timeRange = ref('30d')

const getRankClass = (index: number) => {
  const classes = [
    'bg-yellow-100 text-yellow-800', // 第1名
    'bg-gray-100 text-gray-800',     // 第2名
    'bg-orange-100 text-orange-800', // 第3名
    'bg-blue-100 text-blue-800',     // 其他
    'bg-blue-100 text-blue-800'      // 其他
  ]
  return classes[index] || 'bg-blue-100 text-blue-800'
}

const getActivityIconClass = (type: string) => {
  const classes = {
    lecture: 'bg-blue-100 text-blue-600',
    review: 'bg-green-100 text-green-600',
    upload: 'bg-purple-100 text-purple-600',
    login: 'bg-gray-100 text-gray-600'
  }
  return classes[type as keyof typeof classes] || 'bg-gray-100 text-gray-600'
}

const getActivityIconPath = (type: string) => {
  const paths = {
    lecture: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',
    review: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    upload: 'M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12',
    login: 'M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1'
  }
  return paths[type as keyof typeof paths] || 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

const exportData = () => {
  alert(`导出${timeRange.value}的数据报告\n包含：\n- 教师活动统计\n- 讲座完成情况\n- 系统性能指标\n- 详细分析报告`)
}
</script>