import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useSupabaseAuthStore } from './stores/supabaseAuth'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 初始化 Supabase 认证
const authStore = useSupabaseAuthStore()
authStore.initializeAuth()

app.mount('#app')
