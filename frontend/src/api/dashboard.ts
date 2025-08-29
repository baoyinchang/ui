/**
 * 安全态势API接口
 */

import { http } from './request'
import type {
  SecurityMetrics,
  AlertTrendData,
  ThreatDistribution,
  AssetStatusDistribution
} from '@/types/api'
import { mockDashboardApi } from './mock/dashboard'

// 检查是否为开发模式且禁用认证
const isDevelopmentMode = import.meta.env.VITE_ENABLE_AUTH !== 'true'

/**
 * 真实的安全态势API接口
 */
const realDashboardApi = {
  /**
   * 获取安全态势总览
   */
  getSecurityOverview(): Promise<{
    alert_summary: {
      total: number
      unhandled: number
      critical: number
      high: number
      medium: number
      low: number
      today_new: number
    }
    asset_summary: {
      total: number
      online: number
      offline: number
      honeypots: number
      critical_assets: number
    }
    threat_summary: {
      active_threats: number
      blocked_attacks: number
      ioc_matches: number
      hunting_results: number
    }
    investigation_summary: {
      active_sessions: number
      completed_today: number
      avg_resolution_time: number
    }
  }> {
    return http.get('/dashboard/overview')
  },

  /**
   * 获取安全指标
   */
  getSecurityMetrics(timeRange?: string): Promise<SecurityMetrics> {
    return http.get('/dashboard/metrics', { params: { time_range: timeRange } })
  },

  /**
   * 获取告警趋势数据
   */
  getAlertTrends(days: number = 30): Promise<AlertTrendData> {
    return http.get('/dashboard/alert-trends', { params: { days } })
  },

  /**
   * 获取威胁分布数据
   */
  getThreatDistribution(): Promise<ThreatDistribution> {
    return http.get('/dashboard/threat-distribution')
  },

  /**
   * 获取资产状态分布
   */
  getAssetStatusDistribution(): Promise<AssetStatusDistribution> {
    return http.get('/dashboard/asset-status')
  },

  /**
   * 获取实时告警流
   */
  getRealtimeAlerts(limit?: number): Promise<Array<{
    id: number
    alert_name: string
    severity: string
    asset_name: string
    created_at: string
    status: string
  }>> {
    return http.get('/dashboard/realtime-alerts', { params: { limit } })
  },

  /**
   * 获取热门攻击类型
   */
  getTopAttackTypes(days: number = 7): Promise<Array<{
    attack_type: string
    count: number
    percentage: number
    trend: 'up' | 'down' | 'stable'
  }>> {
    return http.get('/dashboard/top-attacks', { params: { days } })
  },

  /**
   * 获取系统健康状态
   */
  getSystemHealth(): Promise<{
    overall_status: 'healthy' | 'warning' | 'critical'
    components: Array<{
      name: string
      status: 'healthy' | 'warning' | 'critical' | 'offline'
      response_time?: number
      last_check: string
      message?: string
    }>
    performance: {
      cpu_usage: number
      memory_usage: number
      disk_usage: number
      network_io: {
        bytes_sent: number
        bytes_recv: number
      }
    }
  }> {
    return http.get('/dashboard/system-health')
  },

  /**
   * 获取威胁狩猎结果摘要
   */
  getHuntingSummary(): Promise<{
    active_hunts: number
    completed_hunts: number
    total_results: number
    high_confidence_results: number
    recent_hunts: Array<{
      id: number
      name: string
      status: string
      results_count: number
      created_at: string
    }>
  }> {
    return http.get('/dashboard/hunting-summary')
  },

  /**
   * 获取威胁情报摘要
   */
  getIntelligenceSummary(): Promise<{
    total_iocs: number
    active_iocs: number
    recent_matches: number
    feed_status: Array<{
      name: string
      status: 'active' | 'inactive' | 'error'
      last_update: string
      ioc_count: number
    }>
    top_threat_types: Array<{
      type: string
      count: number
    }>
  }> {
    return http.get('/dashboard/intelligence-summary')
  },

  /**
   * 获取风险评分
   */
  getRiskScore(): Promise<{
    overall_risk: number
    risk_level: 'low' | 'medium' | 'high' | 'critical'
    risk_factors: Array<{
      category: string
      score: number
      weight: number
      description: string
      recommendations: string[]
    }>
    trend: Array<{
      date: string
      score: number
    }>
  }> {
    return http.get('/dashboard/risk-score')
  },

  /**
   * 获取自定义仪表板配置
   */
  getDashboardConfig(userId?: number): Promise<{
    layout: Array<{
      id: string
      type: string
      title: string
      position: {
        x: number
        y: number
        w: number
        h: number
      }
      config: any
    }>
    refresh_interval: number
    theme: string
  }> {
    return http.get('/dashboard/config', { params: { user_id: userId } })
  },

  /**
   * 保存自定义仪表板配置
   */
  saveDashboardConfig(config: {
    layout: Array<{
      id: string
      type: string
      title: string
      position: {
        x: number
        y: number
        w: number
        h: number
      }
      config: any
    }>
    refresh_interval?: number
    theme?: string
  }): Promise<{ success: boolean; message: string }> {
    return http.post('/dashboard/config', config)
  },

  /**
   * 获取仪表板小部件数据
   */
  getWidgetData(widgetType: string, config?: any): Promise<any> {
    return http.post('/dashboard/widget-data', {
      widget_type: widgetType,
      config
    })
  },

  /**
   * 获取大屏数据（兼容旧版本）
   */
  getBigScreenData(): Promise<{
    metrics: SecurityMetrics
    alert_trend: AlertTrendData
    threat_distribution: ThreatDistribution
    asset_status: AssetStatusDistribution
    recent_alerts: Array<{
      id: number
      alert_name: string
      severity: string
      asset_name: string
      created_at: string
      status: string
    }>
  }> {
    return http.get('/dashboard/big-screen')
  },

  /**
   * 获取地理威胁分布（SecurityOverview需要）
   */
  getGeoThreatDistribution(): Promise<Array<{
    name: string
    value: [number, number, number]
  }>> {
    return http.get('/dashboard/geo-threats')
  }
}

// 为模拟API添加缺失的方法
const enhancedMockDashboardApi = {
  ...mockDashboardApi,

  // 添加真实API中存在但模拟API中缺失的方法
  async getSecurityMetrics(timeRange?: string) {
    return mockDashboardApi.getSecurityMetrics(timeRange)
  },

  async getTopAttackTypes(days: number = 7) {
    await new Promise(resolve => setTimeout(resolve, 400))
    return [
      { attack_type: '恶意软件', count: 234, percentage: 35.2, trend: 'up' as const },
      { attack_type: '网络扫描', count: 189, percentage: 28.4, trend: 'down' as const },
      { attack_type: '暴力破解', count: 156, percentage: 23.5, trend: 'up' as const },
      { attack_type: '钓鱼攻击', count: 87, percentage: 13.1, trend: 'stable' as const }
    ]
  },

  async getHuntingSummary() {
    await new Promise(resolve => setTimeout(resolve, 300))
    return {
      active_hunts: 8,
      completed_hunts: 156,
      total_results: 2847,
      high_confidence_results: 89,
      recent_hunts: [
        { id: 1, name: 'APT检测规则', status: 'running', results_count: 23, created_at: new Date().toISOString() },
        { id: 2, name: '异常网络流量', status: 'completed', results_count: 45, created_at: new Date().toISOString() }
      ]
    }
  },

  async getRiskScore() {
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      overall_risk: 78,
      risk_level: 'medium' as const,
      risk_factors: [
        { category: '网络安全', score: 85, weight: 0.3, description: '网络防护良好', recommendations: ['加强边界防护'] },
        { category: '终端安全', score: 72, weight: 0.25, description: '终端防护一般', recommendations: ['更新防病毒软件'] }
      ],
      trend: [
        { date: '2024-01-01', score: 75 },
        { date: '2024-01-02', score: 78 }
      ]
    }
  },

  async getDashboardConfig(userId?: number) {
    await new Promise(resolve => setTimeout(resolve, 200))
    return {
      layout: [],
      refresh_interval: 30,
      theme: 'default'
    }
  },

  async saveDashboardConfig(config: any) {
    await new Promise(resolve => setTimeout(resolve, 300))
    return { success: true, message: '配置保存成功' }
  },

  async getWidgetData(widgetType: string, config?: any) {
    await new Promise(resolve => setTimeout(resolve, 400))
    return { data: [], message: '模拟数据' }
  },

  async getBigScreenData() {
    await new Promise(resolve => setTimeout(resolve, 600))
    const metrics = await this.getSecurityMetrics()
    const alert_trend = await this.getAlertTrends()
    const threat_distribution = await this.getThreatDistribution()
    const asset_status = await this.getAssetStatusDistribution()
    const recent_alerts = await this.getRealtimeAlerts(5)

    return {
      metrics,
      alert_trend,
      threat_distribution,
      asset_status,
      recent_alerts
    }
  }
}

// 导出适当的API
export const dashboardApi = isDevelopmentMode ? enhancedMockDashboardApi : realDashboardApi

// 开发模式提示
if (isDevelopmentMode) {
  console.log('🔧 开发模式：使用模拟仪表板API')
}
