/**
 * 威胁情报API接口
 */

import { http } from './request'
import type {
  IOC,
  PaginatedResponse,
  IOCQueryParams,
  SearchParams,
  BatchOperation,
  BatchResponse,
  ExportRequest,
  ExportResponse
} from '@/types/api'

/**
 * 威胁情报API接口
 */
export const intelligenceApi = {
  /**
   * 获取IOC列表
   */
  getIOCs(params?: IOCQueryParams): Promise<PaginatedResponse<IOC>> {
    return http.get('/intelligence/iocs', { params })
  },

  /**
   * 获取IOC详情
   */
  getIOC(id: number): Promise<IOC & {
    related_iocs: IOC[]
    detection_rules: Array<{
      id: number
      name: string
      rule_type: string
      content: string
    }>
    threat_context: {
      campaigns?: string[]
      malware_families?: string[]
      threat_actors?: string[]
      attack_techniques?: string[]
    }
  }> {
    return http.get(`/intelligence/iocs/${id}`)
  },

  /**
   * 创建IOC
   */
  createIOC(data: {
    ioc_type: string
    ioc_value: string
    threat_type?: string
    severity: string
    confidence: number
    description?: string
    source?: string
    tags?: string[]
    expiry_date?: string
    is_active?: boolean
  }): Promise<IOC> {
    return http.post('/intelligence/iocs', data)
  },

  /**
   * 更新IOC
   */
  updateIOC(id: number, data: {
    threat_type?: string
    severity?: string
    confidence?: number
    description?: string
    source?: string
    tags?: string[]
    expiry_date?: string
    is_active?: boolean
  }): Promise<IOC> {
    return http.put(`/intelligence/iocs/${id}`, data)
  },

  /**
   * 删除IOC
   */
  deleteIOC(id: number): Promise<void> {
    return http.delete(`/intelligence/iocs/${id}`)
  },

  /**
   * 批量操作IOC
   */
  batchOperation(operation: BatchOperation): Promise<BatchResponse> {
    return http.post('/intelligence/iocs/batch', operation)
  },

  /**
   * 查询IOC
   */
  queryIOC(value: string, iocType?: string): Promise<{
    found: boolean
    ioc?: IOC
    matches: Array<{
      source: string
      confidence: number
      last_seen: string
      threat_types: string[]
    }>
  }> {
    return http.get('/intelligence/iocs/query', {
      params: { value, ioc_type: iocType }
    })
  },

  /**
   * 获取IOC统计信息
   */
  getIOCStatistics(): Promise<{
    total: number
    active: number
    expired: number
    by_type: Record<string, number>
    by_severity: Record<string, number>
    by_source: Record<string, number>
    recent_additions: number
    avg_confidence: number
  }> {
    return http.get('/intelligence/iocs/statistics')
  },

  /**
   * 获取威胁情报源列表
   */
  getThreatFeeds(params?: SearchParams): Promise<PaginatedResponse<{
    id: number
    name: string
    description?: string
    feed_type: string
    url?: string
    api_key?: string
    update_frequency: number
    last_update: string
    status: string
    ioc_count: number
    is_active: boolean
    created_at: string
  }>> {
    return http.get('/intelligence/feeds', { params })
  },

  /**
   * 创建威胁情报源
   */
  createThreatFeed(data: {
    name: string
    description?: string
    feed_type: string
    url?: string
    api_key?: string
    update_frequency: number
    is_active?: boolean
    config?: Record<string, any>
  }): Promise<{
    id: number
    message: string
  }> {
    return http.post('/intelligence/feeds', data)
  },

  /**
   * 手动更新威胁情报源
   */
  updateThreatFeedManually(id: number): Promise<{
    task_id: string
    message: string
  }> {
    return http.post(`/intelligence/feeds/${id}/update`)
  },

  /**
   * 获取威胁情报趋势
   */
  getThreatTrends(days: number = 30): Promise<{
    dates: string[]
    new_iocs: number[]
    by_type: Record<string, number[]>
    by_severity: Record<string, number[]>
    top_sources: Array<{
      name: string
      count: number
    }>
  }> {
    return http.get('/intelligence/trends', { params: { days } })
  },

  /**
   * 导入IOC数据
   */
  importIOCs(file: File, format: 'csv' | 'json' | 'stix'): Promise<{
    success_count: number
    failed_count: number
    duplicate_count: number
    errors?: string[]
  }> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('format', format)

    return http.post('/intelligence/iocs/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * 导出IOC数据
   */
  exportIOCs(request: ExportRequest): Promise<ExportResponse> {
    return http.post('/intelligence/iocs/export', request)
  },

  /**
   * 下载导出文件
   */
  downloadExport(taskId: string): Promise<Blob> {
    return http.get(`/intelligence/iocs/export/${taskId}/download`, {
      responseType: 'blob'
    })
  },

  /**
   * 搜索威胁情报
   */
  searchThreatIntelligence(query: string, filters?: {
    ioc_types?: string[]
    severity?: string[]
    sources?: string[]
    date_range?: {
      start: string
      end: string
    }
  }): Promise<{
    iocs: IOC[]
    activities: any[]
    campaigns: any[]
    total_results: number
  }> {
    return http.post('/intelligence/search', { query, filters })
  }
}
