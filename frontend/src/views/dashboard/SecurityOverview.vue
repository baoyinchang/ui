<template>
  <div class="security-overview">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h2 class="page-title">安全态势总览</h2>
        <p class="page-description">实时监控网络安全状况和威胁态势</p>
      </div>
      <div class="header-right">
        <el-button-group>
          <el-button
            v-for="period in timePeriods"
            :key="period.value"
            :type="selectedPeriod === period.value ? 'primary' : 'default'"
            @click="handlePeriodChange(period.value)"
          >
            {{ period.label }}
          </el-button>
        </el-button-group>
        <el-button :icon="Refresh" @click="refreshData">刷新</el-button>
      </div>
    </div>

    <!-- 核心指标卡片 -->
    <div class="metrics-cards">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-card class="metric-card critical">
            <div class="metric-content">
              <div class="metric-icon">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="metric-info">
                <div class="metric-value">{{ metrics.criticalAlerts }}</div>
                <div class="metric-label">严重告警</div>
                <div class="metric-trend" :class="getTrendClass(metrics.criticalTrend)">
                  <el-icon><component :is="getTrendIcon(metrics.criticalTrend)" /></el-icon>
                  {{ Math.abs(metrics.criticalTrend) }}%
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="metric-card threats">
            <div class="metric-content">
              <div class="metric-icon">
                <el-icon><Lock /></el-icon>
              </div>
              <div class="metric-info">
                <div class="metric-value">{{ metrics.activeThreats }}</div>
                <div class="metric-label">活跃威胁</div>
                <div class="metric-trend" :class="getTrendClass(metrics.threatsTrend)">
                  <el-icon><component :is="getTrendIcon(metrics.threatsTrend)" /></el-icon>
                  {{ Math.abs(metrics.threatsTrend) }}%
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="metric-card assets">
            <div class="metric-content">
              <div class="metric-icon">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="metric-info">
                <div class="metric-value">{{ metrics.totalAssets }}</div>
                <div class="metric-label">监控资产</div>
                <div class="metric-trend" :class="getTrendClass(metrics.assetsTrend)">
                  <el-icon><component :is="getTrendIcon(metrics.assetsTrend)" /></el-icon>
                  {{ Math.abs(metrics.assetsTrend) }}%
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="metric-card score">
            <div class="metric-content">
              <div class="metric-icon">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="metric-info">
                <div class="metric-value">{{ metrics.securityScore }}</div>
                <div class="metric-label">安全评分</div>
                <div class="metric-trend" :class="getTrendClass(metrics.scoreTrend)">
                  <el-icon><component :is="getTrendIcon(metrics.scoreTrend)" /></el-icon>
                  {{ Math.abs(metrics.scoreTrend) }}%
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 图表区域 -->
    <el-row :gutter="16" class="charts-row">
      <!-- 告警趋势图 -->
      <el-col :span="12">
        <el-card title="告警趋势分析">
          <template #extra>
            <el-button type="text" @click="viewAlertDetails">查看详情</el-button>
          </template>
          <EchartsChart
            :option="alertTrendOption"
            height="350px"
            :loading="chartLoading"
          />
        </el-card>
      </el-col>

      <!-- 威胁类型分布 -->
      <el-col :span="12">
        <el-card title="威胁类型分布">
          <template #extra>
            <el-button type="text" @click="viewThreatDetails">查看详情</el-button>
          </template>
          <EchartsChart
            :option="threatDistributionOption"
            height="350px"
            :loading="chartLoading"
          />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="charts-row">
      <!-- 资产状态分布 -->
      <el-col :span="8">
        <el-card title="资产状态分布">
          <EchartsChart
            :option="assetStatusOption"
            height="300px"
            :loading="chartLoading"
          />
        </el-card>
      </el-col>

      <!-- 地理位置威胁 -->
      <el-col :span="16">
        <el-card title="地理位置威胁分布">
          <EchartsChart
            :option="geoThreatOption"
            height="300px"
            :loading="chartLoading"
          />
        </el-card>
      </el-col>
    </el-row>

    <!-- 实时信息面板 -->
    <el-row :gutter="16" class="info-panels">
      <!-- 最新告警 -->
      <el-col :span="8">
        <el-card title="最新告警">
          <template #extra>
            <el-button type="text" @click="viewAllAlerts">查看全部</el-button>
          </template>
          <div class="alert-list">
            <div
              v-for="alert in recentAlerts"
              :key="alert.id"
              class="alert-item"
              @click="viewAlert(alert)"
            >
              <div class="alert-severity">
                <StatusTag
                  :value="alert.severity"
                  type="alert-severity"
                  size="small"
                />
              </div>
              <div class="alert-content">
                <div class="alert-title">{{ alert.alert_name }}</div>
                <div class="alert-meta">
                  <span class="alert-asset">{{ alert.asset_name }}</span>
                  <span class="alert-time">{{ getRelativeTime(alert.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 系统状态 -->
      <el-col :span="8">
        <el-card title="系统状态">
          <div class="system-status">
            <div
              v-for="component in systemComponents"
              :key="component.name"
              class="status-item"
            >
              <div class="status-name">{{ component.name }}</div>
              <div class="status-indicator">
                <StatusTag
                  :value="component.status"
                  type="system-status"
                  size="small"
                />
              </div>
              <div class="status-metrics">
                <span v-if="component.responseTime">{{ component.responseTime }}ms</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 威胁情报 -->
      <el-col :span="8">
        <el-card title="威胁情报">
          <template #extra>
            <el-button type="text" @click="viewIntelligence">查看全部</el-button>
          </template>
          <div class="intelligence-summary">
            <div class="intel-item">
              <div class="intel-label">IOC总数</div>
              <div class="intel-value">{{ intelligence.totalIOCs }}</div>
            </div>
            <div class="intel-item">
              <div class="intel-label">今日新增</div>
              <div class="intel-value">{{ intelligence.todayNew }}</div>
            </div>
            <div class="intel-item">
              <div class="intel-label">匹配告警</div>
              <div class="intel-value">{{ intelligence.matches }}</div>
            </div>
            <div class="intel-feeds">
              <div class="feeds-title">情报源状态</div>
              <div
                v-for="feed in intelligence.feeds"
                :key="feed.name"
                class="feed-item"
              >
                <span class="feed-name">{{ feed.name }}</span>
                <StatusTag
                  :value="feed.status"
                  type="system-status"
                  size="small"
                />
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Refresh,
  Warning,
  Lock,
  Monitor,
  TrendCharts,
  ArrowUp,
  ArrowDown,
  Minus
} from '@element-plus/icons-vue'
import EchartsChart from '@/components/common/EchartsChart.vue'
import StatusTag from '@/components/common/StatusTag.vue'
import { dashboardApi } from '@/api'
import { getRelativeTime } from '@/utils'
import worldMap from '@/map/world.json' // 假设已下载到本地

// 路由
const router = useRouter()

// 响应式数据
const chartLoading = ref(false)
const selectedPeriod = ref('24h')
const refreshTimer = ref<NodeJS.Timeout>()

// 时间周期选项
const timePeriods = [
  { label: '24小时', value: '24h' },
  { label: '7天', value: '7d' },
  { label: '30天', value: '30d' }
]

// 核心指标
const metrics = reactive({
  criticalAlerts: 0,
  criticalTrend: 0,
  activeThreats: 0,
  threatsTrend: 0,
  totalAssets: 0,
  assetsTrend: 0,
  securityScore: 0,
  scoreTrend: 0
})

// 最新告警
const recentAlerts = ref([])

// 系统组件状态
const systemComponents = ref([])

// 威胁情报摘要
const intelligence = reactive({
  totalIOCs: 0,
  todayNew: 0,
  matches: 0,
  feeds: []
})

// 图表配置
const alertTrendOption = ref({})
const threatDistributionOption = ref({})
const assetStatusOption = ref({})
const geoThreatOption = ref({})

// 获取趋势图标
const getTrendIcon = (trend: number) => {
  if (trend > 0) return ArrowUp
  if (trend < 0) return ArrowDown
  return Minus
}

// 获取趋势样式类
const getTrendClass = (trend: number) => {
  if (trend > 0) return 'trend-up'
  if (trend < 0) return 'trend-down'
  return 'trend-stable'
}

// 加载安全概览数据
const loadSecurityOverview = async () => {
  try {
    const response = await dashboardApi.getSecurityOverview()
    
    // 更新核心指标
    metrics.criticalAlerts = response.alert_summary.critical
    metrics.activeThreats = response.threat_summary.active_threats
    metrics.totalAssets = response.asset_summary.total
    metrics.securityScore = 85 // 示例数据
    
    // 设置趋势数据（示例）
    metrics.criticalTrend = -12
    metrics.threatsTrend = 8
    metrics.assetsTrend = 3
    metrics.scoreTrend = 5
  } catch (error) {
    console.error('加载安全概览失败:', error)
  }
}

// 加载图表数据
const loadChartData = async () => {
  try {
    chartLoading.value = true
    
    // 告警趋势
    const alertTrends = await dashboardApi.getAlertTrends(
      selectedPeriod.value === '24h' ? 1 : 
      selectedPeriod.value === '7d' ? 7 : 30
    )
    
    alertTrendOption.value = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      legend: {
        data: ['严重', '高危', '中危', '低危']
      },
      xAxis: {
        type: 'category',
        data: alertTrends.dates
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '严重',
          type: 'line',
          data: alertTrends.critical,
          itemStyle: { color: '#f56c6c' }
        },
        {
          name: '高危',
          type: 'line',
          data: alertTrends.high,
          itemStyle: { color: '#e6a23c' }
        },
        {
          name: '中危',
          type: 'line',
          data: alertTrends.medium,
          itemStyle: { color: '#409eff' }
        },
        {
          name: '低危',
          type: 'line',
          data: alertTrends.low,
          itemStyle: { color: '#67c23a' }
        }
      ]
    }
    
    // 威胁分布
    const threatDist = await dashboardApi.getThreatDistribution()
    threatDistributionOption.value = {
      tooltip: {
        trigger: 'item'
      },
      series: [
        {
          name: '威胁类型',
          type: 'pie',
          radius: '50%',
          data: threatDist.map((item: any) => ({
            value: item.count,
            name: item.type
          })),
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
    
    // 资产状态
    const assetStatus = await dashboardApi.getAssetStatusDistribution()
    assetStatusOption.value = {
      tooltip: {
        trigger: 'item'
      },
      series: [
        {
          name: '资产状态',
          type: 'pie',
          radius: ['40%', '70%'],
          data: assetStatus.map((item: any) => ({
            value: item.count,
            name: item.status
          }))
        }
      ]
    }
    
    // 地理威胁分布
    const geoThreats = await dashboardApi.getGeoThreatDistribution()
    
    EchartsChart.registerMap('world', worldMap) // 注册地图，'world' 需与配置中的 map 名称一致
    geoThreatOption.value = {
      tooltip: {
        trigger: 'item'
      },
      geo: {
        map: 'world',
        roam: true,
        itemStyle: {
          areaColor: '#e7e8ea'
        },
        emphasis: {
          itemStyle: {
            areaColor: '#389bb7'
          }
        }
      },
      series: [
        {
          name: '威胁分布',
          type: 'scatter',
          coordinateSystem: 'geo',
          data: geoThreats.map((item: any) => ({
            name: item.country,
            value: [item.longitude, item.latitude, item.threat_count]
          })),
          symbolSize: (val: number[]) => Math.max(val[2] / 10, 4),
          itemStyle: {
            color: '#f56c6c'
          }
        }
      ]
    }
  } catch (error) {
    console.error('加载图表数据失败:', error)
  } finally {
    chartLoading.value = false
  }
}

// 加载实时数据
const loadRealtimeData = async () => {
  try {
    // 最新告警
    recentAlerts.value = await dashboardApi.getRealtimeAlerts(5)
    
    // 系统状态
    const systemHealth = await dashboardApi.getSystemHealth()
    systemComponents.value = systemHealth.components
    
    // 威胁情报
    const intelSummary = await dashboardApi.getIntelligenceSummary()
    Object.assign(intelligence, intelSummary)
  } catch (error) {
    console.error('加载实时数据失败:', error)
  }
}

// 刷新所有数据
const refreshData = async () => {
  await Promise.all([
    loadSecurityOverview(),
    loadChartData(),
    loadRealtimeData()
  ])
}

// 处理时间周期变化
const handlePeriodChange = (period: string) => {
  selectedPeriod.value = period
  loadChartData()
}

// 导航方法
const viewAlertDetails = () => {
  router.push('/alerts')
}

const viewThreatDetails = () => {
  router.push('/threats')
}

const viewAllAlerts = () => {
  router.push('/alerts')
}

const viewAlert = (alert: any) => {
  router.push(`/alerts/${alert.id}`)
}

const viewIntelligence = () => {
  router.push('/intelligence')
}

// 生命周期
onMounted(() => {
  refreshData()
  
  // 设置自动刷新
  refreshTimer.value = setInterval(() => {
    loadRealtimeData()
  }, 30000) // 30秒刷新一次实时数据
})

onUnmounted(() => {
  if (refreshTimer.value) {
    clearInterval(refreshTimer.value)
  }
})
</script>

<style scoped lang="scss">
.security-overview {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;

    .header-left {
      .page-title {
        margin: 0 0 8px 0;
        font-size: 24px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }

      .page-description {
        margin: 0;
        color: var(--el-text-color-regular);
      }
    }

    .header-right {
      display: flex;
      gap: 12px;
      align-items: center;
    }
  }

  .metrics-cards {
    margin-bottom: 20px;

    .metric-card {
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .metric-content {
        display: flex;
        align-items: center;
        gap: 16px;

        .metric-icon {
          width: 56px;
          height: 56px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 28px;
        }

        .metric-info {
          flex: 1;

          .metric-value {
            font-size: 32px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 4px;
          }

          .metric-label {
            font-size: 14px;
            color: var(--el-text-color-regular);
            margin-bottom: 8px;
          }

          .metric-trend {
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 12px;
            font-weight: 500;

            &.trend-up {
              color: #f56c6c;
            }

            &.trend-down {
              color: #67c23a;
            }

            &.trend-stable {
              color: var(--el-text-color-regular);
            }
          }
        }
      }

      &.critical {
        .metric-icon {
          background: rgba(245, 108, 108, 0.1);
          color: #f56c6c;
        }
        .metric-value {
          color: #f56c6c;
        }
      }

      &.threats {
        .metric-icon {
          background: rgba(230, 162, 60, 0.1);
          color: #e6a23c;
        }
        .metric-value {
          color: #e6a23c;
        }
      }

      &.assets {
        .metric-icon {
          background: rgba(64, 158, 255, 0.1);
          color: #409eff;
        }
        .metric-value {
          color: #409eff;
        }
      }

      &.score {
        .metric-icon {
          background: rgba(103, 194, 58, 0.1);
          color: #67c23a;
        }
        .metric-value {
          color: #67c23a;
        }
      }
    }
  }

  .charts-row {
    margin-bottom: 20px;
  }

  .info-panels {
    .alert-list {
      .alert-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 0;
        border-bottom: 1px solid var(--el-border-color-lighter);
        cursor: pointer;
        transition: background-color 0.2s;

        &:hover {
          background-color: var(--el-fill-color-lighter);
        }

        &:last-child {
          border-bottom: none;
        }

        .alert-content {
          flex: 1;
          min-width: 0;

          .alert-title {
            font-weight: 500;
            margin-bottom: 4px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }

          .alert-meta {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: var(--el-text-color-secondary);

            .alert-asset {
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
            }
          }
        }
      }
    }

    .system-status {
      .status-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid var(--el-border-color-lighter);

        &:last-child {
          border-bottom: none;
        }

        .status-name {
          font-weight: 500;
        }

        .status-metrics {
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
    }

    .intelligence-summary {
      .intel-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;

        .intel-label {
          color: var(--el-text-color-regular);
        }

        .intel-value {
          font-weight: 600;
          font-size: 18px;
        }
      }

      .intel-feeds {
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid var(--el-border-color-lighter);

        .feeds-title {
          font-weight: 500;
          margin-bottom: 12px;
        }

        .feed-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 4px 0;

          .feed-name {
            font-size: 12px;
          }
        }
      }
    }
  }
}
</style>
