<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航栏 -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo和标题 -->
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <img 
                src="/51talkACADEMY-logo.jpeg" 
                alt="51Talk Academy" 
                class="h-8 w-auto rounded-lg"
              />
              <span class="ml-3 text-xl font-semibold text-gray-900">AI 教师培训</span>
            </div>
          </div>

          <!-- 用户菜单 -->
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-700">欢迎，{{ authStore.user?.full_name }}</span>
            <button
              @click="handleLogout"
              class="text-gray-500 hover:text-gray-700 transition-colors duration-200"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 侧边导航 -->
    <div class="flex">
      <aside class="w-64 bg-white shadow-sm min-h-screen">
        <nav class="mt-8 px-4">
          <ul class="space-y-2">
            <li>
              <router-link
                to="/teacher"
                class="nav-link"
                :class="{ 'nav-link-active': $route.name === 'teacher-dashboard' }"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z" />
                </svg>
                培训概览
              </router-link>
            </li>
            <li>
              <router-link
                to="/teacher/materials"
                class="nav-link"
                :class="{ 'nav-link-active': $route.name === 'training-materials' }"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                学习资料
              </router-link>
            </li>
            <li>
              <router-link
                to="/teacher/practice"
                class="nav-link"
                :class="{ 'nav-link-active': $route.name === 'practice' }"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h8m-5-4v4m2-4v4" />
                </svg>
                试讲练习
              </router-link>
            </li>
            <li>
              <router-link
                to="/teacher/feedback"
                class="nav-link"
                :class="{ 'nav-link-active': $route.name === 'feedback' }"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                反馈报告
              </router-link>
            </li>
            <li>
              <router-link
                to="/teacher/sop"
                class="nav-link"
                :class="{ 'nav-link-active': $route.name === 'sop' }"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                SOP 流程
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
import { useRouter } from 'vue-router'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'
import { componentCacheService } from '@/services/componentCacheService'
import { preloadService } from '@/services/preloadService'

const router = useRouter()
const authStore = useSupabaseAuthStore()

// 性能优化：缓存导航状态
const { data: navigationState, updateCache: updateNavigationCache } = 
  componentCacheService.createReactiveCache('teacher:navigation', {
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
    await componentCacheService.warmupCache('teacher')
    
    // 预加载教师端组件
    preloadService.preloadTeacherComponents()
    
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
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgb(75 85 99);
  border-radius: 0.5rem;
  transition: all 0.2s ease-in-out;
}

.nav-link:hover {
  background-color: rgb(243 244 246);
  color: rgb(17 24 39);
}

.nav-link svg {
  margin-right: 0.75rem;
}

.nav-link-active {
  background-color: rgb(239 246 255);
  color: rgb(29 78 216);
  border-right: 2px solid rgb(37 99 235);
}
</style>