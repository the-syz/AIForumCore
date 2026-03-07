import http from './http'

interface UserInfo {
  id: number
  name: string
  student_id: string
  grade: string
  email: string
  phone: string
  research_direction: string
  wechat: string
  role: string
  is_admin: boolean
}

interface LoginData {
  account: string
  password: string
  remember: boolean
  autoLogin: boolean
}

interface RegisterData {
  name: string
  student_id: string
  password: string
  grade: string
  email: string
  phone: string
  research_direction: string
  wechat: string
}

interface ChangePasswordData {
  old_password: string
  new_password: string
}

interface LoginResponse {
  access_token: string
  token_type: string
}

export const login = (data: LoginData): Promise<LoginResponse> => {
  return http.post('/auth/login', {
    username: data.account,
    password: data.password
  })
}

// 获取当前用户信息
export const getCurrentUserInfo = async (): Promise<UserInfo> => {
  return http.get('/auth/me')
}

export const register = (data: RegisterData) => {
  return http.post('/auth/register', data)
}

export const logout = () => {
  return http.post('/auth/logout')
}

export const getCurrentUser = () => {
  return http.get('/auth/me')
}

export const changePassword = (data: ChangePasswordData) => {
  return http.post('/auth/change-password', data)
}
