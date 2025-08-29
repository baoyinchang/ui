/**
 * 环境配置工具
 */

/**
 * 获取环境变量
 */
export function getEnv(key: string, defaultValue?: string): string {
  // 在构建时，Vite会将import.meta.env替换为实际值
  const env = (import.meta as any).env || {}
  return env[key] || defaultValue || ''
}

/**
 * 检查是否为开发环境
 */
export function isDev(): boolean {
  return getEnv('MODE') === 'development'
}

/**
 * 检查是否为生产环境
 */
export function isProd(): boolean {
  return getEnv('MODE') === 'production'
}

/**
 * 检查是否为测试环境
 */
export function isTest(): boolean {
  return getEnv('MODE') === 'test'
}

/**
 * 获取API基础URL
 */
export function getApiBaseUrl(): string {
  return getEnv('VITE_API_BASE_URL', 'http://localhost:8000')
}

/**
 * 获取应用标题
 */
export function getAppTitle(): string {
  return getEnv('VITE_APP_TITLE', 'H-System EDR平台')
}

/**
 * 获取应用版本
 */
export function getAppVersion(): string {
  return getEnv('VITE_APP_VERSION', '1.0.0')
}

/**
 * 获取应用描述
 */
export function getAppDescription(): string {
  return getEnv('VITE_APP_DESCRIPTION', '蜜罐安全管理系统')
}

/**
 * 检查是否启用Mock
 */
export function isMockEnabled(): boolean {
  return getEnv('VITE_DEV_MOCK', 'false') === 'true'
}

/**
 * 检查是否启用代理
 */
export function isProxyEnabled(): boolean {
  return getEnv('VITE_DEV_PROXY', 'true') === 'true'
}

/**
 * 检查是否启用SourceMap
 */
export function isSourceMapEnabled(): boolean {
  return getEnv('VITE_BUILD_SOURCEMAP', 'false') === 'true'
}

/**
 * 检查是否删除console
 */
export function isDropConsoleEnabled(): boolean {
  return getEnv('VITE_BUILD_DROP_CONSOLE', 'true') === 'true'
}

/**
 * 应用配置
 */
export interface AppConfig {
  title: string
  version: string
  description: string
  apiBaseUrl: string
  isDev: boolean
  isProd: boolean
  isTest: boolean
  enableMock: boolean
  enableProxy: boolean
  enableSourceMap: boolean
  dropConsole: boolean
}

/**
 * 获取应用配置
 */
export function getAppConfig(): AppConfig {
  return {
    title: getAppTitle(),
    version: getAppVersion(),
    description: getAppDescription(),
    apiBaseUrl: getApiBaseUrl(),
    isDev: isDev(),
    isProd: isProd(),
    isTest: isTest(),
    enableMock: isMockEnabled(),
    enableProxy: isProxyEnabled(),
    enableSourceMap: isSourceMapEnabled(),
    dropConsole: isDropConsoleEnabled()
  }
}

/**
 * 设置全局配置到window对象
 */
export function setupGlobalConfig(): void {
  const config = getAppConfig()
  
  // 设置到window对象，供其他地方使用
  if (typeof window !== 'undefined') {
    window.__APP_CONFIG__ = config
  }
  
  // 开发环境下打印配置信息
  if (isDev()) {
    console.group('🚀 应用配置信息')
    console.table(config)
    console.groupEnd()
  }
}

/**
 * 从window对象获取全局配置
 */
export function getGlobalConfig(): AppConfig | undefined {
  if (typeof window !== 'undefined') {
    return window.__APP_CONFIG__
  }
  return undefined
}

/**
 * 环境信息
 */
export interface EnvInfo {
  mode: string
  userAgent: string
  platform: string
  language: string
  timezone: string
  screen: {
    width: number
    height: number
    colorDepth: number
  }
  viewport: {
    width: number
    height: number
  }
}

/**
 * 获取环境信息
 */
export function getEnvInfo(): EnvInfo {
  const info: EnvInfo = {
    mode: getEnv('MODE', 'unknown'),
    userAgent: '',
    platform: '',
    language: '',
    timezone: '',
    screen: {
      width: 0,
      height: 0,
      colorDepth: 0
    },
    viewport: {
      width: 0,
      height: 0
    }
  }

  if (typeof window !== 'undefined' && typeof navigator !== 'undefined') {
    info.userAgent = navigator.userAgent
    info.platform = navigator.platform
    info.language = navigator.language
    info.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone

    if (screen) {
      info.screen = {
        width: screen.width,
        height: screen.height,
        colorDepth: screen.colorDepth
      }
    }

    info.viewport = {
      width: window.innerWidth,
      height: window.innerHeight
    }
  }

  return info
}

/**
 * 检查浏览器支持情况
 */
export interface BrowserSupport {
  es6: boolean
  webgl: boolean
  webWorker: boolean
  localStorage: boolean
  sessionStorage: boolean
  indexedDB: boolean
  webSocket: boolean
  geolocation: boolean
  notification: boolean
  serviceWorker: boolean
}

/**
 * 获取浏览器支持情况
 */
export function getBrowserSupport(): BrowserSupport {
  const support: BrowserSupport = {
    es6: false,
    webgl: false,
    webWorker: false,
    localStorage: false,
    sessionStorage: false,
    indexedDB: false,
    webSocket: false,
    geolocation: false,
    notification: false,
    serviceWorker: false
  }

  if (typeof window === 'undefined') {
    return support
  }

  try {
    // ES6支持检查
    support.es6 = typeof Symbol !== 'undefined'

    // WebGL支持检查
    const canvas = document.createElement('canvas')
    support.webgl = !!(canvas.getContext('webgl') || canvas.getContext('experimental-webgl'))

    // Web Worker支持检查
    support.webWorker = typeof Worker !== 'undefined'

    // 存储支持检查
    support.localStorage = typeof localStorage !== 'undefined'
    support.sessionStorage = typeof sessionStorage !== 'undefined'
    support.indexedDB = typeof indexedDB !== 'undefined'

    // WebSocket支持检查
    support.webSocket = typeof WebSocket !== 'undefined'

    // 地理位置支持检查
    support.geolocation = typeof navigator.geolocation !== 'undefined'

    // 通知支持检查
    support.notification = typeof Notification !== 'undefined'

    // Service Worker支持检查
    support.serviceWorker = 'serviceWorker' in navigator
  } catch (error) {
    console.warn('检查浏览器支持时出错:', error)
  }

  return support
}

/**
 * 检查是否为移动设备
 */
export function isMobile(): boolean {
  if (typeof window === 'undefined') return false
  
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
}

/**
 * 检查是否为iOS设备
 */
export function isIOS(): boolean {
  if (typeof window === 'undefined') return false
  
  return /iPad|iPhone|iPod/.test(navigator.userAgent)
}

/**
 * 检查是否为Android设备
 */
export function isAndroid(): boolean {
  if (typeof window === 'undefined') return false
  
  return /Android/.test(navigator.userAgent)
}

/**
 * 获取设备类型
 */
export function getDeviceType(): 'desktop' | 'tablet' | 'mobile' {
  if (typeof window === 'undefined') return 'desktop'
  
  const userAgent = navigator.userAgent
  
  if (/iPad/.test(userAgent) || (window.innerWidth >= 768 && window.innerWidth <= 1024)) {
    return 'tablet'
  }
  
  if (isMobile()) {
    return 'mobile'
  }
  
  return 'desktop'
}

export default {
  getEnv,
  isDev,
  isProd,
  isTest,
  getApiBaseUrl,
  getAppTitle,
  getAppVersion,
  getAppDescription,
  isMockEnabled,
  isProxyEnabled,
  isSourceMapEnabled,
  isDropConsoleEnabled,
  getAppConfig,
  setupGlobalConfig,
  getGlobalConfig,
  getEnvInfo,
  getBrowserSupport,
  isMobile,
  isIOS,
  isAndroid,
  getDeviceType
}
