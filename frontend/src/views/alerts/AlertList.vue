<template>
  <div class="alert-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h2 class="page-title">告警管理</h2>
        <p class="page-description">实时监控和管理安全告警事件</p>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="handleCreateAlert">
          创建告警
        </el-button>
        <el-button :icon="Setting" @click="showSettingsDialog = true">
          设置
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-card class="stats-card critical">
            <div class="stats-content">
              <div class="stats-icon">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-value">{{ statistics.critical }}</div>
                <div class="stats-label">严重告警</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card high">
            <div class="stats-content">
              <div class="stats-icon">
                <el-icon><InfoFilled /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-value">{{ statistics.high }}</div>
                <div class="stats-label">高危告警</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card unhandled">
            <div class="stats-content">
              <div class="stats-icon">
                <el-icon><Clock /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-value">{{ statistics.unhandled }}</div>
                <div class="stats-label">未处理</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card total">
            <div class="stats-content">
              <div class="stats-icon">
                <el-icon><DataBoard /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-value">{{ statistics.total }}</div>
                <div class="stats-label">总告警数</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

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
        <template #severity="{ row }">
          <StatusTag
            :value="row.severity"
            type="alert-severity"
            :show-dot="true"
          />
        </template>

        <template #status="{ row }">
          <StatusTag
            :value="row.status"
            type="alert-status"
          />
        </template>

        <template #asset_name="{ row }">
          <el-link type="primary" @click="handleViewAsset(row.asset_id)">
            {{ row.asset_name }}
          </el-link>
        </template>

        <template #created_at="{ row }">
          <el-tooltip :content="formatTime(row.created_at, 'YYYY-MM-DD HH:mm:ss')" placement="top">
            <span>{{ getRelativeTime(row.created_at) }}</span>
          </el-tooltip>
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
            v-if="row.status === 'unhandled'"
            type="success"
            size="small"
            :icon="Check"
            @click="handleProcess(row)"
          >
            处理
          </el-button>
          <el-dropdown @command="(command) => handleMoreAction(command, row)">
            <el-button size="small" :icon="More" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="edit" :icon="Edit">编辑</el-dropdown-item>
                <el-dropdown-item command="assign" :icon="User">分配</el-dropdown-item>
                <el-dropdown-item command="close" :icon="CircleClose">关闭</el-dropdown-item>
                <el-dropdown-item command="delete" :icon="Delete" divided>删除</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </DataTable>
    </el-card>

    <!-- 告警详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="告警详情"
      width="80%"
      :close-on-click-modal="false"
    >
      <AlertDetail
        v-if="currentAlert"
        :alert="currentAlert"
        @update="handleAlertUpdate"
        @close="showDetailDialog = false"
      />
    </el-dialog>

    <!-- 告警处理对话框 -->
    <el-dialog
      v-model="showProcessDialog"
      title="处理告警"
      width="600px"
      :close-on-click-modal="false"
    >
      <AlertProcess
        v-if="currentAlert"
        :alert="currentAlert"
        @success="handleProcessSuccess"
        @cancel="showProcessDialog = false"
      />
    </el-dialog>

    <!-- 设置对话框 -->
    <el-dialog
      v-model="showSettingsDialog"
      title="告警设置"
      width="800px"
      :close-on-click-modal="false"
    >
      <AlertSettings
        @save="handleSettingsSave"
        @cancel="showSettingsDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Setting,
  Warning,
  InfoFilled,
  Clock,
  DataBoard,
  View,
  Check,
  More,
  Edit,
  User,
  CircleClose,
  Delete
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import DataTable from '@/components/common/DataTable.vue'
import SearchForm from '@/components/common/SearchForm.vue'
import StatusTag from '@/components/common/StatusTag.vue'
import AlertDetail from './components/AlertDetail.vue'
import AlertProcess from './components/AlertProcess.vue'
import AlertSettings from './components/AlertSettings.vue'
import { alertsApi } from '@/api'
import { formatTime, getRelativeTime } from '@/utils'
import type { Alert } from '@/types/api'
import type { TableColumn } from '@/types/global'

// 路由
const router = useRouter()

// 响应式数据
const searchFormRef = ref()
const tableRef = ref()
const loading = ref(false)
const tableData = ref<Alert[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const selectedRows = ref<Alert[]>([])
const currentAlert = ref<Alert>()
const showDetailDialog = ref(false)
const showProcessDialog = ref(false)
const showSettingsDialog = ref(false)

// 搜索参数
const searchParams = reactive({
  search: '',
  severity: '',
  status: '',
  asset_id: '',
  start_date: '',
  end_date: '',
  assigned_to: ''
})

// 统计数据
const statistics = reactive({
  total: 0,
  critical: 0,
  high: 0,
  unhandled: 0
})

// 搜索字段配置
const searchFields = computed(() => [
  {
    prop: 'search',
    label: '关键词',
    type: 'input',
    placeholder: '搜索告警名称、描述...'
  },
  {
    prop: 'severity',
    label: '严重级别',
    type: 'select',
    placeholder: '选择严重级别',
    options: [
      { label: '严重', value: 'critical' },
      { label: '高', value: 'high' },
      { label: '中', value: 'medium' },
      { label: '低', value: 'low' },
      { label: '信息', value: 'info' }
    ]
  },
  {
    prop: 'status',
    label: '状态',
    type: 'select',
    placeholder: '选择状态',
    options: [
      { label: '未处理', value: 'unhandled' },
      { label: '处理中', value: 'handling' },
      { label: '已解决', value: 'resolved' },
      { label: '已关闭', value: 'closed' }
    ]
  },
  {
    prop: 'date_range',
    label: '时间范围',
    type: 'date',
    dateType: 'datetimerange',
    placeholder: '选择时间范围',
    startPlaceholder: '开始时间',
    endPlaceholder: '结束时间'
  }
])

// 表格列配置
const tableColumns: TableColumn[] = [
  {
    prop: 'alert_name',
    label: '告警名称',
    minWidth: 200,
    showOverflowTooltip: true
  },
  {
    prop: 'severity',
    label: '严重级别',
    width: 100,
    slot: 'severity'
  },
  {
    prop: 'status',
    label: '状态',
    width: 100,
    slot: 'status'
  },
  {
    prop: 'asset_name',
    label: '资产名称',
    width: 150,
    slot: 'asset_name'
  },
  {
    prop: 'source_ip',
    label: '源IP',
    width: 120
  },
  {
    prop: 'assigned_to_name',
    label: '处理人',
    width: 100
  },
  {
    prop: 'created_at',
    label: '创建时间',
    width: 120,
    slot: 'created_at'
  }
]

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    const params = {
      ...searchParams,
      page: currentPage.value,
      size: pageSize.value
    }
    
    const response = await alertsApi.getAlerts(params)
    tableData.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载告警数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 加载统计数据
const loadStatistics = async () => {
  try {
    const response = await alertsApi.getAlertStatistics()
    Object.assign(statistics, response)
  } catch (error) {
    console.error('加载统计数据失败:', error)
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
    severity: '',
    status: '',
    asset_id: '',
    start_date: '',
    end_date: '',
    assigned_to: ''
  })
  currentPage.value = 1
  loadData()
}

const handleTableSearch = (keyword: string) => {
  searchParams.search = keyword
  handleSearch()
}

const handleSelectionChange = (selection: Alert[]) => {
  selectedRows.value = selection
}

const handleView = (alert: Alert) => {
  currentAlert.value = alert
  showDetailDialog.value = true
}

const handleEdit = (alert: Alert) => {
  router.push(`/alerts/edit/${alert.id}`)
}

const handleDelete = async (alert: Alert) => {
  try {
    await alertsApi.deleteAlert(alert.id)
    ElMessage.success('删除成功')
    loadData()
    loadStatistics()
  } catch (error) {
    console.error('删除告警失败:', error)
    ElMessage.error('删除失败')
  }
}

const handleBatchDelete = async (alerts: Alert[]) => {
  try {
    const ids = alerts.map(alert => alert.id)
    await alertsApi.batchDeleteAlerts(ids)
    ElMessage.success('批量删除成功')
    loadData()
    loadStatistics()
  } catch (error) {
    console.error('批量删除失败:', error)
    ElMessage.error('批量删除失败')
  }
}

const handleProcess = (alert: Alert) => {
  currentAlert.value = alert
  showProcessDialog.value = true
}

const handleProcessSuccess = () => {
  showProcessDialog.value = false
  loadData()
  loadStatistics()
  ElMessage.success('处理成功')
}

const handleMoreAction = (command: string, alert: Alert) => {
  switch (command) {
    case 'edit':
      handleEdit(alert)
      break
    case 'assign':
      // 处理分配逻辑
      break
    case 'close':
      // 处理关闭逻辑
      break
    case 'delete':
      handleDelete(alert)
      break
  }
}

const handleCreateAlert = () => {
  router.push('/alerts/create')
}

const handleViewAsset = (assetId: number) => {
  router.push(`/assets/${assetId}`)
}

const handleAlertUpdate = () => {
  loadData()
  loadStatistics()
}

const handleExport = async () => {
  try {
    const response = await alertsApi.exportAlerts(searchParams)
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

const handleSettingsSave = () => {
  showSettingsDialog.value = false
  ElMessage.success('设置保存成功')
}

// 组件挂载
onMounted(() => {
  loadData()
  loadStatistics()
})
</script>

<style scoped lang="scss">
.alert-list {
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

  .stats-cards {
    margin-bottom: 20px;

    .stats-card {
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .stats-content {
        display: flex;
        align-items: center;
        gap: 16px;

        .stats-icon {
          width: 48px;
          height: 48px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;
        }

        .stats-info {
          flex: 1;

          .stats-value {
            font-size: 28px;
            font-weight: 600;
            line-height: 1;
            margin-bottom: 4px;
          }

          .stats-label {
            font-size: 14px;
            color: var(--el-text-color-regular);
          }
        }
      }

      &.critical {
        .stats-icon {
          background: rgba(245, 108, 108, 0.1);
          color: #f56c6c;
        }
        .stats-value {
          color: #f56c6c;
        }
      }

      &.high {
        .stats-icon {
          background: rgba(230, 162, 60, 0.1);
          color: #e6a23c;
        }
        .stats-value {
          color: #e6a23c;
        }
      }

      &.unhandled {
        .stats-icon {
          background: rgba(64, 158, 255, 0.1);
          color: #409eff;
        }
        .stats-value {
          color: #409eff;
        }
      }

      &.total {
        .stats-icon {
          background: rgba(103, 194, 58, 0.1);
          color: #67c23a;
        }
        .stats-value {
          color: #67c23a;
        }
      }
    }
  }

  .search-card,
  .table-card {
    margin-bottom: 20px;
  }
}
</style>
