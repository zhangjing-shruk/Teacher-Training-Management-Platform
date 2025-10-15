<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="max-w-4xl mx-auto px-4">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">系统连接测试</h1>
        
        <!-- 前端状态 -->
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-3">前端状态</h2>
          <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <div class="flex items-center">
              <div class="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span class="text-green-800">前端应用运行正常</span>
            </div>
            <p class="text-green-700 mt-2">Vue 3 + TypeScript + Tailwind CSS</p>
          </div>
        </div>

        <!-- 后端连接测试 -->
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-3">后端连接测试</h2>
          <div class="space-y-3">
            <button 
              @click="testBackendConnection"
              :disabled="loading"
              class="bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white px-4 py-2 rounded-lg transition-colors"
            >
              {{ loading ? '测试中...' : '测试后端连接' }}
            </button>
            
            <div v-if="backendStatus" class="mt-3">
              <div 
                :class="[
                  'border rounded-lg p-4',
                  backendStatus.success 
                    ? 'bg-green-50 border-green-200' 
                    : 'bg-red-50 border-red-200'
                ]"
              >
                <div class="flex items-center">
                  <div 
                    :class="[
                      'w-3 h-3 rounded-full mr-3',
                      backendStatus.success ? 'bg-green-500' : 'bg-red-500'
                    ]"
                  ></div>
                  <span 
                    :class="[
                      backendStatus.success ? 'text-green-800' : 'text-red-800'
                    ]"
                  >
                    {{ backendStatus.message }}
                  </span>
                </div>
                <div v-if="backendStatus.data" class="mt-2">
                  <pre class="text-sm text-gray-600">{{ JSON.stringify(backendStatus.data, null, 2) }}</pre>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 数据库测试 -->
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-3">数据库测试</h2>
          <div class="space-y-3">
            <button 
              @click="testDatabase"
              :disabled="loading"
              class="bg-purple-500 hover:bg-purple-600 disabled:bg-purple-300 text-white px-4 py-2 rounded-lg transition-colors"
            >
              {{ loading ? '测试中...' : '测试数据库连接' }}
            </button>
            
            <div v-if="dbStatus" class="mt-3">
              <div 
                :class="[
                  'border rounded-lg p-4',
                  dbStatus.success 
                    ? 'bg-green-50 border-green-200' 
                    : 'bg-red-50 border-red-200'
                ]"
              >
                <div class="flex items-center">
                  <div 
                    :class="[
                      'w-3 h-3 rounded-full mr-3',
                      dbStatus.success ? 'bg-green-500' : 'bg-red-500'
                    ]"
                  ></div>
                  <span 
                    :class="[
                      dbStatus.success ? 'text-green-800' : 'text-red-800'
                    ]"
                  >
                    {{ dbStatus.message }}
                  </span>
                </div>
                <div v-if="dbStatus.data" class="mt-2">
                  <pre class="text-sm text-gray-600">{{ JSON.stringify(dbStatus.data, null, 2) }}</pre>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 系统信息 -->
        <div>
          <h2 class="text-xl font-semibold text-gray-800 mb-3">系统信息</h2>
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <span class="font-medium text-gray-700">前端地址:</span>
                <span class="text-gray-600 ml-2">http://localhost:5173</span>
              </div>
              <div>
                <span class="font-medium text-gray-700">后端地址:</span>
                <span class="text-gray-600 ml-2">http://localhost:8000</span>
              </div>
              <div>
                <span class="font-medium text-gray-700">API文档:</span>
                <a href="http://localhost:8000/docs" target="_blank" class="text-blue-600 hover:text-blue-800 ml-2">
                  http://localhost:8000/docs
                </a>
              </div>
              <div>
                <span class="font-medium text-gray-700">数据库:</span>
                <span class="text-gray-600 ml-2">SQLite (app.db)</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const loading = ref(false)
const backendStatus = ref<{success: boolean, message: string, data?: any} | null>(null)
const dbStatus = ref<{success: boolean, message: string, data?: any} | null>(null)

const testBackendConnection = async () => {
  loading.value = true
  try {
    const response = await fetch('http://localhost:8000/')
    const data = await response.json()
    
    backendStatus.value = {
      success: true,
      message: '后端连接成功',
      data
    }
  } catch (error) {
    backendStatus.value = {
      success: false,
      message: `后端连接失败: ${error instanceof Error ? error.message : '未知错误'}`
    }
  } finally {
    loading.value = false
  }
}

const testDatabase = async () => {
  loading.value = true
  try {
    const response = await fetch('http://localhost:8000/health')
    const data = await response.json()
    
    dbStatus.value = {
      success: true,
      message: '数据库连接正常',
      data
    }
  } catch (error) {
    dbStatus.value = {
      success: false,
      message: `数据库连接失败: ${error instanceof Error ? error.message : '未知错误'}`
    }
  } finally {
    loading.value = false
  }
}
</script>