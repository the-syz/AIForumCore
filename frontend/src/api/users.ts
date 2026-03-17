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
  created_at: string
  updated_at: string
}

interface UserUpdate {
  name?: string
  student_id?: string
  grade?: string
  email?: string
  phone?: string
  research_direction?: string
  wechat?: string
}

interface ChangePasswordData {
  old_password: string
  new_password: string
}

interface UserCreate {
  name: string
  student_id: string
  password: string
  grade?: string
  email?: string
  phone?: string
  research_direction?: string
  wechat?: string
}

interface UserRoleUpdate {
  role: string
  is_admin: boolean
}

// 获取当前用户信息
export const getCurrentUser = async (): Promise<UserInfo> => {
  return http.get('/users/me')
}

// 更新当前用户信息
export const updateCurrentUser = async (data: UserUpdate): Promise<UserInfo> => {
  return http.put('/users/me', data)
}

// 修改当前用户密码
export const changePassword = async (data: ChangePasswordData): Promise<{ message: string }> => {
  return http.post('/users/me/change-password', data)
}

// 获取用户公开信息（不需要管理员权限）
export const getUserPublic = async (userId: number): Promise<UserInfo> => {
  return http.get(`/users/${userId}/public`)
}

// 获取用户发布的论文列表
export const getUserPapers = async (
  userId: number,
  skip: number = 0,
  limit: number = 20
): Promise<any[]> => {
  return http.get(`/users/${userId}/papers`, {
    params: { skip, limit }
  })
}

// 获取用户发布的经验贴列表
export const getUserPosts = async (
  userId: number,
  skip: number = 0,
  limit: number = 20
): Promise<any[]> => {
  return http.get(`/users/${userId}/posts`, {
    params: { skip, limit }
  })
}

// 获取用户列表（管理员）
export const getUsers = async (
  skip: number = 0,
  limit: number = 100
): Promise<UserInfo[]> => {
  return http.get('/users/', {
    params: { skip, limit }
  })
}

// 获取用户详情（管理员）
export const getUserById = async (userId: number): Promise<UserInfo> => {
  return http.get(`/users/${userId}`)
}

// 添加用户（管理员）
export const createUser = async (data: UserCreate): Promise<UserInfo> => {
  return http.post('/users/', data)
}

// 更新用户角色（管理员）
export const updateUserRole = async (
  userId: number,
  data: UserRoleUpdate
): Promise<{ message: string }> => {
  return http.put(`/users/${userId}/role`, null, {
    params: data
  })
}

// 更新用户信息（管理员）
export const updateUser = async (userId: number, data: UserUpdate): Promise<UserInfo> => {
  return http.put(`/users/${userId}`, data)
}

// 删除用户（管理员）
export const deleteUser = async (userId: number): Promise<{ message: string }> => {
  return http.delete(`/users/${userId}`)
}
