// API响应基础类型
export interface ApiResponse<T = any> {
  success: boolean
  message?: string
  code?: string
  data?: T
}

export interface PaginatedResponse<T> {
  total: number
  items: T[]
  page: number
  size: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

// 用户相关类型
export interface User {
  id: number
  username: string
  full_name?: string
  email: string
  role: string
  is_active: boolean
  avatar?: string
  last_login?: string
  notes?: string
  created_at: string
  updated_at: string
  roles?: Role[]
}

export interface UserStatistics {
  total: number
  active: number
  inactive: number
  admins: number
}

export interface Role {
  id: number
  name: string
  description?: string
  created_at: string
}

export interface Permission {
  id: number
  name: string
  description?: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface RefreshTokenRequest {
  refresh_token: string
}

export interface ChangePasswordRequest {
  old_password: string
  new_password: string
}

export interface ResetPasswordRequest {
  email: string
}

export interface CreateUserRequest {
  username: string
  email: string
  password: string
  full_name?: string
  role: string
  is_active?: boolean
  notes?: string
}

export interface UpdateUserRequest {
  email?: string
  full_name?: string
  role?: string
  is_active?: boolean
  notes?: string
}

// 安全态势相关类型
export interface SecurityMetrics {
  today_alerts: number
  unhandled_alerts: number
  affected_assets: number
  active_hunting_tasks: number
  handled_events: number
}

export interface AlertTrendData {
  dates: string[]
  counts: number[]
  critical_counts: number[]
  high_counts: number[]
  medium_counts: number[]
}

export interface ThreatDistribution {
  types: string[]
  counts: number[]
}

export interface AssetStatusDistribution {
  normal: number
  warning: number
  danger: number
  offline: number
  normal_percent: number
  warning_percent: number
  danger_percent: number
  offline_percent: number
  total: number
}

export interface RecentAlert {
  id: number
  alert_name: string
  severity: string
  asset_name: string
  created_at: string
}

// 告警相关类型
export interface Alert {
  id: number
  alert_name: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  description?: string
  event_id?: number
  asset_id: number
  status: 'unhandled' | 'handling' | 'resolved'
  created_at: string
  updated_at: string
  handled_by?: number
  handle_notes?: string
  handled_at?: string
  asset_name?: string
  handler_name?: string
}

export interface AlertRule {
  id: number
  name: string
  description?: string
  condition: Record<string, any>
  severity: string
  enabled: boolean
  created_at: string
  updated_at: string
}

export interface HandleAlertRequest {
  status: 'handling' | 'resolved'
  handle_notes?: string
}

export interface CreateAlertRuleRequest {
  name: string
  description?: string
  condition: Record<string, any>
  severity: string
  enabled?: boolean
}

export interface AlertStatistics {
  total: number
  unhandled: number
  handling: number
  resolved: number
  critical: number
  high: number
  medium: number
  low: number
}

// 资产相关类型
export interface Asset {
  id: number
  name: string
  asset_type: string
  ip_address: string
  mac_address?: string
  os_version?: string
  status: 'normal' | 'warning' | 'danger' | 'offline'
  is_honeypot: boolean
  is_virtual: boolean
  created_at: string
  updated_at: string
  vulnerability_count?: number
  alert_count?: number
  last_checkin?: string
}

export interface CreateAssetRequest {
  name: string
  asset_type: string
  ip_address: string
  mac_address?: string
  os_version?: string
  is_honeypot?: boolean
  is_virtual?: boolean
}

export interface UpdateAssetRequest {
  name?: string
  asset_type?: string
  ip_address?: string
  mac_address?: string
  os_version?: string
  status?: string
  is_honeypot?: boolean
  is_virtual?: boolean
}

export interface AssetStatistics {
  total: number
  normal: number
  warning: number
  danger: number
  offline: number
  honeypots: number
  virtual: number
}

// 威胁狩猎相关类型
export interface HuntingTask {
  id: number
  name: string
  query_string: string
  query_type: 'advanced' | 'visual'
  created_by: number
  created_at: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  result_count: number
  completed_at?: string
  creator_name?: string
}

export interface HuntingTemplate {
  id: number
  name: string
  description: string
  query_template: string
  category: string
  difficulty: 'easy' | 'medium' | 'hard'
  tags: string[]
}

// 威胁情报相关类型
export interface IOC {
  id: number
  ioc_type: string
  value: string
  threat_type?: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  source?: string
  confidence?: number
  first_seen: string
  last_seen: string
  expires_at?: string
  is_active: boolean
}

// 调查相关类型
export interface InvestigationSession {
  id: number
  name: string
  description?: string
  created_by: number
  created_at: string
  updated_at: string
  status: 'active' | 'completed' | 'archived'
  creator_name?: string
}

// 报告相关类型
export interface ReportTemplate {
  id: number
  name: string
  description: string
  template_type: string
  content_template: string
  created_at: string
  created_by: string
}

export interface Report {
  id: number
  name: string
  description?: string
  template_id: number
  template_name: string
  status: 'generating' | 'completed' | 'failed'
  file_path?: string
  file_size?: number
  created_at: string
  completed_at?: string
  created_by: string
}

// 系统相关类型
export interface SystemInfo {
  hostname: string
  platform: string
  platform_version: string
  architecture: string
  cpu_count: number
  memory_total: number
  disk_total: number
  uptime: number
  python_version: string
}

export interface SystemStatus {
  cpu_usage: number
  memory_usage: number
  disk_usage: number
  network_io: {
    bytes_sent: number
    bytes_recv: number
  }
  active_connections: number
  load_average?: number[]
}

export interface HealthCheckResponse {
  status: string
  timestamp: string
  version: string
  database: string
  services: Record<string, string>
}

// 系统设置相关类型
export interface SystemSettings {
  basic: BasicSettings
  security: SecuritySettings
  email: EmailSettings
  monitoring: MonitoringSettings
  backup: BackupSettings
}

export interface BasicSettings {
  system_name: string
  system_description: string
  system_version: string
  admin_email: string
  timezone: string
  session_timeout: number
  remember_login_enabled: boolean
  concurrent_login_enabled: boolean
  force_logout_enabled: boolean
}

export interface SecuritySettings {
  min_password_length: number
  password_requirements: string[]
  password_expiry_days: number
  password_history_count: number
  login_lockout_enabled: boolean
  max_login_attempts: number
  lockout_duration: number
  captcha_enabled: boolean
  two_factor_enabled: boolean
}

export interface EmailSettings {
  smtp_host: string
  smtp_port: number
  smtp_security: string
  smtp_username: string
  smtp_password: string
  sender_name: string
  sender_email: string
  notification_types: string[]
}

export interface MonitoringSettings {
  log_level: string
  log_retention_days: number
  metrics_enabled: boolean
  performance_monitoring: boolean
  error_reporting: boolean
  audit_log_enabled: boolean
}

export interface BackupSettings {
  auto_backup_enabled: boolean
  backup_frequency: string
  backup_retention_days: number
  backup_location: string
  include_logs: boolean
  compress_backups: boolean
}

// 通用查询参数类型
export interface PaginationParams {
  page?: number
  size?: number
}

export interface SearchParams extends PaginationParams {
  search?: string
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

export interface DateRangeParams {
  start_date?: string
  end_date?: string
}

export interface AlertQueryParams extends SearchParams, DateRangeParams {
  severity?: string
  status?: string
  asset_id?: number
}

export interface AssetQueryParams extends SearchParams {
  asset_type?: string
  status?: string
  is_honeypot?: boolean
}

export interface UserQueryParams extends SearchParams {
  role?: string
  is_active?: boolean
}

export interface IOCQueryParams extends SearchParams {
  ioc_type?: string
  threat_type?: string
  severity?: string
  is_active?: boolean
}

// 批量操作类型
export interface BatchOperation<T = any> {
  action: string
  ids: number[]
  params?: T
}

export interface BatchResponse {
  success_count: number
  failed_count: number
  errors?: string[]
}

// 文件上传类型
export interface FileUploadResponse {
  filename: string
  file_size: number
  file_path: string
  upload_time: string
}

// 导出类型
export interface ExportRequest {
  format: 'csv' | 'excel' | 'pdf'
  filters?: Record<string, any>
  fields?: string[]
}

export interface ExportResponse {
  task_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  download_url?: string
  created_at: string
}
