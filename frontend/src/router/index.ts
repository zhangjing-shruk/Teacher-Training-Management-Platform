import { createRouter, createWebHistory } from 'vue-router'
import { useSupabaseAuthStore } from '@/stores/supabaseAuth'
import { isSupabaseConfigured } from '@/lib/supabase'
import { preloadService } from '@/services/preloadService'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('../views/TestView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/teacher',
      name: 'teacher',
      component: () => import('../layouts/TeacherLayout.vue'),
      meta: { requiresAuth: true, role: 'teacher' },
      children: [
        {
          path: '',
          name: 'teacher-dashboard',
          component: () => import('../views/teacher/DashboardView.vue')
        },
        {
          path: 'materials',
          name: 'training-materials',
          component: () => import('../views/teacher/TrainingMaterialsView.vue')
        },
        {
          path: 'trial-lecture',
          name: 'trial-lecture',
          component: () => import('../views/teacher/TrialLectureView.vue')
        },
        {
          path: 'practice',
          name: 'practice',
          component: () => import('../views/teacher/PracticeView.vue')
        },
        {
          path: 'feedback',
          name: 'feedback',
          component: () => import('../views/teacher/FeedbackView.vue')
        },
        {
          path: 'feedback/:lectureId',
          name: 'feedback-report',
          component: () => import('../views/teacher/FeedbackReportView.vue')
        },
        {
          path: 'sop',
          name: 'sop',
          component: () => import('../views/teacher/SOPView.vue')
        }
      ]
    },
    {
      path: '/manager',
      name: 'manager',
      component: () => import('../layouts/ManagerLayout.vue'),
      meta: { requiresAuth: true, role: 'manager' },
      children: [
        {
          path: '',
          name: 'manager-dashboard',
          component: () => import('../views/manager/DashboardView.vue')
        },
        {
          path: 'dashboard',
          name: 'manager-dashboard-explicit',
          component: () => import('../views/manager/DashboardView.vue')
        },
        {
          path: 'teachers',
          name: 'manager-teachers',
          component: () => import('../views/manager/TeachersView.vue')
        },
        {
          path: 'lectures',
          name: 'manager-lectures',
          component: () => import('../views/manager/LecturesView.vue')
        },
        {
          path: 'materials',
          name: 'manager-materials',
          component: () => import('../views/manager/MaterialsView.vue')
        },
        {
          path: 'analytics',
          name: 'manager-analytics',
          component: () => import('../views/manager/AnalyticsView.vue')
        },
        {
          path: 'test',
          name: 'manager-test',
          component: () => import('../views/manager/TestView.vue')
        },
        {
          path: 'review/:lectureId',
          name: 'lecture-review',
          component: () => import('../views/manager/LectureReviewView.vue')
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue')
    }
  ],
})

// 全局路由守卫
router.beforeEach(async (to, from, next) => {
  try {
    const authStore = useSupabaseAuthStore()
    
    // 确保认证状态已初始化（设置超时）
    const initTimeout = new Promise((_, reject) => 
      setTimeout(() => reject(new Error('Auth initialization timeout')), 3000)
    )
    
    try {
      await Promise.race([authStore.initializeAuth(), initTimeout])
    } catch (error) {
      console.warn('Auth initialization timeout or failed:', error)
      // 如果初始化失败，但不是需要认证的路由，允许访问
      if (!to.meta.requiresAuth) {
        return next()
      }
      return next('/login')
    }
    
    // 权限检查逻辑（无论是否配置Supabase都要执行）
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
      console.log('需要认证但用户未登录，重定向到登录页')
      next('/login')
    } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
      // 等待用户角色加载完成
      let userRole = authStore.user?.role
      if (!userRole && authStore.isAuthenticated) {
        // 如果用户已认证但角色还未加载，等待一下
        await new Promise(resolve => setTimeout(resolve, 100))
        userRole = authStore.user?.role
      }
      
      console.log('用户已登录，角色:', userRole)
      next(userRole === 'manager' ? '/manager' : '/teacher')
    } else if (to.meta.role && authStore.isAuthenticated) {
      // 等待用户角色加载完成
      let userRole = authStore.user?.role
      if (!userRole) {
        // 如果角色还未加载，等待一下
        await new Promise(resolve => setTimeout(resolve, 200))
        userRole = authStore.user?.role
      }
      
      // 角色权限检查
      if (userRole !== to.meta.role) {
        console.log('角色权限不匹配:', {
          required: to.meta.role,
          actual: userRole,
          path: to.path
        })
        // 根据用户实际角色重定向到正确的页面
        if (userRole === 'manager') {
          next('/manager')
        } else if (userRole === 'teacher') {
          next('/teacher')
        } else {
          next('/login')
        }
      } else {
        // 角色匹配，允许访问
        // 智能预加载相关组件
        if (to.meta.requiresAuth && userRole) {
          preloadService.smartPreload(to.path, userRole)
        }
        next()
      }
    } else {
      // 智能预加载相关组件
      if (to.meta.requiresAuth && authStore.user?.role) {
        preloadService.smartPreload(to.path, authStore.user.role)
      }
      next()
    }
  } catch (error) {
    console.error('Router guard error:', error)
    // 如果路由守卫出错，允许访问公共路由
    if (!to.meta.requiresAuth) {
      next()
    } else {
      next('/login')
    }
  }
})

export default router
