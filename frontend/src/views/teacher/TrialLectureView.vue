<template>
  <div class="space-y-6">
    <div class="bg-white shadow rounded-lg p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">试讲练习</h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 试讲设置 -->
        <div class="space-y-4">
          <h2 class="text-lg font-semibold text-gray-800">试讲设置</h2>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">选择课程主题</label>
            <select v-model="selectedTopic" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">请选择课程主题</option>
              <option value="math">数学基础</option>
              <option value="chinese">语文阅读</option>
              <option value="english">英语口语</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">试讲时长</label>
            <select v-model="duration" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="5">5分钟</option>
              <option value="10">10分钟</option>
              <option value="15">15分钟</option>
            </select>
          </div>
          
          <button 
            @click="startLecture"
            :disabled="!selectedTopic"
            class="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
          >
            开始试讲
          </button>
        </div>
        
        <!-- 试讲历史 -->
        <div class="space-y-4">
          <h2 class="text-lg font-semibold text-gray-800">试讲历史</h2>
          
          <div class="space-y-3">
            <div v-for="lecture in lectureHistory" :key="lecture.id" 
                 class="border border-gray-200 rounded-lg p-4">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-medium text-gray-900">{{ lecture.topic }}</h3>
                <span class="text-sm text-gray-500">{{ lecture.date }}</span>
              </div>
              <p class="text-sm text-gray-600 mb-2">时长: {{ lecture.duration }}分钟</p>
              <div class="flex justify-between items-center">
                <span class="text-sm font-medium" :class="getScoreColor(lecture.score)">
                  评分: {{ lecture.score }}/100
                </span>
                <router-link 
                  :to="`/teacher/feedback/${lecture.id}`"
                  class="text-primary-600 hover:text-primary-700 text-sm font-medium"
                >
                  查看反馈
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const selectedTopic = ref('')
const duration = ref('10')

const lectureHistory = ref([
  {
    id: 1,
    topic: '数学基础 - 分数运算',
    duration: 10,
    score: 85,
    date: '2024-01-15'
  },
  {
    id: 2,
    topic: '语文阅读 - 古诗词赏析',
    duration: 15,
    score: 92,
    date: '2024-01-12'
  }
])

const startLecture = () => {
  // 开始试讲逻辑
  console.log('开始试讲:', selectedTopic.value, duration.value)
}

const getScoreColor = (score: number) => {
  if (score >= 90) return 'text-green-600'
  if (score >= 80) return 'text-blue-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}
</script>