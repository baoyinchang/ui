/**
 * 系统常量定义
 */

// API相关常量
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  TIMEOUT: 30000,
  RETRY_COUNT: 3
}

// 存储键名
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'hsystem-access-token',
  REFRESH_TOKEN: 'hsystem-refresh-token',
  USER_INFO: 'hsystem-user-info',
  USER_SETTINGS: 'hsystem-user-settings',
  THEME: 'hsystem-theme',
  LANGUAGE: 'hsystem-language',
  SIDEBAR_COLLAPSED: 'hsystem-sidebar-collapsed',
  SEARCH_HISTORY: 'hsystem-search-history',
  RECENT_VISITS: 'hsystem-recent-visits'
}

// HTTP状态码
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  METHOD_NOT_ALLOWED: 405,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
  BAD_GATEWAY: 502,
  SERVICE_UNAVAILABLE: 503,
  GATEWAY_TIMEOUT: 504
} as const

// 告警严重程度
export const ALERT_SEVERITY = {
  CRITICAL: 'critical',
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low'
} as const

export const ALERT_SEVERITY_LABELS = {
  [ALERT_SEVERITY.CRITICAL]: '紧急',
  [ALERT_SEVERITY.HIGH]: '高危',
  [ALERT_SEVERITY.MEDIUM]: '中危',
  [ALERT_SEVERITY.LOW]: '低危'
}

export const ALERT_SEVERITY_COLORS = {
  [ALERT_SEVERITY.CRITICAL]: '#f56c6c',
  [ALERT_SEVERITY.HIGH]: '#e6a23c',
  [ALERT_SEVERITY.MEDIUM]: '#409eff',
  [ALERT_SEVERITY.LOW]: '#909399'
}

// 告警状态
export const ALERT_STATUS = {
  UNHANDLED: 'unhandled',
  HANDLING: 'handling',
  RESOLVED: 'resolved'
} as const

export const ALERT_STATUS_LABELS = {
  [ALERT_STATUS.UNHANDLED]: '未处理',
  [ALERT_STATUS.HANDLING]: '处理中',
  [ALERT_STATUS.RESOLVED]: '已解决'
}

export const ALERT_STATUS_COLORS = {
  [ALERT_STATUS.UNHANDLED]: '#f56c6c',
  [ALERT_STATUS.HANDLING]: '#e6a23c',
  [ALERT_STATUS.RESOLVED]: '#67c23a'
}

// 资产类型
export const ASSET_TYPES = {
  SERVER: 'server',
  WORKSTATION: 'workstation',
  NETWORK_DEVICE: 'network_device',
  SECURITY_DEVICE: 'security_device',
  MOBILE_DEVICE: 'mobile_device',
  IOT_DEVICE: 'iot_device',
  VIRTUAL_MACHINE: 'virtual_machine',
  CONTAINER: 'container'
} as const

export const ASSET_TYPE_LABELS = {
  [ASSET_TYPES.SERVER]: '服务器',
  [ASSET_TYPES.WORKSTATION]: '工作站',
  [ASSET_TYPES.NETWORK_DEVICE]: '网络设备',
  [ASSET_TYPES.SECURITY_DEVICE]: '安全设备',
  [ASSET_TYPES.MOBILE_DEVICE]: '移动设备',
  [ASSET_TYPES.IOT_DEVICE]: 'IoT设备',
  [ASSET_TYPES.VIRTUAL_MACHINE]: '虚拟机',
  [ASSET_TYPES.CONTAINER]: '容器'
}

// 资产状态
export const ASSET_STATUS = {
  NORMAL: 'normal',
  WARNING: 'warning',
  DANGER: 'danger',
  OFFLINE: 'offline'
} as const

export const ASSET_STATUS_LABELS = {
  [ASSET_STATUS.NORMAL]: '正常',
  [ASSET_STATUS.WARNING]: '警告',
  [ASSET_STATUS.DANGER]: '危险',
  [ASSET_STATUS.OFFLINE]: '离线'
}

// IOC类型
export const IOC_TYPES = {
  IP: 'ip',
  DOMAIN: 'domain',
  URL: 'url',
  FILE_HASH: 'file_hash',
  EMAIL: 'email',
  REGISTRY_KEY: 'registry_key',
  MUTEX: 'mutex',
  USER_AGENT: 'user_agent'
} as const

export const IOC_TYPE_LABELS = {
  [IOC_TYPES.IP]: 'IP地址',
  [IOC_TYPES.DOMAIN]: '域名',
  [IOC_TYPES.URL]: 'URL',
  [IOC_TYPES.FILE_HASH]: '文件哈希',
  [IOC_TYPES.EMAIL]: '邮箱地址',
  [IOC_TYPES.REGISTRY_KEY]: '注册表键',
  [IOC_TYPES.MUTEX]: '互斥体',
  [IOC_TYPES.USER_AGENT]: 'User Agent'
}

// 威胁类型
export const THREAT_TYPES = {
  MALWARE: 'malware',
  PHISHING: 'phishing',
  BOTNET: 'botnet',
  APT: 'apt',
  RANSOMWARE: 'ransomware',
  TROJAN: 'trojan',
  WORM: 'worm',
  VIRUS: 'virus',
  ROOTKIT: 'rootkit',
  SPYWARE: 'spyware'
} as const

export const THREAT_TYPE_LABELS = {
  [THREAT_TYPES.MALWARE]: '恶意软件',
  [THREAT_TYPES.PHISHING]: '钓鱼攻击',
  [THREAT_TYPES.BOTNET]: '僵尸网络',
  [THREAT_TYPES.APT]: 'APT攻击',
  [THREAT_TYPES.RANSOMWARE]: '勒索软件',
  [THREAT_TYPES.TROJAN]: '木马',
  [THREAT_TYPES.WORM]: '蠕虫',
  [THREAT_TYPES.VIRUS]: '病毒',
  [THREAT_TYPES.ROOTKIT]: 'Rootkit',
  [THREAT_TYPES.SPYWARE]: '间谍软件'
}

// 狩猎任务状态
export const HUNTING_STATUS = {
  PENDING: 'pending',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed'
} as const

export const HUNTING_STATUS_LABELS = {
  [HUNTING_STATUS.PENDING]: '待执行',
  [HUNTING_STATUS.RUNNING]: '运行中',
  [HUNTING_STATUS.COMPLETED]: '已完成',
  [HUNTING_STATUS.FAILED]: '失败'
}

// 调查会话状态
export const INVESTIGATION_STATUS = {
  ACTIVE: 'active',
  COMPLETED: 'completed',
  ARCHIVED: 'archived'
} as const

export const INVESTIGATION_STATUS_LABELS = {
  [INVESTIGATION_STATUS.ACTIVE]: '进行中',
  [INVESTIGATION_STATUS.COMPLETED]: '已完成',
  [INVESTIGATION_STATUS.ARCHIVED]: '已归档'
}

// 报告状态
export const REPORT_STATUS = {
  GENERATING: 'generating',
  COMPLETED: 'completed',
  FAILED: 'failed'
} as const

export const REPORT_STATUS_LABELS = {
  [REPORT_STATUS.GENERATING]: '生成中',
  [REPORT_STATUS.COMPLETED]: '已完成',
  [REPORT_STATUS.FAILED]: '失败'
}

// 用户角色
export const USER_ROLES = {
  ADMIN: 'admin',
  ANALYST: 'analyst',
  OPERATOR: 'operator',
  VIEWER: 'viewer'
} as const

export const USER_ROLE_LABELS = {
  [USER_ROLES.ADMIN]: '系统管理员',
  [USER_ROLES.ANALYST]: '安全分析师',
  [USER_ROLES.OPERATOR]: '安全运维',
  [USER_ROLES.VIEWER]: '只读用户'
}

// 分页配置
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZES: [10, 20, 50, 100],
  MAX_PAGE_SIZE: 1000
}

// 文件上传配置
export const UPLOAD_CONFIG = {
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'text/plain'],
  CHUNK_SIZE: 1024 * 1024 // 1MB
}

// 图表颜色配置
export const CHART_COLORS = [
  '#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399',
  '#53a8ff', '#85ce61', '#ebb563', '#f78989', '#a6a9ad',
  '#36cfc9', '#b37feb', '#ff9c6e', '#73d13d', '#40a9ff'
]

// 时间格式
export const TIME_FORMATS = {
  DATE: 'YYYY-MM-DD',
  TIME: 'HH:mm:ss',
  DATETIME: 'YYYY-MM-DD HH:mm:ss',
  DATETIME_SHORT: 'MM-DD HH:mm',
  ISO: 'YYYY-MM-DDTHH:mm:ss.SSSZ'
}

// 正则表达式
export const REGEX_PATTERNS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  IP: /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/,
  URL: /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/,
  PHONE: /^1[3-9]\d{9}$/,
  PASSWORD: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/
}

// 系统配置
export const SYSTEM_CONFIG = {
  APP_NAME: 'H-System EDR平台',
  VERSION: '1.0.0',
  COPYRIGHT: '© 2024 H-System. All rights reserved.',
  SUPPORT_EMAIL: 'support@hsystem.com',
  DOCUMENTATION_URL: 'https://docs.hsystem.com'
}
