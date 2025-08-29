/**
 * 本地存储工具函数
 */

import { STORAGE_KEYS } from './constants'

/**
 * 存储类型
 */
export type StorageType = 'localStorage' | 'sessionStorage'

/**
 * 存储配置
 */
interface StorageConfig {
  type: StorageType
  prefix: string
  encrypt: boolean
}

/**
 * 默认配置
 */
const defaultConfig: StorageConfig = {
  type: 'localStorage',
  prefix: 'hsystem-',
  encrypt: false
}

/**
 * 简单加密/解密（仅用于基础混淆，不适用于敏感数据）
 */
const simpleEncrypt = (text: string): string => {
  return btoa(encodeURIComponent(text))
}

const simpleDecrypt = (text: string): string => {
  try {
    return decodeURIComponent(atob(text))
  } catch {
    return text
  }
}

/**
 * 存储工具类
 */
class StorageUtil {
  private config: StorageConfig

  constructor(config: Partial<StorageConfig> = {}) {
    this.config = { ...defaultConfig, ...config }
  }

  /**
   * 获取存储对象
   */
  private getStorage(): Storage {
    return this.config.type === 'localStorage' ? localStorage : sessionStorage
  }

  /**
   * 生成完整的键名
   */
  private getKey(key: string): string {
    return this.config.prefix + key
  }

  /**
   * 设置存储项
   */
  set<T = any>(key: string, value: T): boolean {
    try {
      const storage = this.getStorage()
      const fullKey = this.getKey(key)
      
      let serializedValue = JSON.stringify({
        data: value,
        timestamp: Date.now(),
        type: typeof value
      })

      if (this.config.encrypt) {
        serializedValue = simpleEncrypt(serializedValue)
      }

      storage.setItem(fullKey, serializedValue)
      return true
    } catch (error) {
      console.error('存储设置失败:', error)
      return false
    }
  }

  /**
   * 获取存储项
   */
  get<T = any>(key: string, defaultValue?: T): T | null {
    try {
      const storage = this.getStorage()
      const fullKey = this.getKey(key)
      let item = storage.getItem(fullKey)

      if (!item) {
        return defaultValue ?? null
      }

      if (this.config.encrypt) {
        item = simpleDecrypt(item)
      }

      const parsed = JSON.parse(item)
      return parsed.data
    } catch (error) {
      console.error('存储获取失败:', error)
      return defaultValue ?? null
    }
  }

  /**
   * 移除存储项
   */
  remove(key: string): boolean {
    try {
      const storage = this.getStorage()
      const fullKey = this.getKey(key)
      storage.removeItem(fullKey)
      return true
    } catch (error) {
      console.error('存储移除失败:', error)
      return false
    }
  }

  /**
   * 清空所有存储项
   */
  clear(): boolean {
    try {
      const storage = this.getStorage()
      const keys = Object.keys(storage).filter(key => 
        key.startsWith(this.config.prefix)
      )
      
      keys.forEach(key => storage.removeItem(key))
      return true
    } catch (error) {
      console.error('存储清空失败:', error)
      return false
    }
  }

  /**
   * 检查存储项是否存在
   */
  has(key: string): boolean {
    const storage = this.getStorage()
    const fullKey = this.getKey(key)
    return storage.getItem(fullKey) !== null
  }

  /**
   * 获取所有键名
   */
  keys(): string[] {
    const storage = this.getStorage()
    return Object.keys(storage)
      .filter(key => key.startsWith(this.config.prefix))
      .map(key => key.replace(this.config.prefix, ''))
  }

  /**
   * 获取存储大小（字节）
   */
  size(): number {
    const storage = this.getStorage()
    let size = 0
    
    Object.keys(storage).forEach(key => {
      if (key.startsWith(this.config.prefix)) {
        const value = storage.getItem(key)
        if (value) {
          size += key.length + value.length
        }
      }
    })
    
    return size
  }

  /**
   * 设置过期时间的存储项
   */
  setWithExpiry<T = any>(key: string, value: T, expiryMinutes: number): boolean {
    try {
      const expiryTime = Date.now() + (expiryMinutes * 60 * 1000)
      const item = {
        data: value,
        expiry: expiryTime,
        timestamp: Date.now()
      }
      
      return this.set(key, item)
    } catch (error) {
      console.error('带过期时间的存储设置失败:', error)
      return false
    }
  }

  /**
   * 获取带过期时间的存储项
   */
  getWithExpiry<T = any>(key: string, defaultValue?: T): T | null {
    try {
      const item = this.get(key)
      
      if (!item || typeof item !== 'object' || !('expiry' in item)) {
        return defaultValue ?? null
      }

      const now = Date.now()
      if (now > item.expiry) {
        this.remove(key)
        return defaultValue ?? null
      }

      return item.data
    } catch (error) {
      console.error('带过期时间的存储获取失败:', error)
      return defaultValue ?? null
    }
  }
}

// 创建默认实例
export const storage = new StorageUtil()

// 创建会话存储实例
export const sessionStorage = new StorageUtil({ type: 'sessionStorage' })

// 创建加密存储实例
export const encryptedStorage = new StorageUtil({ encrypt: true })

/**
 * 令牌存储工具
 */
export const tokenStorage = {
  /**
   * 设置访问令牌
   */
  setAccessToken(token: string): boolean {
    return storage.set(STORAGE_KEYS.ACCESS_TOKEN, token)
  },

  /**
   * 获取访问令牌
   */
  getAccessToken(): string | null {
    return storage.get(STORAGE_KEYS.ACCESS_TOKEN)
  },

  /**
   * 设置刷新令牌
   */
  setRefreshToken(token: string): boolean {
    return storage.set(STORAGE_KEYS.REFRESH_TOKEN, token)
  },

  /**
   * 获取刷新令牌
   */
  getRefreshToken(): string | null {
    return storage.get(STORAGE_KEYS.REFRESH_TOKEN)
  },

  /**
   * 清除所有令牌
   */
  clearTokens(): boolean {
    const accessResult = storage.remove(STORAGE_KEYS.ACCESS_TOKEN)
    const refreshResult = storage.remove(STORAGE_KEYS.REFRESH_TOKEN)
    return accessResult && refreshResult
  },

  /**
   * 检查是否有有效令牌
   */
  hasValidToken(): boolean {
    return !!this.getAccessToken()
  }
}

/**
 * 用户信息存储工具
 */
export const userStorage = {
  /**
   * 设置用户信息
   */
  setUserInfo(userInfo: any): boolean {
    return storage.set(STORAGE_KEYS.USER_INFO, userInfo)
  },

  /**
   * 获取用户信息
   */
  getUserInfo(): any {
    return storage.get(STORAGE_KEYS.USER_INFO)
  },

  /**
   * 清除用户信息
   */
  clearUserInfo(): boolean {
    return storage.remove(STORAGE_KEYS.USER_INFO)
  },

  /**
   * 设置用户设置
   */
  setUserSettings(settings: any): boolean {
    return storage.set(STORAGE_KEYS.USER_SETTINGS, settings)
  },

  /**
   * 获取用户设置
   */
  getUserSettings(): any {
    return storage.get(STORAGE_KEYS.USER_SETTINGS, {})
  }
}

/**
 * 主题存储工具
 */
export const themeStorage = {
  /**
   * 设置主题
   */
  setTheme(theme: string): boolean {
    return storage.set(STORAGE_KEYS.THEME, theme)
  },

  /**
   * 获取主题
   */
  getTheme(): string {
    return storage.get(STORAGE_KEYS.THEME, 'light')
  },

  /**
   * 设置语言
   */
  setLanguage(language: string): boolean {
    return storage.set(STORAGE_KEYS.LANGUAGE, language)
  },

  /**
   * 获取语言
   */
  getLanguage(): string {
    return storage.get(STORAGE_KEYS.LANGUAGE, 'zh-CN')
  },

  /**
   * 设置侧边栏折叠状态
   */
  setSidebarCollapsed(collapsed: boolean): boolean {
    return storage.set(STORAGE_KEYS.SIDEBAR_COLLAPSED, collapsed)
  },

  /**
   * 获取侧边栏折叠状态
   */
  getSidebarCollapsed(): boolean {
    return storage.get(STORAGE_KEYS.SIDEBAR_COLLAPSED, false)
  }
}

/**
 * 搜索历史存储工具
 */
export const searchStorage = {
  /**
   * 添加搜索历史
   */
  addSearchHistory(keyword: string, maxCount = 10): boolean {
    const history = this.getSearchHistory()
    const newHistory = [keyword, ...history.filter(item => item !== keyword)]
    
    if (newHistory.length > maxCount) {
      newHistory.splice(maxCount)
    }
    
    return storage.set(STORAGE_KEYS.SEARCH_HISTORY, newHistory)
  },

  /**
   * 获取搜索历史
   */
  getSearchHistory(): string[] {
    return storage.get(STORAGE_KEYS.SEARCH_HISTORY, [])
  },

  /**
   * 清除搜索历史
   */
  clearSearchHistory(): boolean {
    return storage.remove(STORAGE_KEYS.SEARCH_HISTORY)
  }
}

/**
 * 最近访问存储工具
 */
export const visitStorage = {
  /**
   * 添加访问记录
   */
  addRecentVisit(path: string, title: string, maxCount = 20): boolean {
    const visits = this.getRecentVisits()
    const newVisit = { path, title, timestamp: Date.now() }
    const newVisits = [newVisit, ...visits.filter(item => item.path !== path)]
    
    if (newVisits.length > maxCount) {
      newVisits.splice(maxCount)
    }
    
    return storage.set(STORAGE_KEYS.RECENT_VISITS, newVisits)
  },

  /**
   * 获取最近访问
   */
  getRecentVisits(): Array<{ path: string; title: string; timestamp: number }> {
    return storage.get(STORAGE_KEYS.RECENT_VISITS, [])
  },

  /**
   * 清除访问记录
   */
  clearRecentVisits(): boolean {
    return storage.remove(STORAGE_KEYS.RECENT_VISITS)
  }
}

export default StorageUtil
