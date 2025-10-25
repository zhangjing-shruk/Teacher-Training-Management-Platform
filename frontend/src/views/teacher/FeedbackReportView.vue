<template>
  <div class="space-y-6">
    <!-- 页面头部 -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">试讲反馈报告</h1>
          <p class="text-gray-600 mt-1">{{ formatDate(feedback.date) }}</p>
        </div>
        <div class="flex space-x-3">
          <button @click="downloadReport" class="btn-secondary">
            <i class="fas fa-download mr-2"></i>
            下载报告
          </button>
          <router-link 
            to="/teacher/trial-lecture"
            class="btn-primary"
          >
            ← 返回试讲练习
          </router-link>
        </div>
      </div>
      
      <!-- 基本信息 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="text-sm font-medium text-gray-500 mb-1">课程主题</h3>
          <p class="text-lg font-semibold text-gray-900">{{ feedback.topic }}</p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="text-sm font-medium text-gray-500 mb-1">试讲时长</h3>
          <p class="text-lg font-semibold text-gray-900">{{ feedback.duration }}分钟</p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="text-sm font-medium text-gray-500 mb-1">综合评分</h3>
          <p class="text-lg font-semibold" :class="getScoreColor(feedback.totalScore)">
            {{ feedback.totalScore }}/100
          </p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="text-sm font-medium text-gray-500 mb-1">评分等级</h3>
          <p class="text-lg font-semibold" :class="getScoreColor(feedback.totalScore)">
            {{ getScoreLevel(feedback.totalScore) }}
          </p>
        </div>
      </div>
    </div>

    <!-- 视频回放和时间轴分析 -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">视频回放与分析</h2>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 视频播放器 -->
        <div class="lg:col-span-2">
          <div class="bg-gray-900 rounded-lg aspect-video flex items-center justify-center mb-4">
            <div class="text-center text-white">
              <i class="fas fa-play-circle text-6xl mb-4 opacity-70"></i>
              <p class="text-lg">试讲视频回放</p>
              <p class="text-sm opacity-70">点击播放按钮开始观看</p>
            </div>
          </div>
          
          <!-- 视频控制栏 -->
          <div class="flex items-center space-x-4 mb-4">
            <button @click="togglePlay" class="btn-primary">
              <i :class="isPlaying ? 'fas fa-pause' : 'fas fa-play'" class="mr-2"></i>
              {{ isPlaying ? '暂停' : '播放' }}
            </button>
            <div class="flex-1">
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${playProgress}%` }"
                ></div>
              </div>
            </div>
            <span class="text-sm text-gray-600">{{ formatTime(currentTime) }} / {{ formatTime(totalTime) }}</span>
          </div>
        </div>
        
        <!-- 关键时刻标记 -->
        <div>
          <h3 class="font-medium text-gray-900 mb-3">关键时刻</h3>
          <div class="space-y-3 max-h-80 overflow-y-auto">
            <div v-for="moment in feedback.keyMoments" :key="moment.time" 
                 class="p-3 border rounded-lg cursor-pointer hover:bg-gray-50"
                 @click="seekToTime(moment.time)">
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm font-medium text-gray-900">{{ formatTime(moment.time) }}</span>
                <span class="text-xs px-2 py-1 rounded-full"
                      :class="moment.type === 'highlight' ? 'bg-green-100 text-green-800' :
                             moment.type === 'improvement' ? 'bg-yellow-100 text-yellow-800' :
                             'bg-blue-100 text-blue-800'">
                  {{ moment.typeText }}
                </span>
              </div>
              <p class="text-xs text-gray-600">{{ moment.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 详细评分分析 -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-6">详细评分分析</h2>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 雷达图 -->
        <div>
          <h3 class="font-medium text-gray-900 mb-4">能力雷达图</h3>
          <div class="bg-gray-50 rounded-lg p-6 text-center">
            <div class="w-64 h-64 mx-auto bg-white rounded-lg shadow-inner flex items-center justify-center">
              <div class="text-gray-500">
                <i class="fas fa-chart-radar text-4xl mb-2"></i>
                <p class="text-sm">雷达图可视化</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 各项评分详情 -->
        <div>
          <h3 class="font-medium text-gray-900 mb-4">各项评分详情</h3>
          <div class="space-y-4">
            <div v-for="item in feedback.scores" :key="item.category" 
                 class="border rounded-lg p-4">
              <div class="flex justify-between items-center mb-2">
                <span class="font-medium text-gray-900">{{ item.category }}</span>
                <span class="text-lg font-bold" :class="getScoreColor(item.score)">{{ item.score }}/100</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div 
                  class="h-2 rounded-full transition-all duration-500"
                  :class="getScoreBarColor(item.score)"
                  :style="{ width: `${item.score}%` }"
                ></div>
              </div>
              <p class="text-sm text-gray-600">{{ item.feedback }}</p>
              <div v-if="item.suggestions.length > 0" class="mt-2">
                <p class="text-xs font-medium text-gray-700 mb-1">改进建议：</p>
                <ul class="text-xs text-gray-600 space-y-1">
                  <li v-for="suggestion in item.suggestions" :key="suggestion" class="flex items-start">
                    <span class="text-blue-500 mr-1">•</span>
                    {{ suggestion }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 语音分析 -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-6">语音分析报告</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="text-center p-4 bg-blue-50 rounded-lg">
          <div class="text-2xl font-bold text-blue-600 mb-1">{{ feedback.speechAnalysis.averageSpeed }}</div>
          <div class="text-sm text-gray-600">平均语速 (字/分钟)</div>
        </div>
        <div class="text-center p-4 bg-green-50 rounded-lg">
          <div class="text-2xl font-bold text-green-600 mb-1">{{ feedback.speechAnalysis.clarity }}%</div>
          <div class="text-sm text-gray-600">发音清晰度</div>
        </div>
        <div class="text-center p-4 bg-purple-50 rounded-lg">
          <div class="text-2xl font-bold text-purple-600 mb-1">{{ feedback.speechAnalysis.pauseCount }}</div>
          <div class="text-sm text-gray-600">停顿次数</div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 class="font-medium text-gray-900 mb-3">语速变化趋势</h3>
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="h-32 flex items-end space-x-1">
              <div v-for="(speed, index) in feedback.speechAnalysis.speedTrend" :key="index"
                   class="bg-blue-500 rounded-t"
                   :style="{ height: `${(speed / 200) * 100}%`, width: '8px' }"
                   :title="`第${index + 1}分钟: ${speed}字/分钟`">
              </div>
            </div>
            <div class="text-xs text-gray-500 mt-2 text-center">时间轴 (分钟)</div>
          </div>
        </div>
        
        <div>
          <h3 class="font-medium text-gray-900 mb-3">语音质量分析</h3>
          <div class="space-y-3">
            <div v-for="metric in feedback.speechAnalysis.qualityMetrics" :key="metric.name"
                 class="flex justify-between items-center">
              <span class="text-sm text-gray-700">{{ metric.name }}</span>
              <div class="flex items-center space-x-2">
                <div class="w-20 bg-gray-200 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full"
                    :class="getScoreBarColor(metric.score)"
                    :style="{ width: `${metric.score}%` }"
                  ></div>
                </div>
                <span class="text-sm font-medium text-gray-900 w-8">{{ metric.score }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI智能建议 -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-6">AI智能建议</h2>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
            <h3 class="font-medium text-green-900 mb-3 flex items-center">
              <i class="fas fa-thumbs-up mr-2"></i>
              表现优秀的方面
            </h3>
            <ul class="text-sm text-green-800 space-y-2">
              <li v-for="strength in feedback.strengths" :key="strength" class="flex items-start">
                <i class="fas fa-check-circle text-green-600 mr-2 mt-0.5 text-xs"></i>
                {{ strength }}
              </li>
            </ul>
          </div>
        </div>
        
        <div>
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
            <h3 class="font-medium text-yellow-900 mb-3 flex items-center">
              <i class="fas fa-lightbulb mr-2"></i>
              改进建议
            </h3>
            <ul class="text-sm text-yellow-800 space-y-2">
              <li v-for="suggestion in feedback.suggestions" :key="suggestion" class="flex items-start">
                <i class="fas fa-arrow-right text-yellow-600 mr-2 mt-0.5 text-xs"></i>
                {{ suggestion }}
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <!-- 个性化学习路径 -->
      <div class="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 class="font-medium text-blue-900 mb-3 flex items-center">
          <i class="fas fa-route mr-2"></i>
          个性化学习路径推荐
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div v-for="path in feedback.learningPaths" :key="path.title" 
               class="bg-white rounded-lg p-3 border">
            <h4 class="font-medium text-gray-900 mb-1">{{ path.title }}</h4>
            <p class="text-sm text-gray-600 mb-2">{{ path.description }}</p>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500">预计时长: {{ path.duration }}</span>
              <button class="text-xs text-blue-600 hover:text-blue-800 font-medium">
                开始学习
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 详细反馈 -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">AI详细反馈</h2>
      <div class="bg-gray-50 rounded-lg p-6">
        <div class="prose max-w-none">
          <p class="text-gray-700 leading-relaxed mb-4">{{ feedback.detailedFeedback }}</p>
          
          <div class="mt-6 p-4 bg-white rounded-lg border">
            <h4 class="font-medium text-gray-900 mb-2">总结与展望</h4>
            <p class="text-gray-700 text-sm">{{ feedback.summary }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-center space-x-4">
        <button @click="scheduleRetry" class="btn-primary">
          <i class="fas fa-redo mr-2"></i>
          安排重新试讲
        </button>
        <button @click="shareReport" class="btn-secondary">
          <i class="fas fa-share mr-2"></i>
          分享报告
        </button>
        <button @click="saveToLibrary" class="btn-secondary">
          <i class="fas fa-bookmark mr-2"></i>
          保存到学习档案
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const lectureId = route.params.lectureId

// 视频播放状态
const isPlaying = ref(false)
const currentTime = ref(0)
const totalTime = ref(600) // 10分钟 = 600秒
const playProgress = computed(() => (currentTime.value / totalTime.value) * 100)

const feedback = ref({
  topic: '数学基础 - 分数运算',
  duration: 10,
  date: '2024-01-15T10:30:00Z',
  totalScore: 85,
  scores: [
    { 
      category: '教学内容', 
      score: 88,
      feedback: '知识点讲解准确，概念阐述清晰',
      suggestions: ['可以增加更多实际应用例子', '建议补充相关背景知识']
    },
    { 
      category: '表达能力', 
      score: 82,
      feedback: '语言表达流畅，逻辑清楚',
      suggestions: ['在关键概念处可以适当重复', '语速可以稍微放慢']
    },
    { 
      category: '互动效果', 
      score: 85,
      feedback: '能够引导学生思考，互动自然',
      suggestions: ['可以设计更多提问环节', '增加小组讨论活动']
    },
    { 
      category: '时间控制', 
      score: 90,
      feedback: '时间安排合理，节奏把握得当',
      suggestions: ['可以为突发情况预留更多时间']
    },
    { 
      category: '教学方法', 
      score: 80,
      feedback: '教学方法得当，循序渐进',
      suggestions: ['可以尝试更多元化的教学方式', '增加多媒体辅助工具']
    }
  ],
  strengths: [
    '教学内容结构清晰，逻辑性强',
    '语言表达流畅，声音洪亮',
    '时间控制得当，节奏把握良好'
  ],
  suggestions: [
    '可以增加更多互动环节，提高学生参与度',
    '建议使用更多生动的例子来解释抽象概念',
    '可以适当放慢语速，给学生更多思考时间'
  ],
  detailedFeedback: '本次试讲整体表现良好。教学内容准备充分，知识点讲解清晰。在教学过程中，能够运用适当的教学方法，但在互动环节还有提升空间。建议在今后的教学中，多设计一些启发性问题，让学生主动思考。同时，可以通过更多的实例和练习来帮助学生理解和掌握知识点。',
  summary: '总体而言，这是一次成功的试讲。您在内容准确性和时间控制方面表现突出，建议继续保持。在互动设计和教学方法多样化方面还有提升空间，这将是您下一步重点改进的方向。',
  keyMoments: [
    {
      time: 120,
      type: 'highlight',
      typeText: '亮点',
      description: '用生动的例子解释分数概念，形象易懂'
    },
    {
      time: 240,
      type: 'improvement',
      typeText: '待改进',
      description: '此处可以增加学生互动，检验理解程度'
    },
    {
      time: 360,
      type: 'highlight',
      typeText: '亮点',
      description: '时间控制良好，顺利过渡到下一环节'
    },
    {
      time: 480,
      type: 'note',
      typeText: '注意',
      description: '语速稍快，建议在重点概念处放慢'
    },
    {
      time: 540,
      type: 'highlight',
      typeText: '亮点',
      description: '总结环节简洁明了，重点突出'
    }
  ],
  speechAnalysis: {
    averageSpeed: 175,
    clarity: 88,
    pauseCount: 12,
    speedTrend: [160, 170, 180, 185, 175, 170, 165, 175, 180, 170],
    qualityMetrics: [
      { name: '音量稳定性', score: 85 },
      { name: '语调变化', score: 82 },
      { name: '停顿合理性', score: 88 },
      { name: '发音准确性', score: 90 },
      { name: '语言流畅度', score: 84 }
    ]
  },
  learningPaths: [
    {
      title: '互动教学技巧',
      description: '学习如何设计有效的课堂互动',
      duration: '2小时'
    },
    {
      title: '多媒体教学应用',
      description: '掌握现代教学工具的使用',
      duration: '1.5小时'
    },
    {
      title: '语言表达优化',
      description: '提升教学语言的感染力',
      duration: '1小时'
    }
  ]
})

const getScoreColor = (score: number) => {
  if (score >= 90) return 'text-green-600'
  if (score >= 80) return 'text-blue-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

// 获取评分等级
const getScoreLevel = (score: number) => {
  if (score >= 90) return '优秀'
  if (score >= 80) return '良好'
  if (score >= 70) return '中等'
  if (score >= 60) return '及格'
  return '待改进'
}

// 获取评分条颜色
const getScoreBarColor = (score: number) => {
  if (score >= 90) return 'bg-green-500'
  if (score >= 80) return 'bg-blue-500'
  if (score >= 70) return 'bg-yellow-500'
  return 'bg-red-500'
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 格式化时间
const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// 视频控制方法
const togglePlay = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    // TODO: 实现真实的视频播放控制
    console.log('开始播放视频')
  } else {
    console.log('暂停播放视频')
  }
}

const seekToTime = (time: number) => {
  currentTime.value = time
  // TODO: 实现真实的视频跳转功能
  console.log('跳转到时间:', time)
}

// 操作方法
const downloadReport = () => {
  console.log('下载报告')
  // TODO: 实现报告下载功能
}

const scheduleRetry = () => {
  console.log('安排重新试讲')
  // TODO: 实现重新试讲安排功能
}

const shareReport = () => {
  console.log('分享报告')
  // TODO: 实现报告分享功能
}

const saveToLibrary = () => {
  console.log('保存到学习档案')
  // TODO: 实现保存到学习档案功能
}

onMounted(() => {
  // 根据 lectureId 加载具体的反馈数据
  console.log('Loading feedback for lecture:', lectureId)
})
</script>