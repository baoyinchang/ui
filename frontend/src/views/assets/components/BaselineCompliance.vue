<template>
  <div class="baseline-compliance">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-row">
      <el-col :span="6">
        <el-card class="stat-card total">
          <div class="stat-value">{{ complianceStatus.total || 0 }}</div>
          <div class="stat-label">总检查项</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card passed">
          <div class="stat-value">{{ complianceStatus.passed || 0 }}</div>
          <div class="stat-label">合规项</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card failed">
          <div class="stat-value">{{ complianceStatus.failed || 0 }}</div>
          <div class="stat-label">不合规项</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card compliance-rate">
          <div class="stat-value">{{ ((complianceStatus.passed / complianceStatus.total) * 100).toFixed(1) || 0 }}%</div>
          <div class="stat-label">合规率</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card>
          <template #header>合规率分布</template>
          <div class="chart-container">
            <el-loading v-if="loading" target=".chart-container" fullscreen="false" />
            <canvas id="complianceRateChart"></canvas>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>按策略合规情况</template>
          <div class="chart-container">
            <el-loading v-if="loading" target=".chart-container" fullscreen="false" />
            <canvas id="complianceByPolicyChart"></canvas>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 筛选区域 -->
    <el-card class="filter-card">
      <el-row :gutter="15" class="filter-row">
        <el-col :span="4">
          <el-select v-model="filterForm.policy" placeholder="策略类型">
            <el-option label="全部" value="" />
            <el-option label="密码策略" value="password" />
            <el-option label="系统加固" value="system" />
            <el-option label="应用配置" value="application" />
            <el-option label="网络安全" value="network" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterForm.status" placeholder="合规状态">
            <el-option label="全部" value="" />
            <el-option label="合规" value="passed" />
            <el-option label="不合规" value="failed" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-input v-model="filterForm.keyword" placeholder="搜索检查项" clearable />
        </el-col>
        <el-col :span="4" :offset="6">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 合规检查项表格 -->
    <el-card class="table-card">
      <template #header>基线合规检查项</template>
      <el-table 
        v-loading="loading"
        :data="filteredComplianceData" 
        border 
        stripe
        style="width: 100%"
      >
        <el-table-column prop="policy" label="策略类型" />
        <el-table-column prop="item" label="检查项" width="300" />
        <el-table-column prop="severity" label="严重程度">
          <template #default="scope">
            <el-tag :type="getSeverityType(scope.row.severity)">
              {{ scope.row.severity }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="standard" label="合规标准" />
        <el-table-column prop="affected" label="受影响资产" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'passed' ? 'success' : 'danger'">
              {{ scope.row.status === 'passed' ? '合规' : '不合规' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button 
              type="text" 
              @click="handleViewDetail(scope.row.id)"
            >
              详情
            </el-button>
            <el-button 
              type="text" 
              @click="handleRemediate(scope.row.id)"
              v-if="scope.row.status === 'failed'"
            >
              整改
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
        :total="filteredComplianceData.length"
        layout="total, sizes, prev, pager, next, jumper"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import Chart from 'chart.js/auto'

// 接收父组件参数
const props = defineProps({
  loading: { type: Boolean, default: false },
  complianceData: { type: Array, default: () => [] },
  complianceByPolicy: { type: Object, default: () => ({}) },
  complianceStatus: { type: Object, default: () => ({}) }
})

// 图表实例
let complianceRateChart = null
let complianceByPolicyChart = null

// 筛选表单
const filterForm = ref({
  policy: '',
  status: '',
  keyword: ''
})

// 分页配置
const pagination = ref({
  currentPage: 1,
  pageSize: 10
})

// 获取严重程度对应的标签类型
const getSeverityType = (severity) => {
  const typeMap = {
    '高': 'danger',
    '中': 'warning',
    '低': 'info'
  }
  return typeMap[severity] || 'default'
}

// 筛选后的合规检查项列表
const filteredComplianceData = computed(() => {
  return props.complianceData.filter(item => {
    // 策略类型筛选
    if (filterForm.value.policy && item.policy !== filterForm.value.policy) {
      return false
    }
    // 状态筛选
    if (filterForm.value.status && item.status !== filterForm.value.status) {
      return false
    }
    // 关键词筛选
    if (filterForm.value.keyword) {
      const keyword = filterForm.value.keyword.toLowerCase()
      if (
        !(item.item && item.item.toLowerCase().includes(keyword)) &&
        !(item.standard && item.standard.toLowerCase().includes(keyword))
      ) {
        return false
      }
    }
    return true
  })
})

// 搜索处理
const handleSearch = () => {
  pagination.value.currentPage = 1
}

// 重置筛选
const resetFilter = () => {
  filterForm.value = {
    policy: '',
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
  ElMessage.info(`查看合规检查项 ${id} 的详情`)
}

// 整改操作
const handleRemediate = (id) => {
  ElMessage.info(`整改合规检查项 ${id}`)
}

// 初始化图表
const initCharts = () => {
  // 合规率分布图表
  const rateCtx = document.getElementById('complianceRateChart').getContext('2d')
  if (complianceRateChart) {
    complianceRateChart.destroy()
  }
  complianceRateChart = new Chart(rateCtx, {
    type: 'doughnut',
    data: {
      labels: ['合规', '不合规'],
      datasets: [{
        data: [
          props.complianceStatus.passed || 0,
          props.complianceStatus.failed || 0
        ],
        backgroundColor: ['#67c23a', '#f56c6c']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })

  // 按策略合规情况图表
  const policyCtx = document.getElementById('complianceByPolicyChart').getContext('2d')
  if (complianceByPolicyChart) {
    complianceByPolicyChart.destroy()
  }
  complianceByPolicyChart = new Chart(policyCtx, {
    type: 'bar',
    data: {
      labels: Object.keys(props.complianceByPolicy),
      datasets: [
        {
          label: '合规',
          data: Object.values(props.complianceByPolicy).map(item => item.passed || 0),
          backgroundColor: '#67c23a'
        },
        {
          label: '不合规',
          data: Object.values(props.complianceByPolicy).map(item => item.failed || 0),
          backgroundColor: '#f56c6c'
        }
      ]
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
watch([() => props.complianceByPolicy, () => props.complianceStatus], () => {
  if (Object.keys(props.complianceByPolicy).length > 0) {
    initCharts()
  }
})

// 组件挂载时初始化图表
onMounted(() => {
  if (Object.keys(props.complianceByPolicy).length > 0) {
    initCharts()
  }
})

// 组件卸载时销毁图表
onUnmounted(() => {
  if (complianceRateChart) {
    complianceRateChart.destroy()
  }
  if (complianceByPolicyChart) {
    complianceByPolicyChart.destroy()
  }
})
</script>

<style scoped>
/* 保持与其他组件一致的样式风格 */
.baseline-compliance {
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

.stat-card.total .stat-value {
  color: #303133;
}

.stat-card.passed .stat-value {
  color: #67c23a;
}

.stat-card.failed .stat-value {
  color: #f56c6c;
}

.stat-card.compliance-rate .stat-value {
  color: #409eff;
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