<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-3xl font-bold text-gray-900">试讲练习</h1>
      <p class="mt-2 text-gray-600">AI辅助的试讲练习和实时反馈</p>
    </div>

    <!-- 练习模式选择 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6" v-if="!isRecording && !showResults">
      <div 
        v-for="mode in practiceMode" 
        :key="mode.id"
        class="card cursor-pointer hover:shadow-lg transition-shadow duration-200 border-2"
        :class="selectedMode?.id === mode.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200'"
        @click="selectMode(mode)"
      >
        <div class="text-center">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center"
               :class="mode.color">
            <i :class="mode.icon" class="text-2xl text-white"></i>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ mode.name }}</h3>
          <p class="text-gray-600 text-sm mb-4">{{ mode.description }}</p>
          <div class="text-xs text-gray-500">
            <p>时长：{{ mode.duration }}</p>
            <p>难度：{{ mode.difficulty }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 练习设置 -->
    <div class="card" v-if="selectedMode && !isRecording && !showResults">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">练习设置</h2>
      
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
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">评估重点</label>
          <div class="space-y-2">
            <label v-for="focus in evaluationFocus" :key="focus.id" class="flex items-center">
              <input 
                type="checkbox" 
                v-model="practiceSettings.focusAreas" 
                :value="focus.id"
                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              >
              <span class="ml-2 text-sm text-gray-700">{{ focus.name }}</span>
            </label>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">AI反馈级别</label>
          <select v-model="practiceSettings.feedbackLevel" class="input">
            <option value="basic">基础反馈</option>
            <option value="detailed">详细反馈</option>
            <option value="comprehensive">全面反馈</option>
          </select>
        </div>
      </div>
      
      <div class="mt-6 flex justify-center">
        <button 
          @click="startPractice"
          :disabled="!canStartPractice"
          class="btn-primary px-8 py-3 text-lg"
          :class="{ 'opacity-50 cursor-not-allowed': !canStartPractice }"
        >
          开始练习
        </button>
      </div>
    </div>

    <!-- 练习进行中界面 -->
    <div class="card" v-if="isRecording">
      <div class="text-center">
        <div class="mb-6">
          <div class="w-32 h-32 mx-auto mb-4 rounded-full bg-red-500 flex items-center justify-center animate-pulse">
            <i class="fas fa-microphone text-4xl text-white"></i>
          </div>
          <h2 class="text-2xl font-semibold text-gray-900 mb-2">正在录制中...</h2>
          <p class="text-gray-600">{{ selectedMode?.name }} - {{ practiceSettings.topic }}</p>
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
            <tr v-for="record in filteredHistory" :key="record.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3"
                        :class="getPracticeModeById(record.modeId)?.color || 'bg-gray-500'">
                     <i :class="getPracticeModeById(record.modeId)?.icon || 'fas fa-question'" class="text-sm text-white"></i>
                   </div>
                   <span class="text-sm font-medium text-gray-900">
                     {{ getPracticeModeById(record.modeId)?.name || '未知模式' }}
                   </span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.topic }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.duration }}分钟
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-sm font-medium" :class="getScoreColor(record.score)">
                  {{ record.score }}分
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(record.date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button @click="viewDetails(record)" class="text-blue-600 hover:text-blue-900 mr-3">
                  查看详情
                </button>
                <button @click="repeatPractice(record)" class="text-green-600 hover:text-green-900">
                  重复练习
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

const router = useRouter()

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
}

interface PracticeRecord {
  id: string
  modeId: string
  topic: string
  duration: number
  score: number
  date: string
}

// 响应式数据
const selectedMode = ref<PracticeMode | null>(null)
const isRecording = ref(false)
const showResults = ref(false)
const recordingTime = ref(0)
const recordingTimer = ref<number | null>(null)

const practiceSettings = ref<PracticeSettings>({
  topic: '',
  duration: 10,
  focusAreas: [],
  feedbackLevel: 'detailed'
})

const historyFilter = ref({
  mode: '',
  period: 'month'
})

// 练习数据
const practiceMode: PracticeMode[] = []
const courseTopics: string[] = []
const evaluationFocus: EvaluationFocus[] = []

const realtimeMetrics = ref<RealtimeMetrics>({
  volume: 0,
  clarity: 0,
  pace: '未开始',
  engagement: 0
})

const currentResult = ref<PracticeResult>({
  overallScore: 0,
  detailedScores: [],
  aiFeedback: []
})

const practiceHistory: PracticeRecord[] = []

// 加载练习模式数据
const loadPracticeModes = async () => {
  try {
    // TODO: 从API获取练习模式数据
    // const response = await fetch('/api/teacher/practice-modes')
    // const data = await response.json()
    // practiceMode.splice(0, practiceMode.length, ...data)
    console.log('加载练习模式数据...')
  } catch (error) {
    console.error('加载练习模式失败:', error)
  }
}

// 加载课程主题数据
const loadCourseTopics = async () => {
  try {
    // TODO: 从API获取课程主题数据
    // const response = await fetch('/api/teacher/course-topics')
    // const data = await response.json()
    // courseTopics.splice(0, courseTopics.length, ...data)
    console.log('加载课程主题数据...')
  } catch (error) {
    console.error('加载课程主题失败:', error)
  }
}

// 加载评估重点数据
const loadEvaluationFocus = async () => {
  try {
    // TODO: 从API获取评估重点数据
    // const response = await fetch('/api/teacher/evaluation-focus')
    // const data = await response.json()
    // evaluationFocus.splice(0, evaluationFocus.length, ...data)
    console.log('加载评估重点数据...')
  } catch (error) {
    console.error('加载评估重点失败:', error)
  }
}

// 加载练习历史数据
const loadPracticeHistory = async () => {
  try {
    // TODO: 从API获取练习历史数据
    // const response = await fetch('/api/teacher/practice-history')
    // const data = await response.json()
    // practiceHistory.splice(0, practiceHistory.length, ...data)
    console.log('加载练习历史数据...')
  } catch (error) {
    console.error('加载练习历史失败:', error)
  }
}

// 计算属性
const canStartPractice = computed(() => {
  return practiceSettings.value.topic && practiceSettings.value.focusAreas.length > 0
})

const filteredHistory = computed(() => {
  let filtered = practiceHistory

  if (historyFilter.value.mode) {
    filtered = filtered.filter(record => record.modeId === historyFilter.value.mode)
  }

  const now = new Date()
  if (historyFilter.value.period === 'week') {
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
    filtered = filtered.filter(record => new Date(record.date) >= weekAgo)
  } else if (historyFilter.value.period === 'month') {
    const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
    filtered = filtered.filter(record => new Date(record.date) >= monthAgo)
  }

  return filtered.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
})

// 方法
const selectMode = (mode: PracticeMode) => {
  selectedMode.value = mode
}

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
    // TODO: 调用AI分析API生成练习结果
    // const response = await fetch('/api/teacher/analyze-practice', {
    //   method: 'POST',
    //   body: practiceData
    // })
    // const result = await response.json()
    // currentResult.value = result
    console.log('生成练习结果...')
    showResults.value = true
  } catch (error) {
    console.error('生成结果失败:', error)
  }
}

const restartPractice = () => {
  showResults.value = false
  recordingTime.value = 0
}

const viewHistory = () => {
  showResults.value = false
  selectedMode.value = null
}

const viewDetails = (record: PracticeRecord) => {
  console.log('查看详情:', record)
  // 跳转到反馈报告详情页面
  router.push(`/teacher/feedback/${record.id}`)
}

const repeatPractice = (record: PracticeRecord) => {
  const mode = practiceMode.find(m => m.id === record.modeId)
  if (mode) {
    selectedMode.value = mode
    practiceSettings.value.topic = record.topic
    practiceSettings.value.duration = record.duration
  }
}

const getPracticeModeById = (id: string) => {
  return practiceMode.find(mode => mode.id === id)
}

const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getScoreColor = (score: number) => {
  if (score >= 90) return 'text-green-600'
  if (score >= 80) return 'text-blue-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

const getScoreText = (score: number) => {
  if (score >= 90) return '优秀'
  if (score >= 80) return '良好'
  if (score >= 70) return '及格'
  return '需要改进'
}

// 生命周期
onMounted(() => {
  loadPracticeModes()
  loadCourseTopics()
  loadEvaluationFocus()
  loadPracticeHistory()
})

onUnmounted(() => {
  if (recordingTimer.value) {
    clearInterval(recordingTimer.value)
  }
})
</script>