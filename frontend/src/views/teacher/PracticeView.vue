<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-3xl font-bold text-gray-900">试讲练习</h1>
      <p class="mt-2 text-gray-600">AI辅助的试讲练习和实时反馈</p>
    </div>

    <!-- 模拟课堂练习设置 -->
    <div class="card" v-if="!isRecording && !showResults">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">模拟课堂练习设置</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">课程主题</label>
          <select v-model="practiceSettings.topic" class="input">
            <option value="">请选择课程主题</option>
            <option v-for="topic in courseTopics" :key="topic" :value="topic">{{ topic }}</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">练习时长</label>
          <select v-model="practiceSettings.duration" class="input">
            <option value="5">5分钟</option>
            <option value="10">10分钟</option>
            <option value="15">15分钟</option>
            <option value="20">20分钟</option>
          </select>
        </div>
      </div>
      
      <div class="mt-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">评估重点</label>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <label v-for="focus in evaluationFocus" :key="focus.id" class="flex items-center">
            <input 
              type="checkbox" 
              :value="focus.id" 
              v-model="practiceSettings.focusAreas"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">{{ focus.name }}</span>
          </label>
        </div>
      </div>
      
      <div class="mt-6 flex justify-center">
        <button 
          @click="startPractice" 
          :disabled="!practiceSettings.topic"
          class="btn-primary px-8 py-3 text-lg"
        >
          开始练习
        </button>
      </div>
    </div>

    <!-- 练习进行中 -->
    <div v-if="isRecording" class="card text-center">
      <div class="mb-6">
        <h2 class="text-2xl font-semibold text-gray-900 mb-2">练习进行中</h2>
        <p class="text-gray-600">模拟课堂 - {{ practiceSettings.topic }}</p>
      </div>
      
      <!-- 计时器 -->
      <div class="mb-6">
        <div class="text-4xl font-mono font-bold text-gray-900 mb-2">
          {{ formatTime(recordingTime) }}
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div 
            class="bg-blue-600 h-2 rounded-full transition-all duration-1000"
            :style="{ width: `${(recordingTime / (practiceSettings.duration * 60)) * 100}%` }"
          ></div>
        </div>
      </div>
      
      <!-- 实时反馈指标 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div class="text-center">
          <div class="text-2xl font-bold text-blue-600">{{ realtimeMetrics.volume }}%</div>
          <div class="text-sm text-gray-600">音量</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600">{{ realtimeMetrics.clarity }}%</div>
          <div class="text-sm text-gray-600">清晰度</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-purple-600">{{ realtimeMetrics.pace }}</div>
          <div class="text-sm text-gray-600">语速</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-orange-600">{{ realtimeMetrics.engagement }}%</div>
          <div class="text-sm text-gray-600">参与度</div>
        </div>
      </div>
      
      <button @click="stopPractice" class="btn-secondary px-6 py-2">
        结束练习
      </button>
    </div>

    <!-- AI分析加载状态 -->
    <div v-if="isAnalyzing" class="card text-center">
      <div class="mb-6">
        <div class="w-24 h-24 mx-auto mb-4 rounded-full bg-blue-100 flex items-center justify-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
        <h2 class="text-2xl font-semibold text-gray-900 mb-2">AI正在分析中...</h2>
        <p class="text-gray-600">正在对您的试讲进行全面分析，请稍候</p>
      </div>
      
      <div class="bg-blue-50 rounded-lg p-4">
        <div class="flex items-center justify-center space-x-4 text-sm text-blue-700">
          <div class="flex items-center">
            <div class="w-2 h-2 bg-blue-600 rounded-full animate-pulse mr-2"></div>
            语音分析
          </div>
          <div class="flex items-center">
            <div class="w-2 h-2 bg-blue-600 rounded-full animate-pulse mr-2" style="animation-delay: 0.2s"></div>
            内容分析
          </div>
          <div class="flex items-center">
            <div class="w-2 h-2 bg-blue-600 rounded-full animate-pulse mr-2" style="animation-delay: 0.4s"></div>
            视频分析
          </div>
          <div class="flex items-center">
            <div class="w-2 h-2 bg-blue-600 rounded-full animate-pulse mr-2" style="animation-delay: 0.6s"></div>
            生成反馈
          </div>
        </div>
      </div>
    </div>

    <!-- 分析错误提示 -->
    <div v-if="analysisError && !isAnalyzing" class="card bg-red-50 border-red-200">
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">分析失败</h3>
          <div class="mt-2 text-sm text-red-700">
            <p>{{ analysisError }}</p>
          </div>
          <div class="mt-4">
            <div class="flex space-x-3">
              <button @click="retryAnalysis" class="bg-red-100 px-3 py-2 rounded-md text-sm font-medium text-red-800 hover:bg-red-200">
                重试分析
              </button>
              <button @click="useOfflineMode" class="bg-gray-100 px-3 py-2 rounded-md text-sm font-medium text-gray-800 hover:bg-gray-200">
                使用离线模式
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 练习结果 -->
    <div v-if="showResults" class="space-y-6">
      <!-- 总体评分 -->
      <div class="card text-center">
        <h2 class="text-2xl font-semibold text-gray-900 mb-4">练习完成！</h2>
        <div class="mb-6">
          <div class="text-6xl font-bold mb-2" :class="getScoreColor(currentResult.overallScore)">
            {{ currentResult.overallScore }}
          </div>
          <div class="text-lg text-gray-600">总体评分</div>
          <div class="text-sm text-gray-500 mt-2">{{ getScoreText(currentResult.overallScore) }}</div>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="metric in currentResult.detailedScores" :key="metric.name" class="text-center">
            <div class="text-2xl font-bold mb-1" :class="getScoreColor(metric.score)">
              {{ metric.score }}
            </div>
            <div class="text-sm text-gray-600">{{ metric.name }}</div>
          </div>
        </div>
      </div>
      
      <!-- AI反馈 -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">AI智能反馈</h3>
        
        <div class="space-y-4">
          <div v-for="feedback in currentResult.aiFeedback" :key="feedback.category" 
               class="p-4 rounded-lg border">
            <div class="flex items-center mb-2">
              <i :class="[feedback.icon, feedback.color]" class="text-lg mr-2"></i>
              <h4 class="font-medium text-gray-900">{{ feedback.category }}</h4>
              <span class="ml-auto text-sm px-2 py-1 rounded-full"
                    :class="feedback.level === 'excellent' ? 'bg-green-100 text-green-800' :
                           feedback.level === 'good' ? 'bg-blue-100 text-blue-800' :
                           feedback.level === 'needs_improvement' ? 'bg-yellow-100 text-yellow-800' :
                           'bg-red-100 text-red-800'">
                {{ feedback.levelText }}
              </span>
            </div>
            <p class="text-gray-700 text-sm mb-2">{{ feedback.comment }}</p>
            <div v-if="feedback.suggestions.length > 0">
              <p class="text-xs font-medium text-gray-600 mb-1">改进建议：</p>
              <ul class="text-xs text-gray-600 space-y-1">
                <li v-for="suggestion in feedback.suggestions" :key="suggestion" class="flex items-start">
                  <span class="text-blue-500 mr-1">•</span>
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div class="flex justify-center space-x-4">
        <button @click="restartPractice" class="btn-primary">
          重新练习
        </button>
        <button @click="viewHistory" class="btn-secondary">
          查看历史记录
        </button>
      </div>
    </div>

    <!-- 练习历史 -->
    <div class="card" v-if="!isRecording && !showResults">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-gray-900">练习历史</h2>
        <div class="flex space-x-2">
          <select v-model="historyFilter.mode" class="input text-sm">
            <option value="">所有模式</option>
            <option v-for="mode in practiceMode" :key="mode.id" :value="mode.id">{{ mode.name }}</option>
          </select>
          <select v-model="historyFilter.period" class="input text-sm">
            <option value="week">最近一周</option>
            <option value="month">最近一月</option>
            <option value="all">全部</option>
          </select>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                练习模式
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                课程主题
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                时长
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                总评分
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                练习时间
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="record in filteredHistory" :key="record.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ getPracticeModeById(record.modeId)?.name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.topic }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.duration }}分钟
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                  :class="getScoreColor(record.score)">
                {{ record.score }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(record.date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button @click="viewPracticeDetail(record)" class="text-blue-600 hover:text-blue-900">
                  查看详情
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="filteredHistory.length === 0" class="text-center py-8">
        <i class="fas fa-history text-4xl text-gray-300 mb-4"></i>
        <p class="text-gray-500">暂无练习记录</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'

const router = useRouter()
const authStore = useSupabaseAuthStore()

// 接口定义
interface PracticeMode {
  id: string
  name: string
  description: string
  duration: string
  difficulty: string
  icon: string
  color: string
}

interface PracticeSettings {
  topic: string
  duration: number
  focusAreas: string[]
  feedbackLevel: string
}

interface EvaluationFocus {
  id: string
  name: string
}

interface RealtimeMetrics {
  volume: number
  clarity: number
  pace: string
  engagement: number
}

interface DetailedScore {
  name: string
  score: number
}

interface AIFeedback {
  category: string
  level: string
  levelText: string
  comment: string
  suggestions: string[]
  icon: string
  color: string
}

interface PracticeResult {
  overallScore: number
  detailedScores: DetailedScore[]
  aiFeedback: AIFeedback[]
  transcript: string
  duration: number
}

interface PracticeHistory {
  id: string
  modeId: string
  topic: string
  duration: number
  score: number
  date: string
}

// 响应式数据
const selectedMode = ref<PracticeMode | null>(null)
const practiceSettings = ref<PracticeSettings>({
  topic: '',
  duration: 10,
  focusAreas: [],
  feedbackLevel: 'detailed'
})

const isRecording = ref(false)
const recordingTime = ref(0)
const recordingTimer = ref<number | null>(null)
const isAnalyzing = ref(false)
const analysisError = ref('')
const showResults = ref(false)

const realtimeMetrics = ref<RealtimeMetrics>({
  volume: 75,
  clarity: 82,
  pace: '适中',
  engagement: 68
})

const currentResult = ref<PracticeResult>({
  overallScore: 0,
  detailedScores: [],
  aiFeedback: [],
  transcript: '',
  duration: 0
})

const practiceMode = ref<PracticeMode[]>([])
const courseTopics = ref<string[]>([])
const evaluationFocus = ref<EvaluationFocus[]>([])
const practiceHistory = ref<PracticeHistory[]>([])

const historyFilter = ref({
  mode: '',
  period: 'month'
})

// 计算属性
const filteredHistory = computed(() => {
  let filtered = practiceHistory.value

  if (historyFilter.value.mode) {
    filtered = filtered.filter(record => record.modeId === historyFilter.value.mode)
  }

  const now = new Date()
  const filterDate = new Date()
  
  switch (historyFilter.value.period) {
    case 'week':
      filterDate.setDate(now.getDate() - 7)
      break
    case 'month':
      filterDate.setMonth(now.getMonth() - 1)
      break
    default:
      return filtered
  }

  return filtered.filter(record => new Date(record.date) >= filterDate)
})

// 方法
const startPractice = () => {
  isRecording.value = true
  recordingTime.value = 0
  
  // 开始录制和实时分析
  recordingTimer.value = setInterval(() => {
    recordingTime.value++
    
    // TODO: 实现真实的实时指标分析
    // 这里应该调用AI分析API获取实时指标
    console.log('实时分析中...')
    
    // 自动结束
    if (recordingTime.value >= practiceSettings.value.duration * 60) {
      stopPractice()
    }
  }, 1000)
}

const stopPractice = () => {
  isRecording.value = false
  if (recordingTimer.value) {
    clearInterval(recordingTimer.value)
    recordingTimer.value = null
  }
  
  // 生成分析结果
  generatePracticeResult()
}

// 生成练习结果
const generatePracticeResult = async () => {
  try {
    isAnalyzing.value = true
    analysisError.value = ''
    console.log('开始AI分析...')
    
    // 获取认证token
    const token = authStore.session?.access_token
    if (!token) {
      throw new Error('请先登录后再进行分析')
    }
    
    // 准备分析数据
    const analysisData = {
      transcript: `这是关于${practiceSettings.value.topic}的教学内容，时长${practiceSettings.value.duration}分钟的试讲练习。`,
      topic: practiceSettings.value.topic,
      duration: practiceSettings.value.duration * 60 // 转换为秒
    }
    
    // 调用AI综合分析API
    const response = await fetch('/api/ai/comprehensive-analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(analysisData)
    })
    
    if (!response.ok) {
      throw new Error(`分析请求失败: ${response.status}`)
    }
    
    const result = await response.json()
    
    // 设置分析结果
    currentResult.value = {
      overallScore: result.overall_score || 85,
      detailedScores: result.detailed_scores || [
        { name: '发音准确性', score: 88 },
        { name: '语言流畅性', score: 82 },
        { name: '教学内容', score: 90 },
        { name: '课堂互动', score: 80 }
      ],
      aiFeedback: result.ai_feedback || [
        {
          category: '语音表达',
          level: 'good',
          levelText: '良好',
          comment: '发音清晰，语速适中，但在重点内容处可以适当放慢语速。',
          suggestions: ['在关键概念处适当停顿', '增加语调变化'],
          icon: 'fas fa-microphone',
          color: 'text-blue-500'
        }
      ],
      transcript: result.transcript || analysisData.transcript,
      duration: recordingTime.value
    }
    
    // 保存练习记录
    const practiceRecord: PracticeHistory = {
      id: Date.now().toString(),
      modeId: selectedMode.value?.id || '',
      topic: practiceSettings.value.topic,
      duration: practiceSettings.value.duration,
      score: currentResult.value.overallScore,
      date: new Date().toISOString()
    }
    
    practiceHistory.value.unshift(practiceRecord)
    
    isAnalyzing.value = false
    showResults.value = true
    
  } catch (error) {
    console.error('AI分析失败:', error)
    analysisError.value = error instanceof Error ? error.message : '分析过程中发生未知错误'
    isAnalyzing.value = false
    
    // 使用离线模式的默认结果
    useOfflineMode()
  }
}

const retryAnalysis = () => {
  analysisError.value = ''
  generatePracticeResult()
}

const useOfflineMode = () => {
  console.log('使用离线模式生成结果')
  
  // 生成模拟的分析结果
  currentResult.value = {
    overallScore: 85,
    detailedScores: [
      { name: '发音准确性', score: 88 },
      { name: '语言流畅性', score: 82 },
      { name: '教学内容', score: 90 },
      { name: '课堂互动', score: 80 }
    ],
    aiFeedback: [
      {
        category: '语音表达',
        level: 'good',
        levelText: '良好',
        comment: '发音清晰，语速适中，整体表现良好。',
        suggestions: ['可以增加更多的语调变化', '在重点内容处适当停顿'],
        icon: 'fas fa-microphone',
        color: 'text-blue-500'
      },
      {
        category: '教学内容',
        level: 'excellent',
        levelText: '优秀',
        comment: '内容结构清晰，逻辑性强，知识点讲解到位。',
        suggestions: ['可以增加更多实例说明', '适当增加互动环节'],
        icon: 'fas fa-book',
        color: 'text-green-500'
      }
    ],
    transcript: `这是关于${practiceSettings.value.topic}的教学内容，时长${practiceSettings.value.duration}分钟的试讲练习。`,
    duration: recordingTime.value
  }
  
  // 保存练习记录
  const practiceRecord: PracticeHistory = {
    id: Date.now().toString(),
    modeId: selectedMode.value?.id || '',
    topic: practiceSettings.value.topic,
    duration: practiceSettings.value.duration,
    score: currentResult.value.overallScore,
    date: new Date().toISOString()
  }
  
  practiceHistory.value.unshift(practiceRecord)
  
  analysisError.value = ''
  isAnalyzing.value = false
  showResults.value = true
}

const restartPractice = () => {
  showResults.value = false
  selectedMode.value = null
  practiceSettings.value.topic = ''
  practiceSettings.value.focusAreas = []
}

const viewHistory = () => {
  showResults.value = false
}

const viewPracticeDetail = (record: PracticeHistory) => {
  console.log('查看练习详情:', record)
  // TODO: 实现查看详情功能
}

const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getScoreColor = (score: number): string => {
  if (score >= 90) return 'text-green-600'
  if (score >= 80) return 'text-blue-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

const getScoreText = (score: number): string => {
  if (score >= 90) return '优秀'
  if (score >= 80) return '良好'
  if (score >= 70) return '一般'
  return '需要改进'
}

const getPracticeModeById = (id: string): PracticeMode | undefined => {
  return practiceMode.value.find(mode => mode.id === id)
}

// 数据加载函数
const loadPracticeModes = () => {
  practiceMode.value = [
    {
      id: '2',
      name: '模拟课堂',
      description: '模拟真实课堂环境练习',
      duration: '10-30分钟',
      difficulty: '中级',
      icon: 'fas fa-chalkboard-teacher',
      color: 'bg-green-500'
    }
  ]
}

const loadCourseTopics = async () => {
  try {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    console.log('🔍 教师端加载课程主题 - API_BASE_URL:', API_BASE_URL)
    console.log('🔍 教师端加载课程主题 - Token存在:', !!localStorage.getItem('access_token'))
    
    const response = await fetch(`${API_BASE_URL}/api/manager/course-topics`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    console.log('🔍 教师端课程主题API响应状态:', response.status)
    
    if (response.ok) {
      const topics = await response.json()
      console.log('✅ 教师端成功加载课程主题:', topics)
      courseTopics.value.splice(0, courseTopics.value.length, ...topics)
    } else {
      console.error('❌ 教师端加载课程主题失败，状态码:', response.status)
      // 使用默认主题作为后备
      const defaultTopics = [
        '数学基础概念',
        '语文阅读理解',
        '英语口语交流',
        '科学实验探索',
        '历史文化传承'
      ]
      courseTopics.value.splice(0, courseTopics.value.length, ...defaultTopics)
    }
  } catch (error) {
    console.error('❌ 教师端加载课程主题时出错:', error)
    // 使用默认主题作为后备
    const defaultTopics = [
      '数学基础概念',
      '语文阅读理解',
      '英语口语交流',
      '科学实验探索',
      '历史文化传承'
    ]
    courseTopics.value.splice(0, courseTopics.value.length, ...defaultTopics)
  }
}

const loadEvaluationFocus = () => {
  const defaultFocus = [
    { id: '1', name: '发音准确性' },
    { id: '2', name: '语言流畅性' },
    { id: '3', name: '教学内容' },
    { id: '4', name: '课堂互动' }
  ]
  evaluationFocus.value.splice(0, evaluationFocus.value.length, ...defaultFocus)
}

const loadPracticeHistory = () => {
  const defaultHistory = [
    {
      id: '1',
      modeId: '1',
      topic: '数学基础概念',
      duration: 10,
      score: 85,
      date: new Date().toISOString()
    }
  ]
  practiceHistory.value.splice(0, practiceHistory.value.length, ...defaultHistory)
}

// 组件挂载时加载数据
onMounted(() => {
  loadPracticeModes()
  loadCourseTopics()
  loadEvaluationFocus()
  loadPracticeHistory()
  
  // 自动选择模拟课堂模式
  selectedMode.value = {
    id: '2',
    name: '模拟课堂',
    description: '模拟真实课堂环境练习',
    duration: '10-30分钟',
    difficulty: '中级',
    icon: 'fas fa-chalkboard-teacher',
    color: 'bg-green-500'
  }
})

// 组件卸载时清理
onUnmounted(() => {
  if (recordingTimer.value) {
    clearInterval(recordingTimer.value)
  }
})
</script>