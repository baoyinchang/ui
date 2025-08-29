<template>
  <div class="alerts-container">
    <div class="page-header">
      <h1 class="page-title">告警中心</h1>
      <p class="page-description">集中管理和处理系统安全告警，快速响应威胁事件</p>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in alertStats" :key="stat.key">
        <div class="stat-icon" :class="stat.iconClass">
          <el-icon><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-title">{{ stat.title }}</div>
          <div class="stat-value">{{ stat.value }}</div>
        </div>
      </div>
    </div>
    
    <!-- 搜索和过滤 -->
    <el-card class="filter-card" shadow="never">
      <el-form :model="searchForm" inline>
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="搜索告警名称或资产"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="严重程度">
          <el-select
            v-model="searchForm.severity"
            placeholder="全部"
            clearable
            style="width: 120px"
          >
            <el-option label="紧急" value="critical" />
            <el-option label="高危" value="high" />
            <el-option label="中危" value="medium" />
            <el-option label="低危" value="low" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select
            v-model="searchForm.status"
            placeholder="全部"
            clearable
            style="width: 120px"
          >
            <el-option label="未处理" value="unhandled" />
            <el-option label="处理中" value="handling" />
            <el-option label="已解决" value="resolved" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 告警列表 -->
    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="table-header">
          <span>告警列表</span>
          <div class="table-actions">
            <el-button
              type="primary"
              :disabled="selectedAlerts.length === 0"
              @click="showBatchUpdateDialog"
            >
              批量处理 ({{ selectedAlerts.length }})
            </el-button>
            <el-button @click="refreshData">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="alertList"
        @selection-change="handleSelectionChange"
        stripe
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="alert_name" label="告警名称" min-width="200">
          <template #default="{ row }">
            <el-link
              type="primary"
              @click="goToDetail(row.id)"
              class="alert-name-link"
            >
              {{ row.alert_name }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="severity" label="严重程度" width="100">
          <template #default="{ row }">
            <el-tag :type="getSeverityType(row.severity)" size="small">
              {{ getSeverityText(row.severity) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="asset_name" label="受影响资产" width="150" />
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="handler_name" label="处理人" width="120" />
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="goToDetail(row.id)"
            >
              查看详情
            </el-button>
            <el-dropdown @command="(command) => handleAction(command, row)">
              <el-button size="small">
                更多
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item
                    command="handle"
                    :disabled="row.status !== 'unhandled'"
                  >
                    开始处理
                  </el-dropdown-item>
                  <el-dropdown-item
                    command="resolve"
                    :disabled="row.status === 'resolved'"
                  >
                    标记解决
                  </el-dropdown-item>
                  <el-dropdown-item command="ignore">
                    忽略告警
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 批量处理对话框 -->
    <el-dialog
      v-model="batchUpdateVisible"
      title="批量处理告警"
      width="500px"
    >
      <el-form :model="batchUpdateForm" label-width="80px">
        <el-form-item label="操作类型">
          <el-select v-model="batchUpdateForm.status" placeholder="请选择">
            <el-option label="开始处理" value="handling" />
            <el-option label="标记解决" value="resolved" />
          </el-select>
        </el-form-item>
        <el-form-item label="处理备注">
          <el-input
            v-model="batchUpdateForm.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入处理备注"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="batchUpdateVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="batchUpdateLoading"
          @click="handleBatchUpdate"
        >
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search,
  Refresh,
  ArrowDown,
  Warning,
  Clock,
  CheckCircle,
  Document
} from '@element-plus/icons-vue'
import { alertsApi } from '@/api/alerts'
import type { Alert, PaginatedResponse } from '@/types/api'
import dayjs from 'dayjs'

const router = useRouter()

// 数据状态
const loading = ref(false)
const alertList = ref<Alert[]>([])
const selectedAlerts = ref<Alert[]>([])
const alertStatistics = ref({
  total: 0,
  unhandled: 0,
  handling: 0,
  resolved: 0
})

// 搜索表单
const searchForm = reactive({
  search: '',
  severity: '',
  status: ''
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 批量处理
const batchUpdateVisible = ref(false)
const batchUpdateLoading = ref(false)
const batchUpdateForm = reactive({
  status: '',
  notes: ''
})

// 统计数据
const alertStats = computed(() => [
  {
    key: 'total',
    title: '总告警数',
    value: alertStatistics.value.total,
    icon: Warning,
    iconClass: 'primary'
  },
  {
    key: 'unhandled',
    title: '未处理',
    value: alertStatistics.value.unhandled,
    icon: Clock,
    iconClass: 'warning'
  },
  {
    key: 'handling',
    title: '处理中',
    value: alertStatistics.value.handling,
    icon: Document,
    iconClass: 'info'
  },
  {
    key: 'resolved',
    title: '已解决',
    value: alertStatistics.value.resolved,
    icon: CheckCircle,
    iconClass: 'success'
  }
])

// 初始化
onMounted(() => {
  loadData()
  loadStatistics()
})

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      ...searchForm
    }
    
    const response: PaginatedResponse<Alert> = await alertsApi.getAlerts(params)
    alertList.value = response.items
    pagination.total = response.total
  } catch (error) {
    console.error('加载告警列表失败:', error)
    ElMessage.error('加载告警列表失败')
  } finally {
    loading.value = false
  }
}

// 加载统计数据
const loadStatistics = async () => {
  try {
    const stats = await alertsApi.getAlertStatistics()
    alertStatistics.value = stats
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadData()
}

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    search: '',
    severity: '',
    status: ''
  })
  pagination.page = 1
  loadData()
}

// 刷新数据
const refreshData = () => {
  loadData()
  loadStatistics()
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.size = size
  pagination.page = 1
  loadData()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  loadData()
}

// 选择处理
const handleSelectionChange = (selection: Alert[]) => {
  selectedAlerts.value = selection
}

// 跳转详情
const goToDetail = (id: number) => {
  router.push(`/alerts/${id}`)
}

// 操作处理
const handleAction = async (command: string, row: Alert) => {
  try {
    let status = ''
    let message = ''
    
    switch (command) {
      case 'handle':
        status = 'handling'
        message = '开始处理告警'
        break
      case 'resolve':
        status = 'resolved'
        message = '标记告警为已解决'
        break
      case 'ignore':
        // 这里可以实现忽略逻辑
        ElMessage.info('忽略功能待实现')
        return
    }
    
    await alertsApi.updateAlertStatus(row.id, { status })
    ElMessage.success(message + '成功')
    loadData()
    loadStatistics()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 批量处理
const showBatchUpdateDialog = () => {
  batchUpdateVisible.value = true
  batchUpdateForm.status = ''
  batchUpdateForm.notes = ''
}

const handleBatchUpdate = async () => {
  if (!batchUpdateForm.status) {
    ElMessage.warning('请选择操作类型')
    return
  }
  
  try {
    batchUpdateLoading.value = true
    
    await alertsApi.batchUpdateAlerts({
      alert_ids: selectedAlerts.value.map(alert => alert.id),
      status: batchUpdateForm.status,
      handle_notes: batchUpdateForm.notes
    })
    
    ElMessage.success('批量处理成功')
    batchUpdateVisible.value = false
    selectedAlerts.value = []
    loadData()
    loadStatistics()
  } catch (error) {
    console.error('批量处理失败:', error)
    ElMessage.error('批量处理失败')
  } finally {
    batchUpdateLoading.value = false
  }
}

// 工具函数
const formatTime = (time: string) => dayjs(time).format('YYYY-MM-DD HH:mm:ss')

const getSeverityType = (severity: string) => {
  const typeMap: Record<string, string> = {
    critical: 'danger',
    high: 'warning',
    medium: 'primary',
    low: 'info'
  }
  return typeMap[severity] || 'info'
}

const getSeverityText = (severity: string) => {
  const textMap: Record<string, string> = {
    critical: '紧急',
    high: '高危',
    medium: '中危',
    low: '低危'
  }
  return textMap[severity] || severity
}

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    unhandled: 'danger',
    handling: 'warning',
    resolved: 'success'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    unhandled: '未处理',
    handling: '处理中',
    resolved: '已解决'
  }
  return textMap[status] || status
}
</script>

<style lang="scss" scoped>
.alerts-container {
  padding: 20px;
  
  .page-header {
    margin-bottom: 24px;
    
    .page-title {
      font-size: 24px;
      font-weight: 600;
      color: #303133;
      margin-bottom: 8px;
    }
    
    .page-description {
      color: #606266;
      font-size: 14px;
      margin: 0;
    }
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
    
    .stat-card {
      background: white;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
      display: flex;
      align-items: center;
      
      .stat-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16px;
        font-size: 20px;
        
        &.primary { background: #ecf5ff; color: #409eff; }
        &.success { background: #f0f9ff; color: #67c23a; }
        &.warning { background: #fdf6ec; color: #e6a23c; }
        &.info { background: #f4f4f5; color: #909399; }
      }
      
      .stat-content {
        .stat-title {
          font-size: 14px;
          color: #909399;
          margin-bottom: 4px;
        }
        
        .stat-value {
          font-size: 20px;
          font-weight: 600;
          color: #303133;
        }
      }
    }
  }
  
  .filter-card {
    margin-bottom: 20px;
    
    :deep(.el-card__body) {
      padding: 20px;
    }
  }
  
  .table-card {
    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
      
      .table-actions {
        display: flex;
        gap: 8px;
      }
    }
    
    .alert-name-link {
      font-weight: 500;
    }
    
    .pagination-container {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }
  }
}

@media (max-width: 768px) {
  .alerts-container {
    padding: 16px;
    
    .stats-grid {
      grid-template-columns: 1fr;
    }
    
    .filter-card {
      :deep(.el-form--inline .el-form-item) {
        display: block;
        margin-right: 0;
        margin-bottom: 16px;
      }
    }
  }
}
</style>
