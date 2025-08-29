/**
 * 事件管理 API接口
 */

import { http } from '../request'
import type { PaginationParams, ApiResponse } from '@/types/api'

export interface IncidentListParams extends PaginationParams {
  name?: string
  status?: string
  type?: string
}

export interface CreateIncidentData {
  name: string
  description?: string
  type?: string
  status?: string
}

export interface UpdateIncidentData {
  name?: string
  description?: string
  type?: string
  status?: string
}

export const incidentApi = {
  /**
   * 获取事件列表
   */
  getList: (params: IncidentListParams = {}) => {
    return http.get<ApiResponse<{
      items: any[]
      total: number
      page: number
      size: number
    }>>('/incidents', { params })
  },

  /**
   * 获取事件详情
   */
  getById: (id: number) => {
    return http.get<ApiResponse<any>>(`/incidents/${id}`)
  },

  /**
   * 创建事件
   */
  create: (data: CreateIncidentData) => {
    return http.post<ApiResponse<any>>('/incidents', data)
  },

  /**
   * 更新事件
   */
  update: (id: number, data: UpdateIncidentData) => {
    return http.put<ApiResponse<any>>(`/incidents/${id}`, data)
  },

  /**
   * 删除事件
   */
  delete: (id: number) => {
    return http.delete<ApiResponse<null>>(`/incidents/${id}`)
  },

  /**
   * 批量删除事件
   */
  batchDelete: (ids: number[]) => {
    return http.post<ApiResponse<null>>('/incidents/batch-delete', { ids })
  }
}