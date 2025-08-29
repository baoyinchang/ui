/**
 * HTTP请求工具
 */

import axios, {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  AxiosError,
  InternalAxiosRequestConfig
} from 'axios'
import { ElMessage, ElMessageBox, ElLoading } from 'element-plus'
import { API_CONFIG, HTTP_STATUS, STORAGE_KEYS } from './constants'
import { tokenStorage } from './storage'

/**
 * 请求配置接口
 */
interface RequestConfig extends AxiosRequestConfig {
  showLoading?: boolean
  showError?: boolean
  showSuccess?: boolean
  successMessage?: string
  retryCount?: number
  retryDelay?: number
}

/**
 * 响应数据接口
 */
interface ResponseData<T = any> {
  code?: number
  message?: string
  data?: T
  success?: boolean
  timestamp?: string
  detail?: string // FastAPI错误格式
}

/**
 * 请求状态管理
 */
class RequestManager {
  private pendingRequests = new Map<string, AbortController>()
  private loadingInstance: any = null
  private loadingCount = 0

  /**
   * 生成请求键
   */
  private generateRequestKey(config: InternalAxiosRequestConfig): string {
    const { method, url, params, data } = config
    return `${method}:${url}:${JSON.stringify(params)}:${JSON.stringify(data)}`
  }

  /**
   * 添加请求
   */
  addRequest(config: InternalAxiosRequestConfig): void {
    const requestKey = this.generateRequestKey(config)

    // 如果存在相同请求，取消之前的请求
    if (this.pendingRequests.has(requestKey)) {
      const controller = this.pendingRequests.get(requestKey)
      controller?.abort('重复请求')
    }

    // 创建新的取消控制器
    const controller = new AbortController()
    config.signal = controller.signal
    this.pendingRequests.set(requestKey, controller)
  }

  /**
   * 移除请求
   */
  removeRequest(config: InternalAxiosRequestConfig): void {
    const requestKey = this.generateRequestKey(config)
    this.pendingRequests.delete(requestKey)
  }

  /**
   * 取消所有请求
   */
  cancelAllRequests(): void {
    this.pendingRequests.forEach(controller => {
      controller.abort('取消所有请求')
    })
    this.pendingRequests.clear()
  }

  /**
   * 显示加载状态
   */
  showLoading(): void {
    this.loadingCount++
    if (this.loadingCount === 1) {
      this.loadingInstance = ElLoading.service({
        lock: true,
        text: '加载中...',
        background: 'rgba(0, 0, 0, 0.7)'
      })
    }
  }

  /**
   * 隐藏加载状态
   */
  hideLoading(): void {
    this.loadingCount = Math.max(0, this.loadingCount - 1)
    if (this.loadingCount === 0 && this.loadingInstance) {
      this.loadingInstance.close()
      this.loadingInstance = null
    }
  }
}

// 创建请求管理器实例
const requestManager = new RequestManager()

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const requestConfig = config as RequestConfig

    // 添加请求到管理器
    requestManager.addRequest(config)

    // 显示加载状态
    if (requestConfig.showLoading !== false) {
      requestManager.showLoading()
    }

    // 添加认证token
    const token = tokenStorage.getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 添加时间戳防止缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }

    return config
  },
  (error: AxiosError) => {
    requestManager.hideLoading()
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const config = response.config as RequestConfig

    // 从请求管理器中移除请求
    requestManager.removeRequest(config)

    // 隐藏加载状态
    if (config.showLoading !== false) {
      requestManager.hideLoading()
    }

    // 如果是文件下载，直接返回
    if (response.config.responseType === 'blob') {
      return response
    }

    const { data }: { data: ResponseData } = response

    // 显示成功消息
    if (config.showSuccess && config.successMessage) {
      ElMessage.success(config.successMessage)
    }

    // 检查业务状态码
    // 兼容不同的响应格式
    const responseCode = data.code || response.status
    const responseMessage = data.message || data.detail || '请求失败'

    if (responseCode !== HTTP_STATUS.OK && response.status !== HTTP_STATUS.OK) {
      if (config.showError !== false) {
        ElMessage.error(responseMessage)
      }

      return Promise.reject(new Error(responseMessage))
    }

    return data
  },
  async (error: AxiosError) => {
    const config = error.config as RequestConfig

    if (config) {
      // 从请求管理器中移除请求
      requestManager.removeRequest(config)

      // 隐藏加载状态
      if (config.showLoading !== false) {
        requestManager.hideLoading()
      }
    }

    // 如果是取消请求，不显示错误
    if (axios.isCancel(error)) {
      return Promise.reject(error)
    }

    console.error('响应错误:', error)

    if (error.response) {
      const { status, data } = error.response
      let errorMessage = '请求失败'

      switch (status) {
        case HTTP_STATUS.UNAUTHORIZED:
          errorMessage = '未授权，请重新登录'
          // 清除token
          tokenStorage.clearTokens()
          // 跳转到登录页
          setTimeout(() => {
            window.location.href = '/login'
          }, 1000)
          break
        case HTTP_STATUS.FORBIDDEN:
          errorMessage = '拒绝访问，权限不足'
          break
        case HTTP_STATUS.NOT_FOUND:
          errorMessage = '请求的资源不存在'
          break
        case HTTP_STATUS.UNPROCESSABLE_ENTITY:
          errorMessage = data?.message || '请求参数错误'
          break
        case HTTP_STATUS.INTERNAL_SERVER_ERROR:
          errorMessage = '服务器内部错误'
          break
        case HTTP_STATUS.BAD_GATEWAY:
          errorMessage = '网关错误'
          break
        case HTTP_STATUS.SERVICE_UNAVAILABLE:
          errorMessage = '服务暂时不可用'
          break
        case HTTP_STATUS.GATEWAY_TIMEOUT:
          errorMessage = '网关超时'
          break
        default:
          errorMessage = data?.message || `请求失败 (${status})`
      }

      if (config?.showError !== false) {
        ElMessage.error(errorMessage)
      }
    } else if (error.request) {
      if (config?.showError !== false) {
        ElMessage.error('网络错误，请检查网络连接')
      }
    } else {
      if (config?.showError !== false) {
        ElMessage.error('请求配置错误')
      }
    }

    // 重试机制
    if (config && config.retryCount && config.retryCount > 0) {
      config.retryCount--
      const delay = config.retryDelay || 1000

      await new Promise(resolve => setTimeout(resolve, delay))
      return service(config)
    }

    return Promise.reject(error)
  }
)

// 导出请求管理器
export { requestManager }

// 导出类型
export type { RequestConfig, ResponseData }

export default service