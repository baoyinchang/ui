<template>
  <div class="baseline-compliance">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-row">
      <el-col :span="4.8">
        <el-card class="stat-card success">
          <div class="stat-value">{{ complianceStatus.complianceRate || '0%' }}</div>
          <div class="stat-label">总体合规率</div>
        </el-card>
      </el-col>
      <el-col :span="4.8">
        <el-card class="stat-card">
          <div class="stat-value">{{ complianceStatus.compliant || 0 }}</div>
          <div class="stat-label">合规主机</div>
        </el-card>
      </el-col>
      <el-col :span="4.8">
        <el-card class="stat-card danger">
          <div class="stat-value">{{ complianceStatus.nonCompliant || 0 }}</div>
          <div class="stat-label">不合规主机</div>
        </el-card>
      </el-col>
      <el-col :span="4.8">
        <el-card class="stat-card">
          <div class="stat-value">{{ Object.keys(complianceByPolicy).length }}</div>
          <div class="stat-label">策略数</div>
        </el-card>
      </el-col>
      <el-col :span="4.8">
        <el-card class="stat-card critical">
          <div class="stat-value">{{ complianceData.filter(item => item.severity === '高').length }}</div>
          <div class="stat-label">高危不合规项</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card>
          <template #header>策略合规情况</template>
          <div class="chart-container">
            <el-loading v-if="loading" target=".chart-container" fullscreen="false" />
            <canvas id="complianceByPolicyChart"></canvas>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>合规状态分布</template>
          <div class="chart-container">
            <el-loading v-if="loading" target=".chart-container" fullscreen="false" />
            <canvas id="complianceStatusChart"></canvas>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 不合规项列表 -->
    <el-card class="table-card">
      <template #header>不合规项列表</template>
      <el-table 
        v-loading="loading"
        :data="filteredComplianceItems" 
        border 
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="检查项ID" />
        <el-table-column prop="desc" label="描述" width="300" />
        <el-table-column prop="severity" label="严重性">
          <template #default="scope">
            <el-tag 
              :type="severityTypeMap[scope.row.severity]"
            >
              {{ scope.row.severity }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="policy" label="所属策略" />
        <el-table-column prop="affected" label="不合规资产数" />
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button 
              type="text" 
              @click="handleViewComplianceDetail(scope.row.id)"
            >
              详情
            </el-button>
            <el-button 
              type="text" 
              @click="handleRemediate(scope.row.id)"
            >
              修复
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
        :total="filteredComplianceItems.length"
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
  complianceData: { type: Array, default: () => [] },
  complianceByPolicy: { type: Object, default: () => ({}) },
  complianceStatus: { type: Object, default: () => ({}) }
})

// 图表实例
let complianceByPolicyChart = null
let complianceStatusChart = null

// 筛选表单
const filterForm = ref({
  severity: '',
  policy: '',
  keyword: ''
})

// 分页配置
const pagination = ref({
  currentPage: 1,
  pageSize: 10
})

// 严重性类型映射
const severityTypeMap = {
  '高': 'danger',
  '中': 'warning',
  '低': 'info'
}

// 筛选后的合规项列表
const filteredComplianceItems = computed(() => {
  return props.complianceData.filter(item => {
    // 严重性筛选
    if (filterForm.value.severity && item.severity !== filterForm.value.severity) {
      return false
    }
    // 策略筛选
    if (filterForm.value.policy && item.policy !== filterForm.value.policy) {
      return false
    }
    // 关键词筛选
    if (filterForm.value.keyword) {
      const keyword = filterForm.value.keyword.toLowerCase()
      if (
        !item.id.toLowerCase().includes(keyword) &&
        !item.desc.toLowerCase().includes(keyword)
      ) {
        return false
      }
    }
    return true
  })
})

// 查看合规详情
const handleViewComplianceDetail = (itemId) => {
  ElMessage.info(`查看合规项 ${itemId} 的详情`)
}

// 修复不合规项
const handleRemediate = (itemId) => {
  ElMessage.success(`开始修复不合规项 ${itemId}`)
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.value.pageSize = size
}

const handleCurrentChange = (page) => {
  pagination.value.currentPage = page
}

// 初始化图表
const initCharts = () => {
  // 策略合规情况图表
  const policyCtx = document.getElementById('complianceByPolicyChart').getContext('2d')
  if (complianceByPolicyChart) {
    complianceByPolicyChart.destroy()
  }
  
  // 处理策略合规数据
  const policyLabels = Object.keys(props.complianceByPolicy)
  const compliantData = policyLabels.map(policy => props.complianceByPolicy[policy].compliant)
  const nonCompliantData = policyLabels.map(policy => props.complianceByPolicy[policy].nonCompliant)
  
  complianceByPolicyChart = new Chart(policyCtx, {
    type: 'bar',
    data: {
      labels: policyLabels,
      datasets: [
        {
          label: '合规',
          data: compliantData,
          backgroundColor: '#2ecc71'
        },
        {
          label: '不合规',
          data: nonCompliantData,
          backgroundColor: '#e74c3c'
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
          },
          stacked: true
        },
        x: {
          stacked: true
        }
      }
    }
  })

  // 合规状态分布图表
  const statusCtx = document.getElementById('complianceStatusChart').getContext('2d')
  if (complianceStatusChart) {
    complianceStatusChart.destroy()
  }
  complianceStatusChart = new Chart(statusCtx, {
    type: 'doughnut',
    data: {
      labels: ['合规', '不合规'],
      datasets: [{
        data: [
          props.complianceStatus.compliant || 0,
          props.complianceStatus.nonCompliant || 0
        ],
        backgroundColor: [
          '#2ecc71', '#e74c3c'
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
  if (complianceByPolicyChart) {
    complianceByPolicyChart.destroy()
  }
  if (complianceStatusChart) {
    complianceStatusChart.destroy()
  }
})
</script>

<style scoped>
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

.stat-card.success .stat-value {
  color: #27ae60;
}

.stat-card.danger .stat-value {
  color: #e74c3c;
}

.stat-card.critical .stat-value {
  color: #c0392b;
}

.chart-row {
  margin-bottom: 10px;
}

.chart-container {
  width: 100%;
  height: 300px;
  position: relative;
}

.table-card {
  margin-bottom: 10px;
}

.pagination {
  margin-top: 15px;
  text-align: right;
}
</style>