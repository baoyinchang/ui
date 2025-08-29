<template>
  <div class="alert-detail-container">
    <div class="page-header">
      <el-button @click="goBack" class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <div class="header-content">
        <h1 class="page-title">告警详情</h1>
        <div class="alert-meta" v-if="alertDetail">
          <el-tag :type="getSeverityType(alertDetail.severity)" size="large">
            {{ getSeverityText(alertDetail.severity) }}
          </el-tag>
          <el-tag :type="getStatusType(alertDetail.status)" size="large" class="ml-2">
            {{ getStatusText(alertDetail.status) }}
          </el-tag>
        </div>
      </div>
    </div>
    
    <div v-loading="loading" class="detail-content">
      <template v-if="alertDetail">
        <!-- 基本信息 -->
        <el-card class="info-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
              <div class="header-actions">
                <el-button
                  v-if="alertDetail.status === 'unhandled'"
                  type="primary"
                  @click="handleAlert"
                >
                  开始处理
                </el-button>
                <el-button
                  v-if="alertDetail.status !== 'resolved'"
                  type="success"
                  @click="resolveAlert"
                >
                  标记解决
                </el-button>
                <el-dropdown @command="handleMoreAction">
                  <el-button>
                    更多操作
                    <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="export">导出详情</el-dropdown-item>
                      <el-dropdown-item command="share">分享链接</el-dropdown-item>
                      <el-dropdown-item command="similar">查找相似告警</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </template>
          
          <div class="info-grid">
            <div class="info-item">
              <label>告警名称</label>
              <span>{{ alertDetail.alert_name }}</span>
            </div>
            <div class="info-item">
              <label>事件ID</label>
              <span>{{ alertDetail.event_id || '-' }}</span>
            </div>
            <div class="info-item">
              <label>受影响资产</label>
              <el-link type="primary" @click="goToAsset(alertDetail.asset_id)">
                {{ alertDetail.asset_name }}
              </el-link>
            </div>
            <div class="info-item">
              <label>创建时间</label>
              <span>{{ formatTime(alertDetail.created_at) }}</span>
            </div>
            <div class="info-item">
              <label>更新时间</label>
              <span>{{ formatTime(alertDetail.updated_at) }}</span>
            </div>
            <div class="info-item">
              <label>处理人</label>
              <span>{{ alertDetail.handler_name || '-' }}</span>
            </div>
            <div class="info-item full-width">
              <label>告警描述</label>
              <p class="description">{{ alertDetail.description || '暂无描述' }}</p>
            </div>
          </div>
        </el-card>
        
        <!-- 处理记录 -->
        <el-card class="timeline-card" shadow="never">
          <template #header>
            <span>处理记录</span>
          </template>
          
          <el-timeline>
            <el-timeline-item
              v-for="record in processRecords"
              :key="record.id"
              :timestamp="record.timestamp"
              :type="record.type"
            >
              <div class="timeline-content">
                <div class="timeline-title">{{ record.title }}</div>
                <div class="timeline-description">{{ record.description }}</div>
                <div class="timeline-user">操作人：{{ record.user }}</div>
              </div>
            </el-timeline-item>
          </el-timeline>
        </el-card>
        
        <!-- 相关信息 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card class="related-card" shadow="never">
              <template #header>
                <span>相关事件</span>
              </template>
              
              <div class="related-list">
                <div
                  v-for="event in relatedEvents"
                  :key="event.id"
                  class="related-item"
                  @click="goToEvent(event.id)"
                >
                  <div class="event-info">
                    <div class="event-title">{{ event.title }}</div>
                    <div class="event-time">{{ formatTime(event.timestamp) }}</div>
                  </div>
                  <el-tag :type="event.type" size="small">{{ event.category }}</el-tag>
                </div>
                
                <div v-if="relatedEvents.length === 0" class="empty-state">
                  <el-empty description="暂无相关事件" />
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="12">
            <el-card class="related-card" shadow="never">
              <template #header>
                <span>威胁情报</span>
              </template>
              
              <div class="threat-intel">
                <div
                  v-for="intel in threatIntelligence"
                  :key="intel.id"
                  class="intel-item"
                >
                  <div class="intel-header">
                    <span class="intel-type">{{ intel.type }}</span>
                    <el-tag :type="intel.confidence > 0.8 ? 'success' : 'warning'" size="small">
                      置信度: {{ (intel.confidence * 100).toFixed(0) }}%
                    </el-tag>
                  </div>
                  <div class="intel-content">{{ intel.description }}</div>
                  <div class="intel-source">来源：{{ intel.source }}</div>
                </div>
                
                <div v-if="threatIntelligence.length === 0" class="empty-state">
                  <el-empty description="暂无威胁情报" />
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </template>
    </div>
    
    <!-- 处理对话框 -->
    <el-dialog
      v-model="handleDialogVisible"
      title="处理告警"
      width="500px"
    >
      <el-form :model="handleForm" label-width="80px">
        <el-form-item label="处理备注">
          <el-input
            v-model="handleForm.notes"
            type="textarea"
            :rows="4"
            placeholder="请输入处理备注"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="handleDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="handleLoading"
          @click="confirmHandle"
        >
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, ArrowDown } from '@element-plus/icons-vue'
import { alertsApi } from '@/api/alerts'
import type { Alert } from '@/types/api'
import dayjs from 'dayjs'

const router = useRouter()
const route = useRoute()

// 数据状态
const loading = ref(false)
const alertDetail = ref<Alert | null>(null)
const handleDialogVisible = ref(false)
const handleLoading = ref(false)

// 表单数据
const handleForm = reactive({
  notes: ''
})

// 模拟数据
const processRecords = ref([
  {
    id: 1,
    timestamp: '2025-08-27 14:32:15',
    type: 'danger',
    title: '告警触发',
    description: '系统检测到可疑活动，自动生成告警',
    user: '系统'
  },
  {
    id: 2,
    timestamp: '2025-08-27 14:35:20',
    type: 'warning',
    title: '开始处理',
    description: '安全分析师开始处理此告警',
    user: '张三'
  }
])

const relatedEvents = ref([
  {
    id: 1,
    title: '可疑进程创建',
    timestamp: '2025-08-27T14:30:00Z',
    category: '进程监控',
    type: 'warning'
  },
  {
    id: 2,
    title: '网络连接异常',
    timestamp: '2025-08-27T14:31:00Z',
    category: '网络监控',
    type: 'danger'
  }
])

const threatIntelligence = ref([
  {
    id: 1,
    type: 'IOC',
    description: '检测到已知恶意IP地址 192.168.1.100',
    confidence: 0.95,
    source: 'VirusTotal'
  },
  {
    id: 2,
    type: '威胁家族',
    description: '疑似Emotet恶意软件活动特征',
    confidence: 0.87,
    source: 'MITRE ATT&CK'
  }
])

// 初始化
onMounted(() => {
  const alertId = Number(route.params.id)
  if (alertId) {
    loadAlertDetail(alertId)
  }
})

// 加载告警详情
const loadAlertDetail = async (id: number) => {
  loading.value = true
  try {
    alertDetail.value = await alertsApi.getAlert(id)
  } catch (error) {
    console.error('加载告警详情失败:', error)
    ElMessage.error('加载告警详情失败')
  } finally {
    loading.value = false
  }
}

// 返回
const goBack = () => {
  router.back()
}

// 跳转到资产详情
const goToAsset = (assetId: number) => {
  router.push(`/assets/${assetId}`)
}

// 跳转到事件详情
const goToEvent = (eventId: number) => {
  // 这里可以跳转到事件详情页面
  ElMessage.info(`跳转到事件 ${eventId} 详情`)
}

// 处理告警
const handleAlert = () => {
  handleDialogVisible.value = true
  handleForm.notes = ''
}

// 确认处理
const confirmHandle = async () => {
  if (!alertDetail.value) return
  
  try {
    handleLoading.value = true
    
    await alertsApi.updateAlertStatus(alertDetail.value.id, {
      status: 'handling',
      handle_notes: handleForm.notes
    })
    
    ElMessage.success('开始处理告警成功')
    handleDialogVisible.value = false
    
    // 重新加载详情
    loadAlertDetail(alertDetail.value.id)
  } catch (error) {
    console.error('处理告警失败:', error)
    ElMessage.error('处理告警失败')
  } finally {
    handleLoading.value = false
  }
}

// 解决告警
const resolveAlert = async () => {
  if (!alertDetail.value) return
  
  try {
    await alertsApi.updateAlertStatus(alertDetail.value.id, {
      status: 'resolved',
      handle_notes: '告警已解决'
    })
    
    ElMessage.success('告警已标记为解决')
    loadAlertDetail(alertDetail.value.id)
  } catch (error) {
    console.error('解决告警失败:', error)
    ElMessage.error('解决告警失败')
  }
}

// 更多操作
const handleMoreAction = (command: string) => {
  switch (command) {
    case 'export':
      ElMessage.info('导出功能待实现')
      break
    case 'share':
      ElMessage.info('分享功能待实现')
      break
    case 'similar':
      ElMessage.info('查找相似告警功能待实现')
      break
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
.alert-detail-container {
  padding: 20px;
  
  .page-header {
    display: flex;
    align-items: flex-start;
    margin-bottom: 24px;
    
    .back-btn {
      margin-right: 16px;
      margin-top: 4px;
    }
    
    .header-content {
      flex: 1;
      
      .page-title {
        font-size: 24px;
        font-weight: 600;
        color: #303133;
        margin-bottom: 8px;
      }
      
      .alert-meta {
        display: flex;
        align-items: center;
      }
    }
  }
  
  .detail-content {
    .info-card {
      margin-bottom: 20px;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
        
        .header-actions {
          display: flex;
          gap: 8px;
        }
      }
      
      .info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        
        .info-item {
          &.full-width {
            grid-column: 1 / -1;
          }
          
          label {
            display: block;
            font-weight: 500;
            color: #606266;
            margin-bottom: 4px;
            font-size: 14px;
          }
          
          span {
            color: #303133;
          }
          
          .description {
            margin: 0;
            line-height: 1.6;
            color: #303133;
          }
        }
      }
    }
    
    .timeline-card {
      margin-bottom: 20px;
      
      .timeline-content {
        .timeline-title {
          font-weight: 500;
          color: #303133;
          margin-bottom: 4px;
        }
        
        .timeline-description {
          color: #606266;
          font-size: 14px;
          margin-bottom: 4px;
        }
        
        .timeline-user {
          color: #909399;
          font-size: 12px;
        }
      }
    }
    
    .related-card {
      .related-list {
        .related-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px 0;
          border-bottom: 1px solid #ebeef5;
          cursor: pointer;
          transition: background-color 0.3s;
          
          &:hover {
            background-color: #f5f7fa;
            margin: 0 -20px;
            padding: 12px 20px;
            border-radius: 4px;
          }
          
          &:last-child {
            border-bottom: none;
          }
          
          .event-info {
            flex: 1;
            
            .event-title {
              font-weight: 500;
              color: #303133;
              margin-bottom: 4px;
            }
            
            .event-time {
              font-size: 12px;
              color: #909399;
            }
          }
        }
        
        .empty-state {
          padding: 20px 0;
        }
      }
      
      .threat-intel {
        .intel-item {
          padding: 16px 0;
          border-bottom: 1px solid #ebeef5;
          
          &:last-child {
            border-bottom: none;
          }
          
          .intel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            
            .intel-type {
              font-weight: 500;
              color: #303133;
            }
          }
          
          .intel-content {
            color: #606266;
            margin-bottom: 4px;
            line-height: 1.5;
          }
          
          .intel-source {
            font-size: 12px;
            color: #909399;
          }
        }
        
        .empty-state {
          padding: 20px 0;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .alert-detail-container {
    padding: 16px;
    
    .page-header {
      flex-direction: column;
      align-items: flex-start;
      
      .back-btn {
        margin-bottom: 16px;
        margin-right: 0;
      }
    }
    
    .info-grid {
      grid-template-columns: 1fr !important;
    }
  }
}
</style>
