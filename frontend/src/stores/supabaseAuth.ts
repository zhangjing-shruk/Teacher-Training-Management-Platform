import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { supabase, isSupabaseConfigured, type User, USER_ROLES } from '@/lib/supabase'
import type { AuthError, Session } from '@supabase/supabase-js'
import { parseError, showUserFriendlyError, logError, isNetworkError } from '@/utils/errorHandler'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  full_name: string
  role: typeof USER_ROLES[keyof typeof USER_ROLES]
}

export interface ResetPasswordData {
  email: string
  newPassword: string
}

export const useSupabaseAuthStore = defineStore('supabaseAuth', () => {
  const user = ref<User | null>(null)
  const session = ref<Session | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!session.value && !!user.value)
  const isTeacher = computed(() => user.value?.role === USER_ROLES.TEACHER)
  const isManager = computed(() => user.value?.role === USER_ROLES.MANAGER)

  // 初始化认证状态
  const initializeAuth = async (retryCount = 0) => {
    try {
      loading.value = true
      error.value = null
      
      // 检查是否有有效的 Supabase 配置
      if (!isSupabaseConfigured || !supabase) {
        console.warn('Supabase not configured, skipping auth initialization')
        loading.value = false
        return Promise.resolve()
      }
      
      // 获取当前会话（添加超时保护和重试机制）
      const sessionPromise = supabase.auth.getSession()
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Session fetch timeout')), 10000)
      )
      
      const { data: { session: currentSession } } = await Promise.race([
        sessionPromise,
        timeoutPromise
      ]) as any
      
      if (currentSession) {
        session.value = currentSession
        try {
          await fetchUserProfile(currentSession.user.id)
        } catch (profileError) {
          console.warn('Failed to fetch user profile:', profileError)
          // 继续执行，不阻塞认证流程
        }
      }

      // 监听认证状态变化
      supabase.auth.onAuthStateChange(async (event, newSession) => {
        session.value = newSession
        
        if (newSession?.user) {
          try {
            await fetchUserProfile(newSession.user.id)
          } catch (profileError) {
            console.warn('Failed to fetch user profile on auth change:', profileError)
          }
        } else {
          user.value = null
        }
      })
    } catch (err: any) {
      logError(err, 'Auth initialization')
      const userFriendlyMessage = showUserFriendlyError(err)
      error.value = userFriendlyMessage
      
      // 如果是网络错误且重试次数少于2次，则重试
      if (isNetworkError(err) && retryCount < 2) {
        console.log(`认证初始化重试 ${retryCount + 1}/2`)
        setTimeout(() => {
          initializeAuth(retryCount + 1)
        }, 2000) // 2秒后重试
        return
      }
      
      // 不要抛出错误，让应用继续运行
    } finally {
      loading.value = false
    }
  }

  // 获取用户资料
  const fetchUserProfile = async (userId: string) => {
    if (!supabase) {
      console.warn('Supabase not configured, skipping user profile fetch')
      return null
    }
    
    try {
      const { data, error: fetchError } = await supabase
        .from('users')
        .select('*')
        .eq('id', userId)
        .single()

      if (fetchError) {
        if (fetchError.code === 'PGRST116') {
          // 用户资料不存在，可能需要创建
          console.warn('User profile not found, user may need to complete registration')
          return null
        }
        throw fetchError
      }
      user.value = data
      return data
    } catch (err: any) {
      console.error('Error fetching user profile:', err)
      error.value = err.message
      return null
    }
  }

  // 用户注册
  const register = async (registerData: RegisterData) => {
    if (!supabase) {
      error.value = 'Supabase not configured'
      return { user: null, error: 'Authentication service not available' }
    }
    
    try {
      loading.value = true
      error.value = null

      // 1. 创建认证用户（禁用邮件验证）
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email: registerData.email,
        password: registerData.password,
        options: {
          emailRedirectTo: undefined // 禁用邮件验证
        }
      })

      if (authError) throw authError

      // 2. 创建用户资料
      if (authData.user) {
        const { data: profileData, error: profileError } = await supabase
          .from('users')
          .insert({
            id: authData.user.id,
            email: registerData.email,
            full_name: registerData.full_name,
            role: registerData.role,
            is_active: true
          })
          .select()
          .single()

        if (profileError) {
          console.error('Profile creation error:', profileError)
          throw profileError
        }
        
        // 设置用户信息
        user.value = profileData
      }

      return authData
    } catch (err: any) {
      logError(err, 'User registration')
      const userFriendlyMessage = showUserFriendlyError(err)
      error.value = userFriendlyMessage
      throw err
    } finally {
      loading.value = false
    }
  }

  // 用户登录
  const login = async (credentials: LoginCredentials) => {
    if (!supabase) {
      error.value = 'Supabase not configured'
      return { user: null, session: null, error: 'Authentication service not available' }
    }
    
    try {
      loading.value = true
      error.value = null

      const { data, error: loginError } = await supabase.auth.signInWithPassword({
        email: credentials.email,
        password: credentials.password
      })

      if (loginError) throw loginError

      // 立即获取用户资料
      if (data.user) {
        session.value = data.session
        await fetchUserProfile(data.user.id)
      }

      return data
    } catch (err: any) {
      logError(err, 'User login')
      const userFriendlyMessage = showUserFriendlyError(err)
      error.value = userFriendlyMessage
      throw err
    } finally {
      loading.value = false
    }
  }

  // 用户登出
  const logout = async () => {
    try {
      loading.value = true
      error.value = null

      // 检查是否有有效的 Supabase 实例和会话
      const hasValidSession = supabase && session.value && session.value.access_token
      
      if (hasValidSession && supabase) {
        try {
          // 添加超时控制，避免长时间等待
          const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => reject(new Error('登出请求超时')), 10000)
          })
          
          const logoutPromise = supabase.auth.signOut({ scope: 'local' })
          
          const { error: logoutError } = await Promise.race([logoutPromise, timeoutPromise]) as any
          
          if (logoutError) {
            console.warn('Supabase 登出失败，但将继续清除本地状态:', logoutError.message)
          } else {
            console.log('Supabase 登出成功')
          }
        } catch (networkError: any) {
          // 捕获所有网络相关错误，包括 ERR_ABORTED
          logError(networkError, 'Logout request')
          const userMessage = showUserFriendlyError(networkError)
          console.warn('登出请求失败（可能是网络问题），继续清除本地状态:', userMessage)
        }
      } else {
        console.log('没有有效会话或 Supabase 实例，直接清除本地状态')
      }

      // 无论如何都要清除本地状态
      user.value = null
      session.value = null
      
      // 清除本地存储中的会话信息
      try {
        localStorage.removeItem('supabase.auth.token')
        sessionStorage.removeItem('supabase.auth.token')
        
        // 清除所有 Supabase 相关的本地存储
        const keys = Object.keys(localStorage)
        keys.forEach(key => {
          if (key.startsWith('sb-') || key.includes('supabase')) {
            localStorage.removeItem(key)
          }
        })
        
        // 清除 sessionStorage 中的 Supabase 数据
        const sessionKeys = Object.keys(sessionStorage)
        sessionKeys.forEach(key => {
          if (key.startsWith('sb-') || key.includes('supabase')) {
            sessionStorage.removeItem(key)
          }
        })
        
        console.log('本地状态清除完成')
      } catch (storageError: any) {
        console.warn('清除本地存储时出现错误:', storageError.message)
      }
      
    } catch (err: any) {
      logError(err, 'Logout process')
      const userFriendlyMessage = showUserFriendlyError(err)
      error.value = userFriendlyMessage
      // 即使出错也要清除本地状态
      user.value = null
      session.value = null
      console.error('登出过程中出现错误:', userFriendlyMessage)
    } finally {
      loading.value = false
    }
  }

  // 更新用户资料
  const updateProfile = async (updates: Partial<User>) => {
    if (!supabase) {
      error.value = 'Supabase not configured'
      throw new Error('Authentication service not available')
    }
    
    try {
      loading.value = true
      error.value = null

      if (!user.value) throw new Error('用户未登录')

      const { data, error: updateError } = await supabase
        .from('users')
        .update(updates)
        .eq('id', user.value.id)
        .select()
        .single()

      if (updateError) throw updateError

      user.value = data
      return data
    } catch (err: any) {
      error.value = err.message || '更新资料失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 重置密码
  const resetPassword = async (resetData: ResetPasswordData) => {
    try {
      loading.value = true
      error.value = null

      // 调用后端API重置密码
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(resetData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || '重置密码失败')
      }

      const result = await response.json()
      return result
    } catch (err: any) {
      error.value = err.message || '重置密码失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新密码
  const updatePassword = async (newPassword: string) => {
    if (!supabase) {
      error.value = 'Supabase not configured'
      throw new Error('Authentication service not available')
    }
    
    try {
      loading.value = true
      error.value = null

      const { error: updateError } = await supabase.auth.updateUser({
        password: newPassword
      })

      if (updateError) throw updateError
    } catch (err: any) {
      error.value = err.message || '更新密码失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    user,
    session,
    loading,
    error,
    
    // 计算属性
    isAuthenticated,
    isTeacher,
    isManager,
    
    // 方法
    initializeAuth,
    fetchUserProfile,
    register,
    login,
    logout,
    updateProfile,
    resetPassword,
    updatePassword
  }
})