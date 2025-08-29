/**
 * 表单验证工具函数
 */

import type { FormRule } from '@/types/global'
import { REGEX_PATTERNS } from './constants'

/**
 * 验证规则生成器
 */
export const validationRules = {
  /**
   * 必填验证
   */
  required(message = '此字段为必填项'): FormRule {
    return {
      required: true,
      message,
      trigger: 'blur'
    }
  },

  /**
   * 邮箱验证
   */
  email(message = '请输入有效的邮箱地址'): FormRule {
    return {
      type: 'email',
      message,
      trigger: 'blur'
    }
  },

  /**
   * 手机号验证
   */
  phone(message = '请输入有效的手机号码'): FormRule {
    return {
      pattern: REGEX_PATTERNS.PHONE,
      message,
      trigger: 'blur'
    }
  },

  /**
   * IP地址验证
   */
  ip(message = '请输入有效的IP地址'): FormRule {
    return {
      pattern: REGEX_PATTERNS.IP,
      message,
      trigger: 'blur'
    }
  },

  /**
   * URL验证
   */
  url(message = '请输入有效的URL地址'): FormRule {
    return {
      pattern: REGEX_PATTERNS.URL,
      message,
      trigger: 'blur'
    }
  },

  /**
   * 用户名验证
   */
  username(message = '用户名只能包含字母、数字和下划线，长度3-20位'): FormRule {
    return {
      pattern: /^[a-zA-Z0-9_]{3,20}$/,
      message,
      trigger: 'blur'
    }
  },

  /**
   * 密码验证
   */
  password(message = '密码至少8位，包含大小写字母和数字'): FormRule {
    return {
      pattern: REGEX_PATTERNS.PASSWORD,
      message,
      trigger: 'blur'
    }
  },

  /**
   * 长度验证
   */
  length(min: number, max?: number, message?: string): FormRule {
    if (max !== undefined) {
      return {
        min,
        max,
        message: message || `长度应在 ${min} 到 ${max} 个字符之间`,
        trigger: 'blur'
      }
    } else {
      return {
        min,
        message: message || `长度不能少于 ${min} 个字符`,
        trigger: 'blur'
      }
    }
  },

  /**
   * 数字验证
   */
  number(message = '请输入有效的数字'): FormRule {
    return {
      type: 'number',
      message,
      trigger: 'blur'
    }
  },

  /**
   * 整数验证
   */
  integer(message = '请输入有效的整数'): FormRule {
    return {
      type: 'integer',
      message,
      trigger: 'blur'
    }
  },

  /**
   * 数字范围验证
   */
  range(min: number, max: number, message?: string): FormRule {
    return {
      type: 'number',
      min,
      max,
      message: message || `数值应在 ${min} 到 ${max} 之间`,
      trigger: 'blur'
    }
  },

  /**
   * 自定义验证
   */
  custom(validator: (rule: any, value: any, callback: any) => void, message?: string): FormRule {
    return {
      validator,
      message,
      trigger: 'blur'
    }
  },

  /**
   * 确认密码验证
   */
  confirmPassword(passwordField: string, message = '两次输入的密码不一致'): FormRule {
    return {
      validator: (rule: any, value: any, callback: any) => {
        const form = rule.form
        if (form && form[passwordField] !== value) {
          callback(new Error(message))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  },

  /**
   * 数组非空验证
   */
  arrayRequired(message = '请至少选择一项'): FormRule {
    return {
      type: 'array',
      required: true,
      min: 1,
      message,
      trigger: 'change'
    }
  },

  /**
   * 文件验证
   */
  file(
    options: {
      required?: boolean
      maxSize?: number // MB
      allowedTypes?: string[]
      message?: string
    } = {}
  ): FormRule {
    const { required = false, maxSize, allowedTypes, message } = options

    return {
      required,
      validator: (rule: any, value: any, callback: any) => {
        if (!required && !value) {
          callback()
          return
        }

        if (required && !value) {
          callback(new Error(message || '请选择文件'))
          return
        }

        if (value && typeof value === 'object') {
          // 检查文件大小
          if (maxSize && value.size > maxSize * 1024 * 1024) {
            callback(new Error(`文件大小不能超过 ${maxSize}MB`))
            return
          }

          // 检查文件类型
          if (allowedTypes && allowedTypes.length > 0) {
            const fileType = value.type || ''
            const fileName = value.name || ''
            const fileExt = fileName.split('.').pop()?.toLowerCase()

            const isValidType = allowedTypes.some(type => {
              if (type.includes('/')) {
                return fileType === type
              } else {
                return fileExt === type
              }
            })

            if (!isValidType) {
              callback(new Error(`只允许上传 ${allowedTypes.join(', ')} 格式的文件`))
              return
            }
          }
        }

        callback()
      },
      trigger: 'change'
    }
  }
}

/**
 * 表单验证器类
 */
export class FormValidator {
  private rules: Record<string, FormRule[]> = {}

  /**
   * 添加验证规则
   */
  addRule(field: string, rule: FormRule | FormRule[]): this {
    if (!this.rules[field]) {
      this.rules[field] = []
    }

    if (Array.isArray(rule)) {
      this.rules[field].push(...rule)
    } else {
      this.rules[field].push(rule)
    }

    return this
  }

  /**
   * 获取所有规则
   */
  getRules(): Record<string, FormRule[]> {
    return this.rules
  }

  /**
   * 验证单个字段
   */
  async validateField(field: string, value: any): Promise<boolean> {
    const fieldRules = this.rules[field]
    if (!fieldRules || fieldRules.length === 0) {
      return true
    }

    for (const rule of fieldRules) {
      try {
        await this.validateSingleRule(rule, value)
      } catch (error) {
        return false
      }
    }

    return true
  }

  /**
   * 验证单个规则
   */
  private validateSingleRule(rule: FormRule, value: any): Promise<void> {
    return new Promise((resolve, reject) => {
      // 必填验证
      if (rule.required && (value === undefined || value === null || value === '')) {
        reject(new Error(rule.message || '此字段为必填项'))
        return
      }

      // 如果值为空且不是必填，跳过验证
      if (!rule.required && (value === undefined || value === null || value === '')) {
        resolve()
        return
      }

      // 类型验证
      if (rule.type) {
        if (!this.validateType(rule.type, value)) {
          reject(new Error(rule.message || '类型不匹配'))
          return
        }
      }

      // 长度验证
      if (rule.min !== undefined || rule.max !== undefined) {
        const length = typeof value === 'string' ? value.length : 
                      Array.isArray(value) ? value.length : 
                      typeof value === 'number' ? value : 0

        if (rule.min !== undefined && length < rule.min) {
          reject(new Error(rule.message || `长度不能少于 ${rule.min}`))
          return
        }

        if (rule.max !== undefined && length > rule.max) {
          reject(new Error(rule.message || `长度不能超过 ${rule.max}`))
          return
        }
      }

      // 正则验证
      if (rule.pattern && typeof value === 'string') {
        if (!rule.pattern.test(value)) {
          reject(new Error(rule.message || '格式不正确'))
          return
        }
      }

      // 自定义验证
      if (rule.validator) {
        rule.validator(rule, value, (error?: Error) => {
          if (error) {
            reject(error)
          } else {
            resolve()
          }
        })
        return
      }

      resolve()
    })
  }

  /**
   * 类型验证
   */
  private validateType(type: string, value: any): boolean {
    switch (type) {
      case 'string':
        return typeof value === 'string'
      case 'number':
        return typeof value === 'number' && !isNaN(value)
      case 'integer':
        return typeof value === 'number' && Number.isInteger(value)
      case 'float':
        return typeof value === 'number' && !Number.isInteger(value)
      case 'boolean':
        return typeof value === 'boolean'
      case 'array':
        return Array.isArray(value)
      case 'object':
        return typeof value === 'object' && value !== null && !Array.isArray(value)
      case 'email':
        return typeof value === 'string' && REGEX_PATTERNS.EMAIL.test(value)
      case 'url':
        return typeof value === 'string' && REGEX_PATTERNS.URL.test(value)
      case 'date':
        return value instanceof Date || !isNaN(Date.parse(value))
      default:
        return true
    }
  }

  /**
   * 清空规则
   */
  clear(): this {
    this.rules = {}
    return this
  }
}

/**
 * 常用验证函数
 */
export const validators = {
  /**
   * 验证是否为空
   */
  isEmpty(value: any): boolean {
    return value === undefined || value === null || value === '' || 
           (Array.isArray(value) && value.length === 0) ||
           (typeof value === 'object' && Object.keys(value).length === 0)
  },

  /**
   * 验证邮箱
   */
  isEmail(email: string): boolean {
    return REGEX_PATTERNS.EMAIL.test(email)
  },

  /**
   * 验证手机号
   */
  isPhone(phone: string): boolean {
    return REGEX_PATTERNS.PHONE.test(phone)
  },

  /**
   * 验证IP地址
   */
  isIP(ip: string): boolean {
    return REGEX_PATTERNS.IP.test(ip)
  },

  /**
   * 验证URL
   */
  isURL(url: string): boolean {
    return REGEX_PATTERNS.URL.test(url)
  },

  /**
   * 验证身份证号
   */
  isIDCard(idCard: string): boolean {
    const pattern = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/
    return pattern.test(idCard)
  },

  /**
   * 验证银行卡号
   */
  isBankCard(cardNumber: string): boolean {
    const pattern = /^[1-9]\d{12,18}$/
    return pattern.test(cardNumber)
  },

  /**
   * 验证中文字符
   */
  isChinese(text: string): boolean {
    const pattern = /^[\u4e00-\u9fa5]+$/
    return pattern.test(text)
  },

  /**
   * 验证数字
   */
  isNumber(value: any): boolean {
    return !isNaN(Number(value)) && isFinite(Number(value))
  },

  /**
   * 验证整数
   */
  isInteger(value: any): boolean {
    return Number.isInteger(Number(value))
  },

  /**
   * 验证正整数
   */
  isPositiveInteger(value: any): boolean {
    const num = Number(value)
    return Number.isInteger(num) && num > 0
  },

  /**
   * 验证JSON字符串
   */
  isJSON(str: string): boolean {
    try {
      JSON.parse(str)
      return true
    } catch {
      return false
    }
  }
}

export default validationRules
