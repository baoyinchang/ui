// src/api/modules/compliance.ts
import { http } from '../request'
import type { PaginationParams, ApiResponse } from '@/types/api'

// 合规检查项参数
export interface ComplianceCheckParams extends PaginationParams {
  assetId?: number
  severity?: string
  status?: string // 合规/不合规
}

// 合规检查项响应
export interface ComplianceItem {
  id: number
  checkId: string
  description: string
  severity: string
  policy: string
  status: 'compliant' | 'non-compliant'
  assetId: number
  assetName: string
  checkedAt: string
}

export const complianceApi = {
  /**
   * 获取合规检查项列表
   */
  getList: (params: ComplianceCheckParams = {}) => {
    return http.get<ApiResponse<{
      items: ComplianceItem[]
      total: number
      page: number
      size: number
    }>>('/compliance/checks', { params })
  },

  /**
   * 获取资产合规详情
   */
  getAssetCompliance: (assetId: number) => {
    return http.get<ApiResponse<{
      complianceRate: number
      totalChecks: number
      passedChecks: number
      failedChecks: number
      items: ComplianceItem[]
    }>>(`/assets/${assetId}/compliance`)
  },

  /**
   * 重新执行合规检查
   */
  recheck: (assetId: number) => {
    return http.post<ApiResponse<{
      taskId: string
      message: string
    }>>(`/assets/${assetId}/compliance/recheck`)
  }
}