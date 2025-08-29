/**
 * 资产管理 API接口
 */

import { http } from '../request'
import type { PaginationParams, ApiResponse } from '@/types/api'

export interface AssetListParams extends PaginationParams {
  name?: string
  status?: string
  type?: string
}

export interface CreateAssetData {
  name: string
  description?: string
  type?: string
  status?: string
}

export interface UpdateAssetData {
  name?: string
  description?: string
  type?: string
  status?: string
}

export const assetApi = {
  /**
   * 获取资产列表
   */
  getList: (params: AssetListParams = {}) => {
    return http.get<ApiResponse<{
      items: any[]
      total: number
      page: number
      size: number
    }>>('/assets', { params })
  },

  /**
   * 获取资产详情
   */
  getById: (id: number) => {
    return http.get<ApiResponse<any>>(`/assets/${id}`)
  },

  /**
   * 创建资产
   */
  create: (data: CreateAssetData) => {
    return http.post<ApiResponse<any>>('/assets', data)
  },

  /**
   * 更新资产
   */
  update: (id: number, data: UpdateAssetData) => {
    return http.put<ApiResponse<any>>(`/assets/${id}`, data)
  },

  /**
   * 删除资产
   */
  delete: (id: number) => {
    return http.delete<ApiResponse<null>>(`/assets/${id}`)
  },

  /**
   * 批量删除资产
   */
  batchDelete: (ids: number[]) => {
    return http.post<ApiResponse<null>>('/assets/batch-delete', { ids })
  }
}