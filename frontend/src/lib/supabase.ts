import { createClient } from '@supabase/supabase-js'

// Supabase 配置
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// 检查是否有有效的 Supabase 配置
const hasValidSupabaseConfig = supabaseUrl && supabaseAnonKey && 
  supabaseUrl.startsWith('https://') && supabaseUrl.includes('.supabase.co')

if (!hasValidSupabaseConfig) {
  console.warn('Supabase not configured or invalid configuration. Running in demo mode.')
}

// 创建 Supabase 客户端（仅在有有效配置时）
export const supabase = hasValidSupabaseConfig ? createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
}) : null

// 导出配置状态
export const isSupabaseConfigured = hasValidSupabaseConfig

// 数据库表名常量
export const TABLES = {
  USERS: 'users',
  TRAINING_MATERIALS: 'training_materials',
  PRACTICE_SESSIONS: 'practice_sessions',
  FEEDBACK: 'feedback',
  LEARNING_PROGRESS: 'learning_progress'
} as const

// 用户角色枚举
export const USER_ROLES = {
  TEACHER: 'teacher',
  MANAGER: 'manager'
} as const

// 培训状态枚举
export const TRAINING_STATUS = {
  NOT_STARTED: 'not_started',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed'
} as const

// 资料类型枚举
export const MATERIAL_TYPES = {
  VIDEO: 'video',
  DOCUMENT: 'document',
  INTERACTIVE: 'interactive'
} as const

// 练习状态枚举
export const PRACTICE_STATUS = {
  ACTIVE: 'active',
  COMPLETED: 'completed',
  ABANDONED: 'abandoned'
} as const

// 类型定义
export interface User {
  id: string
  email: string
  full_name: string
  role: typeof USER_ROLES[keyof typeof USER_ROLES]
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface TrainingMaterial {
  id: string
  title: string
  description?: string
  content_url: string
  material_type: typeof MATERIAL_TYPES[keyof typeof MATERIAL_TYPES]
  duration_minutes?: number
  download_count: number
  created_by: string
  created_at: string
  updated_at: string
}

export interface PracticeSession {
  id: string
  user_id: string
  title: string
  description?: string
  status: typeof PRACTICE_STATUS[keyof typeof PRACTICE_STATUS]
  started_at: string
  completed_at?: string
  created_at: string
  updated_at: string
}

export interface Feedback {
  id: string
  session_id: string
  user_id: string
  content: string
  rating?: number
  created_at: string
  updated_at: string
}

export interface LearningProgress {
  id: string
  user_id: string
  material_id: string
  status: typeof TRAINING_STATUS[keyof typeof TRAINING_STATUS]
  progress_percentage: number
  started_at: string
  completed_at?: string
  created_at: string
  updated_at: string
}