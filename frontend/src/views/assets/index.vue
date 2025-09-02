<template>
  <div class="asset-management-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">资产管理中心</h1>
      <div class="page-actions">
        <el-button type="primary" @click="handleRefresh">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <el-button type="primary" @click="handleAddAsset">
          <el-icon><Plus /></el-icon>
          添加资产
        </el-button>
      </div>
    </div>

    <!-- 面包屑导航 -->
    <el-breadcrumb separator="/" class="breadcrumb">
      <el-breadcrumb-item>资产管理</el-breadcrumb-item>
      <el-breadcrumb-item>{{ activeTabName }}</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- Tab 导航 -->
    <el-tabs v-model="activeTab" type="card" class="asset-tabs" @tab-change="handleTabChange">
      <!-- 资产清单标签页 -->
      <el-tab-pane name="inventory" label="资产清单">
        <template #label>
          <el-icon><List /></el-icon>
          资产清单
        </template>
        <AssetInventory 
          :loading="loading" 
          :assetData="assetData"
          :assetDistribution="assetDistribution"
          :endpointStatus="endpointStatus"
          @refresh-data="handleRefresh"
        />
      </el-tab-pane>

      <!-- 漏洞与补丁标签页 -->
      <el-tab-pane name="vulnerability" label="漏洞与补丁">
        <template #label>
          <el-icon><Warning /></el-icon>
          漏洞与补丁
        </template>
        <VulnerabilityManagement 
          :loading="loading"
          :vulnerabilityData="vulnerabilityData"
          :vulnSeverityData="vulnSeverityData"
          :vulnTrendData="vulnTrendData"
          @refresh-data="handleRefresh"
        />
      </el-tab-pane>

      <!-- 基线合规标签页 -->
      <el-tab-pane name="compliance" label="基线合规">
        <template #label>
          <el-icon><Check /></el-icon>
          基线合规
        </template>
        <BaselineCompliance 
          :loading="loading"
          :complianceData="complianceData"
          :complianceByPolicy="complianceByPolicy"
          :complianceStatus="complianceStatus"
          @refresh-data="handleRefresh"
        />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
// 引入图标
import { Refresh, Plus, List, Warning, Check } from '@element-plus/icons-vue'
// 引入所有标签页组件
import AssetInventory from './components/AssetInventory.vue'
import VulnerabilityManagement from './components/VulnerabilityManagement.vue'
import BaselineCompliance from './components/BaselineCompliance.vue'
// 引入API
import { assetApi } from '@/api/modules/asset'
import { vulnerabilityApi } from '@/api/modules/vulnerability'
import { complianceApi } from '@/api/modules/compliance'

// 状态管理
const activeTab = ref('inventory')
const loading = ref(false)

// 所有标签页数据存储
const assetData = ref([])
const assetDistribution = ref({})
const endpointStatus = ref({})
const vulnerabilityData = ref([])
const vulnSeverityData = ref({})
const vulnTrendData = ref({})
const complianceData = ref([])
const complianceByPolicy = ref({})
const complianceStatus = ref({})

// Tab名称映射
const tabNameMap = {
  inventory: '资产清单',
  vulnerability: '漏洞与补丁',
  compliance: '基线合规'
}

// 当前Tab名称
const activeTabName = computed(() => tabNameMap[activeTab.value])

// 刷新数据 - 根据当前标签页加载对应数据
const handleRefresh = async () => {
  loading.value = true
  try {
    if (activeTab.value === 'inventory') {
      await fetchAssetData()
    } else if (activeTab.value === 'vulnerability') {
      await fetchVulnerabilityData()
    } else if (activeTab.value === 'compliance') {
      await fetchComplianceData()
    }
    ElMessage.success('数据刷新成功')
  } catch (error) {
    ElMessage.error('数据刷新失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// Tab切换时加载数据
const handleTabChange = async (tabName) => {
  loading.value = true
  try {
    // 只在首次切换到该标签页时加载数据
    if (tabName === 'inventory' && assetData.value.length === 0) {
      await fetchAssetData()
    } else if (tabName === 'vulnerability' && vulnerabilityData.value.length === 0) {
      await fetchVulnerabilityData()
    } else if (tabName === 'compliance' && complianceData.value.length === 0) {
      await fetchComplianceData()
    }
  } catch (error) {
    console.error(`加载${tabName}数据失败:`, error);
    // 即使加载失败也显示空页面结构
    if (tabName === 'vulnerability' && vulnerabilityData.value.length === 0) {
      vulnerabilityData.value = [];
    } else if (tabName === 'compliance' && complianceData.value.length === 0) {
      complianceData.value = [];
    }
  } finally {
    loading.value = false
  }
}

// 添加资产
const handleAddAsset = () => {
  ElMessage.info('打开添加资产弹窗')
}

// 获取资产数据
const fetchAssetData = async () => {
  const [assetListRes, assetStatsRes] = await Promise.all([
    assetApi.getList(),
    assetApi.getStatistics()
  ])
  assetData.value = assetListRes.data.items
  assetDistribution.value = assetStatsRes.data.distribution
  endpointStatus.value = assetStatsRes.data.status
}

// 获取漏洞数据
const fetchVulnerabilityData = async () => {
  const [vulnListRes, vulnStatsRes] = await Promise.all([
    vulnerabilityApi.getList(),
    vulnerabilityApi.getStatistics()
  ])
  vulnerabilityData.value = vulnListRes.data.items
  vulnSeverityData.value = vulnStatsRes.data.severity
  vulnTrendData.value = vulnStatsRes.data.trend
}

// 获取合规数据
const fetchComplianceData = async () => {
  const [complianceListRes, complianceStatsRes] = await Promise.all([
    complianceApi.getNonCompliantItems(),
    complianceApi.getStatistics()
  ])
  complianceData.value = complianceListRes.data.items
  complianceByPolicy.value = complianceStatsRes.data.byPolicy
  complianceStatus.value = complianceStatsRes.data.status
}

// 页面加载时初始化数据
onMounted(async () => {
  await handleRefresh()
})
</script>

<style scoped>
.asset-management-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.risk-text {
  margin-left: 8px;
  font-size: 14px;
  font-weight: 500;
}

.el-progress {
  width: 120px;
  display: inline-block;
}

.page-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 16px;
}

.breadcrumb {
  margin-bottom: 20px;
}

.asset-tabs {
  width: 100%;
}
</style>