<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-3xl font-bold text-gray-900">讲座评审</h1>
      <p class="mt-2 text-gray-600">评审教师提交的试讲视频</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
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
            <p class="text-sm font-medium text-gray-600">待评审</p>
            <p class="text-2xl font-semibold text-gray-900">{{ lectures.filter(l => l.status === 'pending_review').length }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">AI分析中</p>
            <p class="text-2xl font-semibold text-gray-900">{{ lectures.filter(l => l.status === 'processing').length }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">已通过</p>
            <p class="text-2xl font-semibold text-gray-900">{{ lectures.filter(l => l.status === 'passed').length }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">未通过</p>
            <p class="text-2xl font-semibold text-gray-900">{{ lectures.filter(l => l.status === 'failed').length }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选器 -->
    <div class="card">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索教师姓名..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
        </div>
        <select
          v-model="statusFilter"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">全部状态</option>
          <option value="processing">AI分析中</option>
          <option value="pending_review">待评审</option>
          <option value="passed">已通过</option>
          <option value="failed">未通过</option>
        </select>
        <select
          v-model="sortBy"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="newest">最新提交</option>
          <option value="oldest">最早提交</option>
          <option value="score">AI评分</option>
        </select>
      </div>
    </div>

    <!-- 讲座列表 -->
    <div class="card">
      <div class="space-y-4">
        <div v-for="lecture in filteredLectures" :key="lecture.id" 
             class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-3">
                <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                  <span class="text-sm font-medium text-gray-700">{{ lecture.teacherName.charAt(0) }}</span>
                </div>
                <div>
                  <h3 class="text-lg font-medium text-gray-900">{{ lecture.teacherName }}</h3>
                  <p class="text-sm text-gray-500">第 {{ lecture.attemptNumber }} 次试讲</p>
                </div>
                <span class="px-2 py-1 text-xs font-semibold rounded-full"
                      :class="getStatusClass(lecture.status)">
                  {{ getStatusText(lecture.status) }}
                </span>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <p class="text-sm text-gray-600">提交时间</p>
                  <p class="text-sm font-medium">{{ formatDate(lecture.submittedAt) }}</p>
                </div>
                <div v-if="lecture.aiScore">
                  <p class="text-sm text-gray-600">AI综合评分</p>
                  <p class="text-sm font-medium" :class="getScoreColor(lecture.aiScore)">
                    {{ lecture.aiScore }}/100
                  </p>
                </div>
              </div>

              <div v-if="lecture.aiAnalysis" class="mb-4">
                <p class="text-sm text-gray-600 mb-2">AI分析结果</p>
                <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                  <div class="text-center">
                    <p class="text-xs text-gray-500">发音</p>
                    <p class="text-sm font-medium">{{ lecture.aiAnalysis.pronunciation }}/20</p>
                  </div>
                  <div class="text-center">
                    <p class="text-xs text-gray-500">流畅度</p>
                    <p class="text-sm font-medium">{{ lecture.aiAnalysis.fluency }}/20</p>
                  </div>
                  <div class="text-center">
                    <p class="text-xs text-gray-500">能量</p>
                    <p class="text-sm font-medium">{{ lecture.aiAnalysis.energy }}/20</p>
                  </div>
                  <div class="text-center">
                    <p class="text-xs text-gray-500">内容</p>
                    <p class="text-sm font-medium">{{ lecture.aiAnalysis.content }}/20</p>
                  </div>
                  <div class="text-center">
                    <p class="text-xs text-gray-500">互动</p>
                    <p class="text-sm font-medium">{{ lecture.aiAnalysis.interaction }}/20</p>
                  </div>
                </div>
              </div>

              <div v-if="lecture.managerFeedback" class="mb-4 p-3 bg-gray-50 rounded-lg">
                <p class="text-sm text-gray-600 mb-1">管理员评语</p>
                <p class="text-sm">{{ lecture.managerFeedback }}</p>
              </div>
            </div>

            <div class="flex flex-col space-y-2 ml-4">
              <button 
                @click="viewVideo(lecture)"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
              >
                观看视频
              </button>
              <button 
                v-if="lecture.status === 'pending_review'"
                @click="reviewLecture(lecture)"
                class="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700"
              >
                开始评审
              </button>
              <button 
                @click="viewDetails(lecture)"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
              >
                查看详情
              </button>
            </div>
          </div>
        </div>

        <div v-if="filteredLectures.length === 0" class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">暂无讲座</h3>
          <p class="mt-1 text-sm text-gray-500">没有找到符合条件的试讲记录</p>
        </div>
      </div>
    </div>

    <!-- 评审模态框 -->
    <div v-if="showReviewModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">评审试讲 - {{ selectedLecture?.teacherName }}</h3>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- 视频播放区域 -->
            <div>
              <div class="aspect-video bg-gray-900 rounded-lg flex items-center justify-center">
                <div class="text-center text-white">
                  <svg class="mx-auto h-12 w-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.586a1 1 0 01.707.293l2.414 2.414a1 1 0 00.707.293H15M9 10V9a2 2 0 012-2h2a2 2 0 012 2v1M9 10v5a2 2 0 002 2h2a2 2 0 002-2v-5" />
                  </svg>
                  <p>试讲视频播放器</p>
                  <p class="text-sm text-gray-300">{{ selectedLecture?.videoUrl }}</p>
                </div>
              </div>
              
              <!-- AI分析结果 -->
              <div v-if="selectedLecture?.aiAnalysis" class="mt-4 p-4 bg-gray-50 rounded-lg">
                <h4 class="font-medium text-gray-900 mb-3">AI分析结果</h4>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">发音清晰度</span>
                    <span class="text-sm font-medium">{{ selectedLecture.aiAnalysis.pronunciation }}/20</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">语言流畅度</span>
                    <span class="text-sm font-medium">{{ selectedLecture.aiAnalysis.fluency }}/20</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">能量与热情</span>
                    <span class="text-sm font-medium">{{ selectedLecture.aiAnalysis.energy }}/20</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">内容覆盖度</span>
                    <span class="text-sm font-medium">{{ selectedLecture.aiAnalysis.content }}/20</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">互动性</span>
                    <span class="text-sm font-medium">{{ selectedLecture.aiAnalysis.interaction }}/20</span>
                  </div>
                  <div class="border-t pt-2 mt-2">
                    <div class="flex justify-between font-medium">
                      <span>综合评分</span>
                      <span :class="getScoreColor(selectedLecture.aiScore || 0)">{{ selectedLecture.aiScore }}/100</span>
                    </div>
                  </div>
                </div>
                
                <div v-if="selectedLecture.aiSuggestions" class="mt-4">
                  <h5 class="text-sm font-medium text-gray-900 mb-2">AI建议</h5>
                  <p class="text-sm text-gray-600">{{ selectedLecture.aiSuggestions }}</p>
                </div>
              </div>
            </div>

            <!-- 评审表单 -->
            <div>
              <form @submit.prevent="submitReview">
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">评审结果</label>
                  <div class="space-y-2">
                    <label class="flex items-center">
                      <input v-model="reviewForm.result" type="radio" value="passed" class="mr-2">
                      <span class="text-green-600">通过</span>
                    </label>
                    <label class="flex items-center">
                      <input v-model="reviewForm.result" type="radio" value="failed" class="mr-2">
                      <span class="text-red-600">不通过</span>
                    </label>
                  </div>
                </div>

                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">评语</label>
                  <textarea
                    v-model="reviewForm.feedback"
                    rows="6"
                    required
                    placeholder="请输入详细的评审意见和建议..."
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  ></textarea>
                </div>

                <div class="mb-6">
                  <label class="block text-sm font-medium text-gray-700 mb-2">评分 (可选)</label>
                  <input
                    v-model.number="reviewForm.score"
                    type="number"
                    min="0"
                    max="100"
                    placeholder="0-100"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                </div>

                <div class="flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="showReviewModal = false"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
                  >
                    取消
                  </button>
                  <button
                    type="submit"
                    class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
                  >
                    提交评审
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface AIAnalysis {
  pronunciation: number
  fluency: number
  energy: number
  content: number
  interaction: number
}

interface Lecture {
  id: number
  teacherName: string
  teacherId: number
  attemptNumber: number
  status: 'processing' | 'pending_review' | 'passed' | 'failed'
  submittedAt: string
  videoUrl: string
  aiScore?: number
  aiAnalysis?: AIAnalysis
  aiSuggestions?: string
  managerFeedback?: string
  reviewedAt?: string
}

// 试讲数据
const lectures = ref<Lecture[]>([])

// 加载试讲数据
const loadLectures = async () => {
  try {
    // TODO: 调用API获取试讲数据
    // const response = await fetch('/api/manager/lectures')
    // const data = await response.json()
    // lectures.value = data
    console.log('加载试讲数据')
  } catch (error) {
    console.error('加载试讲数据失败:', error)
  }
}

const searchQuery = ref('')
const statusFilter = ref('')
const sortBy = ref('newest')
const showReviewModal = ref(false)
const selectedLecture = ref<Lecture | null>(null)
const reviewForm = ref({
  result: '',
  feedback: '',
  score: null as number | null
})

const filteredLectures = computed(() => {
  let filtered = lectures.value

  if (searchQuery.value) {
    filtered = filtered.filter(lecture => 
      lecture.teacherName.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(lecture => lecture.status === statusFilter.value)
  }

  // 排序
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'oldest':
        return new Date(a.submittedAt).getTime() - new Date(b.submittedAt).getTime()
      case 'score':
        return (b.aiScore || 0) - (a.aiScore || 0)
      default: // newest
        return new Date(b.submittedAt).getTime() - new Date(a.submittedAt).getTime()
    }
  })

  return filtered
})

const getStatusClass = (status: string) => {
  const classes = {
    processing: 'bg-blue-100 text-blue-800',
    pending_review: 'bg-yellow-100 text-yellow-800',
    passed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status: string) => {
  const texts = {
    processing: 'AI分析中',
    pending_review: '待评审',
    passed: '已通过',
    failed: '未通过'
  }
  return texts[status as keyof typeof texts] || '未知'
}

const getScoreColor = (score: number) => {
  if (score >= 80) return 'text-green-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const viewVideo = (lecture: Lecture) => {
  alert(`播放视频：${lecture.videoUrl}\n教师：${lecture.teacherName}\n第${lecture.attemptNumber}次试讲`)
}

const reviewLecture = (lecture: Lecture) => {
  selectedLecture.value = lecture
  reviewForm.value = {
    result: '',
    feedback: '',
    score: null
  }
  showReviewModal.value = true
}

const viewDetails = (lecture: Lecture) => {
  // 跳转到试讲详情页面
  router.push(`/manager/review/${lecture.id}`)
}

const submitReview = () => {
  if (!selectedLecture.value || !reviewForm.value.result || !reviewForm.value.feedback) {
    alert('请填写完整的评审信息')
    return
  }

  // 更新讲座状态
  const lecture = selectedLecture.value
  const result = reviewForm.value.result
  const feedback = reviewForm.value.feedback
  
  if (lecture && result && feedback) {
    const index = lectures.value.findIndex(l => l.id === lecture.id)
    if (index > -1) {
      const lectureItem = lectures.value[index]
      if (lectureItem) {
        lectureItem.status = result as 'passed' | 'failed'
        lectureItem.managerFeedback = feedback
        lectureItem.reviewedAt = new Date().toISOString()
      }
    }
  }

  showReviewModal.value = false
  alert('评审提交成功！')
}

// 生命周期
onMounted(() => {
  loadLectures()
})
</script>