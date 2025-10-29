// 缓存服务，用于优化Supabase查询性能
interface CacheItem<T> {
  data: T
  timestamp: number
  expiresAt: number
}

interface CacheConfig {
  ttl: number // 生存时间（毫秒）
  maxSize?: number // 最大缓存条目数
}

class CacheService {
  private cache = new Map<string, CacheItem<any>>()
  private defaultTTL = 5 * 60 * 1000 // 默认5分钟
  private maxSize = 100 // 默认最大100个条目

  // 生成缓存键
  private generateKey(prefix: string, params: Record<string, any>): string {
    const sortedParams = Object.keys(params)
      .sort()
      .map(key => `${key}:${JSON.stringify(params[key])}`)
      .join('|')
    return `${prefix}:${sortedParams}`
  }

  // 设置缓存
  set<T>(key: string, data: T, ttl?: number): void {
    const now = Date.now()
    const expiresAt = now + (ttl || this.defaultTTL)
    
    // 如果缓存已满，删除最旧的条目
    if (this.cache.size >= this.maxSize) {
      const oldestKey = this.cache.keys().next().value
      if (oldestKey) {
        this.cache.delete(oldestKey)
      }
    }
    
    this.cache.set(key, {
      data,
      timestamp: now,
      expiresAt
    })
  }

  // 获取缓存
  get<T>(key: string): T | null {
    const item = this.cache.get(key)
    
    if (!item) {
      return null
    }
    
    // 检查是否过期
    if (Date.now() > item.expiresAt) {
      this.cache.delete(key)
      return null
    }
    
    return item.data as T
  }

  // 删除缓存
  delete(key: string): void {
    this.cache.delete(key)
  }

  // 清空缓存
  clear(): void {
    this.cache.clear()
  }

  // 清理过期缓存
  cleanup(): void {
    const now = Date.now()
    for (const [key, item] of this.cache.entries()) {
      if (now > item.expiresAt) {
        this.cache.delete(key)
      }
    }
  }

  // 获取或设置缓存（常用模式）
  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttl?: number
  ): Promise<T> {
    const cached = this.get<T>(key)
    if (cached !== null) {
      return cached
    }
    
    const data = await fetcher()
    this.set(key, data, ttl)
    return data
  }

  // 为查询生成缓存键
  queryKey(table: string, params: Record<string, any> = {}): string {
    return this.generateKey(`query:${table}`, params)
  }

  // 为用户数据生成缓存键
  userKey(userId: string, dataType: string): string {
    return `user:${userId}:${dataType}`
  }

  // 获取缓存统计
  getStats() {
    const now = Date.now()
    let expired = 0
    let valid = 0
    
    for (const item of this.cache.values()) {
      if (now > item.expiresAt) {
        expired++
      } else {
        valid++
      }
    }
    
    return {
      total: this.cache.size,
      valid,
      expired,
      hitRate: valid / (valid + expired) || 0
    }
  }
}

// 创建全局缓存实例
export const cacheService = new CacheService()

// 定期清理过期缓存
setInterval(() => {
  cacheService.cleanup()
}, 60000) // 每分钟清理一次

export default cacheService