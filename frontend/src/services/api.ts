import type { LoginCredentials, AuthResponse, User } from '@/types/auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// HTTP客户端配置
class ApiClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    const token = localStorage.getItem('access_token')

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

const apiClient = new ApiClient(API_BASE_URL)

// 认证API
export const authApi = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    return apiClient.post<AuthResponse>('/auth/login', credentials)
  },
  
  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>('/auth/me')
  }
}

// 教师API
export const teacherApi = {
  async getProfile(): Promise<User> {
    // TODO: 替换为实际API调用
    // return apiClient.get<User>('/teacher/me')
    throw new Error('API_PLACEHOLDER: /teacher/me')
  },

  async getTrainingMaterials(): Promise<any[]> {
    // TODO: 替换为实际API调用
    // return apiClient.get<any[]>('/materials')
    throw new Error('API_PLACEHOLDER: /materials')
  },

  async submitLecture(videoFile: File): Promise<any> {
    // TODO: 替换为实际API调用
    // const formData = new FormData()
    // formData.append('video', videoFile)
    // return apiClient.post<any>('/lectures', formData)
    throw new Error('API_PLACEHOLDER: /lectures')
  },

  async getLectures(): Promise<any[]> {
    // TODO: 替换为实际API调用
    // return apiClient.get<any[]>('/lectures')
    throw new Error('API_PLACEHOLDER: /lectures')
  }
}

// 管理员API
export const managerApi = {
  async getTrainees(): Promise<any[]> {
    // TODO: 替换为实际API调用
    // return apiClient.get<any[]>('/manager/trainees')
    throw new Error('API_PLACEHOLDER: /manager/trainees')
  },

  async getLectureDetails(lectureId: string): Promise<any> {
    // TODO: 替换为实际API调用
    // return apiClient.get<any>(`/manager/lectures/${lectureId}`)
    throw new Error('API_PLACEHOLDER: /manager/lectures/{id}')
  },

  async submitReview(lectureId: string, review: any): Promise<any> {
    // TODO: 替换为实际API调用
    // return apiClient.post<any>(`/manager/lectures/${lectureId}/review`, review)
    throw new Error('API_PLACEHOLDER: /manager/lectures/{id}/review')
  }
}

// 学习进度API
export const learningProgressApi = {
  async startLearning(materialId: number): Promise<any> {
    return apiClient.post<any>('/learning-progress/start', { material_id: materialId })
  },

  async updateProgress(progressId: number, totalStudySeconds: number, isCompleted?: boolean): Promise<any> {
    return apiClient.put<any>(`/learning-progress/${progressId}`, {
      total_study_seconds: totalStudySeconds,
      is_completed: isCompleted
    })
  },

  async getMaterialProgress(materialId: number): Promise<any> {
    return apiClient.get<any>(`/learning-progress/material/${materialId}`)
  },

  async getAllProgress(): Promise<any[]> {
    return apiClient.get<any[]>('/learning-progress/')
  }
}

export default apiClient