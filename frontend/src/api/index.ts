/**
 * API模块入口文件
 * 统一导出所有API接口
 */

// 导出HTTP请求实例
export { http } from './request'

// 导入各个API模块
import { authApi } from './auth'
import { usersApi } from './users'
import { alertsApi } from './alerts'
import { systemApi } from './system'
import { settingsApi } from './settings'
import { assetsApi } from './assets'
import { huntingApi } from './hunting'
import { intelligenceApi } from './intelligence'
import { investigationApi } from './investigation'
import { reportsApi } from './reports'
import { dashboardApi } from './dashboard'

// 导出各个API模块
export { authApi } from './auth'
export { usersApi } from './users'
export { alertsApi } from './alerts'
export { systemApi } from './system'
export { settingsApi } from './settings'
export { assetsApi } from './assets'
export { huntingApi } from './hunting'
export { intelligenceApi } from './intelligence'
export { investigationApi } from './investigation'
export { reportsApi } from './reports'
export { dashboardApi } from './dashboard'

// 创建API实例的工厂函数
export const createApiInstance = () => {
  return {
    auth: authApi,
    users: usersApi,
    alerts: alertsApi,
    system: systemApi,
    settings: settingsApi,
    assets: assetsApi,
    hunting: huntingApi,
    intelligence: intelligenceApi,
    investigation: investigationApi,
    reports: reportsApi,
    dashboard: dashboardApi
  }
}

// 默认API实例
export const api = createApiInstance()

// API基础配置
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  TIMEOUT: 30000,
  RETRY_COUNT: 3
}

// API错误码定义
export const API_ERROR_CODES = {
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  VALIDATION_ERROR: 422,
  INTERNAL_ERROR: 500,
  SERVICE_UNAVAILABLE: 503
}

// API响应状态
export const API_STATUS = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning'
}