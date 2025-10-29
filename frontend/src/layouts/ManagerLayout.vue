<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航栏 -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <img 
                src="/51talkACADEMY-logo.jpeg" 
                alt="51Talk Academy" 
                class="h-8 w-auto rounded-lg"
              />
              <h1 class="ml-3 text-xl font-semibold text-gray-900">AI教师培训平台 - 管理端</h1>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-700">{{ authStore.user?.full_name }}</span>
            <button
              @click="handleLogout"
              class="text-sm text-gray-500 hover:text-gray-700 transition-colors"
            >
              登出
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="flex">
      <!-- 侧边导航栏 -->
      <aside class="w-64 bg-white shadow-sm min-h-screen">
        <nav class="mt-8 px-4">
          <ul class="space-y-2">
            <li>
              <router-link
                to="/manager/dashboard"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/manager/dashboard' }"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z" />
                </svg>
                管理概览
              </router-link>
            </li>
            <li>
              <router-link
                to="/manager/teachers"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/manager/teachers' }"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                教师管理
              </router-link>
            </li>
            <li>
              <router-link
                to="/manager/lectures"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/manager/lectures' }"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                讲座评审
              </router-link>
            </li>
            <li>
              <router-link
                to="/manager/materials"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/manager/materials' }"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                培训资料
              </router-link>
            </li>
            <li>
              <router-link
                to="/manager/analytics"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/manager/analytics' }"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                数据分析
              </router-link>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- 主内容区域 -->
      <main class="flex-1 p-8">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'
import { useRouter } from 'vue-router'
import { componentCacheService } from '@/services/componentCacheService'
import { preloadService } from '@/services/preloadService'

const authStore = useSupabaseAuthStore()
const router = useRouter()

// 性能优化：缓存导航状态
const { data: navigationState, updateCache: updateNavigationCache } = 
  componentCacheService.createReactiveCache('manager:navigation', {
    activeTab: 'dashboard',
    lastVisited: Date.now()
  })

// 计算当前活跃的导航项
const activeRoute = computed(() => router.currentRoute.value.name)

// 优化的登出处理
const isLoggingOut = ref(false)
const handleLogout = async () => {
  if (isLoggingOut.value) return // 防止重复点击
  
  isLoggingOut.value = true
  try {
    await authStore.logout()
    // 清除缓存
    componentCacheService.clear()
    router.push('/login')
  } catch (error) {
    console.error('登出失败:', error)
    // 即使登出失败，也跳转到登录页面
    router.push('/login')
  } finally {
    isLoggingOut.value = false
  }
}

// 组件挂载时的性能优化
onMounted(async () => {
  try {
    // 预热缓存
    await componentCacheService.warmupCache('manager')
    
    // 预加载管理员端组件
    preloadService.preloadManagerComponents()
    
    // 更新导航状态
    updateNavigationCache({
      activeTab: String(activeRoute.value) || 'dashboard',
      lastVisited: Date.now()
    })
  } catch (error) {
    console.warn('Layout optimization failed:', error)
  }
})
</script>

<style scoped>
.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  color: rgb(55 65 81);
  transition: background-color 0.15s ease-in-out;
}

.nav-link:hover {
  background-color: rgb(243 244 246);
}

.nav-link-active {
  background-color: rgb(239 246 255);
  color: rgb(29 78 216);
}
</style>