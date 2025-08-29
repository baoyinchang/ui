/**
 * 威胁狩猎API接口
 */

import { http } from './request'
import type {
  HuntingTask,
  HuntingTemplate,
  PaginatedResponse,
  SearchParams,
  DateRangeParams,
  BatchOperation,
  BatchResponse,
  ExportRequest,
  ExportResponse
} from '@/types/api'

/**
 * 威胁狩猎API接口
 */
export const huntingApi = {
  /**
   * 获取狩猎任务列表
   */
  getHuntingTasks(params?: SearchParams & DateRangeParams & {
    status?: string
    template_id?: number
  }): Promise<PaginatedResponse<HuntingTask>> {
    return http.get('/hunting/tasks', { params })
  },

  /**
   * 获取狩猎任务详情
   */
  getHuntingTask(id: number): Promise<HuntingTask & {
    results: any[]
    logs: Array<{
      timestamp: string
      level: string
      message: string
    }>
  }> {
    return http.get(`/hunting/tasks/${id}`)
  },

  /**
   * 创建狩猎任务
   */
  createHuntingTask(data: {
    name: string
    description?: string
    template_id?: number
    query: string
    time_range: {
      start: string
      end: string
    }
    target_assets?: number[]
  }): Promise<HuntingTask> {
    return http.post('/hunting/tasks', data)
  },

  /**
   * 更新狩猎任务
   */
  updateHuntingTask(id: number, data: {
    name?: string
    description?: string
    query?: string
    time_range?: {
      start: string
      end: string
    }
    target_assets?: number[]
  }): Promise<HuntingTask> {
    return http.put(`/hunting/tasks/${id}`, data)
  },

  /**
   * 执行狩猎任务
   */
  executeHuntingTask(id: number): Promise<{
    task_id: string
    message: string
  }> {
    return http.post(`/hunting/tasks/${id}/execute`)
  },

  /**
   * 停止狩猎任务
   */
  stopHuntingTask(id: number): Promise<{
    success: boolean
    message: string
  }> {
    return http.post(`/hunting/tasks/${id}/stop`)
  },

  /**
   * 删除狩猎任务
   */
  deleteHuntingTask(id: number): Promise<void> {
    return http.delete(`/hunting/tasks/${id}`)
  },

  /**
   * 批量操作狩猎任务
   */
  batchOperation(operation: BatchOperation): Promise<BatchResponse> {
    return http.post('/hunting/tasks/batch', operation)
  },

  /**
   * 获取狩猎模板列表
   */
  getHuntingTemplates(params?: SearchParams): Promise<PaginatedResponse<HuntingTemplate>> {
    return http.get('/hunting/templates', { params })
  },

  /**
   * 获取狩猎模板详情
   */
  getHuntingTemplate(id: number): Promise<HuntingTemplate> {
    return http.get(`/hunting/templates/${id}`)
  },

  /**
   * 创建狩猎模板
   */
  createHuntingTemplate(data: {
    name: string
    description?: string
    category: string
    query_template: string
    parameters: Array<{
      name: string
      type: string
      description?: string
      default_value?: any
      required: boolean
    }>
    tags?: string[]
  }): Promise<HuntingTemplate> {
    return http.post('/hunting/templates', data)
  },

  /**
   * 删除狩猎模板
   */
  deleteHuntingTemplate(id: number): Promise<void> {
    return http.delete(`/hunting/templates/${id}`)
  },

  /**
   * 验证狩猎查询
   */
  validateQuery(query: string): Promise<{
    valid: boolean
    error?: string
    estimated_results?: number
  }> {
    return http.post('/hunting/validate-query', { query })
  },

  /**
   * 获取狩猎统计信息
   */
  getHuntingStatistics(): Promise<{
    total_tasks: number
    running_tasks: number
    completed_tasks: number
    failed_tasks: number
    total_results: number
    high_severity_results: number
    templates_count: number
    avg_execution_time: number
  }> {
    return http.get('/hunting/statistics')
  },

  /**
   * 导出狩猎结果
   */
  exportHuntingResults(request: ExportRequest & {
    task_id?: number
  }): Promise<ExportResponse> {
    return http.post('/hunting/export', request)
  },

  /**
   * 下载导出文件
   */
  downloadExport(taskId: string): Promise<Blob> {
    return http.get(`/hunting/export/${taskId}/download`, {
      responseType: 'blob'
    })
  },

  /**
   * 获取查询建议
   */
  getQuerySuggestions(partial: string): Promise<Array<{
    text: string
    description: string
    category: string
  }>> {
    return http.get('/hunting/query-suggestions', { params: { q: partial } })
  }
}
