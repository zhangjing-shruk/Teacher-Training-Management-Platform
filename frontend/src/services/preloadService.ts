// 组件预加载服务，用于优化路由切换性能
class PreloadService {
  private preloadedComponents = new Set<string>()
  private preloadPromises = new Map<string, Promise<any>>()

  // 预加载组件
  async preloadComponent(importFn: () => Promise<any>, componentName: string): Promise<void> {
    if (this.preloadedComponents.has(componentName)) {
      return
    }

    if (this.preloadPromises.has(componentName)) {
      await this.preloadPromises.get(componentName)
      return
    }

    const promise = importFn().then(module => {
      this.preloadedComponents.add(componentName)
      this.preloadPromises.delete(componentName)
      return module
    }).catch(error => {
      console.warn(`Failed to preload component ${componentName}:`, error)
      this.preloadPromises.delete(componentName)
      throw error
    })

    this.preloadPromises.set(componentName, promise)
    await promise
  }

  // 预加载教师端组件
  async preloadTeacherComponents(): Promise<void> {
    const teacherComponents = [
      { name: 'TeacherDashboard', import: () => import('../views/teacher/DashboardView.vue') },
      { name: 'TrainingMaterials', import: () => import('../views/teacher/TrainingMaterialsView.vue') },
      { name: 'TrialLecture', import: () => import('../views/teacher/TrialLectureView.vue') },
      { name: 'Practice', import: () => import('../views/teacher/PracticeView.vue') },
      { name: 'Feedback', import: () => import('../views/teacher/FeedbackView.vue') }
    ]

    // 并行预加载，但限制并发数
    const concurrency = 2
    for (let i = 0; i < teacherComponents.length; i += concurrency) {
      const batch = teacherComponents.slice(i, i + concurrency)
      await Promise.allSettled(
        batch.map(component => 
          this.preloadComponent(component.import, component.name)
        )
      )
    }
  }

  // 预加载管理员端组件
  async preloadManagerComponents(): Promise<void> {
    const managerComponents = [
      { name: 'ManagerDashboard', import: () => import('../views/manager/DashboardView.vue') },
      { name: 'ManagerTeachers', import: () => import('../views/manager/TeachersView.vue') },
      { name: 'ManagerLectures', import: () => import('../views/manager/LecturesView.vue') },
      { name: 'ManagerMaterials', import: () => import('../views/manager/MaterialsView.vue') },
      { name: 'ManagerAnalytics', import: () => import('../views/manager/AnalyticsView.vue') }
    ]

    // 并行预加载，但限制并发数
    const concurrency = 2
    for (let i = 0; i < managerComponents.length; i += concurrency) {
      const batch = managerComponents.slice(i, i + concurrency)
      await Promise.allSettled(
        batch.map(component => 
          this.preloadComponent(component.import, component.name)
        )
      )
    }
  }

  // 根据用户角色预加载相关组件
  async preloadByRole(role: string): Promise<void> {
    try {
      if (role === 'teacher') {
        await this.preloadTeacherComponents()
      } else if (role === 'manager') {
        await this.preloadManagerComponents()
      }
    } catch (error) {
      console.warn(`Failed to preload components for role ${role}:`, error)
    }
  }

  // 智能预加载：根据当前路由预加载可能访问的组件
  async smartPreload(currentRoute: string, userRole: string): Promise<void> {
    // 延迟预加载，避免阻塞当前页面
    setTimeout(async () => {
      try {
        if (currentRoute.startsWith('/teacher') && userRole === 'teacher') {
          // 如果在教师端，预加载其他教师组件
          await this.preloadTeacherComponents()
        } else if (currentRoute.startsWith('/manager') && userRole === 'manager') {
          // 如果在管理员端，预加载其他管理员组件
          await this.preloadManagerComponents()
        }
      } catch (error) {
        console.warn('Smart preload failed:', error)
      }
    }, 1000) // 1秒后开始预加载
  }

  // 获取预加载状态
  getPreloadStatus(): { total: number; loaded: number; components: string[] } {
    return {
      total: this.preloadedComponents.size + this.preloadPromises.size,
      loaded: this.preloadedComponents.size,
      components: Array.from(this.preloadedComponents)
    }
  }

  // 清除预加载缓存
  clear(): void {
    this.preloadedComponents.clear()
    this.preloadPromises.clear()
  }
}

// 创建全局预加载服务实例
export const preloadService = new PreloadService()

export default preloadService