import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { supabase, isSupabaseConfigured, type User, USER_ROLES } from '@/lib/supabase'
import type { AuthError, Session } from '@supabase/supabase-js'
import { parseError, showUserFriendlyError, logError, isNetworkError } from '@/utils/errorHandler'
import { useLocalAuthStore } from './localAuth'

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
  const session = ref<Session | null>(null)
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // 检查是否为本地开发模式
  const isLocalMode = !isSupabaseConfigured || import.meta.env.VITE_LOCAL_DEV_MODE === 'true'
  
  // 本地认证存储实例
  const localAuth = isLocalMode ? useLocalAuthStore() : null

  const isAuthenticated = computed(() => !!session.value && !!user.value)
  const isTeacher = computed(() => user.value?.role === USER_ROLES.TEACHER)
  const isManager = computed(() => user.value?.role === USER_ROLES.MANAGER)

  // 添加初始化状态缓存
  const isInitialized = ref(false)
  const initializationPromise = ref<Promise<void> | null>(null)

  // 初始化认证状态
  const initializeAuth = async (retryCount = 0) => {
    // 如果已经初始化过，直接返回
    if (isInitialized.value) {
      return Promise.resolve()
    }
    
    // 如果正在初始化，返回现有的Promise
    if (initializationPromise.value) {
      return initializationPromise.value
    }
    
    // 创建新的初始化Promise
    initializationPromise.value = performInitialization(retryCount)
    
    try {
      await initializationPromise.value
      isInitialized.value = true
    } catch (error) {
      // 初始化失败，清除Promise以允许重试
      initializationPromise.value = null
      throw error
    }
    
    return initializationPromise.value
  }

  const performInitialization = async (retryCount = 0) => {
    try {
      loading.value = true
      error.value = null
      
      // 如果是本地模式，使用本地认证
      if (isLocalMode && localAuth) {
        console.log('Running in local development mode')
        await localAuth.initializeAuth()
        
        // 同步本地认证状态到主存储
        if (localAuth.isAuthenticated) {
          const localUser = localAuth.user
          const localSession = localAuth.session
          
          if (localUser && localSession) {
            user.value = {
               id: localUser.id,
               email: localUser.email,
               full_name: localUser.full_name,
               role: localUser.role as typeof USER_ROLES[keyof typeof USER_ROLES],
               is_active: localUser.is_active,
               created_at: localUser.created_at,
               updated_at: localUser.created_at
             }
            
            session.value = {
              access_token: localSession.access_token,
              refresh_token: '',
              expires_in: 86400,
              expires_at: localSession.expires_at,
              token_type: 'bearer',
              user: {
                id: localUser.id,
                email: localUser.email,
                aud: 'authenticated',
                role: 'authenticated',
                created_at: localUser.created_at,
                updated_at: localUser.created_at,
                app_metadata: {},
                user_metadata: {}
              }
            } as Session
          }
        }
        
        loading.value = false
        return Promise.resolve()
      }
      
      // 检查是否有有效的 Supabase 配置
      if (!isSupabaseConfigured || !supabase) {
        console.warn('Supabase not configured, running in local mode')
        loading.value = false
        return Promise.resolve()
      }
      
      // 获取当前会话（减少超时时间）
      const sessionPromise = supabase.auth.getSession()
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Session fetch timeout')), 5000) // 减少到5秒
      )
      
      try {
        const { data: { session: currentSession }, error: sessionError } = await Promise.race([
          sessionPromise,
          timeoutPromise
        ]) as any
        
        if (sessionError) {
          console.warn('Session fetch error:', sessionError)
          throw sessionError
        }
        
        if (currentSession) {
          session.value = currentSession
          // 同步获取用户资料，确保角色信息立即可用
          try {
            await fetchUserProfile(currentSession.user.id)
          } catch (profileError) {
            console.warn('Failed to fetch user profile:', profileError)
            // 如果获取失败，设置默认用户信息避免页面闪烁
            user.value = {
              id: currentSession.user.id,
              email: currentSession.user.email || '',
              full_name: currentSession.user.user_metadata?.full_name || currentSession.user.email || '',
              role: USER_ROLES.TEACHER, // 默认角色
              is_active: true,
              created_at: currentSession.user.created_at || new Date().toISOString(),
              updated_at: currentSession.user.updated_at || new Date().toISOString()
            }
          }
        }

        // 监听认证状态变化（只设置一次）
        if (!isInitialized.value) {
          supabase.auth.onAuthStateChange(async (event, newSession) => {
            session.value = newSession
            
            if (newSession?.user) {
              // 异步获取用户资料
              fetchUserProfile(newSession.user.id).catch(profileError => {
                console.warn('Failed to fetch user profile on auth change:', profileError)
              })
            } else {
              user.value = null
            }
          })
        }
        
      } catch (timeoutError) {
        console.warn('Auth initialization timeout:', timeoutError)
        
        // 简化重试机制：最多重试1次
        if (retryCount < 1) {
          console.log(`认证初始化重试 ${retryCount + 1}/1`)
          await new Promise(resolve => setTimeout(resolve, 1000))
          return performInitialization(retryCount + 1)
        } else {
          console.warn('Auth initialization failed after retry, continuing without auth')
          // 不抛出错误，允许应用继续运行
        }
      }
    } catch (err: any) {
      logError(err, 'Auth initialization')
      const userFriendlyMessage = showUserFriendlyError(err)
      error.value = userFriendlyMessage
      
      // 简化错误处理，不进行额外重试
      console.warn('Auth initialization failed:', userFriendlyMessage)
    } finally {
      loading.value = false
    }
  }

  // 用户资料缓存
  const userProfileCache = ref<Map<string, { data: User, timestamp: number }>>(new Map())
  const CACHE_DURATION = 5 * 60 * 1000 // 5分钟缓存

  // 获取用户资料
  const fetchUserProfile = async (userId: string) => {
    if (!supabase) {
      console.warn('Supabase not configured, skipping user profile fetch')
      return null
    }
    
    // 检查缓存
    const cached = userProfileCache.value.get(userId)
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
      user.value = cached.data
      return cached.data
    }
    
    try {
      // 减少超时时间，提高响应速度
      const profilePromise = supabase
        .from('users')
        .select('*')
        .eq('id', userId)
        .single()
      
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('用户资料获取超时')), 2000) // 减少到2秒
      )
      
      const { data, error: fetchError } = await Promise.race([profilePromise, timeoutPromise]) as any

      if (fetchError) {
        if (fetchError.code === 'PGRST116') {
          // 用户资料不存在，创建默认资料
          console.log('User profile not found, creating default profile')
          const defaultProfile = {
            id: userId,
            email: session.value?.user?.email || '',
            full_name: session.value?.user?.user_metadata?.full_name || session.value?.user?.email || '',
            role: USER_ROLES.TEACHER,
            is_active: true,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          }
          
          // 缓存默认资料
          userProfileCache.value.set(userId, {
            data: defaultProfile,
            timestamp: Date.now()
          })
          
          user.value = defaultProfile
          return defaultProfile
        }
        throw fetchError
      }
      
      // 更新缓存
      userProfileCache.value.set(userId, {
        data: data,
        timestamp: Date.now()
      })
      
      user.value = data
      return data
    } catch (err: any) {
      console.error('Error fetching user profile:', err)
      
      // 设置默认用户信息
      const defaultUser = {
        id: userId,
        email: session.value?.user?.email || '',
        full_name: session.value?.user?.user_metadata?.full_name || session.value?.user?.email || '',
        role: USER_ROLES.TEACHER,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
      
      // 缓存默认用户信息
      userProfileCache.value.set(userId, {
        data: defaultUser,
        timestamp: Date.now()
      })
      
      user.value = defaultUser
      return defaultUser
    }
  }

  // 用户注册
  const register = async (registerData: RegisterData) => {
    // 如果是本地模式，使用本地认证
    if (isLocalMode && localAuth) {
      try {
        loading.value = true
        error.value = null
        
        const result = await localAuth.register(registerData)
        
        // 同步到主存储
        await initializeAuth()
        
        return result
      } catch (err: any) {
        error.value = localAuth.error || '注册失败'
        throw err
      } finally {
        loading.value = false
      }
    }
    
    if (!supabase) {
      error.value = 'Supabase not configured'
      return { user: null, error: 'Authentication service not available' }
    }
    
    try {
      loading.value = true
      error.value = null

      // 1. 创建认证用户（禁用邮件验证）- 添加超时保护
      const signUpPromise = supabase.auth.signUp({
        email: registerData.email,
        password: registerData.password,
        options: {
          emailRedirectTo: undefined // 禁用邮件验证
        }
      })
      
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Registration timeout')), 20000) // 增加到20秒超时
      )

      const { data: authData, error: authError } = await Promise.race([
        signUpPromise,
        timeoutPromise
      ]) as any

      if (authError) throw authError

      // 2. 创建用户资料
      if (authData.user) {
        try {
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
        } catch (profileError) {
          console.warn('Failed to create user profile, but auth user created:', profileError)
          // 不阻塞注册流程，用户可以稍后完善资料
        }
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
    // 如果是本地模式，使用本地认证
    if (isLocalMode && localAuth) {
      try {
        loading.value = true
        error.value = null
        
        const result = await localAuth.login(credentials)
        
        // 同步到主存储
        await initializeAuth()
        
        return result
      } catch (err: any) {
        error.value = localAuth.error || '登录失败'
        throw err
      } finally {
        loading.value = false
      }
    }
    
    if (!supabase) {
      error.value = 'Supabase not configured'
      return { user: null, session: null, error: 'Authentication service not available' }
    }
    
    try {
      loading.value = true
      error.value = null

      // 减少超时时间
      const loginPromise = supabase.auth.signInWithPassword({
        email: credentials.email,
        password: credentials.password
      })
      
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Login timeout')), 8000) // 减少到8秒超时
      )

      const { data, error: loginError } = await Promise.race([
        loginPromise,
        timeoutPromise
      ]) as any

      if (loginError) throw loginError

      // 设置会话并异步获取用户资料
      if (data.user) {
        session.value = data.session

        // 异步获取用户资料，不阻塞登录流程
        fetchUserProfile(data.user.id).catch(profileError => {
          console.warn('Failed to fetch user profile after login:', profileError)
        })
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

      // 如果是本地模式，使用本地认证
      if (isLocalMode && localAuth) {
        await localAuth.logout()
        session.value = null
        user.value = null
        return
      }

      // 检查是否有有效的 Supabase 实例和会话
      const hasValidSession = supabase && session.value && session.value.access_token
      
      if (hasValidSession && supabase) {
        try {
          // 减少超时时间，避免长时间等待
          const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => reject(new Error('登出请求超时')), 3000) // 减少到3秒
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
          console.warn('登出请求失败（可能是网络问题），继续清除本地状态:', networkError.message)
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