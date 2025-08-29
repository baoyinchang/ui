/**
 * 通用工具函数
 */

import { REGEX_PATTERNS, TIME_FORMATS } from './constants'

/**
 * 防抖函数
 * @param func 要防抖的函数
 * @param wait 等待时间（毫秒）
 * @param immediate 是否立即执行
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number,
  immediate = false
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null
  
  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null
      if (!immediate) func(...args)
    }
    
    const callNow = immediate && !timeout
    
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(later, wait)
    
    if (callNow) func(...args)
  }
}

/**
 * 节流函数
 * @param func 要节流的函数
 * @param limit 时间间隔（毫秒）
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean
  
  return function executedFunction(...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

/**
 * 深拷贝对象
 * @param obj 要拷贝的对象
 */
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj
  }
  
  if (obj instanceof Date) {
    return new Date(obj.getTime()) as unknown as T
  }
  
  if (obj instanceof Array) {
    return obj.map(item => deepClone(item)) as unknown as T
  }
  
  if (typeof obj === 'object') {
    const clonedObj = {} as T
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key])
      }
    }
    return clonedObj
  }
  
  return obj
}

/**
 * 生成唯一ID
 * @param prefix 前缀
 */
export function generateId(prefix = ''): string {
  const timestamp = Date.now().toString(36)
  const randomStr = Math.random().toString(36).substring(2, 8)
  return `${prefix}${timestamp}${randomStr}`
}

/**
 * 格式化文件大小
 * @param bytes 字节数
 * @param decimals 小数位数
 */
export function formatFileSize(bytes: number, decimals = 2): string {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

/**
 * 格式化数字
 * @param num 数字
 * @param options 格式化选项
 */
export function formatNumber(
  num: number,
  options: {
    decimals?: number
    separator?: string
    prefix?: string
    suffix?: string
  } = {}
): string {
  const { decimals = 0, separator = ',', prefix = '', suffix = '' } = options
  
  const parts = num.toFixed(decimals).split('.')
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, separator)
  
  return prefix + parts.join('.') + suffix
}

/**
 * 格式化时间
 * @param date 日期
 * @param format 格式
 */
export function formatTime(date: Date | string | number, format = TIME_FORMATS.DATETIME): string {
  const d = new Date(date)
  
  if (isNaN(d.getTime())) {
    return ''
  }
  
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')
  
  return format
    .replace('YYYY', String(year))
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 获取相对时间
 * @param date 日期
 */
export function getRelativeTime(date: Date | string | number): string {
  const now = new Date()
  const target = new Date(date)
  const diff = now.getTime() - target.getTime()
  
  const minute = 60 * 1000
  const hour = minute * 60
  const day = hour * 24
  const week = day * 7
  const month = day * 30
  const year = day * 365
  
  if (diff < minute) {
    return '刚刚'
  } else if (diff < hour) {
    return `${Math.floor(diff / minute)}分钟前`
  } else if (diff < day) {
    return `${Math.floor(diff / hour)}小时前`
  } else if (diff < week) {
    return `${Math.floor(diff / day)}天前`
  } else if (diff < month) {
    return `${Math.floor(diff / week)}周前`
  } else if (diff < year) {
    return `${Math.floor(diff / month)}个月前`
  } else {
    return `${Math.floor(diff / year)}年前`
  }
}

/**
 * 验证邮箱
 * @param email 邮箱地址
 */
export function validateEmail(email: string): boolean {
  return REGEX_PATTERNS.EMAIL.test(email)
}

/**
 * 验证IP地址
 * @param ip IP地址
 */
export function validateIP(ip: string): boolean {
  return REGEX_PATTERNS.IP.test(ip)
}

/**
 * 验证URL
 * @param url URL地址
 */
export function validateURL(url: string): boolean {
  return REGEX_PATTERNS.URL.test(url)
}

/**
 * 验证手机号
 * @param phone 手机号
 */
export function validatePhone(phone: string): boolean {
  return REGEX_PATTERNS.PHONE.test(phone)
}

/**
 * 验证密码强度
 * @param password 密码
 */
export function validatePassword(password: string): boolean {
  return REGEX_PATTERNS.PASSWORD.test(password)
}

/**
 * 获取密码强度等级
 * @param password 密码
 */
export function getPasswordStrength(password: string): {
  level: number
  text: string
  color: string
} {
  let score = 0
  
  // 长度检查
  if (password.length >= 8) score += 1
  if (password.length >= 12) score += 1
  
  // 字符类型检查
  if (/[a-z]/.test(password)) score += 1
  if (/[A-Z]/.test(password)) score += 1
  if (/\d/.test(password)) score += 1
  if (/[^a-zA-Z\d]/.test(password)) score += 1
  
  if (score <= 2) {
    return { level: 1, text: '弱', color: '#f56c6c' }
  } else if (score <= 4) {
    return { level: 2, text: '中', color: '#e6a23c' }
  } else {
    return { level: 3, text: '强', color: '#67c23a' }
  }
}

/**
 * 转换为驼峰命名
 * @param str 字符串
 */
export function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())
}

/**
 * 转换为下划线命名
 * @param str 字符串
 */
export function toSnakeCase(str: string): string {
  return str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`)
}

/**
 * 首字母大写
 * @param str 字符串
 */
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1)
}

/**
 * 截断文本
 * @param text 文本
 * @param length 长度
 * @param suffix 后缀
 */
export function truncate(text: string, length: number, suffix = '...'): string {
  if (text.length <= length) {
    return text
  }
  return text.substring(0, length) + suffix
}

/**
 * 高亮搜索关键词
 * @param text 文本
 * @param keyword 关键词
 * @param className CSS类名
 */
export function highlightKeyword(
  text: string,
  keyword: string,
  className = 'highlight'
): string {
  if (!keyword) return text
  
  const regex = new RegExp(`(${keyword})`, 'gi')
  return text.replace(regex, `<span class="${className}">$1</span>`)
}

/**
 * 下载文件
 * @param data 数据
 * @param filename 文件名
 * @param type MIME类型
 */
export function downloadFile(data: any, filename: string, type = 'application/octet-stream'): void {
  const blob = new Blob([data], { type })
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  
  link.href = url
  link.download = filename
  link.style.display = 'none'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  window.URL.revokeObjectURL(url)
}

/**
 * 复制到剪贴板
 * @param text 文本
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
      return true
    } else {
      // 降级方案
      const textArea = document.createElement('textarea')
      textArea.value = text
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      const result = document.execCommand('copy')
      document.body.removeChild(textArea)
      return result
    }
  } catch (error) {
    console.error('复制失败:', error)
    return false
  }
}
