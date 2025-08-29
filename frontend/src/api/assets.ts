/**
 * 资产管理API接口
 */

import { http } from './request'
import type {
  Asset,
  AssetStatistics,
  CreateAssetRequest,
  UpdateAssetRequest,
  AssetQueryParams,
  PaginatedResponse,
  BatchOperation,
  BatchResponse,
  ExportRequest,
  ExportResponse
} from '@/types/api'

/**
 * 资产管理API接口
 */
export const assetsApi = {
  /**
   * 获取资产列表
   */
  getAssets(params?: AssetQueryParams): Promise<PaginatedResponse<Asset>> {
    return http.get('/assets', { params })
  },

  /**
   * 获取资产详情
   */
  getAsset(id: number): Promise<Asset & {
    vulnerabilities: any[]
    compliance_results: any[]
    recent_alerts: any[]
  }> {
    return http.get(`/assets/${id}`)
  },

  /**
   * 创建资产
   */
  createAsset(data: CreateAssetRequest): Promise<Asset> {
    return http.post('/assets', data)
  },

  /**
   * 更新资产信息
   */
  updateAsset(id: number, data: UpdateAssetRequest): Promise<Asset> {
    return http.put(`/assets/${id}`, data)
  },

  /**
   * 删除资产
   */
  deleteAsset(id: number): Promise<void> {
    return http.delete(`/assets/${id}`)
  },

  /**
   * 批量操作资产
   */
  batchOperation(operation: BatchOperation): Promise<BatchResponse> {
    return http.post('/assets/batch', operation)
  },

  /**
   * 获取资产统计信息
   */
  getAssetStatistics(): Promise<AssetStatistics> {
    return http.get('/assets/statistics')
  },

  /**
   * 获取资产状态分布
   */
  getAssetStatusDistribution(): Promise<{
    normal: number
    warning: number
    danger: number
    offline: number
  }> {
    return http.get('/assets/status-distribution')
  },

  /**
   * 扫描资产漏洞
   */
  scanAssetVulnerabilities(id: number): Promise<{
    task_id: string
    message: string
  }> {
    return http.post(`/assets/${id}/scan`)
  },

  /**
   * 获取资产漏洞列表
   */
  getAssetVulnerabilities(id: number, params?: {
    severity?: string
    status?: string
    page?: number
    size?: number
  }): Promise<PaginatedResponse<{
    id: number
    cve_id: string
    title: string
    severity: string
    score: number
    status: string
    description: string
    solution?: string
    discovered_at: string
  }>> {
    return http.get(`/assets/${id}/vulnerabilities`, { params })
  },

  /**
   * 资产心跳检测
   */
  pingAsset(id: number): Promise<{
    success: boolean
    response_time?: number
    message: string
  }> {
    return http.post(`/assets/${id}/ping`)
  },

  /**
   * 导入资产
   */
  importAssets(file: File): Promise<{
    success_count: number
    failed_count: number
    errors?: string[]
  }> {
    const formData = new FormData()
    formData.append('file', file)

    return http.post('/assets/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * 导出资产数据
   */
  exportAssets(request: ExportRequest): Promise<ExportResponse> {
    return http.post('/assets/export', request)
  },

  /**
   * 下载导出文件
   */
  downloadExport(taskId: string): Promise<Blob> {
    return http.get(`/assets/export/${taskId}/download`, {
      responseType: 'blob'
    })
  },

  /**
   * 自动发现资产
   */
  discoverAssets(params: {
    ip_range: string
    scan_ports?: number[]
    timeout?: number
  }): Promise<{
    task_id: string
    message: string
  }> {
    return http.post('/assets/discover', params)
  },

  /**
   * 获取资产发现状态
   */
  getDiscoveryStatus(taskId: string): Promise<{
    status: string
    progress: number
    discovered_count: number
    total_ips: number
    message: string
  }> {
    return http.get(`/assets/discover/${taskId}`)
  }
}
