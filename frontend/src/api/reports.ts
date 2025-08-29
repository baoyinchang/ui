/**
 * 报告中心API接口
 */

import { http } from './request'
import type {
  Report,
  ReportTemplate,
  PaginatedResponse,
  SearchParams,
  DateRangeParams,
  BatchOperation,
  BatchResponse,
  ExportRequest,
  ExportResponse
} from '@/types/api'

/**
 * 报告中心API接口
 */
export const reportsApi = {
  /**
   * 获取报告列表
   */
  getReports(params?: SearchParams & DateRangeParams & {
    report_type?: string
    status?: string
    created_by?: number
    template_id?: number
  }): Promise<PaginatedResponse<Report>> {
    return http.get('/reports', { params })
  },

  /**
   * 获取报告详情
   */
  getReport(id: number): Promise<Report & {
    content: string
    charts: Array<{
      id: string
      type: string
      title: string
      data: any
      config: any
    }>
    attachments: Array<{
      id: number
      name: string
      file_path: string
      file_size: number
      uploaded_at: string
    }>
  }> {
    return http.get(`/reports/${id}`)
  },

  /**
   * 创建报告
   */
  createReport(data: {
    title: string
    description?: string
    report_type: string
    template_id?: number
    parameters?: Record<string, any>
    schedule?: {
      enabled: boolean
      frequency?: string
      cron_expression?: string
      recipients?: string[]
    }
    tags?: string[]
  }): Promise<Report> {
    return http.post('/reports', data)
  },

  /**
   * 更新报告
   */
  updateReport(id: number, data: {
    title?: string
    description?: string
    content?: string
    status?: string
    parameters?: Record<string, any>
    schedule?: {
      enabled: boolean
      frequency?: string
      cron_expression?: string
      recipients?: string[]
    }
    tags?: string[]
  }): Promise<Report> {
    return http.put(`/reports/${id}`, data)
  },

  /**
   * 删除报告
   */
  deleteReport(id: number): Promise<void> {
    return http.delete(`/reports/${id}`)
  },

  /**
   * 生成报告
   */
  generateReport(id: number, parameters?: Record<string, any>): Promise<{
    task_id: string
    message: string
  }> {
    return http.post(`/reports/${id}/generate`, { parameters })
  },

  /**
   * 获取报告生成状态
   */
  getReportGenerationStatus(taskId: string): Promise<{
    status: string
    progress: number
    message: string
    completed_at?: string
    download_url?: string
  }> {
    return http.get(`/reports/generation/${taskId}`)
  },

  /**
   * 下载报告
   */
  downloadReport(id: number, format?: 'pdf' | 'html' | 'docx' | 'xlsx'): Promise<Blob> {
    return http.get(`/reports/${id}/download`, {
      params: { format },
      responseType: 'blob'
    })
  },

  /**
   * 预览报告
   */
  previewReport(id: number): Promise<{
    html_content: string
    charts: Array<{
      id: string
      type: string
      title: string
      data: any
    }>
  }> {
    return http.get(`/reports/${id}/preview`)
  },

  /**
   * 发送报告
   */
  sendReport(id: number, data: {
    recipients: string[]
    subject?: string
    message?: string
    format?: 'pdf' | 'html' | 'docx'
    include_attachments?: boolean
  }): Promise<{
    success: boolean
    message: string
    sent_count: number
  }> {
    return http.post(`/reports/${id}/send`, data)
  },

  /**
   * 批量操作报告
   */
  batchOperation(operation: BatchOperation): Promise<BatchResponse> {
    return http.post('/reports/batch', operation)
  },

  /**
   * 获取报告模板列表
   */
  getReportTemplates(params?: SearchParams & {
    category?: string
    report_type?: string
  }): Promise<PaginatedResponse<ReportTemplate>> {
    return http.get('/reports/templates', { params })
  },

  /**
   * 获取报告模板详情
   */
  getReportTemplate(id: number): Promise<ReportTemplate & {
    template_content: string
    sample_data: any
    parameters: Array<{
      name: string
      type: string
      label: string
      description?: string
      required: boolean
      default_value?: any
      options?: Array<{
        label: string
        value: any
      }>
    }>
  }> {
    return http.get(`/reports/templates/${id}`)
  },

  /**
   * 创建报告模板
   */
  createReportTemplate(data: {
    name: string
    description?: string
    category: string
    report_type: string
    template_content: string
    parameters: Array<{
      name: string
      type: string
      label: string
      description?: string
      required: boolean
      default_value?: any
      options?: Array<{
        label: string
        value: any
      }>
    }>
    tags?: string[]
  }): Promise<ReportTemplate> {
    return http.post('/reports/templates', data)
  },

  /**
   * 更新报告模板
   */
  updateReportTemplate(id: number, data: {
    name?: string
    description?: string
    category?: string
    template_content?: string
    parameters?: Array<{
      name: string
      type: string
      label: string
      description?: string
      required: boolean
      default_value?: any
      options?: Array<{
        label: string
        value: any
      }>
    }>
    tags?: string[]
  }): Promise<ReportTemplate> {
    return http.put(`/reports/templates/${id}`, data)
  },

  /**
   * 删除报告模板
   */
  deleteReportTemplate(id: number): Promise<void> {
    return http.delete(`/reports/templates/${id}`)
  },

  /**
   * 复制报告模板
   */
  cloneReportTemplate(id: number, name: string): Promise<ReportTemplate> {
    return http.post(`/reports/templates/${id}/clone`, { name })
  },

  /**
   * 获取报告统计信息
   */
  getReportStatistics(): Promise<{
    total_reports: number
    generated_reports: number
    scheduled_reports: number
    failed_reports: number
    by_type: Record<string, number>
    by_status: Record<string, number>
    templates_count: number
    avg_generation_time: number
    total_downloads: number
  }> {
    return http.get('/reports/statistics')
  },

  /**
   * 获取报告趋势数据
   */
  getReportTrends(days: number = 30): Promise<{
    dates: string[]
    generated_counts: number[]
    download_counts: number[]
    by_type: Record<string, number[]>
  }> {
    return http.get('/reports/trends', { params: { days } })
  },

  /**
   * 获取报告调度任务列表
   */
  getReportSchedules(params?: SearchParams): Promise<PaginatedResponse<{
    id: number
    report_id: number
    report_title: string
    frequency: string
    cron_expression: string
    recipients: string[]
    last_run?: string
    next_run: string
    status: string
    is_active: boolean
    created_at: string
  }>> {
    return http.get('/reports/schedules', { params })
  },

  /**
   * 创建报告调度任务
   */
  createReportSchedule(data: {
    report_id: number
    frequency: string
    cron_expression?: string
    recipients: string[]
    parameters?: Record<string, any>
    is_active?: boolean
  }): Promise<{
    id: number
    message: string
  }> {
    return http.post('/reports/schedules', data)
  },

  /**
   * 更新报告调度任务
   */
  updateReportSchedule(id: number, data: {
    frequency?: string
    cron_expression?: string
    recipients?: string[]
    parameters?: Record<string, any>
    is_active?: boolean
  }): Promise<{ success: boolean; message: string }> {
    return http.put(`/reports/schedules/${id}`, data)
  },

  /**
   * 删除报告调度任务
   */
  deleteReportSchedule(id: number): Promise<void> {
    return http.delete(`/reports/schedules/${id}`)
  },

  /**
   * 手动执行调度任务
   */
  executeReportSchedule(id: number): Promise<{
    task_id: string
    message: string
  }> {
    return http.post(`/reports/schedules/${id}/execute`)
  }
}
