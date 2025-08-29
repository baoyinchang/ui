/**
 * 系统设置API接口
 */

import { http } from './request'
import type {
  SystemSettings,
  BasicSettings,
  SecuritySettings,
  EmailSettings,
  MonitoringSettings,
  BackupSettings
} from '@/types/api'

/**
 * 系统设置API接口
 */
export const settingsApi = {
  /**
   * 获取所有系统设置
   */
  getSettings(): Promise<SystemSettings> {
    return http.get('/settings')
  },

  /**
   * 更新系统设置
   */
  updateSettings(settings: Partial<SystemSettings>): Promise<SystemSettings> {
    return http.put('/settings', settings)
  },

  /**
   * 重置系统设置
   */
  resetSettings(): Promise<void> {
    return http.post('/settings/reset')
  },

  /**
   * 获取基本设置
   */
  getBasicSettings(): Promise<BasicSettings> {
    return http.get('/settings/basic')
  },

  /**
   * 更新基本设置
   */
  updateBasicSettings(settings: Partial<BasicSettings>): Promise<BasicSettings> {
    return http.put('/settings/basic', settings)
  },

  /**
   * 获取安全设置
   */
  getSecuritySettings(): Promise<SecuritySettings> {
    return http.get('/settings/security')
  },

  /**
   * 更新安全设置
   */
  updateSecuritySettings(settings: Partial<SecuritySettings>): Promise<SecuritySettings> {
    return http.put('/settings/security', settings)
  },

  /**
   * 获取邮件设置
   */
  getEmailSettings(): Promise<EmailSettings> {
    return http.get('/settings/email')
  },

  /**
   * 更新邮件设置
   */
  updateEmailSettings(settings: Partial<EmailSettings>): Promise<EmailSettings> {
    return http.put('/settings/email', settings)
  },

  /**
   * 测试邮件配置
   */
  testEmail(settings: EmailSettings): Promise<{ success: boolean; message: string }> {
    return http.post('/settings/email/test', settings)
  },

  /**
   * 获取监控设置
   */
  getMonitoringSettings(): Promise<MonitoringSettings> {
    return http.get('/settings/monitoring')
  },

  /**
   * 更新监控设置
   */
  updateMonitoringSettings(settings: Partial<MonitoringSettings>): Promise<MonitoringSettings> {
    return http.put('/settings/monitoring', settings)
  },

  /**
   * 获取备份设置
   */
  getBackupSettings(): Promise<BackupSettings> {
    return http.get('/settings/backup')
  },

  /**
   * 更新备份设置
   */
  updateBackupSettings(settings: Partial<BackupSettings>): Promise<BackupSettings> {
    return http.put('/settings/backup', settings)
  },

  /**
   * 创建备份
   */
  createBackup(): Promise<{ task_id: string; message: string }> {
    return http.post('/settings/backup/create')
  },

  /**
   * 获取备份列表
   */
  getBackupList(): Promise<Array<{
    id: string
    filename: string
    size: number
    created_at: string
    status: string
  }>> {
    return http.get('/settings/backup/list')
  },

  /**
   * 恢复备份
   */
  restoreBackup(backupId: string): Promise<{ task_id: string; message: string }> {
    return http.post(`/settings/backup/restore/${backupId}`)
  },

  /**
   * 删除备份
   */
  deleteBackup(backupId: string): Promise<void> {
    return http.delete(`/settings/backup/${backupId}`)
  },

  /**
   * 下载备份文件
   */
  downloadBackup(backupId: string): Promise<Blob> {
    return http.get(`/settings/backup/download/${backupId}`, {
      responseType: 'blob'
    })
  },

  /**
   * 获取系统日志配置
   */
  getLogConfig(): Promise<{
    level: string
    retention_days: number
    max_file_size: number
    max_files: number
  }> {
    return http.get('/settings/logs/config')
  },

  /**
   * 更新系统日志配置
   */
  updateLogConfig(config: {
    level?: string
    retention_days?: number
    max_file_size?: number
    max_files?: number
  }): Promise<void> {
    return http.put('/settings/logs/config', config)
  },

  /**
   * 清理系统日志
   */
  cleanupLogs(days?: number): Promise<{ deleted_files: number; freed_space: number }> {
    return http.post('/settings/logs/cleanup', { days })
  },

  /**
   * 获取系统许可证信息
   */
  getLicenseInfo(): Promise<{
    license_key: string
    license_type: string
    expires_at: string
    max_users: number
    max_assets: number
    features: string[]
  }> {
    return http.get('/settings/license')
  },

  /**
   * 更新许可证
   */
  updateLicense(licenseKey: string): Promise<{ success: boolean; message: string }> {
    return http.post('/settings/license', { license_key: licenseKey })
  },

  /**
   * 获取系统版本信息
   */
  getVersionInfo(): Promise<{
    version: string
    build_date: string
    git_commit: string
    python_version: string
    dependencies: Record<string, string>
  }> {
    return http.get('/settings/version')
  },

  /**
   * 检查系统更新
   */
  checkUpdates(): Promise<{
    has_update: boolean
    latest_version?: string
    release_notes?: string
    download_url?: string
  }> {
    return http.get('/settings/updates/check')
  },

  /**
   * 导出系统配置
   */
  exportConfig(): Promise<Blob> {
    return http.get('/settings/export', {
      responseType: 'blob'
    })
  },

  /**
   * 导入系统配置
   */
  importConfig(file: File): Promise<{ success: boolean; message: string }> {
    const formData = new FormData()
    formData.append('config_file', file)
    
    return http.post('/settings/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}
