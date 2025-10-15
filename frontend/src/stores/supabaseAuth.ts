import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { supabase, type User, USER_ROLES } from '@/lib/supabase'
import type { AuthError, Session } from '@supabase/supabase-js'

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

export const useSupabaseAuthStore = defineStore('supabaseAuth', () => {
  const user = ref<User | null>(null)
  const session = ref<Session | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!session.value && !!user.value)
  const isTeacher = computed(() => user.value?.role === USER_ROLES.TEACHER)
  const isManager = computed(() => user.value?.role === USER_ROLES.MANAGER)

  // 初始化认证状态
  const initializeAuth = async () => {
    try {
      loading.value = true
      
      // 检查是否有有效的 Supabase 配置
      if (!import.meta.env.VITE_SUPABASE_URL || !import.meta.env.VITE_SUPABASE_ANON_KEY) {
        console.warn('Supabase not configured, skipping auth initialization')
        return
      }
      
      // 获取当前会话
      const { data: { session: currentSession } } = await supabase.auth.getSession()
      
      if (currentSession) {
        session.value = currentSession
        await fetchUserProfile(currentSession.user.id)
      }

      // 监听认证状态变化
      supabase.auth.onAuthStateChange(async (event, newSession) => {
        session.value = newSession
        
        if (newSession?.user) {
          await fetchUserProfile(newSession.user.id)
        } else {
          user.value = null
        }
      })
    } catch (err: any) {
      console.error('Auth initialization error:', err)
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  // 获取用户资料
  const fetchUserProfile = async (userId: string) => {
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
      error.value = err.message || '注册失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 用户登录
  const login = async (credentials: LoginCredentials) => {
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
      error.value = err.message || '登录失败'
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

      // 尝试从 Supabase 登出，但即使失败也要清除本地状态
      try {
        const { error: logoutError } = await supabase.auth.signOut({ scope: 'local' })
        if (logoutError) {
          console.warn('Supabase 登出失败，但将继续清除本地状态:', logoutError.message)
        }
      } catch (networkError: any) {
        console.warn('网络错误，无法连接到 Supabase，但将继续清除本地状态:', networkError.message)
      }

      // 无论如何都要清除本地状态
      user.value = null
      session.value = null
      
      // 清除本地存储中的会话信息
      localStorage.removeItem('supabase.auth.token')
      sessionStorage.removeItem('supabase.auth.token')
      
    } catch (err: any) {
      error.value = err.message || '登出失败'
      // 即使出错也要清除本地状态
      user.value = null
      session.value = null
      console.error('登出过程中出现错误:', err)
    } finally {
      loading.value = false
    }
  }

  // 更新用户资料
  const updateProfile = async (updates: Partial<User>) => {
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
  const resetPassword = async (email: string) => {
    try {
      loading.value = true
      error.value = null

      const { error: resetError } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`
      })

      if (resetError) throw resetError
    } catch (err: any) {
      error.value = err.message || '重置密码失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新密码
  const updatePassword = async (newPassword: string) => {
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
    register,
    login,
    logout,
    updateProfile,
    resetPassword,
    updatePassword
  }
})