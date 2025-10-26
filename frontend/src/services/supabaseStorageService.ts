import { supabase, isSupabaseConfigured } from '@/lib/supabase'

export interface UploadResult {
  success: boolean
  url?: string
  error?: string
  path?: string
}

export class SupabaseStorageService {
  private static readonly BUCKET_NAME = 'training-materials'
  
  /**
   * 确保 Supabase 可用
   */
  private static ensureSupabaseAvailable() {
    if (!supabase || !isSupabaseConfigured) {
      throw new Error('Supabase service is not available. Please configure Supabase environment variables.')
    }
    return supabase
  }

  /**
   * 上传文件到 Supabase Storage
   */
  static async uploadFile(file: File, folder: string = 'materials'): Promise<UploadResult> {
    try {
      const client = this.ensureSupabaseAvailable()
      
      // 生成唯一文件名
      const timestamp = Date.now()
      const randomString = Math.random().toString(36).substring(2, 15)
      const fileExtension = file.name.split('.').pop()
      const uniqueFileName = `${timestamp}_${randomString}.${fileExtension}`
      const filePath = `${folder}/${uniqueFileName}`

      console.log('开始上传文件到 Supabase Storage:', {
        fileName: file.name,
        size: file.size,
        type: file.type,
        path: filePath
      })

      // 上传文件
      const { data, error } = await client.storage
        .from(this.BUCKET_NAME)
        .upload(filePath, file, {
          cacheControl: '3600',
          upsert: false
        })

      if (error) {
        console.error('文件上传失败:', error)
        return {
          success: false,
          error: `文件上传失败: ${error.message}`
        }
      }

      console.log('文件上传成功:', data)

      // 获取公共 URL
      const { data: urlData } = client.storage
        .from(this.BUCKET_NAME)
        .getPublicUrl(filePath)

      return {
        success: true,
        url: urlData.publicUrl,
        path: filePath
      }

    } catch (error: any) {
      console.error('上传文件时发生错误:', error)
      return {
        success: false,
        error: `上传失败: ${error.message}`
      }
    }
  }

  /**
   * 获取文件的公共 URL
   */
  static getPublicUrl(filePath: string): string | null {
    try {
      const client = this.ensureSupabaseAvailable()
      
      const { data } = client.storage
        .from(this.BUCKET_NAME)
        .getPublicUrl(filePath)

      return data.publicUrl
    } catch (error) {
      console.error('获取文件 URL 失败:', error)
      return null
    }
  }

  /**
   * 删除文件
   */
  static async deleteFile(filePath: string): Promise<boolean> {
    try {
      const client = this.ensureSupabaseAvailable()
      
      const { error } = await client.storage
        .from(this.BUCKET_NAME)
        .remove([filePath])

      if (error) {
        console.error('删除文件失败:', error)
        return false
      }

      return true
    } catch (error) {
      console.error('删除文件时发生错误:', error)
      return false
    }
  }

  /**
   * 检查 bucket 是否存在，如果不存在则创建
   */
  static async ensureBucketExists(): Promise<boolean> {
    try {
      const client = this.ensureSupabaseAvailable()
      
      // 检查 bucket 是否存在
      const { data: buckets, error: listError } = await client.storage.listBuckets()
      
      if (listError) {
        console.error('获取 bucket 列表失败:', listError)
        return false
      }

      const bucketExists = buckets?.some(bucket => bucket.name === this.BUCKET_NAME)
      
      if (!bucketExists) {
        console.log(`Bucket ${this.BUCKET_NAME} 不存在，尝试创建...`)
        
        // 创建 bucket - 使用简化配置避免 API 限制
        const { error: createError } = await client.storage.createBucket(this.BUCKET_NAME, {
          public: true
        })

        if (createError) {
          console.error('创建 bucket 失败:', createError)
          return false
        }

        console.log(`Bucket ${this.BUCKET_NAME} 创建成功`)
        
        // 创建 bucket 后，设置 RLS 策略
        await this.setupStoragePolicies()
      }

      return true
    } catch (error) {
      console.error('检查/创建 bucket 时发生错误:', error)
      return false
    }
  }

  /**
   * 设置 Storage RLS 策略（需要在 Supabase 控制台手动执行）
   */
  private static async setupStoragePolicies(): Promise<void> {
    console.log('⚠️  需要在 Supabase 控制台手动设置 Storage RLS 策略')
    console.log('请在 Supabase SQL Editor 中执行 FIX_STORAGE_POLICY.sql 文件中的 SQL 语句')
  }

  /**
   * 从旧的文件 URL 迁移到 Supabase Storage
   */
  static migrateFromOldUrl(oldUrl: string): string | null {
    try {
      // 如果已经是 Supabase URL，直接返回
      if (oldUrl.includes('supabase.co')) {
        return oldUrl
      }

      // 如果是相对路径（如 /uploads/materials/xxx），需要转换
      if (oldUrl.startsWith('/uploads/') || oldUrl.startsWith('uploads/')) {
        const fileName = oldUrl.split('/').pop()
        if (fileName) {
          // 假设文件已经在 Supabase Storage 中，构造 URL
          return this.getPublicUrl(`materials/${fileName}`)
        }
      }

      return null
    } catch (error) {
      console.error('迁移文件 URL 失败:', error)
      return null
    }
  }
}

export default SupabaseStorageService