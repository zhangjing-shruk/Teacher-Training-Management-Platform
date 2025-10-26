<template>
  <div class="space-y-8">
    <!-- 页面标题 -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900">培训资料</h1>
      <p class="mt-2 text-gray-600">学习教学方法和技巧，为试讲做好准备</p>
    </div>

    <!-- 学习进度概览 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
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
            <h3 class="text-lg font-medium text-gray-900">总资料数</h3>
            <p class="text-2xl font-bold text-blue-600">{{ totalMaterials }}</p>
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
            <p class="text-2xl font-bold text-green-600">{{ completedMaterials }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">完成率</h3>
            <p class="text-2xl font-bold text-purple-600">{{ Math.round((completedMaterials / totalMaterials) * 100) }}%</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选和搜索 -->
    <div class="card">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- 分类筛选 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">分类筛选</label>
          <select v-model="selectedCategory" class="form-select">
            <option value="">全部分类</option>
            <option value="teaching_methods">教学方法</option>
            <option value="classroom_management">课堂管理</option>
            <option value="student_interaction">学生互动</option>
            <option value="assessment">评估技巧</option>
            <option value="教学文档">教学文档</option>
            <option value="其他培训文档">其他培训文档</option>
          </select>
        </div>

        <!-- 状态筛选 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">学习状态</label>
          <select v-model="selectedStatus" class="form-select">
            <option value="">全部状态</option>
            <option value="not_started">未开始</option>
            <option value="in_progress">学习中</option>
            <option value="completed">已完成</option>
          </select>
        </div>

        <!-- 搜索 -->
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-2">搜索资料</label>
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索标题或描述..."
              class="form-input pl-10"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      <span class="ml-3 text-gray-600">正在加载培训资料...</span>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="card">
      <div class="text-center py-8">
        <svg class="mx-auto h-12 w-12 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 15.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">加载失败</h3>
        <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
        <div class="mt-6">
          <button
            @click="fetchMaterials"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            重试
          </button>
        </div>
      </div>
    </div>

    <!-- 培训资料列表 -->
    <div v-else-if="filteredMaterials.length === 0 && !loading" class="card">
      <div class="text-center py-8">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">暂无培训资料</h3>
        <p class="mt-1 text-sm text-gray-500">
          {{ searchQuery || selectedCategory || selectedStatus ? '没有找到符合条件的资料' : '管理员还未上传任何培训资料' }}
        </p>
      </div>
    </div>

    <!-- 资料网格 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="material in filteredMaterials"
        :key="material.id"
        class="card hover:shadow-lg transition-shadow duration-200 flex flex-col h-full"
      >
        <!-- 主要内容区域 -->
        <div class="flex-grow flex flex-col">
          <!-- 头部区域：类别和状态 - 固定高度 -->
          <div class="flex items-start justify-between mb-4 h-12">
            <div class="flex items-center">
              <div 
                class="h-10 w-10 rounded-lg flex items-center justify-center mr-3"
                :class="getCategoryColor(material.category || 'teaching_methods').bg"
              >
                <svg class="h-5 w-5" :class="getCategoryColor(material.category || 'teaching_methods').text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getCategoryIcon(material.category || 'teaching_methods')" />
                </svg>
              </div>
              <div>
                <span 
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="getCategoryColor(material.category || 'teaching_methods').bg + ' ' + getCategoryColor(material.category || 'teaching_methods').text"
                >
                  {{ getCategoryName(material.category || 'teaching_methods') }}
                </span>
              </div>
            </div>
            <span 
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              :class="getStatusColor(material.status || 'not_started')"
            >
              {{ getStatusText(material.status || 'not_started') }}
            </span>
          </div>

          <!-- 标题区域 - 固定高度 -->
          <div class="mb-3 h-14 flex items-start">
            <h3 class="text-lg font-bold text-black line-clamp-2">{{ material.title }}</h3>
          </div>

          <!-- 简介区域 - 可展开 -->
          <div class="mb-4 flex-grow">
            <div class="relative">
              <p 
                class="text-gray-600 transition-all duration-300"
                :class="expandedDescriptions[material.id] ? '' : 'line-clamp-3'"
              >
                {{ material.description }}
              </p>
              <button 
                v-if="material.description && material.description.length > 100"
                @click="toggleDescription(material.id)"
                class="text-blue-600 hover:text-blue-800 text-sm mt-1 font-medium"
              >
                {{ expandedDescriptions[material.id] ? '收起' : 'more' }}
              </button>
            </div>
          </div>

          <!-- 文档类型和时长 - 固定高度 -->
          <div class="flex items-center justify-between text-sm text-gray-500 mb-4 h-5">
            <span>{{ material.type === 'video' ? '视频' : material.type === 'pdf' ? 'PDF文档' : '文档' }}</span>
            <span>{{ material.duration_minutes }}分钟</span>
          </div>

          <!-- 进度条区域 - 固定高度 -->
          <div class="mb-4 h-12">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>学习进度</span>
              <span>{{ material.progress || 0 }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-blue-600 h-2 rounded-full transition-all duration-500"
                   :style="{ width: `${material.progress || 0}%` }"></div>
            </div>
          </div>
        </div>

        <!-- 底部按钮区域 - 固定高度 -->
        <div class="flex gap-2 h-12">
          <button 
            @click="startLearning(material)"
            class="flex-1 btn-primary"
            :disabled="(material.status || 'not_started') === 'completed'"
          >
            {{ (material.status || 'not_started') === 'completed' ? '已完成' : '点击学习' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 学习建议 -->
    <div class="card bg-blue-50 border-blue-200">
      <h2 class="text-xl font-semibold text-blue-900 mb-4">学习建议</h2>
      <div class="space-y-3">
        <div class="flex items-start">
          <div class="h-6 w-6 bg-blue-100 rounded-full flex items-center justify-center mt-0.5">
            <span class="text-xs font-medium text-blue-600">1</span>
          </div>
          <p class="ml-3 text-blue-800">建议按照教学方法 → 课堂管理 → 学生互动 → 评估技巧的顺序学习</p>
        </div>
        <div class="flex items-start">
          <div class="h-6 w-6 bg-blue-100 rounded-full flex items-center justify-center mt-0.5">
            <span class="text-xs font-medium text-blue-600">2</span>
          </div>
          <p class="ml-3 text-blue-800">每个资料学习完成后，建议做笔记并思考如何应用到实际教学中</p>
        </div>
        <div class="flex items-start">
          <div class="h-6 w-6 bg-blue-100 rounded-full flex items-center justify-center mt-0.5">
            <span class="text-xs font-medium text-blue-600">3</span>
          </div>
          <p class="ml-3 text-blue-800">完成所有资料学习后，即可开始试讲练习</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'
import { useLocalAuthStore } from '@/stores/localAuth'
import { LearningProgressService } from '@/services/supabaseService'
import { TrainingMaterialService } from '@/services/supabaseService'

interface TrainingMaterial {
  id: number
  title: string
  description: string
  type: string
  duration_minutes: number
  // 文件相关属性
  file_url?: string
  file_path?: string
  file_size?: string
  download_count?: number
  // 前端添加的字段用于显示和筛选
  category?: string
  status?: 'not_started' | 'in_progress' | 'completed'
  progress?: number
  learning_progress_id?: number
  total_study_seconds?: number
}

// 使用认证store
const authStore = useSupabaseAuthStore()
const localAuthStore = useLocalAuthStore()

// 筛选条件
const selectedCategory = ref('')
const selectedStatus = ref('')
const searchQuery = ref('')

// 数据状态
const materials = ref<TrainingMaterial[]>([])
const loading = ref(false)
const error = ref('')

// 学习计时器相关
const learningTimers = ref<Record<string, number>>({})
const currentLearningMaterial = ref<string | null>(null)

// 简介展开状态
const expandedDescriptions = ref<Record<number, boolean>>({})

// 获取培训资料
const fetchMaterials = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // 使用 Supabase 服务获取培训资料
    const { TrainingMaterialService } = await import('@/services/supabaseService')
    const data = await TrainingMaterialService.getAll()

    // 根据认证模式获取学习进度
    let progressData: any[] = []
    
    if (import.meta.env.VITE_LOCAL_DEV_MODE === 'true') {
      // 本地模式：使用本地存储的进度
      progressData = localAuthStore.getUserLearningProgress()
    } else {
      // Supabase模式：从服务器获取进度
      try {
        const { useSupabaseAuthStore } = await import('@/stores/supabaseAuth')
        const authStore = useSupabaseAuthStore()
        
        if (authStore.user) {
          const { LearningProgressService } = await import('@/services/supabaseService')
          progressData = await LearningProgressService.getUserProgress(authStore.user.id)
        }
      } catch (progressErr) {
        console.warn('获取学习进度失败:', progressErr)
      }
    }

    // 转换数据格式以匹配 TrainingMaterial 接口
    materials.value = data.map((material: any) => {
      // 查找对应的学习进度
      const progress = progressData.find(p => p.material_id === material.id)
      
      let status: 'not_started' | 'in_progress' | 'completed' = 'not_started'
      let progressPercentage = 0
      
      if (progress) {
        if (progress.is_completed) {
          status = 'completed'
          progressPercentage = 100
        } else if (progress.total_study_seconds > 0) {
          status = 'in_progress'
          progressPercentage = Math.round(progress.progress_percentage || 0)
        }
      }

      return {
        id: material.id,
        title: material.title,
        description: material.description || '',
        category: material.category || getCategoryFromType(material.material_type || 'document'),
        type: material.material_type || 'document',
        file_path: material.content_url,
        file_url: material.content_url,
        duration_minutes: material.duration_minutes || 0,
        file_size: '未知',
        download_count: material.download_count || 0,
        status,
        progress: progressPercentage,
        learning_progress_id: progress?.id,
        total_study_seconds: progress?.total_study_seconds || 0
      }
    })
  } catch (err: any) {
    console.error('获取培训资料失败:', err)
    error.value = err.message || '获取培训资料失败'
  } finally {
    loading.value = false
  }
}

// 根据类型映射分类
const getCategoryFromType = (type: string) => {
  const typeMapping: { [key: string]: string } = {
    'video': 'teaching_methods',
    'pdf': 'classroom_management', 
    'document': 'assessment',
    'audio': 'student_interaction'
  }
  return typeMapping[type] || 'teaching_methods'
}

// 组件挂载时获取数据
onMounted(() => {
  fetchMaterials()
})

// 组件卸载时清理计时器
onUnmounted(() => {
  Object.values(learningTimers.value).forEach(timer => {
    clearInterval(timer)
  })
  learningTimers.value = {}
})

// 计算属性
const totalMaterials = computed(() => materials.value.length)
const completedMaterials = computed(() => materials.value.filter(m => (m.status || 'not_started') === 'completed').length)

const filteredMaterials = computed(() => {
  return materials.value.filter(material => {
    const matchesCategory = !selectedCategory.value || (material.category || 'teaching_methods') === selectedCategory.value
    const matchesStatus = !selectedStatus.value || (material.status || 'not_started') === selectedStatus.value
    const matchesSearch = !searchQuery.value || 
      material.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      material.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    return matchesCategory && matchesStatus && matchesSearch
  })
})

// 工具函数
const getCategoryColor = (category: string) => {
  const colors = {
    teaching_methods: { bg: 'bg-blue-100', text: 'text-blue-600' },
    classroom_management: { bg: 'bg-green-100', text: 'text-green-600' },
    student_interaction: { bg: 'bg-purple-100', text: 'text-purple-600' },
    assessment: { bg: 'bg-orange-100', text: 'text-orange-600' },
    '教学文档': { bg: 'bg-blue-100', text: 'text-blue-600' },
    '其他培训文档': { bg: 'bg-indigo-100', text: 'text-indigo-600' }
  }
  return colors[category as keyof typeof colors] || colors.teaching_methods
}

const getCategoryIcon = (category: string) => {
  const icons = {
    teaching_methods: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
    classroom_management: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
    student_interaction: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
    assessment: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
    '教学文档': 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
    '其他培训文档': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'
  }
  return icons[category as keyof typeof icons] || icons.teaching_methods
}

const getCategoryName = (category: string) => {
  const names = {
    teaching_methods: '教学方法',
    classroom_management: '课堂管理',
    student_interaction: '学生互动',
    assessment: '评估技巧',
    '教学文档': '教学文档',
    '其他培训文档': '其他培训文档'
  }
  return names[category as keyof typeof names] || category || '未知分类'
}

const getStatusColor = (status: string) => {
  const colors = {
    not_started: 'bg-gray-100 text-gray-800',
    in_progress: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800'
  }
  return colors[status as keyof typeof colors] || colors.not_started
}

const getStatusText = (status: string) => {
  const texts = {
    not_started: '未开始',
    in_progress: '学习中',
    completed: '已完成'
  }
  return texts[status as keyof typeof texts] || '未知状态'
}

// 切换简介展开状态
const toggleDescription = (materialId: number) => {
  expandedDescriptions.value[materialId] = !expandedDescriptions.value[materialId]
}

// 操作函数
const startLearning = async (material: TrainingMaterial) => {
  try {
    // 停止之前的学习计时器
    if (currentLearningMaterial.value && learningTimers.value[currentLearningMaterial.value]) {
      clearInterval(learningTimers.value[currentLearningMaterial.value])
      delete learningTimers.value[currentLearningMaterial.value]
    }
    
    // 更新材料状态为进行中
     const materialIndex = materials.value.findIndex(m => m.id === material.id)
     if (materialIndex !== -1 && materials.value[materialIndex]) {
       materials.value[materialIndex].status = 'in_progress'
     }
    
    // 记录学习开始
     await recordLearningStart(material.id?.toString() || '', material.title)
     
     // 设置当前学习材料
     currentLearningMaterial.value = material.id?.toString() || ''
     
     // 启动学习计时器（每10秒更新一次进度）
     const materialIdStr = material.id?.toString() || ''
     learningTimers.value[materialIdStr] = setInterval(() => {
       updateLearningProgress(materialIdStr, 10) // 每次增加10秒
     }, 10000)
    
    // 构建文件URL
    const fileUrl = material.file_url || material.file_path
    if (!fileUrl) {
      alert('文件路径不存在，无法预览')
      return
    }
    
    // 打开文件
    window.open(fileUrl, '_blank')
    
  } catch (err) {
    console.error('开始学习失败:', err)
    alert('开始学习失败，请重试')
  }
}

// 记录学习开始
const recordLearningStart = async (materialId: string, materialTitle: string) => {
  if (import.meta.env.VITE_LOCAL_DEV_MODE === 'true') {
    // 本地模式：使用本地存储
    localAuthStore.startLearning(materialId, materialTitle)
  } else {
     // Supabase模式：调用API
     try {
       const { LearningProgressService } = await import('@/services/supabaseService')
       if (authStore.user?.id) {
         await LearningProgressService.startLearning(authStore.user.id, materialId)
       }
     } catch (error) {
       console.error('记录学习开始失败:', error)
     }
   }
}

// 更新学习进度
const updateLearningProgress = async (materialId: string, studySeconds: number) => {
  if (import.meta.env.VITE_LOCAL_DEV_MODE === 'true') {
    // 本地模式：使用本地存储
    const updatedProgress = localAuthStore.updateLearningProgress(materialId, studySeconds)
    
    if (updatedProgress) {
       // 更新UI中的进度
       const materialIndex = materials.value.findIndex(m => m.id?.toString() === materialId)
       if (materialIndex !== -1 && materials.value[materialIndex]) {
         materials.value[materialIndex].progress = updatedProgress.progress_percentage
         materials.value[materialIndex].total_study_seconds = updatedProgress.total_study_seconds
         
         if (updatedProgress.is_completed) {
           materials.value[materialIndex].status = 'completed'
           // 停止计时器
           if (learningTimers.value[materialId]) {
             clearInterval(learningTimers.value[materialId])
             delete learningTimers.value[materialId]
           }
         }
       }
     }
  } else {
     // Supabase模式：调用API
     try {
       const { LearningProgressService } = await import('@/services/supabaseService')
       if (authStore.user?.id) {
         // 计算进度百分比（假设10分钟完成100%）
         const targetMinutes = 10
         const progressPercentage = Math.min(100, (studySeconds / (targetMinutes * 60)) * 100)
         await LearningProgressService.updateProgress(authStore.user.id, materialId, Math.round(progressPercentage))
         // 重新获取材料以更新进度
         await fetchMaterials()
       }
     } catch (error) {
       console.error('更新学习进度失败:', error)
     }
   }
}

// 停止学习
const stopLearning = (materialId: string) => {
  if (learningTimers.value[materialId]) {
    clearInterval(learningTimers.value[materialId])
    delete learningTimers.value[materialId]
  }
  
  if (currentLearningMaterial.value === materialId) {
    currentLearningMaterial.value = null
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  /* 现代浏览器支持 */
  line-clamp: 2;
  /* 回退方案 */
  max-height: calc(1.2em * 2);
  line-height: 1.2;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  /* 现代浏览器支持 */
  line-clamp: 3;
  /* 回退方案 */
  max-height: calc(1.2em * 3);
  line-height: 1.2;
}
</style>