/**
 * 用户管理API接口
 */

import { http } from './request'
import type {
  User,
  UserStatistics,
  CreateUserRequest,
  UpdateUserRequest,
  ChangePasswordRequest,
  ResetPasswordRequest,
  PaginatedResponse,
  UserQueryParams,
  BatchOperation,
  BatchResponse
} from '@/types/api'

/**
 * 用户API接口
 */
export const usersApi = {
  /**
   * 获取用户列表
   */
  getUsers(params?: UserQueryParams): Promise<PaginatedResponse<User>> {
    return http.get('/users', { params })
  },

  /**
   * 获取用户详情
   */
  getUserById(id: number): Promise<User> {
    return http.get(`/users/${id}`)
  },

  /**
   * 创建用户
   */
  createUser(data: CreateUserRequest): Promise<User> {
    return http.post('/users', data)
  },

  /**
   * 更新用户信息
   */
  updateUser(id: number, data: UpdateUserRequest): Promise<User> {
    return http.put(`/users/${id}`, data)
  },

  /**
   * 删除用户
   */
  deleteUser(id: number): Promise<void> {
    return http.delete(`/users/${id}`)
  },

  /**
   * 启用/禁用用户
   */
  toggleUserStatus(id: number, is_active: boolean): Promise<User> {
    return http.patch(`/users/${id}/status`, { is_active })
  },

  /**
   * 重置用户密码
   */
  resetUserPassword(id: number): Promise<{ new_password: string }> {
    return http.post(`/users/${id}/reset-password`)
  },

  /**
   * 修改密码
   */
  changePassword(data: ChangePasswordRequest): Promise<void> {
    return http.post('/users/change-password', data)
  },

  /**
   * 忘记密码
   */
  forgotPassword(data: ResetPasswordRequest): Promise<void> {
    return http.post('/users/forgot-password', data)
  },

  /**
   * 获取用户统计信息
   */
  getUserStatistics(): Promise<UserStatistics> {
    return http.get('/users/statistics')
  },

  /**
   * 批量操作用户
   */
  batchOperation(operation: BatchOperation): Promise<BatchResponse> {
    return http.post('/users/batch', operation)
  },

  /**
   * 获取当前用户信息
   */
  getCurrentUser(): Promise<User> {
    return http.get('/users/me')
  },

  /**
   * 更新当前用户信息
   */
  updateCurrentUser(data: Partial<UpdateUserRequest>): Promise<User> {
    return http.put('/users/me', data)
  },

  /**
   * 上传用户头像
   */
  uploadAvatar(file: File): Promise<{ avatar_url: string }> {
    const formData = new FormData()
    formData.append('avatar', file)
    
    return http.post('/users/me/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * 获取用户角色列表
   */
  getUserRoles(): Promise<Array<{ value: string; label: string }>> {
    return http.get('/users/roles')
  },

  /**
   * 检查用户名是否可用
   */
  checkUsername(username: string): Promise<{ available: boolean }> {
    return http.get('/users/check-username', { params: { username } })
  },

  /**
   * 检查邮箱是否可用
   */
  checkEmail(email: string): Promise<{ available: boolean }> {
    return http.get('/users/check-email', { params: { email } })
  }
}
