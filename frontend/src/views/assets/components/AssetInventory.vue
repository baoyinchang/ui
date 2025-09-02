<template>
  <div class="asset-inventory">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ assetData.length }}</div>
          <div class="stat-label">资产总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card success">
          <div class="stat-value">{{ endpointStatus.online || 0 }}</div>
          <div class="stat-label">在线资产</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card danger">
          <div class="stat-value">{{ endpointStatus.threatened || 0 }}</div>
          <div class="stat-label">受威胁资产</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card warning">
          <div class="stat-value">{{ endpointStatus.noEdr || 0 }}</div>
          <div class="stat-label">未安装EDR</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card>
          <template #header>资产分布</template>
          <div class="chart-container">
            <el-loading v-if="loading" target=".chart-container" fullscreen="false" />
            <canvas id="assetDistributionChart"></canvas>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>终端安全状态分布</template>
          <div class="chart-container">
            <el-loading v-if="loading" target=".chart-container" fullscreen="false" />
            <canvas id="endpointStatusChart"></canvas>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 筛选区域 -->
    <el-card class="filter-card">
      <el-row :gutter="15" class="filter-row">
        <el-col :span="4">
          <el-select v-model="filterForm.assetType" placeholder="资产类型">
            <el-option label="全部" value="" />
            <el-option label="服务器" value="server" />
            <el-option label="工作站" value="workstation" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterForm.status" placeholder="状态">
            <el-option label="全部" value="" />
            <el-option label="在线" value="online" />
            <el-option label="离线" value="offline" />
            <el-option label="受威胁" value="threatened" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-input v-model="filterForm.keyword" placeholder="搜索主机名/IP" clearable />
        </el-col>
        <el-col :span="4" :offset="6">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 资产表格 -->
    <el-card class="table-card">
      <template #header>资产列表</template>
      <el-table 
        v-loading="loading"
        :data="filteredAssets" 
        border 
        stripe
        style="width: 100%"
      >
        <el-table-column prop="hostname" label="主机名" />
        <el-table-column prop="ip" label="IP地址" />
        <el-table-column prop="type" label="类型">
          <template #default="scope">
            <el-tag type="success" v-if="scope.row.type === 'server'">服务器</el-tag>
            <el-tag type="info" v-else>工作站</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag type="danger" v-if="scope.row.status === 'threatened'">受威胁</el-tag>
            <el-tag type="warning" v-else-if="scope.row.status === 'attention'">需关注</el-tag>
            <el-tag type="success" v-else-if="scope.row.status === 'normal'">正常</el-tag>
            <el-tag type="info" v-else>离线</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="edrVersion" label="EDR版本" />
        <el-table-column prop="department" label="所属部门" />
        <el-table-column prop="owner" label="负责人" />
        <el-table-column prop="lastOnline" label="最后在线时间" />
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button 
              type="text" 
              @click="handleViewDetail(scope.row.id)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        :total="filteredAssets.length"
        layout="total, sizes, prev, pager, next, jumper"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import Chart from 'chart.js/auto'

// 接收父组件参数
const props = defineProps({
  loading: { type: Boolean, default: false },
  assetData: { type: Array, default: () => [] },
  assetDistribution: { type: Object, default: () => ({}) },
  endpointStatus: { type: Object, default: () => ({}) }
})

// 图表实例
let assetDistributionChart = null
let endpointStatusChart = null

// 筛选表单
const filterForm = ref({
  assetType: '',
  status: '',
  keyword: ''
})

// 分页配置
const pagination = ref({
  currentPage: 1,
  pageSize: 10
})

// 筛选后的资产列表
const filteredAssets = computed(() => {
  return props.assetData.filter(asset => {
    // 类型筛选
    if (filterForm.value.assetType && asset.type !== filterForm.value.assetType) {
      return false
    }
    // 状态筛选
    if (filterForm.value.status && asset.status !== filterForm.value.status) {
      return false
    }
    // 关键词筛选
    if (filterForm.value.keyword) {
      const keyword = filterForm.value.keyword.toLowerCase()
      if (
        !asset.hostname.toLowerCase().includes(keyword) &&
        !asset.ip.toLowerCase().includes(keyword)
      ) {
        return false
      }
    }
    return true
  })
})

// 搜索处理
const handleSearch = () => {
  pagination.value.currentPage = 1 // 重置到第一页
}

// 重置筛选
const resetFilter = () => {
  filterForm.value = {
    assetType: '',
    status: '',
    keyword: ''
  }
  pagination.value.currentPage = 1
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.value.pageSize = size
}

const handleCurrentChange = (page) => {
  pagination.value.currentPage = page
}

// 查看详情
const handleViewDetail = (id) => {
  // 可以跳转到详情页或打开详情弹窗
  ElMessage.info(`查看资产ID: ${id} 的详情`)
}

// 初始化图表
const initCharts = () => {
  // 资产分布图表
  const distributionCtx = document.getElementById('assetDistributionChart').getContext('2d')
  if (assetDistributionChart) {
    assetDistributionChart.destroy()
  }
  assetDistributionChart = new Chart(distributionCtx, {
    type: 'doughnut',
    data: {
      labels: Object.keys(props.assetDistribution),
      datasets: [{
        data: Object.values(props.assetDistribution),
        backgroundColor: [
          '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c'
        ]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right'
        }
      }
    }
  })

  // 终端状态图表
  const statusCtx = document.getElementById('endpointStatusChart').getContext('2d')
  if (endpointStatusChart) {
    endpointStatusChart.destroy()
  }
  endpointStatusChart = new Chart(statusCtx, {
    type: 'bar',
    data: {
      labels: Object.keys(props.endpointStatus),
      datasets: [{
        label: '终端数量',
        data: Object.values(props.endpointStatus),
        backgroundColor: '#3498db'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  })
}

// 监听数据变化，重新渲染图表
watch([() => props.assetDistribution, () => props.endpointStatus], () => {
  if (Object.keys(props.assetDistribution).length > 0) {
    initCharts()
  }
})

// 组件挂载时初始化图表
onMounted(() => {
  if (Object.keys(props.assetDistribution).length > 0) {
    initCharts()
  }
})

// 组件卸载时销毁图表
onUnmounted(() => {
  if (assetDistributionChart) {
    assetDistributionChart.destroy()
  }
  if (endpointStatusChart) {
    endpointStatusChart.destroy()
  }
})
</script>

<style scoped>
.asset-inventory {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stat-row {
  margin-bottom: 10px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
  height: 100%;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #6c757d;
}

.stat-card.success .stat-value {
  color: #27ae60;
}

.stat-card.danger .stat-value {
  color: #e74c3c;
}

.stat-card.warning .stat-value {
  color: #f39c12;
}

.chart-row {
  margin-bottom: 10px;
}

.chart-container {
  width: 100%;
  height: 300px;
  position: relative;
}

.filter-card {
  padding: 15px;
  margin-bottom: 10px;
}

.filter-row {
  align-items: center;
}

.table-card {
  margin-bottom: 10px;
}

.pagination {
  margin-top: 15px;
  text-align: right;
}
</style>