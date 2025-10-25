<template>
  <div class="space-y-8">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">培训概览</h1>
        <p class="mt-2 text-gray-600">欢迎来到AI教师培训平台，开始您的学习之旅</p>
      </div>
      <div class="flex items-center space-x-2">
        <div class="h-3 w-3 bg-green-400 rounded-full animate-pulse"></div>
        <span class="text-sm text-gray-600">在线</span>
      </div>
    </div>

    <!-- 进度概览卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- 学习进度 -->
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">学习资料</h3>
            <p class="text-sm text-gray-600">{{ trainingStatus.materialsCompleted ? '已完成' : '进行中' }}</p>
          </div>
        </div>
        <div class="mt-4">
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-600 h-2 rounded-full transition-all duration-500"
              :style="{ width: trainingStatus.materialsCompleted ? '100%' : '60%' }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 试讲进度 -->
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">试讲练习</h3>
            <p class="text-sm text-gray-600">{{ trainingStatus.lecturesSubmitted }}/{{ trainingStatus.maxLectures }} 次</p>
          </div>
        </div>
        <div class="mt-4">
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-purple-600 h-2 rounded-full transition-all duration-500"
              :style="{ width: `${(trainingStatus.lecturesSubmitted / trainingStatus.maxLectures) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 当前状态 -->
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 rounded-lg flex items-center justify-center"
                 :class="getStatusColor(trainingStatus.currentStatus).bg">
              <svg class="h-6 w-6" :class="getStatusColor(trainingStatus.currentStatus).text" 
                   fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      :d="getStatusIcon(trainingStatus.currentStatus)" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">当前状态</h3>
            <p class="text-sm text-gray-600">{{ getStatusText(trainingStatus.currentStatus) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 培训流程步骤 -->
    <div class="card">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">培训流程</h2>
      <div class="space-y-4">
        <!-- 步骤1: 学习资料 -->
        <div class="flex items-center p-4 rounded-lg border"
             :class="trainingStatus.materialsCompleted ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'">
          <div class="flex-shrink-0">
            <div class="h-8 w-8 rounded-full flex items-center justify-center"
                 :class="trainingStatus.materialsCompleted ? 'bg-green-100 text-green-600' : 'bg-gray-200 text-gray-500'">
              <svg v-if="trainingStatus.materialsCompleted" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span v-else class="text-sm font-medium">1</span>
            </div>
          </div>
          <div class="ml-4 flex-1">
            <h3 class="text-lg font-medium text-gray-900">学习培训资料</h3>
            <p class="text-sm text-gray-600">阅读和下载教学材料，了解教学方法和技巧</p>
          </div>
          <div class="flex-shrink-0">
            <router-link to="/teacher/materials" class="btn-primary">
              {{ trainingStatus.materialsCompleted ? '重新查看' : '开始学习' }}
            </router-link>
          </div>
        </div>

        <!-- 步骤2: 试讲练习 -->
        <div class="flex items-center p-4 rounded-lg border"
             :class="trainingStatus.lecturesSubmitted > 0 ? 'bg-blue-50 border-blue-200' : 'bg-gray-50 border-gray-200'">
          <div class="flex-shrink-0">
            <div class="h-8 w-8 rounded-full flex items-center justify-center"
                 :class="trainingStatus.lecturesSubmitted > 0 ? 'bg-blue-100 text-blue-600' : 'bg-gray-200 text-gray-500'">
              <span class="text-sm font-medium">2</span>
            </div>
          </div>
          <div class="ml-4 flex-1">
            <h3 class="text-lg font-medium text-gray-900">试讲练习</h3>
            <p class="text-sm text-gray-600">录制试讲视频，获得AI智能分析和反馈</p>
          </div>
          <div class="flex-shrink-0">
            <router-link to="/teacher/trial-lecture" 
                         class="btn-primary"
                         :class="{ 'opacity-50 cursor-not-allowed': !trainingStatus.materialsCompleted }">
              开始练习
            </router-link>
          </div>
        </div>

        <!-- 步骤3: SOP学习 -->
        <div class="flex items-center p-4 rounded-lg border"
             :class="trainingStatus.sopUnlocked ? 'bg-yellow-50 border-yellow-200' : 'bg-gray-50 border-gray-200'">
          <div class="flex-shrink-0">
            <div class="h-8 w-8 rounded-full flex items-center justify-center"
                 :class="trainingStatus.sopUnlocked ? 'bg-yellow-100 text-yellow-600' : 'bg-gray-200 text-gray-500'">
              <svg v-if="trainingStatus.sopUnlocked" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span v-else class="text-sm font-medium">3</span>
            </div>
          </div>
          <div class="ml-4 flex-1">
            <h3 class="text-lg font-medium text-gray-900">SOP流程学习</h3>
            <p class="text-sm text-gray-600">学习平台使用和标准化操作流程</p>
          </div>
          <div class="flex-shrink-0">
            <router-link v-if="trainingStatus.sopUnlocked" to="/teacher/sop" class="btn-primary">
              开始学习
            </router-link>
            <span v-else class="text-sm text-gray-500">通过试讲后解锁</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="card">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">最近活动</h2>
      <div class="space-y-4">
        <div v-for="activity in recentActivities" :key="activity.id" 
             class="flex items-center p-3 bg-gray-50 rounded-lg">
          <div class="flex-shrink-0">
            <div class="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
              <svg class="h-4 w-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="activity.icon" />
              </svg>
            </div>
          </div>
          <div class="ml-3 flex-1">
            <p class="text-sm text-gray-900">{{ activity.description }}</p>
            <p class="text-xs text-gray-500">{{ activity.time }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { TrainingStatus } from '@/types/auth'

// 定义活动类型
interface Activity {
  id: number
  description: string
  time: string
  icon: string
}

// 培训状态数据
const trainingStatus = ref<TrainingStatus>({
  materialsCompleted: false,
  lecturesSubmitted: 0,
  maxLectures: 5,
  currentStatus: 'learning',
  sopUnlocked: false
})

// 最近活动数据
const recentActivities = ref<Activity[]>([])

const getStatusColor = (status: string) => {
  const colors = {
    learning: { bg: 'bg-blue-100', text: 'text-blue-600' },
    practicing: { bg: 'bg-purple-100', text: 'text-purple-600' },
    pending_review: { bg: 'bg-yellow-100', text: 'text-yellow-600' },
    passed: { bg: 'bg-green-100', text: 'text-green-600' },
    failed: { bg: 'bg-red-100', text: 'text-red-600' }
  }
  return colors[status as keyof typeof colors] || colors.learning
}

const getStatusText = (status: string) => {
  const texts = {
    learning: '学习中',
    practicing: '练习中',
    pending_review: '待审核',
    passed: '已通过',
    failed: '需重练'
  }
  return texts[status as keyof typeof texts] || '未知状态'
}

const getStatusIcon = (status: string) => {
  const icons = {
    learning: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
    practicing: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',
    pending_review: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
    passed: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    failed: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z'
  }
  return icons[status as keyof typeof icons] || icons.learning
}

// 加载培训状态数据
const loadTrainingStatus = async () => {
  try {
    // TODO: 从API获取实际的培训状态数据
    // const response = await fetch('/api/teacher/training-status')
    // const data = await response.json()
    // trainingStatus.value = data
    console.log('加载培训状态数据...')
  } catch (error) {
    console.error('加载培训状态失败:', error)
  }
}

// 加载最近活动数据
const loadRecentActivities = async () => {
  try {
    // TODO: 从API获取实际的活动数据
    // const response = await fetch('/api/teacher/recent-activities')
    // const data = await response.json()
    // recentActivities.value = data
    console.log('加载最近活动数据...')
  } catch (error) {
    console.error('加载最近活动失败:', error)
  }
}

onMounted(() => {
  loadTrainingStatus()
  loadRecentActivities()
})
</script>