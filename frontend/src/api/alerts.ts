/**
 * 告警管理API接口
 */

import { http } from './request'
import type {
  Alert,
  AlertRule,
  AlertStatistics,
  HandleAlertRequest,
  CreateAlertRuleRequest,
  AlertQueryParams,
  PaginatedResponse,
  BatchOperation,
  BatchResponse,
  ExportRequest,
  ExportResponse
} from '@/types/api'

/**
 * 告警API接口
 */
export const alertsApi = {
  /**
   * 获取告警列表
   */
  getAlerts(params?: AlertQueryParams): Promise<PaginatedResponse<Alert>> {
    return http.get('/alerts', { params })
  },
  
  /**
   * 获取告警详情
   */
  getAlert(id: number): Promise<Alert> {
    return http.get(`/alerts/${id}`)
  },

  /**
   * 创建告警
   */
  createAlert(data: {
    alert_name: string
    severity: string
    description?: string
    asset_id: number
    event_id?: number
  }): Promise<Alert> {
    return http.post('/alerts', data)
  },

  /**
   * 处理告警
   */
  handleAlert(id: number, data: HandleAlertRequest): Promise<Alert> {
    return http.put(`/alerts/${id}/handle`, data)
  },

  /**
   * 批量处理告警
   */
  batchHandleAlerts(operation: BatchOperation<HandleAlertRequest>): Promise<BatchResponse> {
    return http.post('/alerts/batch', operation)
  },

  /**
   * 删除告警
   */
  deleteAlert(id: number): Promise<void> {
    return http.delete(`/alerts/${id}`)
  },

  /**
   * 批量删除告警
   */
  batchDeleteAlerts(ids: number[]): Promise<BatchResponse> {
    return http.post('/alerts/batch', {
      action: 'delete',
      ids
    })
  },
  
  /**
   * 获取告警统计信息
   */
  getAlertStatistics(): Promise<AlertStatistics> {
    return http.get('/alerts/statistics')
  },

  /**
   * 获取告警趋势数据
   */
  getAlertTrends(days: number = 30): Promise<{
    dates: string[]
    counts: number[]
    severity_breakdown: Record<string, number[]>
  }> {
    return http.get('/alerts/trends', { params: { days } })
  },

  /**
   * 获取告警规则列表
   */
  getAlertRules(params?: {
    page?: number
    size?: number
    enabled?: boolean
    search?: string
  }): Promise<PaginatedResponse<AlertRule>> {
    return http.get('/alerts/rules', { params })
  },

  /**
   * 获取告警规则详情
   */
  getAlertRule(id: number): Promise<AlertRule> {
    return http.get(`/alerts/rules/${id}`)
  },

  /**
   * 创建告警规则
   */
  createAlertRule(data: CreateAlertRuleRequest): Promise<AlertRule> {
    return http.post('/alerts/rules', data)
  },

  /**
   * 更新告警规则
   */
  updateAlertRule(id: number, data: Partial<CreateAlertRuleRequest>): Promise<AlertRule> {
    return http.put(`/alerts/rules/${id}`, data)
  },

  /**
   * 删除告警规则
   */
  deleteAlertRule(id: number): Promise<void> {
    return http.delete(`/alerts/rules/${id}`)
  },

  /**
   * 启用/禁用告警规则
   */
  toggleAlertRule(id: number, enabled: boolean): Promise<AlertRule> {
    return http.patch(`/alerts/rules/${id}/toggle`, { enabled })
  },

  /**
   * 测试告警规则
   */
  testAlertRule(data: CreateAlertRuleRequest): Promise<{
    matched_events: number
    sample_events: any[]
    estimated_alerts: number
  }> {
    return http.post('/alerts/rules/test', data)
  },

  /**
   * 导出告警数据
   */
  exportAlerts(request: ExportRequest): Promise<ExportResponse> {
    return http.post('/alerts/export', request)
  },

  /**
   * 获取告警导出状态
   */
  getExportStatus(taskId: string): Promise<ExportResponse> {
    return http.get(`/alerts/export/${taskId}`)
  },

  /**
   * 下载告警导出文件
   */
  downloadExport(taskId: string): Promise<Blob> {
    return http.get(`/alerts/export/${taskId}/download`, {
      responseType: 'blob'
    })
  }
}
