/**
 * 全局类型定义文件
 * 定义全局使用的类型、接口和声明
 */

// 全局环境变量类型定义
declare global {
  interface ImportMetaEnv {
    readonly VITE_API_BASE_URL: string
    readonly VITE_APP_TITLE: string
    readonly VITE_APP_VERSION: string
    readonly VITE_APP_DESCRIPTION: string
    readonly VITE_DEV_MOCK: string
    readonly VITE_DEV_PROXY: string
    readonly VITE_BUILD_SOURCEMAP: string
    readonly VITE_BUILD_DROP_CONSOLE: string
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
}

// 窗口对象扩展
declare interface Window {
  // 全局配置
  __APP_CONFIG__?: AppConfig
  // 开发工具
  __VUE_DEVTOOLS_GLOBAL_HOOK__?: any
  // 第三方库
  AMap?: any
  BMap?: any
  // 埋点统计
  gtag?: (...args: any[]) => void
  dataLayer?: any[]
}

// 应用配置类型
export interface AppConfig {
  title: string
  version: string
  description: string
  apiBaseUrl: string
  enableMock: boolean
  enableProxy: boolean
}

// 通用响应类型
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  success: boolean
  timestamp: string
}

// 分页响应类型
export interface PaginatedResponse<T = any> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

// 通用列表查询参数
export interface ListQueryParams {
  page?: number
  size?: number
  search?: string
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

// 通用表格列定义
export interface TableColumn {
  prop: string
  label: string
  width?: string | number
  minWidth?: string | number
  fixed?: boolean | 'left' | 'right'
  sortable?: boolean
  filterable?: boolean
  formatter?: (row: any, column: any, cellValue: any) => string
  align?: 'left' | 'center' | 'right'
  headerAlign?: 'left' | 'center' | 'right'
  showOverflowTooltip?: boolean
  resizable?: boolean
}

// 表单验证规则类型
export interface FormRule {
  required?: boolean
  message?: string
  trigger?: string | string[]
  min?: number
  max?: number
  len?: number
  pattern?: RegExp
  validator?: (rule: any, value: any, callback: any) => void
  type?: 'string' | 'number' | 'boolean' | 'method' | 'regexp' | 'integer' | 'float' | 'array' | 'object' | 'enum' | 'date' | 'url' | 'hex' | 'email'
}

// 菜单项类型
export interface MenuItem {
  id: string
  title: string
  icon?: string
  path?: string
  component?: string
  redirect?: string
  children?: MenuItem[]
  meta?: {
    title?: string
    icon?: string
    roles?: string[]
    permissions?: string[]
    hidden?: boolean
    alwaysShow?: boolean
    noCache?: boolean
    breadcrumb?: boolean
    affix?: boolean
  }
}

// 用户信息类型
export interface UserInfo {
  id: number
  username: string
  email: string
  full_name?: string
  avatar?: string
  roles: string[]
  permissions: string[]
  last_login?: string
  is_active: boolean
}

// 路由元信息类型
export interface RouteMeta {
  title?: string
  icon?: string
  roles?: string[]
  permissions?: string[]
  hidden?: boolean
  alwaysShow?: boolean
  noCache?: boolean
  breadcrumb?: boolean
  affix?: boolean
  activeMenu?: string
}

// 面包屑项类型
export interface BreadcrumbItem {
  title: string
  path?: string
  icon?: string
}

// 通知消息类型
export interface NotificationItem {
  id: string
  title: string
  content: string
  type: 'info' | 'success' | 'warning' | 'error'
  read: boolean
  created_at: string
  action?: {
    text: string
    url: string
  }
}

// 文件上传类型
export interface UploadFile {
  name: string
  size: number
  type: string
  url?: string
  status: 'ready' | 'uploading' | 'success' | 'error'
  percent?: number
  response?: any
  error?: string
}

// 图表配置类型
export interface ChartConfig {
  type: 'line' | 'bar' | 'pie' | 'scatter' | 'radar' | 'gauge' | 'funnel'
  title?: string
  data: any[]
  xAxis?: any
  yAxis?: any
  series?: any[]
  legend?: any
  tooltip?: any
  grid?: any
  color?: string[]
  animation?: boolean
  responsive?: boolean
}

// 主题配置类型
export interface ThemeConfig {
  mode: 'light' | 'dark' | 'auto'
  primaryColor: string
  layout: 'vertical' | 'horizontal' | 'mix'
  sidebarCollapsed: boolean
  showBreadcrumb: boolean
  showTabs: boolean
  showFooter: boolean
  fixedHeader: boolean
  fixedSidebar: boolean
}

// 系统设置类型
export interface SystemSettings {
  theme: ThemeConfig
  language: string
  timezone: string
  dateFormat: string
  timeFormat: string
  pageSize: number
  autoRefresh: boolean
  refreshInterval: number
}

// 操作日志类型
export interface OperationLog {
  id: number
  user_id: number
  username: string
  action: string
  resource: string
  resource_id?: string
  ip_address: string
  user_agent: string
  details?: Record<string, any>
  created_at: string
}

// 错误信息类型
export interface ErrorInfo {
  code: string | number
  message: string
  details?: any
  stack?: string
  timestamp: string
}

// WebSocket消息类型
export interface WebSocketMessage {
  type: string
  data: any
  timestamp: string
  id?: string
}

// 导出配置类型
export interface ExportConfig {
  format: 'csv' | 'excel' | 'pdf'
  filename?: string
  fields?: string[]
  filters?: Record<string, any>
  options?: Record<string, any>
}

// 搜索配置类型
export interface SearchConfig {
  placeholder?: string
  fields: string[]
  operators?: ('=' | '!=' | '>' | '<' | '>=' | '<=' | 'like' | 'in' | 'not_in')[]
  suggestions?: boolean
  history?: boolean
  maxHistory?: number
}

// 权限定义类型
export interface Permission {
  id: string
  name: string
  description?: string
  resource: string
  action: string
  conditions?: Record<string, any>
}

// 角色定义类型
export interface Role {
  id: string
  name: string
  description?: string
  permissions: Permission[]
  is_system?: boolean
  created_at: string
  updated_at: string
}

// 类型工具函数
export type ComponentProps<T> = T extends new (...args: any[]) => any
  ? InstanceType<T>['$props']
  : never

export type EventHandler<T = Event> = (event: T) => void
export type AsyncFunction<T = any> = (...args: any[]) => Promise<T>
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>
export type RequiredFields<T, K extends keyof T> = T & { [P in K]-?: T[P] }
export type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P]
}
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}
export type ValueOf<T> = T[keyof T]

export {}