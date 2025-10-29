/**
 * 性能测试工具
 * 用于测试和监控应用性能
 */

interface PerformanceMetrics {
  loadTime: number
  renderTime: number
  cacheHitRate: number
  memoryUsage: number
  bundleSize?: number
}

interface RoutePerformance {
  route: string
  loadTime: number
  renderTime: number
  cacheHit: boolean
}

class PerformanceMonitor {
  private metrics: PerformanceMetrics[] = []
  private routeMetrics: RoutePerformance[] = []
  private startTime: number = 0

  /**
   * 开始性能监控
   */
  startMonitoring(): void {
    this.startTime = performance.now()
    
    // 监听页面加载性能
    if (typeof window !== 'undefined') {
      window.addEventListener('load', () => {
        this.recordPageLoadMetrics()
      })
    }
  }

  /**
   * 记录页面加载性能指标
   */
  private recordPageLoadMetrics(): void {
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
    
    if (navigation) {
      const metrics: PerformanceMetrics = {
        loadTime: navigation.loadEventEnd - navigation.loadEventStart,
        renderTime: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        cacheHitRate: this.calculateCacheHitRate(),
        memoryUsage: this.getMemoryUsage()
      }
      
      this.metrics.push(metrics)
      console.log('页面性能指标:', metrics)
    }
  }

  /**
   * 记录路由切换性能
   */
  recordRoutePerformance(route: string, startTime: number, cacheHit: boolean = false): void {
    const endTime = performance.now()
    const loadTime = endTime - startTime
    
    const routeMetric: RoutePerformance = {
      route,
      loadTime,
      renderTime: loadTime, // 简化处理
      cacheHit
    }
    
    this.routeMetrics.push(routeMetric)
    console.log(`路由 ${route} 性能:`, routeMetric)
  }

  /**
   * 计算缓存命中率
   */
  private calculateCacheHitRate(): number {
    const totalRequests = this.routeMetrics.length
    const cacheHits = this.routeMetrics.filter(m => m.cacheHit).length
    
    return totalRequests > 0 ? (cacheHits / totalRequests) * 100 : 0
  }

  /**
   * 获取内存使用情况
   */
  private getMemoryUsage(): number {
    if ('memory' in performance) {
      const memory = (performance as any).memory
      return memory.usedJSHeapSize / 1024 / 1024 // MB
    }
    return 0
  }

  /**
   * 测试组件懒加载性能
   */
  async testLazyLoading(): Promise<void> {
    console.log('开始测试组件懒加载性能...')
    
    const routes = [
      '/teacher/dashboard',
      '/teacher/materials',
      '/teacher/practice',
      '/manager/dashboard',
      '/manager/users',
      '/manager/analytics'
    ]

    for (const route of routes) {
      const startTime = performance.now()
      
      try {
        // 模拟路由导航
        await this.simulateRouteNavigation(route)
        this.recordRoutePerformance(route, startTime)
      } catch (error) {
        console.error(`路由 ${route} 测试失败:`, error)
      }
    }
  }

  /**
   * 模拟路由导航
   */
  private async simulateRouteNavigation(route: string): Promise<void> {
    // 这里可以添加实际的路由导航逻辑
    return new Promise(resolve => {
      setTimeout(resolve, Math.random() * 100 + 50) // 模拟加载时间
    })
  }

  /**
   * 测试缓存性能
   */
  testCachePerformance(): void {
    console.log('开始测试缓存性能...')
    
    const testData = {
      key: 'test-cache-key',
      data: { message: 'Hello Cache!', timestamp: Date.now() }
    }

    // 测试缓存写入性能
    const writeStartTime = performance.now()
    localStorage.setItem(testData.key, JSON.stringify(testData.data))
    const writeTime = performance.now() - writeStartTime

    // 测试缓存读取性能
    const readStartTime = performance.now()
    const cachedData = localStorage.getItem(testData.key)
    const readTime = performance.now() - readStartTime

    console.log('缓存性能测试结果:', {
      writeTime: `${writeTime.toFixed(2)}ms`,
      readTime: `${readTime.toFixed(2)}ms`,
      dataSize: JSON.stringify(testData.data).length
    })

    // 清理测试数据
    localStorage.removeItem(testData.key)
  }

  /**
   * 获取性能报告
   */
  getPerformanceReport(): {
    averageLoadTime: number
    averageRenderTime: number
    cacheHitRate: number
    memoryUsage: number
    routeMetrics: RoutePerformance[]
  } {
    const avgLoadTime = this.metrics.reduce((sum, m) => sum + m.loadTime, 0) / this.metrics.length || 0
    const avgRenderTime = this.metrics.reduce((sum, m) => sum + m.renderTime, 0) / this.metrics.length || 0
    const avgMemoryUsage = this.metrics.reduce((sum, m) => sum + m.memoryUsage, 0) / this.metrics.length || 0

    return {
      averageLoadTime: avgLoadTime,
      averageRenderTime: avgRenderTime,
      cacheHitRate: this.calculateCacheHitRate(),
      memoryUsage: avgMemoryUsage,
      routeMetrics: this.routeMetrics
    }
  }

  /**
   * 运行完整的性能测试套件
   */
  async runFullPerformanceTest(): Promise<void> {
    console.log('🚀 开始完整性能测试...')
    
    this.startMonitoring()
    
    // 测试缓存性能
    this.testCachePerformance()
    
    // 测试懒加载性能
    await this.testLazyLoading()
    
    // 等待一段时间收集指标
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 生成报告
    const report = this.getPerformanceReport()
    console.log('📊 性能测试报告:', report)
    
    // 性能建议
    this.generatePerformanceRecommendations(report)
  }

  /**
   * 生成性能优化建议
   */
  private generatePerformanceRecommendations(report: any): void {
    console.log('💡 性能优化建议:')
    
    if (report.averageLoadTime > 1000) {
      console.log('- 页面加载时间较长，建议进一步优化组件懒加载')
    }
    
    if (report.cacheHitRate < 50) {
      console.log('- 缓存命中率较低，建议优化缓存策略')
    }
    
    if (report.memoryUsage > 50) {
      console.log('- 内存使用较高，建议检查内存泄漏')
    }
    
    console.log('✅ 性能测试完成!')
  }
}

// 导出性能监控实例
export const performanceMonitor = new PerformanceMonitor()

// 在开发环境下自动启动性能监控
if (import.meta.env.DEV) {
  performanceMonitor.startMonitoring()
}