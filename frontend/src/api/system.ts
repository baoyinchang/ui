/**
 * 系统管理API接口
 */

import { http } from './request'
import type { SystemInfo, SystemStatus, HealthCheckResponse } from '@/types/api'

/**
 * 系统管理API接口
 */
export const systemApi = {
  /**
   * 系统健康检查
   */
  healthCheck(): Promise<HealthCheckResponse> {
    return http.get('/system/health')
  },

  /**
   * 获取系统信息
   */
  getSystemInfo(): Promise<SystemInfo> {
    return http.get('/system/info')
  },

  /**
   * 获取系统状态
   */
  getSystemStatus(): Promise<SystemStatus> {
    return http.get('/system/status')
  },

  /**
   * 获取系统日志
   */
  getSystemLogs(params?: {
    level?: string
    module?: string
    start_date?: string
    end_date?: string
    page?: number
    size?: number
  }): Promise<{
    items: Array<{
      id: number
      timestamp: string
      level: string
      module: string
      message: string
      details?: any
    }>
    total: number
  }> {
    return http.get('/system/logs', { params })
  },

  /**
   * 清理系统日志
   */
  cleanupLogs(days?: number): Promise<{
    deleted_files: number
    freed_space: number
  }> {
    return http.post('/system/logs/cleanup', { days })
  },

  /**
   * 获取系统性能指标
   */
  getPerformanceMetrics(timeRange?: string): Promise<{
    cpu_usage: number[]
    memory_usage: number[]
    disk_usage: number[]
    network_io: { in: number[]; out: number[] }
    timestamps: string[]
  }> {
    return http.get('/system/metrics', { params: { time_range: timeRange } })
  },

  /**
   * 获取系统进程列表
   */
  getProcessList(): Promise<Array<{
    pid: number
    name: string
    cpu_percent: number
    memory_percent: number
    status: string
    create_time: string
  }>> {
    return http.get('/system/processes')
  },

  /**
   * 终止系统进程
   */
  killProcess(pid: number): Promise<{ success: boolean; message: string }> {
    return http.post(`/system/processes/${pid}/kill`)
  },

  /**
   * 重启系统服务
   */
  restartService(serviceName: string): Promise<{ success: boolean; message: string }> {
    return http.post(`/system/services/${serviceName}/restart`)
  },

  /**
   * 获取系统服务状态
   */
  getServiceStatus(serviceName?: string): Promise<Record<string, {
    status: string
    pid?: number
    uptime?: number
    memory_usage?: number
    cpu_usage?: number
  }>> {
    const url = serviceName ? `/system/services/${serviceName}` : '/system/services'
    return http.get(url)
  },

  /**
   * 启动系统服务
   */
  startService(serviceName: string): Promise<{ success: boolean; message: string }> {
    return http.post(`/system/services/${serviceName}/start`)
  },

  /**
   * 停止系统服务
   */
  stopService(serviceName: string): Promise<{ success: boolean; message: string }> {
    return http.post(`/system/services/${serviceName}/stop`)
  },

  /**
   * 获取系统配置
   */
  getSystemConfig(): Promise<Record<string, any>> {
    return http.get('/system/config')
  },

  /**
   * 更新系统配置
   */
  updateSystemConfig(config: Record<string, any>): Promise<{ success: boolean; message: string }> {
    return http.put('/system/config', config)
  },

  /**
   * 重启系统
   */
  restartSystem(): Promise<{ success: boolean; message: string }> {
    return http.post('/system/restart')
  },

  /**
   * 关闭系统
   */
  shutdownSystem(): Promise<{ success: boolean; message: string }> {
    return http.post('/system/shutdown')
  },

  /**
   * 获取系统更新信息
   */
  checkUpdates(): Promise<{
    has_update: boolean
    current_version: string
    latest_version?: string
    release_notes?: string
    download_url?: string
  }> {
    return http.get('/system/updates/check')
  },

  /**
   * 执行系统更新
   */
  performUpdate(): Promise<{ task_id: string; message: string }> {
    return http.post('/system/updates/perform')
  },

  /**
   * 获取更新状态
   */
  getUpdateStatus(taskId: string): Promise<{
    status: string
    progress: number
    message: string
    completed_at?: string
  }> {
    return http.get(`/system/updates/status/${taskId}`)
  }
}
