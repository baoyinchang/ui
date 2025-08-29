/**
 * 仪表板模拟API - 开发模式使用
 */

// 模拟网络延迟
const delay = (ms: number = 500) => new Promise(resolve => setTimeout(resolve, ms))

/**
 * 模拟仪表板API接口
 */
export const mockDashboardApi = {
  /**
   * 获取安全态势总览
   */
  async getSecurityOverview() {
    await delay(800)
    return {
      alert_summary: {
        total: 1247,
        unhandled: 23,
        critical: 5,
        high: 18,
        medium: 156,
        low: 1068,
        today_new: 47
      },
      asset_summary: {
        total: 342,
        online: 298,
        offline: 44,
        honeypots: 12,
        critical_assets: 28
      },
      threat_summary: {
        active_threats: 15,
        blocked_attacks: 2847,
        ioc_matches: 89,
        hunting_results: 156
      },
      investigation_summary: {
        active_sessions: 8,
        completed_today: 12,
        avg_resolution_time: 45
      }
    }
  },

  /**
   * 获取告警趋势数据
   */
  async getAlertTrends(days: number = 30) {
    await delay(600)
    
    const dates = []
    const criticalData = []
    const highData = []
    const mediumData = []
    const lowData = []
    
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      dates.push(date.toISOString().split('T')[0])
      
      criticalData.push(Math.floor(Math.random() * 10) + 1)
      highData.push(Math.floor(Math.random() * 20) + 5)
      mediumData.push(Math.floor(Math.random() * 50) + 10)
      lowData.push(Math.floor(Math.random() * 100) + 20)
    }
    
    return {
      dates,
      series: [
        { name: '严重', data: criticalData, color: '#ff4757' },
        { name: '高危', data: highData, color: '#ff6b35' },
        { name: '中危', data: mediumData, color: '#ffa502' },
        { name: '低危', data: lowData, color: '#26de81' }
      ]
    }
  },

  /**
   * 获取威胁分布数据
   */
  async getThreatDistribution() {
    await delay(400)
    return [
      { name: '恶意软件', value: 234, color: '#ff4757' },
      { name: '网络攻击', value: 189, color: '#ff6b35' },
      { name: '数据泄露', value: 156, color: '#ffa502' },
      { name: '钓鱼攻击', value: 98, color: '#26de81' },
      { name: '内部威胁', value: 67, color: '#3742fa' },
      { name: '其他', value: 45, color: '#a4b0be' }
    ]
  },

  /**
   * 获取资产状态分布
   */
  async getAssetStatusDistribution() {
    await delay(300)
    return [
      { status: '在线', count: 298, color: '#26de81' },
      { status: '离线', count: 44, color: '#ff4757' },
      { status: '维护中', count: 12, color: '#ffa502' },
      { status: '未知', count: 8, color: '#a4b0be' }
    ]
  },

  /**
   * 获取地理威胁分布
   */
  async getGeoThreatDistribution() {
    await delay(500)
    return [
      { name: '北京', value: [116.46, 39.92, 89] },
      { name: '上海', value: [121.48, 31.22, 67] },
      { name: '广州', value: [113.23, 23.16, 45] },
      { name: '深圳', value: [114.07, 22.62, 78] },
      { name: '杭州', value: [120.19, 30.26, 34] },
      { name: '成都', value: [104.06, 30.67, 23] },
      { name: '西安', value: [108.95, 34.27, 19] },
      { name: '武汉', value: [114.31, 30.52, 28] }
    ]
  },

  /**
   * 获取实时告警
   */
  async getRealtimeAlerts(limit: number = 5) {
    await delay(200)
    
    const alertTypes = ['恶意软件检测', '异常登录', '数据泄露', '网络攻击', '权限提升']
    const severities = ['critical', 'high', 'medium', 'low']
    const assets = ['Web服务器-01', '数据库-02', '邮件服务器', '文件服务器', '域控制器']
    const statuses = ['unhandled', 'investigating', 'resolved']
    
    const alerts = []
    for (let i = 0; i < limit; i++) {
      const date = new Date()
      date.setMinutes(date.getMinutes() - Math.floor(Math.random() * 60))
      
      alerts.push({
        id: 1000 + i,
        alert_name: alertTypes[Math.floor(Math.random() * alertTypes.length)],
        severity: severities[Math.floor(Math.random() * severities.length)],
        asset_name: assets[Math.floor(Math.random() * assets.length)],
        created_at: date.toISOString(),
        status: statuses[Math.floor(Math.random() * statuses.length)]
      })
    }
    
    return alerts
  },

  /**
   * 获取系统健康状态
   */
  async getSystemHealth() {
    await delay(300)
    return {
      overall_status: 'healthy' as const,
      components: [
        {
          name: '告警引擎',
          status: 'healthy' as const,
          response_time: 45,
          last_check: new Date().toISOString(),
          message: '运行正常'
        },
        {
          name: '数据采集',
          status: 'healthy' as const,
          response_time: 23,
          last_check: new Date().toISOString(),
          message: '数据流正常'
        },
        {
          name: '威胁检测',
          status: 'warning' as const,
          response_time: 89,
          last_check: new Date().toISOString(),
          message: '响应时间较慢'
        },
        {
          name: '蜜罐服务',
          status: 'healthy' as const,
          response_time: 12,
          last_check: new Date().toISOString(),
          message: '12个蜜罐在线'
        }
      ],
      performance: {
        cpu_usage: 45.6,
        memory_usage: 67.8,
        disk_usage: 23.4,
        network_io: {
          bytes_sent: 1024 * 1024 * 45,
          bytes_recv: 1024 * 1024 * 89
        }
      }
    }
  },

  /**
   * 获取威胁情报摘要
   */
  async getIntelligenceSummary() {
    await delay(400)
    return {
      total: 45678,
      active: 12345,
      todayNew: 234,
      matches: 89,
      feeds: [
        { name: 'AlienVault OTX', status: 'active', lastUpdate: '2分钟前', count: 12456 },
        { name: 'VirusTotal', status: 'active', lastUpdate: '5分钟前', count: 8934 },
        { name: 'Malware Domain List', status: 'warning', lastUpdate: '1小时前', count: 3456 },
        { name: 'Emerging Threats', status: 'active', lastUpdate: '3分钟前', count: 15678 }
      ]
    }
  },

  /**
   * 获取安全指标
   */
  async getSecurityMetrics(timeRange?: string) {
    await delay(500)
    return {
      security_score: 78,
      risk_level: 'medium' as const,
      total_alerts: 1247,
      critical_alerts: 5,
      resolved_alerts: 1156,
      active_threats: 15,
      blocked_attacks: 2847,
      monitored_assets: 342,
      honeypot_interactions: 156,
      threat_intelligence_matches: 89
    }
  }
}
