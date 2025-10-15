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

// 虚拟数据
const practiceMode: PracticeMode[] = [
  {
    id: 'free_speech',
    name: '自由演讲',
    description: '自由选择主题进行演讲练习',
    duration: '5-20分钟',
    difficulty: '初级',
    icon: 'fas fa-microphone',
    color: 'bg-blue-500'
  },
  {
    id: 'structured_lesson',
    name: '结构化授课',
    description: '按照教学大纲进行结构化授课',
    duration: '10-30分钟',
    difficulty: '中级',
    icon: 'fas fa-chalkboard-teacher',
    color: 'bg-green-500'
  },
  {
    id: 'interactive_teaching',
    name: '互动教学',
    description: '模拟师生互动的教学场景',
    duration: '15-25分钟',
    difficulty: '高级',
    icon: 'fas fa-users',
    color: 'bg-purple-500'
  }
]

const courseTopics = [
  '数学基础概念',
  '语文阅读理解',
  '英语口语表达',
  '科学实验演示',
  '历史事件分析',
  '地理知识讲解',
  '艺术欣赏指导',
  '体育技能教学'
]

const evaluationFocus: EvaluationFocus[] = [
  { id: 'pronunciation', name: '发音清晰度' },
  { id: 'pace', name: '语速控制' },
  { id: 'structure', name: '内容结构' },
  { id: 'engagement', name: '互动参与' },
  { id: 'body_language', name: '肢体语言' },
  { id: 'time_management', name: '时间管理' }
]

const realtimeMetrics = ref<RealtimeMetrics>({
  volume: 75,
  clarity: 82,
  pace: '适中',
  engagement: 68
})

const currentResult = ref<PracticeResult>({
  overallScore: 85,
  detailedScores: [
    { name: '发音', score: 88 },
    { name: '语速', score: 82 },
    { name: '结构', score: 87 },
    { name: '互动', score: 83 }
  ],
  aiFeedback: [
    {
      category: '发音清晰度',
      level: 'excellent',
      levelText: '优秀',
      comment: '发音清晰，语调自然，能够很好地传达教学内容。',
      suggestions: [],
      icon: 'fas fa-volume-up',
      color: 'text-green-500'
    },
    {
      category: '教学结构',
      level: 'good',
      levelText: '良好',
      comment: '教学结构较为清晰，但在过渡环节可以更加流畅。',
      suggestions: [
        '在章节之间添加更明确的过渡语句',
        '可以使用更多的总结性语言'
      ],
      icon: 'fas fa-sitemap',
      color: 'text-blue-500'
    },
    {
      category: '互动参与',
      level: 'needs_improvement',
      levelText: '待改进',
      comment: '互动环节较少，建议增加更多与学生的互动。',
      suggestions: [
        '增加提问频率',
        '设计更多互动环节',
        '鼓励学生参与讨论'
      ],
      icon: 'fas fa-comments',
      color: 'text-yellow-500'
    }
  ]
})

const practiceHistory: PracticeRecord[] = [
  {
    id: '1',
    modeId: 'free_speech',
    topic: '数学基础概念',
    duration: 10,
    score: 85,
    date: '2024-01-15T10:30:00Z'
  },
  {
    id: '2',
    modeId: 'structured_lesson',
    topic: '语文阅读理解',
    duration: 15,
    score: 78,
    date: '2024-01-14T14:20:00Z'
  },
  {
    id: '3',
    modeId: 'interactive_teaching',
    topic: '英语口语表达',
    duration: 20,
    score: 92,
    date: '2024-01-13T09:15:00Z'
  },
  {
    id: '4',
    modeId: 'free_speech',
    topic: '科学实验演示',
    duration: 12,
    score: 88,
    date: '2024-01-12T16:45:00Z'
  },
  {
    id: '5',
    modeId: 'structured_lesson',
    topic: '历史事件分析',
    duration: 18,
    score: 76,
    date: '2024-01-11T11:30:00Z'
  }
]

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
  
  // 模拟实时指标更新
  recordingTimer.value = setInterval(() => {
    recordingTime.value++
    
    // 模拟实时指标变化
    const paceOptions = ['较慢', '适中', '较快'] as const
    const randomIndex = Math.floor(Math.random() * paceOptions.length)
    realtimeMetrics.value = {
      volume: Math.floor(Math.random() * 30) + 70,
      clarity: Math.floor(Math.random() * 20) + 75,
      pace: paceOptions[randomIndex] || '适中',
      engagement: Math.floor(Math.random() * 40) + 60
    }
    
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
  
  // 模拟生成结果
  setTimeout(() => {
    showResults.value = true
  }, 1000)
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
onUnmounted(() => {
  if (recordingTimer.value) {
    clearInterval(recordingTimer.value)
  }
})
</script>