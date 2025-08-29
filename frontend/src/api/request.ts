import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { useUserStore } from '@/store/user'
import router from '@/router'

// 配置NProgress
NProgress.configure({
  showSpinner: false,
  minimum: 0.2,
  speed: 500
})

// 创建axios实例
const request: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // 显示进度条
    NProgress.start()
    
    // 添加认证token
    const userStore = useUserStore()
    const token = userStore.token
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    NProgress.done()
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    NProgress.done()
    
    // 直接返回响应数据
    return response.data
  },
  (error) => {
    NProgress.done()
    
    const { response } = error
    
    if (response) {
      const { status, data } = response
      
      switch (status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          const userStore = useUserStore()
          userStore.logout()
          router.push('/login')
          ElMessage.error('登录已过期，请重新登录')
          break
          
        case 403:
          ElMessage.error('权限不足，无法访问')
          break
          
        case 404:
          ElMessage.error('请求的资源不存在')
          break
          
        case 422:
          // 表单验证错误
          if (data?.detail) {
            if (Array.isArray(data.detail)) {
              const errors = data.detail.map((item: any) => item.msg).join(', ')
              ElMessage.error(`参数错误: ${errors}`)
            } else {
              ElMessage.error(data.detail)
            }
          } else {
            ElMessage.error('参数验证失败')
          }
          break
          
        case 500:
          ElMessage.error('服务器内部错误')
          break
          
        default:
          ElMessage.error(data?.detail || data?.message || '请求失败')
      }
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请稍后重试')
    } else if (error.message === 'Network Error') {
      ElMessage.error('网络连接失败，请检查网络')
    } else {
      ElMessage.error('请求失败，请稍后重试')
    }
    
    return Promise.reject(error)
  }
)

// 封装常用请求方法
export const http = {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return request.get(url, config)
  },
  
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return request.post(url, data, config)
  },
  
  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return request.put(url, data, config)
  },
  
  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return request.delete(url, config)
  },
  
  patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return request.patch(url, data, config)
  }
}

export default request
