<template>
  <div class="space-y-6">
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-2xl font-bold text-gray-900">试讲审核</h1>
        <router-link 
          to="/manager"
          class="text-primary-600 hover:text-primary-700 font-medium"
        >
          ← 返回管理面板
        </router-link>
      </div>
      
      <!-- 教师信息 -->
      <div class="bg-gray-50 rounded-lg p-4 mb-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-3">教师信息</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <span class="text-sm text-gray-500">姓名:</span>
            <p class="font-medium text-gray-900">{{ lecture.teacherName }}</p>
          </div>
          <div>
            <span class="text-sm text-gray-500">工号:</span>
            <p class="font-medium text-gray-900">{{ lecture.teacherId }}</p>
          </div>
          <div>
            <span class="text-sm text-gray-500">试讲时间:</span>
            <p class="font-medium text-gray-900">{{ lecture.date }}</p>
          </div>
        </div>
      </div>
      
      <!-- 试讲详情 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div>
          <h2 class="text-lg font-semibold text-gray-800 mb-4">试讲详情</h2>
          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-gray-600">课程主题:</span>
              <span class="font-medium">{{ lecture.topic }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">试讲时长:</span>
              <span class="font-medium">{{ lecture.duration }}分钟</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">AI评分:</span>
              <span class="font-medium" :class="getScoreColor(lecture.aiScore)">
                {{ lecture.aiScore }}/100
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">状态:</span>
              <span class="px-2 py-1 rounded-full text-xs font-medium" :class="getStatusColor(lecture.status)">
                {{ getStatusText(lecture.status) }}
              </span>
            </div>
          </div>
        </div>
        
        <div>
          <h2 class="text-lg font-semibold text-gray-800 mb-4">AI分析结果</h2>
          <div class="space-y-4">
            <div v-for="item in lecture.aiAnalysis" :key="item.category" 
                 class="flex justify-between items-center">
              <span class="text-gray-700">{{ item.category }}</span>
              <div class="flex items-center space-x-2">
                <div class="w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-primary-600 h-2 rounded-full" 
                    :style="{ width: `${item.score}%` }"
                  ></div>
                </div>
                <span class="text-sm font-medium text-gray-900 w-8">{{ item.score }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 审核操作 -->
      <div v-if="lecture.status === 'pending'" class="border-t pt-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">审核操作</h2>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">审核意见</label>
            <textarea 
              v-model="reviewComment"
              rows="4"
              class="w-full border border-gray-300 rounded-md px-3 py-2"
              placeholder="请输入审核意见..."
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">管理员评分</label>
            <input 
              v-model="managerScore"
              type="number"
              min="0"
              max="100"
              class="w-32 border border-gray-300 rounded-md px-3 py-2"
              placeholder="0-100"
            >
          </div>
          
          <div class="flex space-x-4">
            <button 
              @click="approveLecture"
              class="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200"
            >
              通过审核
            </button>
            <button 
              @click="rejectLecture"
              class="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200"
            >
              不通过
            </button>
            <button 
              @click="requestRevision"
              class="bg-yellow-600 hover:bg-yellow-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200"
            >
              要求修改
            </button>
          </div>
        </div>
      </div>
      
      <!-- 已审核信息 -->
      <div v-else class="border-t pt-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">审核结果</h2>
        <div class="bg-gray-50 rounded-lg p-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <span class="text-sm text-gray-500">审核状态:</span>
              <p class="font-medium" :class="getStatusColor(lecture.status)">
                {{ getStatusText(lecture.status) }}
              </p>
            </div>
            <div>
              <span class="text-sm text-gray-500">管理员评分:</span>
              <p class="font-medium">{{ lecture.managerScore }}/100</p>
            </div>
          </div>
          <div>
            <span class="text-sm text-gray-500">审核意见:</span>
            <p class="mt-1 text-gray-700">{{ lecture.reviewComment }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const lectureId = route.params.lectureId

const reviewComment = ref('')
const managerScore = ref<number | null>(null)

const lecture = ref({
  id: 1,
  teacherName: '张老师',
  teacherId: 'T001',
  topic: '数学基础 - 分数运算',
  duration: 10,
  date: '2024-01-15 14:30',
  aiScore: 85,
  status: 'pending', // pending, approved, rejected, revision_required
  aiAnalysis: [
    { category: '教学内容', score: 88 },
    { category: '表达能力', score: 82 },
    { category: '互动效果', score: 85 },
    { category: '时间控制', score: 90 },
    { category: '教学方法', score: 80 }
  ],
  managerScore: null,
  reviewComment: ''
})

const getScoreColor = (score: number) => {
  if (score >= 90) return 'text-green-600'
  if (score >= 80) return 'text-blue-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending': return 'bg-yellow-100 text-yellow-800'
    case 'approved': return 'bg-green-100 text-green-800'
    case 'rejected': return 'bg-red-100 text-red-800'
    case 'revision_required': return 'bg-orange-100 text-orange-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'pending': return '待审核'
    case 'approved': return '已通过'
    case 'rejected': return '未通过'
    case 'revision_required': return '需修改'
    default: return '未知'
  }
}

const approveLecture = () => {
  if (!reviewComment.value || managerScore.value === null) {
    alert('请填写审核意见和评分')
    return
  }
  
  // 提交审核结果
  console.log('通过审核:', {
    lectureId: lectureId,
    comment: reviewComment.value,
    score: managerScore.value
  })
  
  router.push('/manager')
}

const rejectLecture = () => {
  if (!reviewComment.value) {
    alert('请填写审核意见')
    return
  }
  
  console.log('拒绝审核:', {
    lectureId: lectureId,
    comment: reviewComment.value
  })
  
  router.push('/manager')
}

const requestRevision = () => {
  if (!reviewComment.value) {
    alert('请填写修改要求')
    return
  }
  
  console.log('要求修改:', {
    lectureId: lectureId,
    comment: reviewComment.value
  })
  
  router.push('/manager')
}

onMounted(() => {
  // 根据 lectureId 加载具体的试讲数据
  console.log('Loading lecture for review:', lectureId)
})
</script>