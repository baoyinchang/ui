<template>
  <div class="asset-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h2 class="page-title">资产管理</h2>
        <p class="page-description">管理和监控网络资产的安全状态</p>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="handleCreateAsset">
          添加资产
        </el-button>
        <el-button :icon="Upload" @click="showImportDialog = true">
          批量导入
        </el-button>
        <el-button :icon="Refresh" @click="handleScanAssets">
          资产扫描
        </el-button>
      </div>
    </div>

    <!-- 资产概览 -->
    <div class="asset-overview">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon server">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-value">{{ overview.total }}</div>
                <div class="card-label">总资产数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon online">
                <el-icon><CircleCheck /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-value">{{ overview.online }}</div>
                <div class="card-label">在线资产</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon warning">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-value">{{ overview.warning }}</div>
                <div class="card-label">告警资产</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon offline">
                <el-icon><CircleClose /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-value">{{ overview.offline }}</div>
                <div class="card-label">离线资产</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 资产分布图表 -->
    <el-row :gutter="16" class="charts-row">
      <el-col :span="12">
        <el-card title="资产类型分布">
          <EchartsChart
            :option="assetTypeChartOption"
            height="300px"
            :loading="chartLoading"
          />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card title="资产状态分布">
          <EchartsChart
            :option="assetStatusChartOption"
            height="300px"
            :loading="chartLoading"
          />
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索表单 -->
    <el-card class="search-card">
      <SearchForm
        ref="searchFormRef"
        :fields="searchFields"
        v-model="searchParams"
        @search="handleSearch"
        @reset="handleReset"
      />
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <DataTable
        ref="tableRef"
        :data="tableData"
        :columns="tableColumns"
        :loading="loading"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        :show-selection="true"
        :show-index="true"
        @refresh="loadData"
        @search="handleTableSearch"
        @selection-change="handleSelectionChange"
        @edit="handleEdit"
        @delete="handleDelete"
        @batch-delete="handleBatchDelete"
        @export="handleExport"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      >
        <!-- 自定义列插槽 -->
        <template #asset_type="{ row }">
          <StatusTag
            :value="row.asset_type"
            type="custom"
            :custom-mapping="assetTypeMapping"
          />
        </template>

        <template #status="{ row }">
          <StatusTag
            :value="row.status"
            type="asset-status"
            :show-dot="true"
          />
        </template>

        <template #ip_address="{ row }">
          <el-tag type="info" size="small">{{ row.ip_address }}</el-tag>
        </template>

        <template #last_seen="{ row }">
          <el-tooltip :content="formatTime(row.last_seen)" placement="top">
            <span>{{ getRelativeTime(row.last_seen) }}</span>
          </el-tooltip>
        </template>

        <template #risk_score="{ row }">
          <el-progress
            :percentage="row.risk_score"
            :color="getRiskColor(row.risk_score)"
            :show-text="false"
            :stroke-width="8"
          />
          <span class="risk-text">{{ row.risk_score }}%</span>
        </template>

        <template #actions="{ row }">
          <el-button
            type="primary"
            size="small"
            :icon="View"
            @click="handleView(row)"
          >
            查看
          </el-button>
          <el-button
            type="success"
            size="small"
            :icon="Monitor"
            @click="handleMonitor(row)"
          >
            监控
          </el-button>
          <el-dropdown @command="(command) => handleMoreAction(command, row)">
            <el-button size="small" :icon="More" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="edit" :icon="Edit">编辑</el-dropdown-item>
                <el-dropdown-item command="scan" :icon="Search">扫描</el-dropdown-item>
                <el-dropdown-item command="history" :icon="Clock">历史记录</el-dropdown-item>
                <el-dropdown-item command="delete" :icon="Delete" divided>删除</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </DataTable>
    </el-card>

    <!-- 资产详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="资产详情"
      width="80%"
      :close-on-click-modal="false"
    >
      <AssetDetail
        v-if="currentAsset"
        :asset="currentAsset"
        @update="handleAssetUpdate"
        @close="showDetailDialog = false"
      />
    </el-dialog>

    <!-- 批量导入对话框 -->
    <el-dialog
      v-model="showImportDialog"
      title="批量导入资产"
      width="600px"
      :close-on-click-modal="false"
    >
      <AssetImport
        @success="handleImportSuccess"
        @cancel="showImportDialog = false"
      />
    </el-dialog>

    <!-- 资产扫描对话框 -->
    <el-dialog
      v-model="showScanDialog"
      title="资产扫描"
      width="800px"
      :close-on-click-modal="false"
    >
      <AssetScan
        @success="handleScanSuccess"
        @cancel="showScanDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Upload,
  Refresh,
  Monitor,
  CircleCheck,
  Warning,
  CircleClose,
  View,
  More,
  Edit,
  Search,
  Clock,
  Delete
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import DataTable from '@/components/common/DataTable.vue'
import SearchForm from '@/components/common/SearchForm.vue'
import StatusTag from '@/components/common/StatusTag.vue'
import EchartsChart from '@/components/common/EchartsChart.vue'
import AssetDetail from './components/AssetDetail.vue'
import AssetImport from './components/AssetImport.vue'
import AssetScan from './components/AssetScan.vue'
import { assetsApi } from '@/api'
import { formatTime, getRelativeTime, ASSET_TYPE_LABELS } from '@/utils'
import type { Asset } from '@/types/api'
import type { TableColumn } from '@/types/global'

// 路由
const router = useRouter()

// 响应式数据
const searchFormRef = ref()
const tableRef = ref()
const loading = ref(false)
const chartLoading = ref(false)
const tableData = ref<Asset[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const selectedRows = ref<Asset[]>([])
const currentAsset = ref<Asset>()
const showDetailDialog = ref(false)
const showImportDialog = ref(false)
const showScanDialog = ref(false)

// 搜索参数
const searchParams = reactive({
  search: '',
  asset_type: '',
  status: '',
  ip_range: '',
  location: '',
  tags: []
})

// 概览数据
const overview = reactive({
  total: 0,
  online: 0,
  warning: 0,
  offline: 0
})

// 资产类型映射
const assetTypeMapping = computed(() => {
  const mapping: Record<string, { text: string; color?: string }> = {}
  Object.entries(ASSET_TYPE_LABELS).forEach(([key, value]) => {
    mapping[key] = { text: value }
  })
  return mapping
})

// 搜索字段配置
const searchFields = computed(() => [
  {
    prop: 'search',
    label: '关键词',
    type: 'input',
    placeholder: '搜索资产名称、IP地址...'
  },
  {
    prop: 'asset_type',
    label: '资产类型',
    type: 'select',
    placeholder: '选择资产类型',
    options: Object.entries(ASSET_TYPE_LABELS).map(([key, value]) => ({
      label: value,
      value: key
    }))
  },
  {
    prop: 'status',
    label: '状态',
    type: 'select',
    placeholder: '选择状态',
    options: [
      { label: '正常', value: 'normal' },
      { label: '警告', value: 'warning' },
      { label: '危险', value: 'danger' },
      { label: '离线', value: 'offline' }
    ]
  },
  {
    prop: 'ip_range',
    label: 'IP范围',
    type: 'input',
    placeholder: '如：192.168.1.0/24'
  }
])

// 表格列配置
const tableColumns: TableColumn[] = [
  {
    prop: 'name',
    label: '资产名称',
    minWidth: 150,
    showOverflowTooltip: true
  },
  {
    prop: 'asset_type',
    label: '类型',
    width: 120,
    slot: 'asset_type'
  },
  {
    prop: 'ip_address',
    label: 'IP地址',
    width: 130,
    slot: 'ip_address'
  },
  {
    prop: 'status',
    label: '状态',
    width: 100,
    slot: 'status'
  },
  {
    prop: 'os',
    label: '操作系统',
    width: 120,
    showOverflowTooltip: true
  },
  {
    prop: 'location',
    label: '位置',
    width: 100
  },
  {
    prop: 'risk_score',
    label: '风险评分',
    width: 120,
    slot: 'risk_score'
  },
  {
    prop: 'last_seen',
    label: '最后在线',
    width: 120,
    slot: 'last_seen'
  }
]

// 图表配置
const assetTypeChartOption = ref({})
const assetStatusChartOption = ref({})

// 获取风险颜色
const getRiskColor = (score: number) => {
  if (score >= 80) return '#f56c6c'
  if (score >= 60) return '#e6a23c'
  if (score >= 40) return '#409eff'
  return '#67c23a'
}

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    const params = {
      ...searchParams,
      page: currentPage.value,
      size: pageSize.value
    }
    
    const response = await assetsApi.getAssets(params)
    tableData.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载资产数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 加载概览数据
const loadOverview = async () => {
  try {
    const response = await assetsApi.getAssetStatistics()
    Object.assign(overview, response)
  } catch (error) {
    console.error('加载概览数据失败:', error)
  }
}

// 加载图表数据
const loadChartData = async () => {
  try {
    chartLoading.value = true
    
    // 资产类型分布
    const typeResponse = await assetsApi.getAssetTypeDistribution()
    assetTypeChartOption.value = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '资产类型',
          type: 'pie',
          radius: '50%',
          data: typeResponse.map((item: any) => ({
            value: item.count,
            name: ASSET_TYPE_LABELS[item.type as keyof typeof ASSET_TYPE_LABELS] || item.type
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
    
    // 资产状态分布
    const statusResponse = await assetsApi.getAssetStatusDistribution()
    assetStatusChartOption.value = {
      tooltip: {
        trigger: 'item'
      },
      series: [
        {
          name: '资产状态',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 20,
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: statusResponse.map((item: any) => ({
            value: item.count,
            name: item.status,
            itemStyle: {
              color: getRiskColor(item.status === 'normal' ? 20 : 
                     item.status === 'warning' ? 60 : 
                     item.status === 'danger' ? 90 : 50)
            }
          }))
        }
      ]
    }
  } catch (error) {
    console.error('加载图表数据失败:', error)
  } finally {
    chartLoading.value = false
  }
}

// 事件处理
const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const handleReset = () => {
  Object.assign(searchParams, {
    search: '',
    asset_type: '',
    status: '',
    ip_range: '',
    location: '',
    tags: []
  })
  currentPage.value = 1
  loadData()
}

const handleTableSearch = (keyword: string) => {
  searchParams.search = keyword
  handleSearch()
}

const handleSelectionChange = (selection: Asset[]) => {
  selectedRows.value = selection
}

const handleView = (asset: Asset) => {
  currentAsset.value = asset
  showDetailDialog.value = true
}

const handleEdit = (asset: Asset) => {
  router.push(`/assets/edit/${asset.id}`)
}

const handleDelete = async (asset: Asset) => {
  try {
    await assetsApi.deleteAsset(asset.id)
    ElMessage.success('删除成功')
    loadData()
    loadOverview()
  } catch (error) {
    console.error('删除资产失败:', error)
    ElMessage.error('删除失败')
  }
}

const handleBatchDelete = async (assets: Asset[]) => {
  try {
    const ids = assets.map(asset => asset.id)
    await assetsApi.batchDeleteAssets(ids)
    ElMessage.success('批量删除成功')
    loadData()
    loadOverview()
  } catch (error) {
    console.error('批量删除失败:', error)
    ElMessage.error('批量删除失败')
  }
}

const handleMonitor = (asset: Asset) => {
  router.push(`/assets/${asset.id}/monitor`)
}

const handleMoreAction = (command: string, asset: Asset) => {
  switch (command) {
    case 'edit':
      handleEdit(asset)
      break
    case 'scan':
      // 处理扫描逻辑
      break
    case 'history':
      router.push(`/assets/${asset.id}/history`)
      break
    case 'delete':
      handleDelete(asset)
      break
  }
}

const handleCreateAsset = () => {
  router.push('/assets/create')
}

const handleScanAssets = () => {
  showScanDialog.value = true
}

const handleAssetUpdate = () => {
  loadData()
  loadOverview()
}

const handleImportSuccess = () => {
  showImportDialog.value = false
  loadData()
  loadOverview()
  ElMessage.success('导入成功')
}

const handleScanSuccess = () => {
  showScanDialog.value = false
  loadData()
  loadOverview()
  ElMessage.success('扫描完成')
}

const handleExport = async () => {
  try {
    const response = await assetsApi.exportAssets(searchParams)
    // 处理导出逻辑
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadData()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadData()
}

// 组件挂载
onMounted(() => {
  loadData()
  loadOverview()
  loadChartData()
})
</script>

<style scoped lang="scss">
.asset-list {
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
    }
  }

  .asset-overview {
    margin-bottom: 20px;

    .overview-card {
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .card-content {
        display: flex;
        align-items: center;
        gap: 16px;

        .card-icon {
          width: 48px;
          height: 48px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;

          &.server {
            background: rgba(64, 158, 255, 0.1);
            color: #409eff;
          }

          &.online {
            background: rgba(103, 194, 58, 0.1);
            color: #67c23a;
          }

          &.warning {
            background: rgba(230, 162, 60, 0.1);
            color: #e6a23c;
          }

          &.offline {
            background: rgba(144, 147, 153, 0.1);
            color: #909399;
          }
        }

        .card-info {
          flex: 1;

          .card-value {
            font-size: 28px;
            font-weight: 600;
            line-height: 1;
            margin-bottom: 4px;
          }

          .card-label {
            font-size: 14px;
            color: var(--el-text-color-regular);
          }
        }
      }
    }
  }

  .charts-row {
    margin-bottom: 20px;
  }

  .search-card,
  .table-card {
    margin-bottom: 20px;
  }

  .risk-text {
    margin-left: 8px;
    font-size: 12px;
    color: var(--el-text-color-regular);
  }
}
</style>
