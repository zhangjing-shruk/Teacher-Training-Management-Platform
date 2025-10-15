<template>
  <div class="space-y-8">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">教师管理</h1>
        <p class="mt-2 text-gray-600">管理教师账户和培训进度</p>
      </div>
      <button 
        @click="showAddModal = true"
        class="btn-primary"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        添加教师
      </button>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">总教师数</p>
            <p class="text-2xl font-semibold text-gray-900">{{ teachers.length }}</p>
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
            <p class="text-sm font-medium text-gray-600">已通过培训</p>
            <p class="text-2xl font-semibold text-gray-900">{{ teachers.filter(t => t.status === 'passed').length }}</p>
          </div>
        </div>
      </div>

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
            <p class="text-sm font-medium text-gray-600">培训中</p>
            <p class="text-2xl font-semibold text-gray-900">{{ teachers.filter(t => t.status === 'training').length }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">待审核</p>
            <p class="text-2xl font-semibold text-gray-900">{{ teachers.filter(t => t.status === 'pending_review').length }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选和搜索 -->
    <div class="card">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索教师姓名或邮箱..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
        </div>
        <select
          v-model="statusFilter"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">全部状态</option>
          <option value="training">培训中</option>
          <option value="pending_review">待审核</option>
          <option value="passed">已通过</option>
          <option value="failed">未通过</option>
        </select>
      </div>
    </div>

    <!-- 教师列表 -->
    <div class="card">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">教师信息</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">培训状态</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">试讲次数</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">注册时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="teacher in filteredTeachers" :key="teacher.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                      <span class="text-sm font-medium text-gray-700">{{ teacher.name.charAt(0) }}</span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ teacher.name }}</div>
                    <div class="text-sm text-gray-500">{{ teacher.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                      :class="getStatusClass(teacher.status)">
                  {{ getStatusText(teacher.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ teacher.lectureCount }}/5
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(teacher.createdAt) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex space-x-2">
                  <button 
                    @click="viewTeacher(teacher)"
                    class="text-blue-600 hover:text-blue-900"
                  >
                    查看
                  </button>
                  <button 
                    @click="editTeacher(teacher)"
                    class="text-green-600 hover:text-green-900"
                  >
                    编辑
                  </button>
                  <button 
                    @click="deleteTeacher(teacher)"
                    class="text-red-600 hover:text-red-900"
                  >
                    删除
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 添加教师模态框 -->
    <div v-if="showAddModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">添加新教师</h3>
          <form @submit.prevent="addTeacher">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">姓名</label>
              <input
                v-model="newTeacher.name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
              <input
                v-model="newTeacher.email"
                type="email"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
            </div>
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">初始密码</label>
              <input
                v-model="newTeacher.password"
                type="password"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
            </div>
            <div class="flex justify-end space-x-3">
              <button
                type="button"
                @click="showAddModal = false"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
              >
                添加
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Teacher {
  id: number
  name: string
  email: string
  status: 'training' | 'pending_review' | 'passed' | 'failed'
  lectureCount: number
  createdAt: string
}

// 虚拟数据
const teachers = ref<Teacher[]>([
  {
    id: 1,
    name: '张小明',
    email: 'zhang.xiaoming@example.com',
    status: 'training',
    lectureCount: 2,
    createdAt: '2024-01-15'
  },
  {
    id: 2,
    name: '李小红',
    email: 'li.xiaohong@example.com',
    status: 'pending_review',
    lectureCount: 3,
    createdAt: '2024-01-14'
  },
  {
    id: 3,
    name: '王小华',
    email: 'wang.xiaohua@example.com',
    status: 'passed',
    lectureCount: 4,
    createdAt: '2024-01-13'
  },
  {
    id: 4,
    name: '刘小强',
    email: 'liu.xiaoqiang@example.com',
    status: 'failed',
    lectureCount: 5,
    createdAt: '2024-01-12'
  },
  {
    id: 5,
    name: '陈小美',
    email: 'chen.xiaomei@example.com',
    status: 'training',
    lectureCount: 1,
    createdAt: '2024-01-11'
  }
])

const searchQuery = ref('')
const statusFilter = ref('')
const showAddModal = ref(false)
const newTeacher = ref({
  name: '',
  email: '',
  password: ''
})

const filteredTeachers = computed(() => {
  let filtered = teachers.value

  if (searchQuery.value) {
    filtered = filtered.filter(teacher => 
      teacher.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      teacher.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(teacher => teacher.status === statusFilter.value)
  }

  return filtered
})

const getStatusClass = (status: string) => {
  const classes = {
    training: 'bg-blue-100 text-blue-800',
    pending_review: 'bg-yellow-100 text-yellow-800',
    passed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status: string) => {
  const texts = {
    training: '培训中',
    pending_review: '待审核',
    passed: '已通过',
    failed: '未通过'
  }
  return texts[status as keyof typeof texts] || '未知'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const addTeacher = () => {
  const newId = Math.max(...teachers.value.map(t => t.id)) + 1
  teachers.value.push({
    id: newId,
    name: newTeacher.value.name,
    email: newTeacher.value.email,
    status: 'training',
    lectureCount: 0,
    createdAt: new Date().toISOString().split('T')[0]
  })
  
  // 重置表单
  newTeacher.value = { name: '', email: '', password: '' }
  showAddModal.value = false
  
  alert('教师添加成功！')
}

const viewTeacher = (teacher: Teacher) => {
  alert(`查看教师：${teacher.name}\n邮箱：${teacher.email}\n状态：${getStatusText(teacher.status)}`)
}

const editTeacher = (teacher: Teacher) => {
  const newName = prompt('请输入新的姓名：', teacher.name)
  if (newName !== null && newName !== teacher.name && newName.trim() !== '') {
    const index = teachers.value.findIndex(t => t.id === teacher.id)
    if (index > -1) {
      teachers.value[index].name = newName
      alert('教师信息更新成功！')
    }
  }
}

const deleteTeacher = (teacher: Teacher) => {
  if (confirm(`确定要删除教师 ${teacher.name} 吗？`)) {
    const index = teachers.value.findIndex(t => t.id === teacher.id)
    if (index > -1) {
      teachers.value.splice(index, 1)
      alert('教师删除成功！')
    }
  }
}
</script>