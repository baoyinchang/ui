<template>
  <div class="intelligence-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h2 class="page-title">威胁情报</h2>
        <p class="page-description">管理和分析威胁指标(IOC)，提供实时威胁情报</p>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
          添加IOC
        </el-button>
        <el-button :icon="Upload" @click="showImportDialog = true">
          批量导入
        </el-button>
        <el-button :icon="Refresh" @click="refreshData">
          刷新
        </el-button>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="stats-overview">
      <el-row :gutter="16">
        <el-col :span="6" v-for="stat in intelligenceStats" :key="stat.key">
          <el-card class="stat-card" :class="stat.type">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon><component :is="stat.icon" /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stat.value }}</div>
                <div class="stat-label">{{ stat.label }}</div>
                <div class="stat-trend" :class="stat.trendClass">
                  <el-icon><component :is="stat.trendIcon" /></el-icon>
                  {{ stat.trend }}%
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 搜索和过滤 -->
    <el-card class="filter-card" shadow="never">
      <el-form :model="searchForm" inline>
        <el-form-item label="IOC类型">
          <el-select v-model="searchForm.iocType" placeholder="全部类型" clearable style="width: 120px">
            <el-option label="IP地址" value="ip" />
            <el-option label="域名" value="domain" />
            <el-option label="文件哈希" value="hash" />
            <el-option label="URL" value="url" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="威胁类型">
          <el-select v-model="searchForm.threatType" placeholder="全部威胁" clearable style="width: 120px">
            <el-option label="恶意软件" value="malware" />
            <el-option label="勒索软件" value="ransomware" />
            <el-option label="钓鱼攻击" value="phishing" />
            <el-option label="C2服务器" value="c2" />
            <el-option label="漏洞利用" value="exploit" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="可信度">
          <el-select v-model="searchForm.confidence" placeholder="全部可信度" clearable style="width: 120px">
            <el-option label="高 (70-100%)" value="high" />
            <el-option label="中 (40-69%)" value="medium" />
            <el-option label="低 (1-39%)" value="low" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="searchForm.search"
            placeholder="搜索IOC值、威胁名称或描述..."
            style="width: 300px"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
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

    <!-- 最近更新的IOC -->
    <el-card class="recent-iocs-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>最近更新的威胁指标</span>
          <el-button type="text" @click="viewAllIocs">查看全部</el-button>
        </div>
      </template>
      
      <div class="ioc-grid">
        <div
          v-for="ioc in recentIocs"
          :key="ioc.id"
          class="ioc-card"
          @click="showIocDetails(ioc)"
        >
          <div class="ioc-type" :class="`type-${ioc.type}`">
            {{ getIocTypeLabel(ioc.type) }}
          </div>
          <div class="ioc-value">{{ ioc.value }}</div>
          <div class="ioc-meta">
            <span>{{ ioc.threat_name }}</span>
            <span>{{ getRelativeTime(ioc.updated_at) }}</span>
          </div>
          <div class="ioc-tags">
            <el-tag
              v-for="tag in ioc.threat_tags"
              :key="tag"
              :type="getTagType(tag)"
              size="small"
              class="threat-tag"
            >
              {{ getTagLabel(tag) }}
            </el-tag>
          </div>
          <div class="confidence">
            <span>可信度：{{ ioc.confidence }}%</span>
            <el-progress
              :percentage="ioc.confidence"
              :color="getConfidenceColor(ioc.confidence)"
              :stroke-width="6"
              :show-text="false"
            />
          </div>
        </div>
      </div>
    </el-card>

    <!-- 情报列表 -->
    <el-card class="intelligence-list-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>威胁情报列表</span>
          <div class="header-actions">
            <el-select v-model="viewMode" style="width: 120px" @change="changeViewMode">
              <el-option label="表格视图" value="table" />
              <el-option label="分组视图" value="grouped" />
            </el-select>
          </div>
        </div>
      </template>
      
      <!-- 表格视图 -->
      <div v-if="viewMode === 'table'">
        <el-table
          :data="filteredIntelligence"
          v-loading="loading"
          @row-click="showIocDetails"
          class="intelligence-table"
        >
          <el-table-column prop="value" label="IOC值" min-width="200">
            <template #default="{ row }">
              <span class="monospace">{{ row.value }}</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="type" label="类型" width="100">
            <template #default="{ row }">
              <el-tag :type="getIocTypeTagType(row.type)" size="small">
                {{ getIocTypeLabel(row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="threat_name" label="威胁名称" min-width="150" />
          
          <el-table-column prop="threat_tags" label="威胁类型" min-width="200">
            <template #default="{ row }">
              <el-tag
                v-for="tag in row.threat_tags"
                :key="tag"
                :type="getTagType(tag)"
                size="small"
                class="threat-tag"
              >
                {{ getTagLabel(tag) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="confidence" label="可信度" width="120">
            <template #default="{ row }">
              <div class="confidence-display">
                <span>{{ row.confidence }}%</span>
                <el-progress
                  :percentage="row.confidence"
                  :color="getConfidenceColor(row.confidence)"
                  :stroke-width="4"
                  :show-text="false"
                />
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="first_seen" label="首次发现" width="120" />
          <el-table-column prop="updated_at" label="最近更新" width="120" />
          
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <el-button
                type="text"
                size="small"
                @click.stop="showIocDetails(row)"
              >
                <el-icon><View /></el-icon>
              </el-button>
              <el-button
                type="text"
                size="small"
                @click.stop="huntWithIoc(row)"
              >
                <el-icon><Aim /></el-icon>
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
      
      <!-- 分组视图 -->
      <div v-else class="grouped-view">
        <div
          v-for="group in groupedIntelligence"
          :key="group.type"
          class="group-section"
        >
          <h3 class="group-title">{{ getIocTypeLabel(group.type) }}</h3>
          <div class="group-content">
            <div
              v-for="ioc in group.items"
              :key="ioc.id"
              class="grouped-ioc-item"
              @click="showIocDetails(ioc)"
            >
              <div class="ioc-main">
                <span class="ioc-value">{{ ioc.value }}</span>
                <span class="ioc-threat">{{ ioc.threat_name }}</span>
              </div>
              <div class="ioc-meta">
                <span class="confidence-badge" :class="getConfidenceClass(ioc.confidence)">
                  {{ ioc.confidence }}%
                </span>
                <span class="update-time">{{ getRelativeTime(ioc.updated_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 添加IOC对话框 -->
    <el-dialog
      v-model="showAddDialog"
      title="添加威胁指标"
      width="600px"
      :before-close="handleCloseDialog"
    >
      <el-form :model="addForm" :rules="addFormRules" ref="addFormRef" label-width="100px">
        <el-form-item label="IOC类型" prop="type">
          <el-select v-model="addForm.type" placeholder="选择IOC类型" style="width: 100%">
            <el-option label="IP地址" value="ip" />
            <el-option label="域名" value="domain" />
            <el-option label="文件哈希" value="hash" />
            <el-option label="URL" value="url" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="IOC值" prop="value">
          <el-input v-model="addForm.value" placeholder="输入IOC值" />
        </el-form-item>
        
        <el-form-item label="威胁名称" prop="threat_name">
          <el-input v-model="addForm.threat_name" placeholder="输入威胁名称" />
        </el-form-item>
        
        <el-form-item label="威胁类型" prop="threat_tags">
          <el-select
            v-model="addForm.threat_tags"
            multiple
            placeholder="选择威胁类型"
            style="width: 100%"
          >
            <el-option label="恶意软件" value="malware" />
            <el-option label="勒索软件" value="ransomware" />
            <el-option label="钓鱼攻击" value="phishing" />
            <el-option label="C2服务器" value="c2" />
            <el-option label="漏洞利用" value="exploit" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="可信度" prop="confidence">
          <el-slider
            v-model="addForm.confidence"
            :min="1"
            :max="100"
            :step="1"
            show-input
            :format-tooltip="(val) => `${val}%`"
          />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="addForm.description"
            type="textarea"
            :rows="3"
            placeholder="输入威胁描述"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleAddIoc">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- IOC详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="IOC详情"
      width="800px"
      :before-close="handleCloseDialog"
    >
      <div v-if="selectedIoc" class="ioc-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="IOC值">
            <span class="monospace">{{ selectedIoc.value }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="IOC类型">
            <el-tag :type="getIocTypeTagType(selectedIoc.type)">
              {{ getIocTypeLabel(selectedIoc.type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="威胁名称">
            {{ selectedIoc.threat_name }}
          </el-descriptions-item>
          <el-descriptions-item label="可信度">
            <el-progress
              :percentage="selectedIoc.confidence"
              :color="getConfidenceColor(selectedIoc.confidence)"
              :stroke-width="8"
            />
          </el-descriptions-item>
          <el-descriptions-item label="威胁类型">
            <el-tag
              v-for="tag in selectedIoc.threat_tags"
              :key="tag"
              :type="getTagType(tag)"
              class="threat-tag"
            >
              {{ getTagLabel(tag) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="首次发现">
            {{ selectedIoc.first_seen }}
          </el-descriptions-item>
          <el-descriptions-item label="最近更新">
            {{ selectedIoc.updated_at }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ selectedIoc.description || '暂无描述' }}
          </el-descriptions-item>
        </el-descriptions>
        
        <div class="detail-actions">
          <el-button type="primary" @click="huntWithIoc(selectedIoc)">
            <el-icon><Aim /></el-icon>
            开始狩猎
          </el-button>
          <el-button @click="editIoc(selectedIoc)">
            <el-icon><Edit /></el-icon>
            编辑
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Upload,
  Refresh,
  Search,
  View,
  Aim,
  Edit,
  Warning,
  TrendCharts,
  DataAnalysis,
  Monitor
} from '@element-plus/icons-vue'
import { intelligenceApi } from '@/api/intelligence'

// 响应式数据
const loading = ref(false)
const showAddDialog = ref(false)
const showImportDialog = ref(false)
const showDetailDialog = ref(false)
const selectedIoc = ref(null)
const viewMode = ref('table')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 统计数据
const intelligenceStats = ref([
  {
    key: 'total',
    label: '总IOC数量',
    value: 0,
    type: 'total',
    icon: DataAnalysis,
    trend: 0,
    trendIcon: TrendCharts,
    trendClass: 'trend-stable'
  },
  {
    key: 'high_confidence',
    label: '高可信度',
    value: 0,
    type: 'high',
    icon: Warning,
    trend: 0,
    trendIcon: TrendCharts,
    trendClass: 'trend-up'
  },
  {
    key: 'new_today',
    label: '今日新增',
    value: 0,
    type: 'new',
    icon: Plus,
    trend: 0,
    trendIcon: TrendCharts,
    trendClass: 'trend-up'
  },
  {
    key: 'active_threats',
    label: '活跃威胁',
    value: 0,
    type: 'active',
    icon: Monitor,
    trend: 0,
    trendIcon: TrendCharts,
    trendClass: 'trend-down'
  }
])

// 最近IOC数据
const recentIocs = ref([])

// 情报列表数据
const intelligenceList = ref([])

// 搜索表单
const searchForm = reactive({
  iocType: '',
  threatType: '',
  confidence: '',
  search: ''
})

// 添加表单
const addForm = reactive({
  type: '',
  value: '',
  threat_name: '',
  threat_tags: [],
  confidence: 50,
  description: ''
})

// 表单验证规则
const addFormRules = {
  type: [{ required: true, message: '请选择IOC类型', trigger: 'change' }],
  value: [{ required: true, message: '请输入IOC值', trigger: 'blur' }],
  threat_name: [{ required: true, message: '请输入威胁名称', trigger: 'blur' }],
  threat_tags: [{ required: true, message: '请选择威胁类型', trigger: 'change' }],
  confidence: [{ required: true, message: '请设置可信度', trigger: 'change' }]
}

// 表单引用
const addFormRef = ref()

// 计算属性
const filteredIntelligence = computed(() => {
  let filtered = intelligenceList.value

  if (searchForm.iocType) {
    filtered = filtered.filter(item => item.type === searchForm.iocType)
  }

  if (searchForm.threatType) {
    filtered = filtered.filter(item => 
      item.threat_tags.includes(searchForm.threatType)
    )
  }

  if (searchForm.confidence) {
    const confidenceMap = {
      high: [70, 100],
      medium: [40, 69],
      low: [1, 39]
    }
    const [min, max] = confidenceMap[searchForm.confidence]
    filtered = filtered.filter(item => 
      item.confidence >= min && item.confidence <= max
    )
  }

  if (searchForm.search) {
    const searchLower = searchForm.search.toLowerCase()
    filtered = filtered.filter(item =>
      item.value.toLowerCase().includes(searchLower) ||
      item.threat_name.toLowerCase().includes(searchLower) ||
      (item.description && item.description.toLowerCase().includes(searchLower))
    )
  }

  return filtered
})

const groupedIntelligence = computed(() => {
  const groups = {}
  filteredIntelligence.value.forEach(item => {
    if (!groups[item.type]) {
      groups[item.type] = []
    }
    groups[item.type].push(item)
  })
  
  return Object.entries(groups).map(([type, items]) => ({
    type,
    items
  }))
})

// 方法
const refreshData = async () => {
  await Promise.all([
    loadIntelligenceStats(),
    loadRecentIocs(),
    loadIntelligenceList()
  ])
}

const loadIntelligenceStats = async () => {
  try {
    const response = await intelligenceApi.getIntelligenceStats()
    if (response.data) {
      const stats = response.data
      intelligenceStats.value.forEach(stat => {
        if (stats[stat.key] !== undefined) {
          stat.value = stats[stat.key]
        }
      })
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  }
}

const loadRecentIocs = async () => {
  try {
    const response = await intelligenceApi.getRecentIocs(8)
    if (response.data) {
      recentIocs.value = response.data
    }
  } catch (error) {
    console.error('加载最近IOC失败:', error)
    ElMessage.error('加载最近IOC失败')
  }
}

const loadIntelligenceList = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      ...searchForm
    }
    const response = await intelligenceApi.getIntelligenceList(params)
    if (response.data) {
      intelligenceList.value = response.data.items || response.data
      total.value = response.data.total || response.data.length
    }
  } catch (error) {
    console.error('加载情报列表失败:', error)
    ElMessage.error('加载情报列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadIntelligenceList()
}

const handleReset = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  currentPage.value = 1
  loadIntelligenceList()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadIntelligenceList()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadIntelligenceList()
}

const changeViewMode = (mode: string) => {
  viewMode.value = mode
}

const showIocDetails = (ioc: any) => {
  selectedIoc.value = ioc
  showDetailDialog.value = true
}

const viewAllIocs = () => {
  // 滚动到情报列表
  const listElement = document.querySelector('.intelligence-list-card')
  if (listElement) {
    listElement.scrollIntoView({ behavior: 'smooth' })
  }
}

const huntWithIoc = (ioc: any) => {
  ElMessage.info(`开始使用 ${ioc.value} 进行威胁狩猎`)
  // TODO: 跳转到威胁狩猎页面
}

const editIoc = (ioc: any) => {
  ElMessage.info(`编辑 ${ioc.value}`)
  // TODO: 实现编辑功能
}

const handleAddIoc = async () => {
  try {
    await addFormRef.value.validate()
    const response = await intelligenceApi.addIntelligence(addForm)
    if (response.data) {
      ElMessage.success('IOC添加成功')
      showAddDialog.value = false
      resetAddForm()
      refreshData()
    }
  } catch (error) {
    console.error('添加IOC失败:', error)
    ElMessage.error('添加IOC失败')
  }
}

const resetAddForm = () => {
  Object.keys(addForm).forEach(key => {
    if (key === 'confidence') {
      addForm[key] = 50
    } else if (key === 'threat_tags') {
      addForm[key] = []
    } else {
      addForm[key] = ''
    }
  })
}

const handleCloseDialog = () => {
  if (showAddDialog.value) {
    resetAddForm()
  }
  showAddDialog.value = false
  showDetailDialog.value = false
}

// 工具方法
const getIocTypeLabel = (type: string) => {
  const typeMap = {
    ip: 'IP地址',
    domain: '域名',
    hash: '文件哈希',
    url: 'URL'
  }
  return typeMap[type] || type
}

const getIocTypeTagType = (type: string) => {
  const typeMap = {
    ip: 'primary',
    domain: 'success',
    hash: 'warning',
    url: 'danger'
  }
  return typeMap[type] || 'info'
}

const getTagLabel = (tag: string) => {
  const tagMap = {
    malware: '恶意软件',
    ransomware: '勒索软件',
    phishing: '钓鱼攻击',
    c2: 'C2服务器',
    exploit: '漏洞利用'
  }
  return tagMap[tag] || tag
}

const getTagType = (tag: string) => {
  const typeMap = {
    malware: 'danger',
    ransomware: 'danger',
    phishing: 'warning',
    c2: 'danger',
    exploit: 'warning'
  }
  return typeMap[tag] || 'info'
}

const getConfidenceColor = (confidence: number) => {
  if (confidence >= 70) return '#f56c6c'
  if (confidence >= 40) return '#e6a23c'
  return '#67c23a'
}

const getConfidenceClass = (confidence: number) => {
  if (confidence >= 70) return 'confidence-high'
  if (confidence >= 40) return 'confidence-medium'
  return 'confidence-low'
}

const getRelativeTime = (time: string) => {
  // 简单的相对时间显示
  const date = new Date(time)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  if (days < 365) return `${Math.floor(days / 30)}个月前`
  return `${Math.floor(days / 365)}年前`
}

// 生命周期
onMounted(async () => {
  await refreshData()
})
</script>

<style scoped>
.intelligence-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin: 0 0 8px 0;
}

.page-description {
  font-size: 14px;
  color: #606266;
  margin: 0;
}

.header-right {
  display: flex;
  gap: 12px;
}

.stats-overview {
  margin-bottom: 20px;
}

.stat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.stat-card .el-card__body {
  padding: 20px;
}

.stat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-icon {
  font-size: 40px;
  color: #409eff;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-trend {
  font-size: 12px;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 4px;
}

.trend-up {
  color: #f56c6c;
}

.trend-down {
  color: #67c23a;
}

.trend-stable {
  color: #909399;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-card .el-card__body {
  padding: 20px;
}

.filter-card .el-form-item {
  margin-bottom: 10px;
}

.filter-card .el-form-item:last-child {
  margin-bottom: 0;
}

.recent-iocs-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ioc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
}

.ioc-card {
  background-color: #f9fafc;
  border: 1px solid #e9e9eb;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.ioc-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-3px);
}

.ioc-type {
  font-size: 12px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ioc-value {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
  word-break: break-all;
  font-family: 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', 'monospace';
}

.ioc-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
}

.ioc-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 8px;
}

.threat-tag {
  font-size: 11px;
  font-weight: bold;
}

.confidence {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: auto;
}

.confidence span {
  font-size: 12px;
  color: #606266;
}

.intelligence-list-card {
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.intelligence-table {
  width: 100%;
}

.intelligence-table th {
  background-color: #f5f7fa;
  color: #303133;
  font-weight: bold;
}

.intelligence-table td {
  padding: 12px 0;
}

.intelligence-table .el-tag {
  margin-right: 5px;
}

.confidence-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.confidence-display .el-progress {
  flex-grow: 1;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.grouped-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.group-section {
  background-color: #f9fafc;
  border: 1px solid #e9e9eb;
  border-radius: 8px;
  padding: 15px;
}

.group-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.group-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.grouped-ioc-item {
  background-color: #fff;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  padding: 12px 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.grouped-ioc-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transform: translateX(5px);
}

.ioc-main {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.ioc-threat {
  font-size: 14px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ioc-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #909399;
}

.update-time {
  white-space: nowrap;
}

.confidence-badge {
  font-size: 12px;
  font-weight: bold;
  color: #fff;
  padding: 2px 6px;
  border-radius: 4px;
  background-color: #409eff;
}

.confidence-high {
  background-color: #f56c6c;
}

.confidence-medium {
  background-color: #e6a23c;
}

.confidence-low {
  background-color: #67c23a;
}

.detail-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.ioc-detail .el-descriptions {
  margin-bottom: 20px;
}

.ioc-detail .el-descriptions-item__label {
  font-weight: bold;
  color: #303133;
}

.ioc-detail .el-descriptions-item__content {
  color: #606266;
}

.ioc-detail .el-tag {
  margin-right: 5px;
}

.monospace {
  font-family: 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', 'monospace';
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .header-right {
    width: 100%;
    justify-content: flex-start;
  }
  
  .ioc-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-card .el-form {
    display: flex;
    flex-direction: column;
  }
  
  .filter-card .el-form-item {
    margin-bottom: 15px;
  }
}
</style>