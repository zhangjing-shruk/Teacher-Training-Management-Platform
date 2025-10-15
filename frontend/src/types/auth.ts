export interface User {
  id: number
  email: string
  name: string
  role: string
  training_status: string
  training_progress: number
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface TrainingStatus {
  materialsCompleted: boolean
  lecturesSubmitted: number
  maxLectures: number
  currentStatus: 'learning' | 'practicing' | 'pending_review' | 'passed' | 'failed'
  sopUnlocked: boolean
}