import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useSupabaseAuthStore } from './stores/supabaseAuth'
import { performanceMonitor } from './utils/performanceTest'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 初始化 Supabase 认证
const authStore = useSupabaseAuthStore()
authStore.initializeAuth()

// 启动性能监控（仅在开发环境）
if (import.meta.env.DEV) {
  performanceMonitor.startMonitoring()
  
  // 在应用挂载后运行性能测试
  app.mount('#app')
  
  // 延迟运行完整性能测试，确保应用完全加载
  setTimeout(() => {
    performanceMonitor.runFullPerformanceTest()
  }, 3000)
} else {
  app.mount('#app')
}
