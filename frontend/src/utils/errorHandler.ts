// 错误处理工具函数

export interface ErrorInfo {
  message: string
  type: 'network' | 'auth' | 'timeout' | 'server' | 'unknown'
  userMessage: string
  suggestions?: string[]
}

// 错误类型映射
const ERROR_MESSAGES: Record<string, ErrorInfo> = {
  'Session fetch timeout': {
    message: 'Session fetch timeout',
    type: 'timeout',
    userMessage: '网络连接超时，正在重试...',
    suggestions: [
      '请检查网络连接',
      '稍后再试',
      '如果问题持续，请联系技术支持'
    ]
  },
  '登出请求超时': {
    message: '登出请求超时',
    type: 'timeout',
    userMessage: '登出请求超时，已自动清除本地状态',
    suggestions: [
      '您已安全登出',
      '如需重新登录，请刷新页面'
    ]
  },
  'Failed to fetch': {
    message: 'Failed to fetch',
    type: 'network',
    userMessage: '网络连接失败，请检查网络设置',
    suggestions: [
      '检查网络连接',
      '尝试刷新页面',
      '检查防火墙设置'
    ]
  },
  'ERR_ABORTED': {
    message: 'ERR_ABORTED',
    type: 'network',
    userMessage: '请求被中断，可能是网络问题',
    suggestions: [
      '请重试操作',
      '检查网络稳定性'
    ]
  },
  'Invalid login credentials': {
    message: 'Invalid login credentials',
    type: 'auth',
    userMessage: '用户名或密码错误',
    suggestions: [
      '请检查用户名和密码',
      '确认账号是否已激活',
      '如忘记密码，请使用找回密码功能'
    ]
  },
  'Supabase not configured': {
    message: 'Supabase not configured',
    type: 'server',
    userMessage: '服务暂时不可用，请稍后再试',
    suggestions: [
      '服务正在维护中',
      '请稍后重试',
      '如问题持续，请联系管理员'
    ]
  }
}

// 解析错误信息
export function parseError(error: any): ErrorInfo {
  const errorMessage = error?.message || error?.toString() || '未知错误'
  
  // 检查是否有预定义的错误信息
  for (const [key, errorInfo] of Object.entries(ERROR_MESSAGES)) {
    if (errorMessage.includes(key)) {
      return errorInfo
    }
  }
  
  // 默认错误处理
  return {
    message: errorMessage,
    type: 'unknown',
    userMessage: '操作失败，请重试',
    suggestions: [
      '请重试操作',
      '如问题持续，请联系技术支持'
    ]
  }
}

// 显示用户友好的错误提示
export function showUserFriendlyError(error: any): string {
  const errorInfo = parseError(error)
  return errorInfo.userMessage
}

// 获取错误建议
export function getErrorSuggestions(error: any): string[] {
  const errorInfo = parseError(error)
  return errorInfo.suggestions || []
}

// 判断是否为网络错误
export function isNetworkError(error: any): boolean {
  const errorInfo = parseError(error)
  return errorInfo.type === 'network' || errorInfo.type === 'timeout'
}

// 判断是否为认证错误
export function isAuthError(error: any): boolean {
  const errorInfo = parseError(error)
  return errorInfo.type === 'auth'
}

// 错误日志记录
export function logError(error: any, context?: string) {
  const errorInfo = parseError(error)
  const logData = {
    timestamp: new Date().toISOString(),
    context: context || 'unknown',
    error: errorInfo,
    userAgent: navigator.userAgent,
    url: window.location.href
  }
  
  console.error('Error logged:', logData)
  
  // 在生产环境中，这里可以发送到错误监控服务
  // 例如：Sentry, LogRocket 等
}

// 创建错误处理装饰器
export function withErrorHandling<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  context?: string
): T {
  return (async (...args: any[]) => {
    try {
      return await fn(...args)
    } catch (error) {
      logError(error, context)
      throw error
    }
  }) as T
}