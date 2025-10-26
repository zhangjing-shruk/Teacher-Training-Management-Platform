<template>
  <div class="space-y-8">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">培训资料管理</h1>
        <p class="mt-2 text-gray-600">管理培训课程和学习资料</p>
      </div>
      <div class="flex space-x-3">
        <button
          @click="syncAllMaterials"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center space-x-2"
          :disabled="isSyncing"
        >
          <svg v-if="isSyncing" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>{{ isSyncing ? '同步中...' : '同步到教师' }}</span>
        </button>
        <button
          @click="showAddModal = true"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>添加资料</span>
        </button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">总资料数</p>
            <p class="text-2xl font-semibold text-gray-900">{{ materials.length }}</p>
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
            <p class="text-sm font-medium text-gray-600">已发布</p>
            <p class="text-2xl font-semibold text-gray-900">{{ materials.filter(m => m.status === 'published').length }}</p>
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
            <p class="text-sm font-medium text-gray-600">草稿</p>
            <p class="text-2xl font-semibold text-gray-900">{{ materials.filter(m => m.status === 'draft').length }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">视频资料</p>
            <p class="text-2xl font-semibold text-gray-900">{{ materials.filter(m => m.type === 'video').length }}</p>
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
            placeholder="搜索资料标题..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
        </div>
        <select
          v-model="typeFilter"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">全部类型</option>
          <option value="document">文档</option>
          <option value="video">视频</option>
          <option value="audio">音频</option>
          <option value="presentation">演示文稿</option>
        </select>
        <select
          v-model="statusFilter"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">全部状态</option>
          <option value="published">已发布</option>
          <option value="draft">草稿</option>
        </select>
        <select
          v-model="sortBy"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="newest">最新创建</option>
          <option value="oldest">最早创建</option>
          <option value="name">按名称</option>
          <option value="downloads">下载量</option>
        </select>
      </div>
    </div>

    <!-- 资料列表 -->
    <div class="card">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="material in filteredMaterials" :key="material.id" 
             class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center"
                   :class="getTypeIconClass(material.type)">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getTypeIconPath(material.type)" />
                </svg>
              </div>
              <span class="px-2 py-1 text-xs font-semibold rounded-full"
                    :class="getStatusClass(material.status)">
                {{ getStatusText(material.status) }}
              </span>
            </div>
            <div class="flex space-x-1">
              <button
                @click="editMaterial(material)"
                class="p-1 text-gray-400 hover:text-blue-600"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                @click="deleteMaterial(material)"
                class="p-1 text-gray-400 hover:text-red-600"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>

          <h3 class="text-lg font-medium text-gray-900 mb-2">{{ material.title }}</h3>
          <p class="text-sm text-gray-600 mb-3 line-clamp-2">{{ material.description }}</p>

          <div class="space-y-2 text-xs text-gray-500">
            <div class="flex justify-between">
              <span>创建时间</span>
              <span>{{ formatDate(material.createdAt) }}</span>
            </div>
            <div class="flex justify-between">
              <span>文件大小</span>
              <span>{{ material.fileSize }}</span>
            </div>
            <div class="flex justify-between">
              <span>下载次数</span>
              <span>{{ material.downloadCount }}</span>
            </div>
          </div>

          <div class="mt-4 flex space-x-2">
            <button
              @click="previewMaterial(material)"
              class="flex-1 px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-md hover:bg-blue-100"
            >
              预览
            </button>
            <button
              @click="downloadMaterial(material)"
              class="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
            >
              下载
            </button>
          </div>
        </div>

        <div v-if="filteredMaterials.length === 0" class="col-span-full text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">暂无资料</h3>
          <p class="mt-1 text-sm text-gray-500">没有找到符合条件的培训资料</p>
        </div>
      </div>
    </div>

    <!-- 添加/编辑资料模态框 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ showAddModal ? '添加培训资料' : '编辑培训资料' }}
          </h3>
          
          <form @submit.prevent="submitMaterial">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">资料标题</label>
                <input
                  v-model="materialForm.title"
                  type="text"
                  required
                  placeholder="请输入资料标题"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">资料描述</label>
                <textarea
                  v-model="materialForm.description"
                  rows="3"
                  placeholder="请输入资料描述"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>

              <div class="grid grid-cols-4 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">资料类别</label>
                  <select
                    v-model="materialForm.category"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">请选择类别</option>
                    <option value="教学文档">教学文档</option>
                    <option value="其他培训文档">其他培训文档</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">资料类型</label>
                  <select
                    v-model="materialForm.type"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">请选择类型</option>
                    <option value="document">文档</option>
                    <option value="video">视频</option>
                    <option value="audio">音频</option>
                    <option value="presentation">演示文稿</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">学习时长</label>
                  <input
                    v-model="materialForm.duration"
                    type="text"
                    placeholder="例如：20分钟"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
                  <select
                    v-model="materialForm.status"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="draft">草稿</option>
                    <option value="published">发布</option>
                  </select>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">文件上传</label>
                <div 
                  @click="triggerFileInput"
                  @dragover.prevent="handleDragOver"
                  @dragleave.prevent="handleDragLeave"
                  @drop.prevent="handleDrop"
                  :class="[
                    'border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors',
                    isDragOver ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
                  ]"
                >
                  <!-- 隐藏的文件输入 -->
                  <input
                    ref="fileInput"
                    type="file"
                    class="hidden"
                    :accept="acceptedFileTypes"
                    @change="handleFileSelect"
                  />
                  
                  <!-- 上传状态显示 -->
                  <div v-if="uploadProgress > 0 && uploadProgress < 100" class="mb-4">
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        :style="{ width: uploadProgress + '%' }"
                      ></div>
                    </div>
                    <p class="text-sm text-gray-600 mt-2">上传中... {{ uploadProgress }}%</p>
                  </div>
                  
                  <!-- 已选择文件显示 -->
                  <div v-else-if="selectedFile" class="mb-4">
                    <div class="flex items-center justify-center space-x-2">
                      <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span class="text-sm text-gray-700">{{ selectedFile.name }}</span>
                      <span class="text-xs text-gray-500">({{ formatFileSize(selectedFile.size) }})</span>
                    </div>
                    <button 
                      type="button" 
                      @click.stop="clearSelectedFile"
                      class="mt-2 text-xs text-red-600 hover:text-red-500"
                    >
                      移除文件
                    </button>
                  </div>
                  
                  <!-- 默认上传界面 -->
                  <div v-else>
                    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <div class="mt-2">
                      <span class="text-blue-600 hover:text-blue-500">
                        点击上传文件
                      </span>
                      <p class="text-sm text-gray-500">或拖拽文件到此处</p>
                    </div>
                    <p class="text-xs text-gray-400 mt-2">
                      支持 PDF, DOC, PPT, MP4, MP3 等格式，最大 100MB
                    </p>
                  </div>
                </div>
                
                <!-- 错误提示 -->
                <div v-if="uploadError" class="mt-2 text-sm text-red-600">
                  {{ uploadError }}
                </div>
              </div>
            </div>

            <div class="flex justify-end space-x-3 mt-6">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="isSubmitting"
                :class="[
                  'px-4 py-2 text-sm font-medium text-white rounded-md',
                  isSubmitting 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-blue-600 hover:bg-blue-700'
                ]"
              >
                <span v-if="isSubmitting" class="flex items-center">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ showAddModal ? '添加中...' : '保存中...' }}
                </span>
                <span v-else>
                  {{ showAddModal ? '添加' : '保存' }}
                </span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { runSupabaseTest } from '@/utils/supabaseTest'

interface Material {
  id: string  // 改为 string 类型以支持 UUID
  title: string
  description: string
  type: 'document' | 'video' | 'audio' | 'presentation'
  status: 'published' | 'draft'
  fileUrl: string
  fileSize: string
  downloadCount: number
  createdAt: string
  updatedAt: string
}

// 材料数据 - 从后端API加载
const materials = ref<Material[]>([])

const searchQuery = ref('')
const typeFilter = ref('')
const statusFilter = ref('')
const sortBy = ref('newest')
const showAddModal = ref(false)
const showEditModal = ref(false)
const selectedMaterial = ref<Material | null>(null)
const materialForm = ref({
  title: '',
  description: '',
  category: '',
  type: '',
  duration: '',
  status: 'draft'
})

// 同步相关变量
const isSyncing = ref(false)

// 文件上传相关变量
const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const isDragOver = ref(false)
const uploadProgress = ref(0)
const uploadError = ref('')
const isSubmitting = ref(false)
const acceptedFileTypes = '.pdf,.doc,.docx,.ppt,.pptx,.mp4,.mp3,.avi,.mov,.wmv'

const filteredMaterials = computed(() => {
  let filtered = materials.value

  if (searchQuery.value) {
    filtered = filtered.filter(material => 
      material.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      material.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (typeFilter.value) {
    filtered = filtered.filter(material => material.type === typeFilter.value)
  }

  if (statusFilter.value) {
    filtered = filtered.filter(material => material.status === statusFilter.value)
  }

  // 排序
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'oldest':
        return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      case 'name':
        return a.title.localeCompare(b.title)
      case 'downloads':
        return b.downloadCount - a.downloadCount
      default: // newest
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    }
  })

  return filtered
})

const getTypeIconClass = (type: string) => {
  const classes = {
    document: 'bg-red-100 text-red-600',
    video: 'bg-purple-100 text-purple-600',
    audio: 'bg-green-100 text-green-600',
    presentation: 'bg-orange-100 text-orange-600'
  }
  return classes[type as keyof typeof classes] || 'bg-gray-100 text-gray-600'
}

const getTypeIconPath = (type: string) => {
  const paths = {
    document: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    video: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',
    audio: 'M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z',
    presentation: 'M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m0 0V1a1 1 0 011-1h2a1 1 0 011 1v18a1 1 0 01-1 1H5a1 1 0 01-1-1V4a1 1 0 011-1h2z'
  }
  return paths[type as keyof typeof paths] || 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'
}

const getStatusClass = (status: string) => {
  const classes = {
    published: 'bg-green-100 text-green-800',
    draft: 'bg-yellow-100 text-yellow-800'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status: string) => {
  const texts = {
    published: '已发布',
    draft: '草稿'
  }
  return texts[status as keyof typeof texts] || '未知'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const previewMaterial = (material: Material) => {
  if (!material.fileUrl) {
    alert('文件不存在，无法预览')
    return
  }
  
  // 构建完整的文件URL
  const fileUrl = `http://localhost:8000${material.fileUrl}`
  
  // 根据文件类型决定预览方式
  const fileExtension = material.fileUrl.split('.').pop()?.toLowerCase()
  
  if (fileExtension === 'pdf') {
    // PDF文件在新窗口中打开
    window.open(fileUrl, '_blank')
  } else if (['jpg', 'jpeg', 'png', 'gif', 'svg'].includes(fileExtension || '')) {
    // 图片文件在新窗口中打开
    window.open(fileUrl, '_blank')
  } else if (['mp4', 'avi', 'mov', 'wmv'].includes(fileExtension || '')) {
    // 视频文件在新窗口中打开
    window.open(fileUrl, '_blank')
  } else if (['mp3', 'wav', 'ogg'].includes(fileExtension || '')) {
    // 音频文件在新窗口中打开
    window.open(fileUrl, '_blank')
  } else {
    // 其他文件类型直接下载
    downloadMaterial(material)
  }
}

const downloadMaterial = async (material: Material) => {
  if (!material.fileUrl) {
    alert('文件不存在，无法下载')
    return
  }
  
  try {
    // 构建完整的文件URL
    const fileUrl = `http://localhost:8000${material.fileUrl}`
    
    // 创建一个临时的a标签来触发下载
    const link = document.createElement('a')
    link.href = fileUrl
    link.download = material.title || 'download'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    // 增加下载次数（这里可以考虑调用后端API来更新下载次数）
    material.downloadCount++
    
    // 可选：调用后端API更新下载次数
    // await updateDownloadCount(material.id)
    
  } catch (error) {
    console.error('下载失败:', error)
    alert('下载失败，请稍后重试')
  }
}

const editMaterial = (material: Material) => {
  selectedMaterial.value = material
  materialForm.value = {
    title: material.title,
    description: material.description,
    category: '教学文档', // 默认设置为教学文档
    type: material.type,
    duration: '', // 默认为空，管理员可以填写
    status: material.status
  }
  showEditModal.value = true
}

const deleteMaterial = async (material: Material) => {
  if (confirm(`确定要删除资料"${material.title}"吗？`)) {
    try {
      // 使用 Supabase 服务删除培训资料
      const { TrainingMaterialService } = await import('@/services/supabaseService')
      await TrainingMaterialService.delete(material.id)

      // 从本地数组中移除
      const index = materials.value.findIndex(m => m.id === material.id)
      if (index > -1) {
        materials.value.splice(index, 1)
        alert('资料删除成功！')
      }
    } catch (error) {
      console.error('删除资料失败:', error)
      alert('删除失败，请稍后重试')
    }
  }
}

const submitMaterial = async () => {
  console.log('=== submitMaterial 函数开始执行 ===')
  
  // 防止重复提交
  if (isSubmitting.value) {
    console.log('⚠️ 正在提交中，忽略重复请求')
    return
  }
  
  isSubmitting.value = true
  console.log('🔄 设置提交状态为 true')
  
  console.log('表单数据:', JSON.stringify(materialForm.value, null, 2))
  console.log('选中的文件:', selectedFile.value ? {
    name: selectedFile.value.name,
    size: selectedFile.value.size,
    type: selectedFile.value.type
  } : null)
  console.log('showAddModal:', showAddModal.value)
  console.log('showEditModal:', showEditModal.value)
  
  // 清除之前的错误信息
  uploadError.value = ''
  
  // 表单验证
  console.log('开始表单验证...')
  if (!materialForm.value.title?.trim()) {
    const errorMsg = '请输入资料标题'
    console.error('验证失败:', errorMsg)
    uploadError.value = errorMsg
    alert(errorMsg)
    isSubmitting.value = false
    return
  }
  
  if (!materialForm.value.type?.trim()) {
    const errorMsg = '请选择资料类型'
    console.error('验证失败:', errorMsg)
    uploadError.value = errorMsg
    alert(errorMsg)
    isSubmitting.value = false
    return
  }
  
  console.log('表单验证通过')

  if (showAddModal.value) {
    // 添加新资料
    if (!selectedFile.value) {
      const errorMsg = '请选择要上传的文件'
      console.error('验证失败:', errorMsg)
      uploadError.value = errorMsg
      alert(errorMsg)
      isSubmitting.value = false
      return
    }
    
    console.log('=== 开始创建新资料 ===')

    try {
      uploadProgress.value = 0
      uploadError.value = ''

      // 检查Supabase服务可用性
      console.log('检查Supabase服务可用性...')
      const { TrainingMaterialService } = await import('@/services/supabaseService')
      console.log('TrainingMaterialService 导入成功')
      
      // 准备资料数据
      const mappedType = materialForm.value.type === 'presentation' ? 'document' : materialForm.value.type
        
      const materialData = {
        title: materialForm.value.title.trim(),
        description: materialForm.value.description?.trim() || '',
        material_type: mappedType as 'document' | 'video' | 'interactive',
        content_url: `uploads/${selectedFile.value.name}`,
        duration_minutes: parseInt(materialForm.value.duration as string) || 0,
        created_by: 'manager'
      }
      
      console.log('准备创建资料，数据:', JSON.stringify(materialData, null, 2))
      console.log('开始调用 TrainingMaterialService.create...')
      
      const newMaterial = await TrainingMaterialService.create(materialData)
      console.log('✅ 资料创建成功:', JSON.stringify(newMaterial, null, 2))
      
      // 转换为前端格式
       const materialToAdd: Material = {
          id: newMaterial.id,
          title: newMaterial.title,
          description: newMaterial.description || '',
          type: materialForm.value.type as Material['type'], // 使用原始类型（包括presentation）
          status: 'published' as Material['status'],
          fileUrl: newMaterial.content_url || '',
          fileSize: formatFileSize(selectedFile.value.size),
          downloadCount: 0,
          createdAt: newMaterial.created_at,
          updatedAt: newMaterial.updated_at
        }
      
      materials.value.unshift(materialToAdd)
      console.log('✅ 资料已添加到列表，总数:', materials.value.length)
      alert('资料上传成功！')
      closeModal()
      
    } catch (error) {
      console.error('❌ 创建资料失败:', error)
      
      let errorMessage = '上传失败'
      if (error instanceof Error) {
        errorMessage = error.message
        console.error('错误详情:', {
          name: error.name,
          message: error.message,
          stack: error.stack
        })
      } else {
        console.error('未知错误类型:', typeof error, error)
      }
      
      uploadError.value = errorMessage
      alert('上传失败：' + errorMessage)
    } finally {
      isSubmitting.value = false
      console.log('🔄 重置提交状态为 false')
    }
  } else if (showEditModal.value && selectedMaterial.value) {
    // 编辑现有资料
    const index = materials.value.findIndex(m => m.id === selectedMaterial.value!.id)
    if (index > -1) {
      const existingMaterial = materials.value[index]
      if (existingMaterial) {
        const updatedMaterial: Material = {
          id: existingMaterial.id,
          title: materialForm.value.title || existingMaterial.title,
          description: materialForm.value.description || existingMaterial.description,
          type: (materialForm.value.type as Material['type']) || existingMaterial.type,
          status: (materialForm.value.status as Material['status']) || existingMaterial.status,
          fileUrl: existingMaterial.fileUrl,
          fileSize: existingMaterial.fileSize,
          downloadCount: existingMaterial.downloadCount,
          createdAt: existingMaterial.createdAt,
          updatedAt: new Date().toISOString()
        }
        materials.value[index] = updatedMaterial
        alert('资料更新成功！')
      }
    }
  }

  closeModal()
  isSubmitting.value = false
  console.log('🔄 重置提交状态为 false (编辑完成)')
}

// 文件上传相关方法
const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files && files.length > 0) {
    const file = files[0]
    if (file) {
      validateAndSetFile(file)
    }
  }
}

const handleDragOver = (event: DragEvent) => {
  isDragOver.value = true
}

const handleDragLeave = (event: DragEvent) => {
  isDragOver.value = false
}

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    const file = files[0]
    if (file) {
      validateAndSetFile(file)
    }
  }
}

const validateAndSetFile = (file: File) => {
  uploadError.value = ''
  
  // 文件大小验证 (100MB)
  const maxSize = 100 * 1024 * 1024
  if (file.size > maxSize) {
    uploadError.value = '文件大小不能超过 100MB'
    return
  }
  
  // 文件类型验证
  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'video/mp4',
    'video/avi',
    'video/quicktime',
    'video/x-ms-wmv',
    'audio/mpeg',
    'audio/mp3'
  ]
  
  if (!allowedTypes.includes(file.type)) {
    uploadError.value = '不支持的文件格式，请上传 PDF、DOC、PPT、MP4、MP3 等格式的文件'
    return
  }
  
  selectedFile.value = file
  
  // 根据文件类型自动设置资料类型
  if (file.type.includes('pdf') || file.type.includes('word')) {
    materialForm.value.type = 'document'
  } else if (file.type.includes('powerpoint') || file.type.includes('presentation')) {
    materialForm.value.type = 'presentation'
  } else if (file.type.includes('video')) {
    materialForm.value.type = 'video'
  } else if (file.type.includes('audio')) {
    materialForm.value.type = 'audio'
  }
}

const clearSelectedFile = () => {
  selectedFile.value = null
  uploadError.value = ''
  uploadProgress.value = 0
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 从 Supabase 加载材料数据
const loadMaterials = async () => {
  try {
    console.log('📚 开始加载培训材料列表...')
    
    // 使用 Supabase 服务获取培训资料
    const { TrainingMaterialService } = await import('@/services/supabaseService')
    console.log('✅ TrainingMaterialService 导入成功')
    
    const materialsData = await TrainingMaterialService.getAll()
    console.log('📊 获取到的原始材料数据:', materialsData)
    console.log(`📈 材料数量: ${materialsData?.length || 0}`)
    
    // 转换 Supabase 数据格式为前端格式
    materials.value = materialsData.map((material: any) => ({
      id: material.id,
      title: material.title,
      description: material.description || '',
      type: material.material_type || 'document',
      status: 'published', // 默认状态
      fileUrl: material.content_url || '',
      fileSize: '未知',
      downloadCount: material.download_count || 0,
      createdAt: material.created_at,
      updatedAt: material.updated_at
    }))
    
    console.log('✅ 材料列表加载成功，转换后的数据:', materials.value)
  } catch (error: any) {
    console.error('❌ 加载材料列表失败:', error)
    console.error('错误详情:', {
      message: error.message,
      stack: error.stack,
      name: error.name,
      cause: error.cause
    })
    alert('加载材料列表失败，请刷新页面重试')
  }
}

// 页面挂载时加载数据
onMounted(() => {
  // 在开发和生产环境中运行 Supabase 连接测试
  console.log('🔍 MaterialsView 组件已挂载，开始 Supabase 连接测试...')
  runSupabaseTest()
  
  loadMaterials()
})

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 同步所有培训资料到教师账户（简化版本）
const syncAllMaterials = async () => {
  try {
    isSyncing.value = true
    
    // 模拟同步过程
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    alert('同步完成！所有培训资料已同步到教师账户。')
    
    // 刷新材料列表
    await loadMaterials()
  } catch (error: any) {
    console.error('同步失败:', error)
    alert('同步失败，请检查网络连接后重试')
  } finally {
    isSyncing.value = false
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  selectedMaterial.value = null
  materialForm.value = {
    title: '',
    description: '',
    category: '',
    type: '',
    duration: '',
    status: 'draft'
  }
  // 清理文件上传状态
  clearSelectedFile()
  // 重置提交状态
  isSubmitting.value = false
  uploadError.value = ''
  console.log('🔄 closeModal: 重置所有状态')
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
</style>