<template>
  <div class="space-y-8">
    <!-- 页面标题 -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900">反馈报告</h1>
      <p class="mt-2 text-gray-600">查看试讲练习的详细反馈和改进建议</p>
    </div>

    <!-- 筛选器 -->
    <div class="card">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">时间范围</label>
          <select v-model="selectedTimeRange" class="w-full border border-gray-300 rounded-md px-3 py-2">
            <option value="all">全部时间</option>
            <option value="week">最近一周</option>
            <option value="month">最近一月</option>
            <option value="quarter">最近三月</option>
          </select>
        </div>
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">课程主题</label>
          <select v-model="selectedSubject" class="w-full border border-gray-300 rounded-md px-3 py-2">
            <option value="">全部主题</option>
            <option value="math">数学</option>
            <option value="chinese">语文</option>
            <option value="english">英语</option>
          </select>
        </div>
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">评分范围</label>
          <select v-model="selectedScoreRange" class="w-full border border-gray-300 rounded-md px-3 py-2">
            <option value="">全部评分</option>
            <option value="excellent">优秀 (90-100)</option>
            <option value="good">良好 (80-89)</option>
            <option value="average">一般 (70-79)</option>
            <option value="poor">需改进 (<70)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">总报告数</h3>
            <p class="text-2xl font-bold text-blue-600">{{ filteredReports.length }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">平均评分</h3>
            <p class="text-2xl font-bold text-green-600">{{ averageScore.toFixed(1) }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">最高评分</h3>
            <p class="text-2xl font-bold text-purple-600">{{ highestScore }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-12 w-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">最新报告</h3>
            <p class="text-sm text-orange-600">{{ latestReportDate }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 反馈报告列表 -->
    <div class="card">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-gray-900">反馈报告列表</h2>
        <button @click="generateNewReport" class="btn-primary">
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          生成新报告
        </button>
      </div>

      <div class="space-y-4">
        <div v-for="report in filteredReports" :key="report.id" 
             class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <h3 class="text-lg font-semibold text-gray-900">{{ report.title }}</h3>
                <span class="px-2 py-1 text-xs font-medium rounded-full"
                      :class="getScoreColor(report.overallScore)">
                  {{ report.overallScore }}/100
                </span>
              </div>
              <div class="flex items-center gap-4 text-sm text-gray-600">
                <span>{{ getSubjectName(report.subject) }}</span>
                <span>{{ report.duration }}分钟</span>
                <span>{{ report.date }}</span>
              </div>
            </div>
            <div class="flex gap-2">
              <button @click="viewReport(report)" class="btn-secondary">
                查看详情
              </button>
              <button @click="downloadReport(report)" class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- 评分详情 -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-600">{{ report.scores.content }}</div>
              <div class="text-sm text-gray-600">内容质量</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600">{{ report.scores.delivery }}</div>
              <div class="text-sm text-gray-600">表达能力</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-purple-600">{{ report.scores.interaction }}</div>
              <div class="text-sm text-gray-600">互动效果</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-orange-600">{{ report.scores.time }}</div>
              <div class="text-sm text-gray-600">时间控制</div>
            </div>
          </div>

          <!-- 关键反馈 -->
          <div class="bg-gray-50 rounded-lg p-4">
            <h4 class="font-medium text-gray-900 mb-2">关键反馈</h4>
            <div class="space-y-2">
              <div v-for="feedback in report.keyFeedback" :key="feedback.id" 
                   class="flex items-start gap-2">
                <div class="h-2 w-2 rounded-full mt-2"
                     :class="feedback.type === 'positive' ? 'bg-green-400' : feedback.type === 'negative' ? 'bg-red-400' : 'bg-yellow-400'">
                </div>
                <p class="text-sm text-gray-700">{{ feedback.text }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 改进建议 -->
    <div class="card bg-blue-50 border-blue-200">
      <h2 class="text-xl font-semibold text-blue-900 mb-4">AI智能建议</h2>
      <div class="space-y-4">
        <div class="bg-white rounded-lg p-4 border border-blue-200">
          <h3 class="font-medium text-blue-900 mb-2">📈 进步最快的方面</h3>
          <p class="text-blue-800">您在表达能力方面进步显著，最近三次试讲的评分从75分提升到88分。</p>
        </div>
        <div class="bg-white rounded-lg p-4 border border-blue-200">
          <h3 class="font-medium text-blue-900 mb-2">🎯 重点改进建议</h3>
          <p class="text-blue-800">建议加强时间控制能力，可以通过制定详细的教学计划和设置时间提醒来改善。</p>
        </div>
        <div class="bg-white rounded-lg p-4 border border-blue-200">
          <h3 class="font-medium text-blue-900 mb-2">💡 下次练习重点</h3>
          <p class="text-blue-800">建议选择"学生互动"主题进行练习，这是您相对薄弱的环节。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface FeedbackReport {
  id: number
  title: string
  subject: string
  date: string
  duration: number
  overallScore: number
  scores: {
    content: number
    delivery: number
    interaction: number
    time: number
  }
  keyFeedback: Array<{
    id: number
    type: 'positive' | 'negative' | 'suggestion'
    text: string
  }>
}

// 筛选条件
const selectedTimeRange = ref('all')
const selectedSubject = ref('')
const selectedScoreRange = ref('')

// 反馈报告数据
const reports = ref<FeedbackReport[]>([])

// 计算属性
const filteredReports = computed(() => {
  return reports.value.filter(report => {
    const matchesSubject = !selectedSubject.value || report.subject === selectedSubject.value
    const matchesScore = !selectedScoreRange.value || checkScoreRange(report.overallScore, selectedScoreRange.value)
    // 简化时间筛选逻辑
    return matchesSubject && matchesScore
  })
})

const averageScore = computed(() => {
  if (filteredReports.value.length === 0) return 0
  const total = filteredReports.value.reduce((sum, report) => sum + report.overallScore, 0)
  return total / filteredReports.value.length
})

const highestScore = computed(() => {
  if (filteredReports.value.length === 0) return 0
  return Math.max(...filteredReports.value.map(report => report.overallScore))
})

const latestReportDate = computed(() => {
  if (filteredReports.value.length === 0) return '暂无'
  const latest = filteredReports.value.reduce((latest, report) => 
    new Date(report.date) > new Date(latest.date) ? report : latest
  )
  return latest.date
})

// 加载反馈报告数据
const loadFeedbackReports = async () => {
  try {
    // TODO: 从API获取实际的反馈报告数据
    // const response = await fetch('/api/teacher/feedback-reports')
    // const data = await response.json()
    // reports.value = data
    console.log('加载反馈报告数据...')
  } catch (error) {
    console.error('加载反馈报告失败:', error)
  }
}

// 工具函数
const checkScoreRange = (score: number, range: string) => {
  switch (range) {
    case 'excellent': return score >= 90
    case 'good': return score >= 80 && score < 90
    case 'average': return score >= 70 && score < 80
    case 'poor': return score < 70
    default: return true
  }
}

const getScoreColor = (score: number) => {
  if (score >= 90) return 'bg-green-100 text-green-800'
  if (score >= 80) return 'bg-blue-100 text-blue-800'
  if (score >= 70) return 'bg-yellow-100 text-yellow-800'
  return 'bg-red-100 text-red-800'
}

const getSubjectName = (subject: string) => {
  const names = {
    math: '数学',
    chinese: '语文',
    english: '英语'
  }
  return names[subject as keyof typeof names] || '未知'
}

// 操作函数
const viewReport = (report: FeedbackReport) => {
  console.log('查看报告详情:', report.title)
  // 跳转到详细报告页面
  router.push(`/teacher/feedback/${report.id}`)
}

const downloadReport = (report: FeedbackReport) => {
  console.log('下载报告:', report.title)
  // TODO: 实现报告下载功能
  alert(`下载报告: ${report.title}`)
}

const generateNewReport = () => {
  console.log('生成新的反馈报告')
  // TODO: 实现AI报告生成功能
  alert('正在生成新的反馈报告...')
}

// 组件挂载时加载数据
onMounted(() => {
  loadFeedbackReports()
})
</script>