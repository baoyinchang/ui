<template>
  <el-card class="alert-card" :class="alertClass">
    <template #header>
      <div class="alert-header">
        <div class="alert-level">
          <el-tag :type="levelType" size="small">
            {{ alert.level }}
          </el-tag>
        </div>
        <div class="alert-time">
          {{ formatTime(alert.created_at) }}
        </div>
      </div>
    </template>
    
    <div class="alert-content">
      <h4 class="alert-title">{{ alert.title }}</h4>
      <p class="alert-description">{{ alert.description }}</p>
      
      <div class="alert-details">
        <div class="detail-item">
          <span class="label">来源:</span>
          <span class="value">{{ alert.source }}</span>
        </div>
        <div class="detail-item">
          <span class="label">IP地址:</span>
          <span class="value">{{ alert.source_ip }}</span>
        </div>
        <div class="detail-item" v-if="alert.target_ip">
          <span class="label">目标IP:</span>
          <span class="value">{{ alert.target_ip }}</span>
        </div>
      </div>
    </div>
    
    <template #footer>
      <div class="alert-actions">
        <el-button size="small" @click="handleView">
          查看详情
        </el-button>
        <el-button 
          size="small" 
          type="primary" 
          @click="handleProcess"
          v-if="alert.status === 'pending'"
        >
          处理
        </el-button>
        <el-button 
          size="small" 
          type="success" 
          @click="handleIgnore"
          v-if="alert.status === 'pending'"
        >
          忽略
        </el-button>
      </div>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'
import type { Alert } from '@/types/api'

interface Props {
  alert: Alert
}

interface Emits {
  (e: 'view', alert: Alert): void
  (e: 'process', alert: Alert): void
  (e: 'ignore', alert: Alert): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// 计算属性
const levelType = computed(() => {
  const typeMap: Record<string, string> = {
    '高危': 'danger',
    '中危': 'warning',
    '低危': 'info',
    '信息': 'success'
  }
  return typeMap[props.alert.level] || 'info'
})

const alertClass = computed(() => {
  return `alert-${props.alert.level.toLowerCase()}`
})

// 方法
const formatTime = (time: string) => {
  return formatDistanceToNow(new Date(time), {
    addSuffix: true,
    locale: zhCN
  })
}

const handleView = () => {
  emit('view', props.alert)
}

const handleProcess = () => {
  emit('process', props.alert)
}

const handleIgnore = () => {
  emit('ignore', props.alert)
}
</script>

<style scoped>
.alert-card {
  margin-bottom: 16px;
  border-left: 4px solid #dcdfe6;
}

.alert-card.alert-高危 {
  border-left-color: #f56c6c;
}

.alert-card.alert-中危 {
  border-left-color: #e6a23c;
}

.alert-card.alert-低危 {
  border-left-color: #67c23a;
}

.alert-card.alert-信息 {
  border-left-color: #409eff;
}

.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alert-time {
  font-size: 12px;
  color: #909399;
}

.alert-content {
  padding: 8px 0;
}

.alert-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.alert-description {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

.alert-details {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  font-size: 12px;
}

.detail-item .label {
  color: #909399;
  margin-right: 4px;
}

.detail-item .value {
  color: #606266;
  font-weight: 500;
}

.alert-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
</style>
