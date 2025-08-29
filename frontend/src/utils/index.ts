/**
 * 工具函数集合
 */

import dayjs from 'dayjs'
import type { App } from 'vue'

// 导出其他工具模块
export * from './constants'
export * from './storage'
export * from './validation'
export { default as request } from './request'
export type { RequestConfig, ResponseData } from './request'

/**
 * 格式化时间
 */
export const formatTime = (time: string | Date, format = 'YYYY-MM-DD HH:mm:ss') => {
  return dayjs(time).format(format)
}

/**
 * 格式化相对时间
 */
export const formatRelativeTime = (time: string | Date) => {
  const now = dayjs()
  const target = dayjs(time)
  const diff = now.diff(target, 'minute')

  if (diff < 1) return '刚刚'
  if (diff < 60) return `${diff}分钟前`
  if (diff < 1440) return `${Math.floor(diff / 60)}小时前`
  if (diff < 10080) return `${Math.floor(diff / 1440)}天前`
  return target.format('YYYY-MM-DD')
}

/**
 * 格式化数字（添加千分位分隔符）
 */
export const formatNumber = (num: number): string => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 格式化文件大小
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 防抖函数
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: number | undefined
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func.apply(this, args), wait)
  }
}

/**
 * 节流函数
 */
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

/**
 * 深拷贝
 */
export const deepClone = <T>(obj: T): T => {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime()) as unknown as T
  if (obj instanceof Array) return obj.map(item => deepClone(item)) as unknown as T
  if (typeof obj === 'object') {
    const clonedObj = {} as { [key: string]: any }
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key])
      }
    }
    return clonedObj as T
  }
  return obj
}

/**
 * 生成UUID
 */
export const generateUUID = (): string => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

/**
 * 生成随机字符串
 */
export const generateRandomString = (length: number = 8): string => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * 复制到剪贴板
 */
export const copyToClipboard = async (text: string): Promise<boolean> => {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (error) {
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = text
    document.body.appendChild(textArea)
    textArea.focus()
    textArea.select()
    try {
      document.execCommand('copy')
      document.body.removeChild(textArea)
      return true
    } catch (err) {
      document.body.removeChild(textArea)
      return false
    }
  }
}

/**
 * 下载文件
 */
export const downloadFile = (url: string, filename?: string) => {
  const link = document.createElement('a')
  link.href = url
  if (filename) {
    link.download = filename
  }
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * 获取文件扩展名
 */
export const getFileExtension = (filename: string): string => {
  return filename.slice(((filename.lastIndexOf('.') - 1) >>> 0) + 2)
}

/**
 * 验证邮箱格式
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * 验证IP地址格式
 */
export const isValidIP = (ip: string): boolean => {
  const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
  return ipRegex.test(ip)
}

/**
 * 验证URL格式
 */
export const isValidURL = (url: string): boolean => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * 验证密码强度
 */
export const validatePasswordStrength = (password: string): {
  score: number
  feedback: string[]
} => {
  const feedback: string[] = []
  let score = 0

  if (password.length >= 8) score += 1
  else feedback.push('密码长度至少8位')

  if (/[a-z]/.test(password)) score += 1
  else feedback.push('包含小写字母')

  if (/[A-Z]/.test(password)) score += 1
  else feedback.push('包含大写字母')

  if (/\d/.test(password)) score += 1
  else feedback.push('包含数字')

  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 1
  else feedback.push('包含特殊字符')

  return { score, feedback }
}

/**
 * 脱敏处理
 */
export const maskSensitiveData = (data: string, type: 'email' | 'phone' | 'ip' | 'custom' = 'custom', maskChar = '*'): string => {
  if (!data) return data

  // 兼容性的repeat函数
  const repeatChar = (char: string, count: number): string => {
    return new Array(count + 1).join(char)
  }

  switch (type) {
    case 'email':
      const [username, domain] = data.split('@')
      if (!domain) return data
      const maskedUsername = username.length > 2
        ? username.slice(0, 2) + repeatChar(maskChar, username.length - 2)
        : repeatChar(maskChar, username.length)
      return `${maskedUsername}@${domain}`

    case 'phone':
      if (data.length < 7) return data
      return data.slice(0, 3) + repeatChar(maskChar, 4) + data.slice(-4)

    case 'ip':
      const parts = data.split('.')
      if (parts.length !== 4) return data
      return `${parts[0]}.${parts[1]}.${repeatChar(maskChar, 3)}.${repeatChar(maskChar, 3)}`

    default:
      if (data.length <= 4) return repeatChar(maskChar, data.length)
      return data.slice(0, 2) + repeatChar(maskChar, data.length - 4) + data.slice(-2)
  }
}

/**
 * 获取随机颜色
 */
export const getRandomColor = (): string => {
  const colors = [
    '#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399',
    '#53a8ff', '#85ce61', '#ebb563', '#f78989', '#a6a9ad'
  ]
  return colors[Math.floor(Math.random() * colors.length)]
}

/**
 * 树形数据扁平化
 */
export const flattenTree = <T extends { children?: T[] }>(
  tree: T[],
  childrenKey = 'children'
): T[] => {
  const result: T[] = []
  const stack = [...tree]
  
  while (stack.length) {
    const node = stack.pop()!
    result.push(node)
    
    if (node[childrenKey as keyof T]) {
      stack.push(...(node[childrenKey as keyof T] as T[]))
    }
  }
  
  return result
}

/**
 * 数组转树形结构
 */
export const arrayToTree = <T extends { id: any; parentId?: any; children?: T[] }>(
  array: T[],
  options: {
    idKey?: string
    parentIdKey?: string
    childrenKey?: string
  } = {}
): T[] => {
  const { idKey = 'id', parentIdKey = 'parentId', childrenKey = 'children' } = options
  const tree: T[] = []
  const map: { [key: string]: T } = {}

  // 创建映射
  array.forEach(item => {
    const key = String(item[idKey as keyof T])
    map[key] = { ...item, [childrenKey]: [] } as T
  })

  // 构建树形结构
  array.forEach(item => {
    const key = String(item[idKey as keyof T])
    const node = map[key]
    const parentId = item[parentIdKey as keyof T]

    if (parentId && map[String(parentId)]) {
      const parent = map[String(parentId)]
      ;(parent[childrenKey as keyof T] as T[]).push(node)
    } else {
      tree.push(node)
    }
  })

  return tree
}

/**
 * 安装工具函数到Vue应用
 */
export const installUtils = (app: App) => {
  app.config.globalProperties.$utils = {
    formatTime,
    formatFileSize,
    debounce,
    throttle,
    deepClone,
    generateUUID,
    copyToClipboard,
    downloadFile,
    getFileExtension,
    isValidEmail,
    isValidIP,
    isValidURL,
    getRandomColor,
    flattenTree,
    arrayToTree
  }
}
