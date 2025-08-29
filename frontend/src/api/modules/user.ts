/**
 * 用户管理 API接口
 */

import { http } from '../request'
import type { User, PaginationParams, ApiResponse } from '@/types/api'

export interface UserListParams extends PaginationParams {
  username?: string
  email?: string
  role?: string
  is_active?: boolean
}

export interface CreateUserData {
  username: string
  email: string
  password: string
  full_name?: string
  role?: string
  is_active?: boolean
}

export interface UpdateUserData {
  email?: string
  full_name?: string
  role?: string
  is_active?: boolean
}

export interface ChangePasswordData {
  old_password: string
  new_password: string
}

export const userApi = {
  /**
   * 获取用户列表
   */
  getList: (params: UserListParams = {}) => {
    return http.get<ApiResponse<{
      items: User[]
      total: number
      page: number
      size: number
    }>>('/users', { params })
  },

  /**
   * 获取用户详情
   */
  getById: (id: number) => {
    return http.get<ApiResponse<User>>(`/users/${id}`)
  },

  /**
   * 获取当前用户信息
   */
  getCurrentUser: () => {
    return http.get<ApiResponse<User>>('/users/me')
  },

  /**
   * 创建用户
   */
  create: (data: CreateUserData) => {
    return http.post<ApiResponse<User>>('/users', data)
  },

  /**
   * 更新用户信息
   */
  update: (id: number, data: UpdateUserData) => {
    return http.put<ApiResponse<User>>(`/users/${id}`, data)
  },

  /**
   * 删除用户
   */
  delete: (id: number) => {
    return http.delete<ApiResponse<null>>(`/users/${id}`)
  },

  /**
   * 批量删除用户
   */
  batchDelete: (ids: number[]) => {
    return http.post<ApiResponse<null>>('/users/batch-delete', { ids })
  },

  /**
   * 启用/禁用用户
   */
  toggleStatus: (id: number, is_active: boolean) => {
    return http.patch<ApiResponse<User>>(`/users/${id}/status`, { is_active })
  },

  /**
   * 修改密码
   */
  changePassword: (data: ChangePasswordData) => {
    return http.post<ApiResponse<null>>('/users/change-password', data)
  },

  /**
   * 重置用户密码
   */
  resetPassword: (id: number) => {
    return http.post<ApiResponse<{ new_password: string }>>(`/users/${id}/reset-password`)
  },

  /**
   * 获取用户权限
   */
  getPermissions: (id: number) => {
    return http.get<ApiResponse<{
      permissions: string[]
      roles: string[]
    }>>(`/users/${id}/permissions`)
  },

  /**
   * 更新用户权限
   */
  updatePermissions: (id: number, data: { permissions: string[], roles: string[] }) => {
    return http.post<ApiResponse<null>>(`/users/${id}/permissions`, data)
  }
}
