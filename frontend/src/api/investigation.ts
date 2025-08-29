/**
 * 调查响应API接口
 */

import { http } from './request'
import type {
  InvestigationSession,
  PaginatedResponse,
  SearchParams,
  DateRangeParams,
  BatchOperation,
  BatchResponse,
  ExportRequest,
  ExportResponse
} from '@/types/api'

/**
 * 调查响应API接口
 */
export const investigationApi = {
  /**
   * 获取调查会话列表
   */
  getInvestigationSessions(params?: SearchParams & DateRangeParams & {
    status?: string
    priority?: string
    assigned_to?: number
  }): Promise<PaginatedResponse<InvestigationSession>> {
    return http.get('/investigation/sessions', { params })
  },

  /**
   * 获取调查会话详情
   */
  getInvestigationSession(id: number): Promise<InvestigationSession & {
    timeline: Array<{
      id: number
      timestamp: string
      event_type: string
      description: string
      user_id: number
      user_name: string
      data?: any
    }>
    evidence: Array<{
      id: number
      name: string
      type: string
      file_path?: string
      description?: string
      hash?: string
      collected_at: string
      collected_by: string
    }>
    related_alerts: Array<{
      id: number
      alert_name: string
      severity: string
      created_at: string
    }>
    related_assets: Array<{
      id: number
      name: string
      ip_address: string
      asset_type: string
    }>
  }> {
    return http.get(`/investigation/sessions/${id}`)
  },

  /**
   * 创建调查会话
   */
  createInvestigationSession(data: {
    title: string
    description?: string
    priority: string
    alert_ids?: number[]
    asset_ids?: number[]
    assigned_to?: number
    tags?: string[]
  }): Promise<InvestigationSession> {
    return http.post('/investigation/sessions', data)
  },

  /**
   * 更新调查会话
   */
  updateInvestigationSession(id: number, data: {
    title?: string
    description?: string
    priority?: string
    status?: string
    assigned_to?: number
    tags?: string[]
    conclusion?: string
  }): Promise<InvestigationSession> {
    return http.put(`/investigation/sessions/${id}`, data)
  },

  /**
   * 删除调查会话
   */
  deleteInvestigationSession(id: number): Promise<void> {
    return http.delete(`/investigation/sessions/${id}`)
  },

  /**
   * 添加调查笔记
   */
  addInvestigationNote(sessionId: number, data: {
    content: string
    note_type?: string
    is_private?: boolean
  }): Promise<{
    id: number
    message: string
  }> {
    return http.post(`/investigation/sessions/${sessionId}/notes`, data)
  },

  /**
   * 上传证据文件
   */
  uploadEvidence(sessionId: number, file: File, description?: string): Promise<{
    id: number
    name: string
    file_path: string
    hash: string
    message: string
  }> {
    const formData = new FormData()
    formData.append('file', file)
    if (description) {
      formData.append('description', description)
    }

    return http.post(`/investigation/sessions/${sessionId}/evidence`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * 批量操作调查会话
   */
  batchOperation(operation: BatchOperation): Promise<BatchResponse> {
    return http.post('/investigation/sessions/batch', operation)
  },

  /**
   * 获取调查统计信息
   */
  getInvestigationStatistics(): Promise<{
    total_sessions: number
    active_sessions: number
    completed_sessions: number
    archived_sessions: number
    by_priority: Record<string, number>
    by_status: Record<string, number>
    avg_resolution_time: number
    total_evidence: number
  }> {
    return http.get('/investigation/statistics')
  },

  /**
   * 获取调查模板列表
   */
  getInvestigationTemplates(params?: SearchParams): Promise<PaginatedResponse<{
    id: number
    name: string
    description?: string
    category: string
    checklist: Array<{
      id: number
      title: string
      description?: string
      required: boolean
      completed?: boolean
    }>
    created_at: string
    created_by: string
  }>> {
    return http.get('/investigation/templates', { params })
  },

  /**
   * 应用调查模板
   */
  applyInvestigationTemplate(sessionId: number, templateId: number): Promise<{
    success: boolean
    message: string
    checklist_items: number
  }> {
    return http.post(`/investigation/sessions/${sessionId}/apply-template`, {
      template_id: templateId
    })
  },

  /**
   * 导出调查报告
   */
  exportInvestigationReport(sessionId: number, format: 'pdf' | 'docx' | 'html'): Promise<ExportResponse> {
    return http.post(`/investigation/sessions/${sessionId}/export`, { format })
  },

  /**
   * 下载调查报告
   */
  downloadInvestigationReport(taskId: string): Promise<Blob> {
    return http.get(`/investigation/export/${taskId}/download`, {
      responseType: 'blob'
    })
  },

  /**
   * 搜索调查会话
   */
  searchInvestigationSessions(query: string, filters?: {
    status?: string[]
    priority?: string[]
    assigned_to?: number[]
    date_range?: {
      start: string
      end: string
    }
  }): Promise<{
    sessions: InvestigationSession[]
    total_results: number
  }> {
    return http.post('/investigation/search', { query, filters })
  }
}
