import { ref, shallowRef, type Component } from 'vue'

// 组件缓存服务，用于优化组件渲染性能
class ComponentCacheService {
  private componentCache = new Map<string, Component>()
  private dataCache = new Map<string, any>()
  private cacheTimestamps = new Map<string, number>()
  private maxCacheSize = 20
  private defaultTTL = 10 * 60 * 1000 // 10分钟

  // 缓存组件实例
  cacheComponent(key: string, component: Component): void {
    if (this.componentCache.size >= this.maxCacheSize) {
      // 删除最旧的缓存
      const oldestKey = this.getOldestCacheKey()
      if (oldestKey) {
        this.removeFromCache(oldestKey)
      }
    }
    
    this.componentCache.set(key, component)
    this.cacheTimestamps.set(key, Date.now())
  }

  // 获取缓存的组件
  getCachedComponent(key: string): Component | null {
    if (!this.componentCache.has(key)) {
      return null
    }

    const timestamp = this.cacheTimestamps.get(key)
    if (timestamp && Date.now() - timestamp > this.defaultTTL) {
      this.removeFromCache(key)
      return null
    }

    return this.componentCache.get(key) || null
  }

  // 缓存组件数据
  cacheData(key: string, data: any, ttl?: number): void {
    this.dataCache.set(key, {
      data,
      timestamp: Date.now(),
      ttl: ttl || this.defaultTTL
    })
  }

  // 获取缓存的数据
  getCachedData(key: string): any {
    const cached = this.dataCache.get(key)
    if (!cached) {
      return null
    }

    if (Date.now() - cached.timestamp > cached.ttl) {
      this.dataCache.delete(key)
      return null
    }

    return cached.data
  }

  // 创建响应式缓存数据
  createReactiveCache<T>(key: string, initialValue: T) {
    const cached = this.getCachedData(key)
    const reactiveData = ref(cached || initialValue)
    
    // 监听数据变化并更新缓存
    return {
      data: reactiveData,
      updateCache: (newValue: T) => {
        reactiveData.value = newValue
        this.cacheData(key, newValue)
      }
    }
  }

  // 创建浅响应式缓存（适用于大对象）
  createShallowReactiveCache<T>(key: string, initialValue: T) {
    const cached = this.getCachedData(key)
    const reactiveData = shallowRef(cached || initialValue)
    
    return {
      data: reactiveData,
      updateCache: (newValue: T) => {
        reactiveData.value = newValue
        this.cacheData(key, newValue)
      }
    }
  }

  // 获取最旧的缓存键
  private getOldestCacheKey(): string | null {
    let oldestKey: string | null = null
    let oldestTime = Date.now()

    for (const [key, timestamp] of this.cacheTimestamps.entries()) {
      if (timestamp < oldestTime) {
        oldestTime = timestamp
        oldestKey = key
      }
    }

    return oldestKey
  }

  // 从缓存中移除
  private removeFromCache(key: string): void {
    this.componentCache.delete(key)
    this.dataCache.delete(key)
    this.cacheTimestamps.delete(key)
  }

  // 清理过期缓存
  cleanup(): void {
    const now = Date.now()
    
    for (const [key, timestamp] of this.cacheTimestamps.entries()) {
      if (now - timestamp > this.defaultTTL) {
        this.removeFromCache(key)
      }
    }
  }

  // 清空所有缓存
  clear(): void {
    this.componentCache.clear()
    this.dataCache.clear()
    this.cacheTimestamps.clear()
  }

  // 获取缓存统计信息
  getStats() {
    return {
      componentCacheSize: this.componentCache.size,
      dataCacheSize: this.dataCache.size,
      totalSize: this.componentCache.size + this.dataCache.size,
      maxSize: this.maxCacheSize
    }
  }

  // 预热缓存（预加载常用数据）
  async warmupCache(userRole: string): Promise<void> {
    try {
      // 根据用户角色预加载常用数据
      if (userRole === 'teacher') {
        // 预加载教师常用数据
        this.cacheData('teacher:navigation', {
          activeTab: 'dashboard',
          lastVisited: Date.now()
        })
      } else if (userRole === 'manager') {
        // 预加载管理员常用数据
        this.cacheData('manager:navigation', {
          activeTab: 'dashboard',
          lastVisited: Date.now()
        })
      }
    } catch (error) {
      console.warn('Failed to warmup cache:', error)
    }
  }
}

// 创建全局组件缓存服务实例
export const componentCacheService = new ComponentCacheService()

// 定期清理过期缓存
setInterval(() => {
  componentCacheService.cleanup()
}, 5 * 60 * 1000) // 每5分钟清理一次

export default componentCacheService