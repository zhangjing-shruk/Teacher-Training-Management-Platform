import { 
  supabase, 
  isSupabaseConfigured,
  TABLES, 
  type TrainingMaterial, 
  type PracticeSession, 
  type Feedback, 
  type LearningProgress,
  TRAINING_STATUS,
  PRACTICE_STATUS,
  MATERIAL_TYPES
} from '@/lib/supabase'

// 检查 Supabase 是否可用的辅助函数
function ensureSupabaseAvailable() {
  if (!supabase || !isSupabaseConfigured) {
    throw new Error('Supabase service is not available. Please configure Supabase environment variables.')
  }
  return supabase
}

// 培训资料服务
export class TrainingMaterialService {
  // 获取所有培训资料
  static async getAll() {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.TRAINING_MATERIALS)
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as TrainingMaterial[]
  }

  // 根据ID获取培训资料
  static async getById(id: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.TRAINING_MATERIALS)
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data as TrainingMaterial
  }

  // 创建培训资料（管理员）
  static async create(material: Omit<TrainingMaterial, 'id' | 'created_at' | 'updated_at' | 'download_count'>) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.TRAINING_MATERIALS)
      .insert({
        ...material,
        download_count: 0
      })
      .select()
      .single()

    if (error) throw error
    return data as TrainingMaterial
  }

  // 更新培训资料
  static async update(id: string, updates: Partial<TrainingMaterial>) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.TRAINING_MATERIALS)
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as TrainingMaterial
  }

  // 删除培训资料
  static async delete(id: string) {
    const client = ensureSupabaseAvailable()
    const { error } = await client
      .from(TABLES.TRAINING_MATERIALS)
      .delete()
      .eq('id', id)

    if (error) throw error
  }

  // 增加下载次数
  static async incrementDownloadCount(id: string) {
    const client = ensureSupabaseAvailable()
    const { error } = await client.rpc('increment_download_count', { material_id: id })
    if (error) throw error
  }
}

// 学习进度服务
export class LearningProgressService {
  // 获取用户学习进度
  static async getUserProgress(userId: string) {
    const client = ensureSupabaseAvailable()
    
    // 简化查询，避免复杂的关联查询
    const { data, error } = await client
      .from(TABLES.LEARNING_PROGRESS)
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(50) // 限制返回数量，提高性能

    if (error) throw error
    return data as LearningProgress[]
  }

  // 获取用户学习进度（包含资料信息）- 仅在需要时调用
  static async getUserProgressWithMaterials(userId: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.LEARNING_PROGRESS)
      .select(`
        *,
        training_materials (
          id,
          title,
          description,
          material_type,
          duration_minutes
        )
      `)
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(20) // 限制返回数量

    if (error) throw error
    return data as (LearningProgress & { training_materials: TrainingMaterial })[]
  }

  // 开始学习
  static async startLearning(userId: string, materialId: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.LEARNING_PROGRESS)
      .insert({
        user_id: userId,
        material_id: materialId,
        status: TRAINING_STATUS.IN_PROGRESS,
        progress_percentage: 0,
        started_at: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data as LearningProgress
  }

  // 更新学习进度
  static async updateProgress(userId: string, materialId: string, progressPercentage: number) {
    const client = ensureSupabaseAvailable()
    const updates: Partial<LearningProgress> = {
      progress_percentage: progressPercentage
    }

    if (progressPercentage >= 100) {
      updates.status = TRAINING_STATUS.COMPLETED
      updates.completed_at = new Date().toISOString()
    }

    const { data, error } = await client
      .from(TABLES.LEARNING_PROGRESS)
      .update(updates)
      .eq('user_id', userId)
      .eq('material_id', materialId)
      .select()
      .single()

    if (error) throw error
    return data as LearningProgress
  }

  // 完成学习
  static async completeLearning(userId: string, materialId: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.LEARNING_PROGRESS)
      .update({
        status: TRAINING_STATUS.COMPLETED,
        progress_percentage: 100,
        completed_at: new Date().toISOString()
      })
      .eq('user_id', userId)
      .eq('material_id', materialId)
      .select()
      .single()

    if (error) throw error
    return data as LearningProgress
  }
}

// 练习会话服务
export class PracticeSessionService {
  // 获取用户练习会话
  static async getUserSessions(userId: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.PRACTICE_SESSIONS)
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(30) // 限制返回数量，提高性能

    if (error) throw error
    return data as PracticeSession[]
  }

  // 根据ID获取练习会话
  static async getById(id: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.PRACTICE_SESSIONS)
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data as PracticeSession
  }

  // 创建练习会话
  static async create(session: Omit<PracticeSession, 'id' | 'created_at' | 'updated_at'>) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.PRACTICE_SESSIONS)
      .insert({
        ...session,
        started_at: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data as PracticeSession
  }

  // 更新练习会话
  static async update(id: string, updates: Partial<PracticeSession>) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.PRACTICE_SESSIONS)
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as PracticeSession
  }

  // 完成练习会话
  static async complete(id: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.PRACTICE_SESSIONS)
      .update({
        status: PRACTICE_STATUS.COMPLETED,
        completed_at: new Date().toISOString()
      })
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as PracticeSession
  }

  // 获取用户练习统计
  static async getUserStats(userId: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client.rpc('get_user_practice_stats', { user_id: userId })
    if (error) throw error
    return data
  }
}

// 反馈服务
export class FeedbackService {
  // 根据会话获取反馈
  static async getBySession(sessionId: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.FEEDBACK)
      .select('*')
      .eq('session_id', sessionId)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as Feedback[]
  }

  // 根据用户获取反馈
  static async getByUser(userId: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.FEEDBACK)
      .select(`
        *,
        practice_sessions (
          id,
          title,
          description
        )
      `)
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(25) // 限制返回数量，提高性能

    if (error) throw error
    return data as (Feedback & { practice_sessions: PracticeSession })[]
  }

  // 创建反馈
  static async create(feedback: Omit<Feedback, 'id' | 'created_at' | 'updated_at'>) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.FEEDBACK)
      .insert(feedback)
      .select()
      .single()

    if (error) throw error
    return data as Feedback
  }

  // 更新反馈
  static async update(id: string, updates: Partial<Feedback>) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.FEEDBACK)
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as Feedback
  }

  // 删除反馈
  static async delete(id: string) {
    const client = ensureSupabaseAvailable()
    const { error } = await client
      .from(TABLES.FEEDBACK)
      .delete()
      .eq('id', id)

    if (error) throw error
  }
}

// 管理员统计服务
export class AdminStatsService {
  // 获取所有用户统计
  static async getAllUserStats() {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client.rpc('get_all_user_stats')
    if (error) throw error
    return data
  }

  // 获取资料统计
  static async getMaterialStats(materialId: string) {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client.rpc('get_material_stats', { material_id: materialId })
    if (error) throw error
    return data
  }

  // 获取所有反馈
  static async getAllFeedback() {
    const client = ensureSupabaseAvailable()
    const { data, error } = await client
      .from(TABLES.FEEDBACK)
      .select(`
        *,
        users (
          id,
          full_name,
          email
        ),
        practice_sessions (
          id,
          title,
          description
        )
      `)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data
  }
}