import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { USER_ROLES } from '@/lib/supabase'

export interface LocalUser {
  id: string
  email: string
  full_name: string
  role: string
  is_active: boolean
  created_at: string
}

export interface LocalSession {
  access_token: string
  user: LocalUser
  expires_at: number
}

export interface LocalLoginCredentials {
  email: string
  password: string
}

export interface LocalRegisterData {
  email: string
  password: string
  full_name: string
  role: string
}

export const useLocalAuthStore = defineStore('localAuth', () => {
  const session = ref<LocalSession | null>(null)
  const user = ref<LocalUser | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const isAuthenticated = computed(() => !!session.value && !!user.value)
  const isTeacher = computed(() => user.value?.role === USER_ROLES.TEACHER)
  const isManager = computed(() => user.value?.role === USER_ROLES.MANAGER)

  // 本地存储键
  const LOCAL_STORAGE_KEY = 'local_auth_session'

  // 生成简单的ID
  const generateId = () => Math.random().toString(36).substr(2, 9)

  // 生成访问令牌
  const generateAccessToken = () => `local_token_${Date.now()}_${generateId()}`

  // 保存会话到本地存储
  const saveSession = (sessionData: LocalSession) => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(sessionData))
  }

  // 从本地存储加载会话
  const loadSession = (): LocalSession | null => {
    try {
      const stored = localStorage.getItem(LOCAL_STORAGE_KEY)
      if (!stored) return null
      
      const sessionData = JSON.parse(stored) as LocalSession
      
      // 检查是否过期
      if (sessionData.expires_at < Date.now()) {
        localStorage.removeItem(LOCAL_STORAGE_KEY)
        return null
      }
      
      return sessionData
    } catch (error) {
      console.warn('Failed to load local session:', error)
      localStorage.removeItem(LOCAL_STORAGE_KEY)
      return null
    }
  }

  // 清除会话
  const clearSession = () => {
    localStorage.removeItem(LOCAL_STORAGE_KEY)
    session.value = null
    user.value = null
  }

  // 初始化认证状态
  const initializeAuth = async () => {
    try {
      loading.value = true
      error.value = null

      const storedSession = loadSession()
      if (storedSession) {
        session.value = storedSession
        user.value = storedSession.user
      }
    } catch (err: any) {
      console.warn('Failed to initialize local auth:', err)
      error.value = '认证初始化失败'
    } finally {
      loading.value = false
    }
  }

  // 用户登录
  const login = async (credentials: LocalLoginCredentials) => {
    try {
      loading.value = true
      error.value = null

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 500))

      // 简单的演示用户验证
      const demoUsers = [
        {
          email: 'teacher@demo.com',
          password: '123456',
          full_name: '演示教师',
          role: USER_ROLES.TEACHER
        },
        {
          email: 'manager@demo.com',
          password: '123456',
          full_name: '演示管理员',
          role: USER_ROLES.MANAGER
        },
        // 添加更多管理员账号支持
        {
          email: 'admin@demo.com',
          password: '123456',
          full_name: '演示管理员',
          role: USER_ROLES.MANAGER
        },
        {
          email: 'administrator@demo.com',
          password: '123456',
          full_name: '演示管理员',
          role: USER_ROLES.MANAGER
        }
      ]

      const foundUser = demoUsers.find(u => 
        u.email === credentials.email && u.password === credentials.password
      )

      if (!foundUser) {
        // 特定管理员邮箱列表
        const adminEmails = [
          'zhangjing32@51talk.com',
          'admin@51talk.com',
          'manager@51talk.com'
        ]
        
        // 检查是否是管理员邮箱
        const isSpecificAdminEmail = adminEmails.includes(credentials.email.toLowerCase())
        const isAdminKeywordEmail = credentials.email.toLowerCase().includes('admin') || 
                                  credentials.email.toLowerCase().includes('manager') || 
                                  credentials.email.toLowerCase().includes('管理')
        
        const role = (isSpecificAdminEmail || isAdminKeywordEmail) ? USER_ROLES.MANAGER : USER_ROLES.TEACHER
        
        // 允许任何邮箱登录，根据邮箱特征分配角色
        const newUser: LocalUser = {
          id: generateId(),
          email: credentials.email,
          full_name: credentials.email.split('@')[0] || 'User',
          role: role,
          is_active: true,
          created_at: new Date().toISOString()
        }

        const newSession: LocalSession = {
          access_token: generateAccessToken(),
          user: newUser,
          expires_at: Date.now() + (24 * 60 * 60 * 1000) // 24小时
        }

        session.value = newSession
        user.value = newUser
        saveSession(newSession)

        console.log('本地登录成功（自动分配角色）:', { email: credentials.email, role: role })
        return { user: newUser, session: newSession }
      }

      // 使用演示用户
      const demoUser: LocalUser = {
        id: generateId(),
        email: foundUser.email,
        full_name: foundUser.full_name,
        role: foundUser.role,
        is_active: true,
        created_at: new Date().toISOString()
      }

      const newSession: LocalSession = {
        access_token: generateAccessToken(),
        user: demoUser,
        expires_at: Date.now() + (24 * 60 * 60 * 1000) // 24小时
      }

      session.value = newSession
      user.value = demoUser
      saveSession(newSession)

      return { user: demoUser, session: newSession }
    } catch (err: any) {
      error.value = '登录失败，请重试'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 用户注册
  const register = async (registerData: LocalRegisterData) => {
    try {
      loading.value = true
      error.value = null

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 800))

      const newUser: LocalUser = {
        id: generateId(),
        email: registerData.email,
        full_name: registerData.full_name,
        role: registerData.role,
        is_active: true,
        created_at: new Date().toISOString()
      }

      const newSession: LocalSession = {
        access_token: generateAccessToken(),
        user: newUser,
        expires_at: Date.now() + (24 * 60 * 60 * 1000) // 24小时
      }

      session.value = newSession
      user.value = newUser
      saveSession(newSession)

      return { user: newUser, session: newSession }
    } catch (err: any) {
      error.value = '注册失败，请重试'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 用户登出
  const logout = async () => {
    try {
      loading.value = true
      clearSession()
    } catch (err: any) {
      console.warn('Logout error:', err)
    } finally {
      loading.value = false
    }
  }

  // 重置密码（演示功能）
  const resetPassword = async (email: string) => {
    try {
      loading.value = true
      error.value = null

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 1000))

      console.log('Password reset requested for:', email)
      return { success: true, message: '密码重置邮件已发送（演示模式）' }
    } catch (err: any) {
      error.value = '密码重置失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    session: computed(() => session.value),
    user: computed(() => user.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    
    // 计算属性
    isAuthenticated,
    isTeacher,
    isManager,
    
    // 方法
    initializeAuth,
    login,
    register,
    logout,
    resetPassword
  }
})