import { supabase, isSupabaseConfigured } from '@/lib/supabase'

export async function testSupabaseConnection() {
  console.log('🔍 开始测试 Supabase 连接...')
  
  // 1. 检查配置
  console.log('1. 检查 Supabase 配置:')
  console.log('   - isSupabaseConfigured:', isSupabaseConfigured)
  console.log('   - VITE_SUPABASE_URL:', import.meta.env.VITE_SUPABASE_URL)
  console.log('   - VITE_SUPABASE_ANON_KEY 长度:', import.meta.env.VITE_SUPABASE_ANON_KEY?.length || 0)
  
  if (!supabase) {
    console.error('❌ Supabase 客户端未初始化')
    return false
  }
  
  // 2. 测试基本连接
  try {
    console.log('2. 测试基本连接...')
    const { data, error } = await supabase.auth.getSession()
    if (error) {
      console.warn('⚠️ Auth session 错误:', error.message)
    } else {
      console.log('✅ Auth session 正常')
    }
  } catch (error) {
    console.error('❌ 基本连接测试失败:', error)
    return false
  }
  
  // 3. 测试 Storage 权限
  try {
    console.log('3. 测试 Storage 权限...')
    const { data: buckets, error } = await supabase.storage.listBuckets()
    
    if (error) {
       console.error('❌ 获取 bucket 列表失败:', error)
       console.error('   错误详情:', {
         message: error.message
       })
       return false
     }
    
    console.log('✅ Storage 权限正常')
    console.log('   现有 buckets:', buckets?.map(b => b.name) || [])
    
    // 4. 检查 training-materials bucket
    const trainingBucket = buckets?.find(b => b.name === 'training-materials')
    if (trainingBucket) {
      console.log('✅ training-materials bucket 存在')
      console.log('   bucket 配置:', trainingBucket)
    } else {
      console.log('⚠️ training-materials bucket 不存在，需要创建')
    }
    
    return true
  } catch (error) {
    console.error('❌ Storage 测试失败:', error)
    return false
  }
}

export async function testBucketCreation() {
  console.log('🔧 测试创建 training-materials bucket...')
  
  if (!supabase) {
    console.error('❌ Supabase 客户端未初始化')
    return false
  }
  
  try {
    const { error } = await supabase.storage.createBucket('training-materials', {
      public: true,
      allowedMimeTypes: [
        'application/pdf',
        'image/jpeg',
        'image/png',
        'video/mp4'
      ],
      fileSizeLimit: 104857600 // 100MB
    })
    
    if (error) {
      if (error.message.includes('already exists')) {
        console.log('✅ Bucket 已存在')
        return true
      } else {
        console.error('❌ 创建 bucket 失败:', error)
        return false
      }
    }
    
    console.log('✅ Bucket 创建成功')
    return true
  } catch (error) {
    console.error('❌ 创建 bucket 异常:', error)
    return false
  }
}