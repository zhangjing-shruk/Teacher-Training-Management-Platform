/**
 * Supabase 连接测试工具
 * 用于检查生产环境的 Supabase 连接状态
 */

import { supabase, isSupabaseConfigured, TABLES } from '@/lib/supabase'

export interface SupabaseTestResult {
  isConfigured: boolean
  connectionTest: boolean
  authTest: boolean
  databaseTest: boolean
  errors: string[]
  details: {
    url?: string
    hasAnonKey?: boolean
    tablesAccessible?: string[]
  }
}

export async function testSupabaseConnection(): Promise<SupabaseTestResult> {
  const result: SupabaseTestResult = {
    isConfigured: false,
    connectionTest: false,
    authTest: false,
    databaseTest: false,
    errors: [],
    details: {}
  }

  try {
    // 1. 检查配置
    console.log('🔧 检查 Supabase 配置...')
    result.isConfigured = isSupabaseConfigured
    result.details.url = import.meta.env.VITE_SUPABASE_URL
    result.details.hasAnonKey = !!import.meta.env.VITE_SUPABASE_ANON_KEY

    if (!result.isConfigured) {
      result.errors.push('Supabase 配置无效或缺失')
      console.error('❌ Supabase 配置检查失败')
      return result
    }

    console.log('✅ Supabase 配置检查通过')

    if (!supabase) {
      result.errors.push('Supabase 客户端未初始化')
      return result
    }

    // 2. 测试基本连接
    console.log('🌐 测试 Supabase 连接...')
    try {
      // 尝试获取当前会话（这会测试基本连接）
      const { data: sessionData, error: sessionError } = await supabase.auth.getSession()
      if (sessionError) {
        console.warn('⚠️ 会话获取警告:', sessionError.message)
      } else {
        console.log('✅ Supabase 连接测试通过')
        result.connectionTest = true
      }
    } catch (error) {
      const errorMsg = `连接测试失败: ${error instanceof Error ? error.message : String(error)}`
      result.errors.push(errorMsg)
      console.error('❌', errorMsg)
    }

    // 3. 测试认证功能
    console.log('🔐 测试认证功能...')
    try {
      const { data: user, error: userError } = await supabase.auth.getUser()
      if (userError && userError.message !== 'Invalid JWT') {
        console.warn('⚠️ 用户获取警告:', userError.message)
      } else {
        console.log('✅ 认证功能测试通过')
        result.authTest = true
      }
    } catch (error) {
      const errorMsg = `认证测试失败: ${error instanceof Error ? error.message : String(error)}`
      result.errors.push(errorMsg)
      console.error('❌', errorMsg)
    }

    // 4. 测试数据库访问
    console.log('🗄️ 测试数据库访问...')
    const accessibleTables: string[] = []
    
    // 测试各个表的访问权限
    for (const [tableName, tableKey] of Object.entries(TABLES)) {
      try {
        console.log(`  测试表: ${tableKey}`)
        const { data, error } = await supabase
          .from(tableKey)
          .select('*')
          .limit(1)

        if (error) {
          console.warn(`  ⚠️ 表 ${tableKey} 访问警告:`, error.message)
          result.errors.push(`表 ${tableKey} 访问错误: ${error.message}`)
        } else {
          console.log(`  ✅ 表 ${tableKey} 访问正常`)
          accessibleTables.push(tableKey)
        }
      } catch (error) {
        const errorMsg = `表 ${tableKey} 访问失败: ${error instanceof Error ? error.message : String(error)}`
        result.errors.push(errorMsg)
        console.error(`  ❌ ${errorMsg}`)
      }
    }

    result.details.tablesAccessible = accessibleTables
    result.databaseTest = accessibleTables.length > 0

    if (result.databaseTest) {
      console.log('✅ 数据库访问测试通过')
    } else {
      console.error('❌ 数据库访问测试失败')
    }

  } catch (error) {
    const errorMsg = `Supabase 测试过程中发生错误: ${error instanceof Error ? error.message : String(error)}`
    result.errors.push(errorMsg)
    console.error('❌', errorMsg)
  }

  return result
}

// 在浏览器控制台中运行测试的便捷函数
export function runSupabaseTest() {
  console.log('🚀 开始 Supabase 连接测试...')
  testSupabaseConnection().then(result => {
    console.log('📊 测试结果:', result)
    
    if (result.errors.length === 0) {
      console.log('🎉 所有测试通过！Supabase 连接正常')
    } else {
      console.error('⚠️ 发现问题:')
      result.errors.forEach(error => console.error(`  - ${error}`))
    }
  }).catch(error => {
    console.error('💥 测试执行失败:', error)
  })
}

// 将测试函数暴露到全局，方便在浏览器控制台调用
if (typeof window !== 'undefined') {
  (window as any).runSupabaseTest = runSupabaseTest;
  (window as any).testSupabaseConnection = testSupabaseConnection;
}