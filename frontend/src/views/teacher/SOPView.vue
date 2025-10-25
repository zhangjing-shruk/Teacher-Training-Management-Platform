<template>
  <div class="space-y-8">
    <!-- 页面标题 -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900">SOP 流程</h1>
      <p class="mt-2 text-gray-600">标准化教学流程和操作指南</p>
    </div>

    <!-- 学习进度概览 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">总流程数</h3>
            <p class="text-2xl font-bold text-blue-600">{{ sopDocuments.length }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">已完成</h3>
            <p class="text-2xl font-bold text-green-600">{{ completedCount }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">完成率</h3>
            <p class="text-2xl font-bold text-purple-600">{{ completionRate }}%</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 流程分类筛选 -->
    <div class="card">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">流程分类</label>
          <select v-model="selectedCategory" class="w-full border border-gray-300 rounded-md px-3 py-2">
            <option value="">全部分类</option>
            <option value="teaching">教学流程</option>
            <option value="assessment">评估流程</option>
            <option value="management">管理流程</option>
            <option value="emergency">应急流程</option>
          </select>
        </div>
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">学习状态</label>
          <select v-model="selectedStatus" class="w-full border border-gray-300 rounded-md px-3 py-2">
            <option value="">全部状态</option>
            <option value="completed">已完成</option>
            <option value="in_progress">学习中</option>
            <option value="not_started">未开始</option>
          </select>
        </div>
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">搜索</label>
          <input v-model="searchQuery" type="text" placeholder="搜索流程名称..." 
                 class="w-full border border-gray-300 rounded-md px-3 py-2">
        </div>
      </div>
    </div>

    <!-- SOP流程列表 -->
    <div class="space-y-6">
      <div v-for="document in filteredDocuments" :key="document.id" class="card">
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="text-lg font-semibold text-gray-900">{{ document.title }}</h3>
              <span class="px-2 py-1 text-xs font-medium rounded-full"
                    :class="getStatusColor(document.status)">
                {{ getStatusText(document.status) }}
              </span>
              <span class="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800">
                {{ getCategoryName(document.category) }}
              </span>
            </div>
            <p class="text-gray-600 mb-3">{{ document.description }}</p>
            <div class="flex items-center gap-4 text-sm text-gray-500">
              <span>{{ document.steps.length }} 个步骤</span>
              <span>预计 {{ document.estimatedTime }} 分钟</span>
              <span>更新于 {{ document.updatedAt }}</span>
            </div>
          </div>
          <div class="flex gap-2">
            <button @click="startLearning(document)" 
                    :disabled="document.status === 'completed'"
                    class="btn-primary"
                    :class="{ 'opacity-50 cursor-not-allowed': document.status === 'completed' }">
              {{ document.status === 'completed' ? '已完成' : document.status === 'in_progress' ? '继续学习' : '开始学习' }}
            </button>
            <button @click="viewDocument(document)" class="btn-secondary">
              查看详情
            </button>
          </div>
        </div>

        <!-- 进度条 -->
        <div class="mb-4">
          <div class="flex items-center justify-between text-sm text-gray-600 mb-1">
            <span>学习进度</span>
            <span>{{ document.progress }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                 :style="{ width: document.progress + '%' }"></div>
          </div>
        </div>

        <!-- 流程步骤预览 -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="font-medium text-gray-900 mb-3">流程步骤</h4>
          <div class="space-y-2">
            <div v-for="(step, index) in document.steps.slice(0, 3)" :key="step.id"
                 class="flex items-center gap-3">
              <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium"
                   :class="step.completed ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'">
                {{ index + 1 }}
              </div>
              <span class="text-sm" :class="step.completed ? 'text-green-800' : 'text-gray-700'">
                {{ step.title }}
              </span>
              <svg v-if="step.completed" class="h-4 w-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div v-if="document.steps.length > 3" class="text-sm text-gray-500 ml-9">
              还有 {{ document.steps.length - 3 }} 个步骤...
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 学习建议 -->
    <div class="card bg-blue-50 border-blue-200">
      <h2 class="text-xl font-semibold text-blue-900 mb-4">学习建议</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white rounded-lg p-4 border border-blue-200">
          <h3 class="font-medium text-blue-900 mb-2">📚 推荐优先学习</h3>
          <p class="text-blue-800 text-sm">建议先完成"课堂教学基本流程"，这是其他流程的基础。</p>
        </div>
        <div class="bg-white rounded-lg p-4 border border-blue-200">
          <h3 class="font-medium text-blue-900 mb-2">⏰ 学习时间安排</h3>
          <p class="text-blue-800 text-sm">每天安排30-45分钟学习SOP流程，循序渐进掌握标准操作。</p>
        </div>
        <div class="bg-white rounded-lg p-4 border border-blue-200">
          <h3 class="font-medium text-blue-900 mb-2">🎯 实践应用</h3>
          <p class="text-blue-800 text-sm">学习完每个流程后，建议在试讲练习中实际应用。</p>
        </div>
        <div class="bg-white rounded-lg p-4 border border-blue-200">
          <h3 class="font-medium text-blue-900 mb-2">📝 定期复习</h3>
          <p class="text-blue-800 text-sm">建议每周复习已学习的流程，确保操作标准化。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface SOPStep {
  id: number
  title: string
  description: string
  completed: boolean
}

interface SOPDocument {
  id: number
  title: string
  description: string
  category: string
  status: 'not_started' | 'in_progress' | 'completed'
  progress: number
  estimatedTime: number
  updatedAt: string
  steps: SOPStep[]
}

// 筛选条件
const selectedCategory = ref('')
const selectedStatus = ref('')
const searchQuery = ref('')

// 虚拟SOP文档数据
const sopDocuments = ref<SOPDocument[]>([])

// 加载SOP文档数据
const loadSOPDocuments = async () => {
  try {
    // TODO: 调用API获取SOP文档数据
    // const response = await fetch('/api/teacher/sop-documents')
    // const data = await response.json()
    // sopDocuments.value = data
    console.log('加载SOP文档数据')
  } catch (error) {
    console.error('加载SOP文档失败:', error)
  }
}

// 计算属性
const filteredDocuments = computed(() => {
  return sopDocuments.value.filter(doc => {
    const matchesCategory = !selectedCategory.value || doc.category === selectedCategory.value
    const matchesStatus = !selectedStatus.value || doc.status === selectedStatus.value
    const matchesSearch = !searchQuery.value || 
      doc.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      doc.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    return matchesCategory && matchesStatus && matchesSearch
  })
})

const completedCount = computed(() => {
  return sopDocuments.value.filter(doc => doc.status === 'completed').length
})

const completionRate = computed(() => {
  if (sopDocuments.value.length === 0) return 0
  return Math.round((completedCount.value / sopDocuments.value.length) * 100)
})

// 工具函数
const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-green-100 text-green-800'
    case 'in_progress': return 'bg-blue-100 text-blue-800'
    case 'not_started': return 'bg-gray-100 text-gray-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'completed': return '已完成'
    case 'in_progress': return '学习中'
    case 'not_started': return '未开始'
    default: return '未知'
  }
}

const getCategoryName = (category: string) => {
  const names = {
    teaching: '教学流程',
    assessment: '评估流程',
    management: '管理流程',
    emergency: '应急流程'
  }
  return names[category as keyof typeof names] || '未知'
}

// 操作函数
const startLearning = (document: SOPDocument) => {
  if (document.status === 'completed') return
  
  console.log('开始学习SOP流程:', document.title)
  // TODO: 实现学习功能
  alert(`开始学习: ${document.title}`)
}

const viewDocument = (document: SOPDocument) => {
  console.log('查看SOP文档详情:', document.title)
  // TODO: 跳转到详细页面
  alert(`查看详情: ${document.title}`)
}

// 生命周期
onMounted(() => {
  loadSOPDocuments()
})
</script>