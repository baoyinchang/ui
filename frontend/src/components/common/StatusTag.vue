<template>
  <el-tag
    :type="tagType"
    :size="size"
    :effect="effect"
    :color="customColor"
    :hit="hit"
    :round="round"
    :closable="closable"
    :disable-transitions="disableTransitions"
    @close="handleClose"
    @click="handleClick"
  >
    <el-icon v-if="icon" class="status-icon">
      <component :is="icon" />
    </el-icon>
    <span class="status-text">{{ displayText }}</span>
    <span v-if="showDot" class="status-dot" :style="{ backgroundColor: dotColor }"></span>
  </el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  ALERT_SEVERITY,
  ALERT_SEVERITY_LABELS,
  ALERT_SEVERITY_COLORS,
  ALERT_STATUS,
  ALERT_STATUS_LABELS,
  ASSET_STATUS,
  ASSET_STATUS_LABELS,
  INVESTIGATION_STATUS,
  INVESTIGATION_STATUS_LABELS,
  INVESTIGATION_PRIORITY,
  INVESTIGATION_PRIORITY_LABELS,
  REPORT_STATUS,
  REPORT_STATUS_LABELS
} from '@/utils/constants'

// 状态类型定义
type StatusType = 
  | 'alert-severity'
  | 'alert-status'
  | 'asset-status'
  | 'investigation-status'
  | 'investigation-priority'
  | 'report-status'
  | 'user-status'
  | 'system-status'
  | 'custom'

// 组件属性
interface Props {
  value: string | number
  type?: StatusType
  size?: 'large' | 'default' | 'small'
  effect?: 'dark' | 'light' | 'plain'
  hit?: boolean
  round?: boolean
  closable?: boolean
  disableTransitions?: boolean
  icon?: any
  showDot?: boolean
  customText?: string
  customColor?: string
  customMapping?: Record<string | number, { text: string; color?: string; type?: string }>
}

const props = withDefaults(defineProps<Props>(), {
  type: 'custom',
  size: 'default',
  effect: 'light',
  hit: false,
  round: false,
  closable: false,
  disableTransitions: false,
  showDot: false
})

// 事件定义
const emit = defineEmits(['close', 'click'])

// 状态映射配置
const statusMappings = {
  'alert-severity': {
    labels: ALERT_SEVERITY_LABELS,
    colors: ALERT_SEVERITY_COLORS,
    types: {
      [ALERT_SEVERITY.CRITICAL]: 'danger',
      [ALERT_SEVERITY.HIGH]: 'warning',
      [ALERT_SEVERITY.MEDIUM]: 'primary',
      [ALERT_SEVERITY.LOW]: 'success',
      [ALERT_SEVERITY.INFO]: 'info'
    }
  },
  'alert-status': {
    labels: ALERT_STATUS_LABELS,
    colors: {
      [ALERT_STATUS.UNHANDLED]: '#f56c6c',
      [ALERT_STATUS.HANDLING]: '#e6a23c',
      [ALERT_STATUS.RESOLVED]: '#67c23a',
      [ALERT_STATUS.CLOSED]: '#909399'
    },
    types: {
      [ALERT_STATUS.UNHANDLED]: 'danger',
      [ALERT_STATUS.HANDLING]: 'warning',
      [ALERT_STATUS.RESOLVED]: 'success',
      [ALERT_STATUS.CLOSED]: 'info'
    }
  },
  'asset-status': {
    labels: ASSET_STATUS_LABELS,
    colors: {
      [ASSET_STATUS.NORMAL]: '#67c23a',
      [ASSET_STATUS.WARNING]: '#e6a23c',
      [ASSET_STATUS.DANGER]: '#f56c6c',
      [ASSET_STATUS.OFFLINE]: '#909399'
    },
    types: {
      [ASSET_STATUS.NORMAL]: 'success',
      [ASSET_STATUS.WARNING]: 'warning',
      [ASSET_STATUS.DANGER]: 'danger',
      [ASSET_STATUS.OFFLINE]: 'info'
    }
  },
  'investigation-status': {
    labels: INVESTIGATION_STATUS_LABELS,
    colors: {
      [INVESTIGATION_STATUS.ACTIVE]: '#409eff',
      [INVESTIGATION_STATUS.COMPLETED]: '#67c23a',
      [INVESTIGATION_STATUS.ARCHIVED]: '#909399',
      [INVESTIGATION_STATUS.CANCELLED]: '#f56c6c'
    },
    types: {
      [INVESTIGATION_STATUS.ACTIVE]: 'primary',
      [INVESTIGATION_STATUS.COMPLETED]: 'success',
      [INVESTIGATION_STATUS.ARCHIVED]: 'info',
      [INVESTIGATION_STATUS.CANCELLED]: 'danger'
    }
  },
  'investigation-priority': {
    labels: INVESTIGATION_PRIORITY_LABELS,
    colors: {
      [INVESTIGATION_PRIORITY.CRITICAL]: '#f56c6c',
      [INVESTIGATION_PRIORITY.HIGH]: '#e6a23c',
      [INVESTIGATION_PRIORITY.MEDIUM]: '#409eff',
      [INVESTIGATION_PRIORITY.LOW]: '#67c23a'
    },
    types: {
      [INVESTIGATION_PRIORITY.CRITICAL]: 'danger',
      [INVESTIGATION_PRIORITY.HIGH]: 'warning',
      [INVESTIGATION_PRIORITY.MEDIUM]: 'primary',
      [INVESTIGATION_PRIORITY.LOW]: 'success'
    }
  },
  'report-status': {
    labels: REPORT_STATUS_LABELS,
    colors: {
      [REPORT_STATUS.DRAFT]: '#909399',
      [REPORT_STATUS.GENERATING]: '#e6a23c',
      [REPORT_STATUS.COMPLETED]: '#67c23a',
      [REPORT_STATUS.FAILED]: '#f56c6c',
      [REPORT_STATUS.SCHEDULED]: '#409eff'
    },
    types: {
      [REPORT_STATUS.DRAFT]: 'info',
      [REPORT_STATUS.GENERATING]: 'warning',
      [REPORT_STATUS.COMPLETED]: 'success',
      [REPORT_STATUS.FAILED]: 'danger',
      [REPORT_STATUS.SCHEDULED]: 'primary'
    }
  },
  'user-status': {
    labels: {
      active: '活跃',
      inactive: '非活跃',
      locked: '已锁定',
      pending: '待激活'
    },
    colors: {
      active: '#67c23a',
      inactive: '#909399',
      locked: '#f56c6c',
      pending: '#e6a23c'
    },
    types: {
      active: 'success',
      inactive: 'info',
      locked: 'danger',
      pending: 'warning'
    }
  },
  'system-status': {
    labels: {
      online: '在线',
      offline: '离线',
      maintenance: '维护中',
      error: '错误'
    },
    colors: {
      online: '#67c23a',
      offline: '#909399',
      maintenance: '#e6a23c',
      error: '#f56c6c'
    },
    types: {
      online: 'success',
      offline: 'info',
      maintenance: 'warning',
      error: 'danger'
    }
  }
}

// 计算属性
const currentMapping = computed(() => {
  if (props.type === 'custom' && props.customMapping) {
    return props.customMapping[props.value]
  }
  
  const mapping = statusMappings[props.type as keyof typeof statusMappings]
  if (!mapping) return null
  
  return {
    text: mapping.labels[props.value as keyof typeof mapping.labels],
    color: mapping.colors[props.value as keyof typeof mapping.colors],
    type: mapping.types[props.value as keyof typeof mapping.types]
  }
})

const displayText = computed(() => {
  if (props.customText) return props.customText
  return currentMapping.value?.text || String(props.value)
})

const tagType = computed(() => {
  if (props.customColor) return undefined
  return currentMapping.value?.type || 'primary'
})

const customColor = computed(() => {
  if (props.customColor) return props.customColor
  if (props.effect === 'plain' || props.effect === 'light') {
    return undefined
  }
  return currentMapping.value?.color
})

const dotColor = computed(() => {
  return currentMapping.value?.color || props.customColor || '#409eff'
})

// 事件处理
const handleClose = (event: Event) => {
  emit('close', event)
}

const handleClick = (event: Event) => {
  emit('click', event)
}
</script>

<script lang="ts">
export default {
  name: 'StatusTag'
}
</script>

<style scoped lang="scss">
.el-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  
  .status-icon {
    font-size: 12px;
  }
  
  .status-text {
    line-height: 1;
  }
  
  .status-dot {
    font-size: 8px;
    margin-left: 2px;
  }
}

// 自定义状态样式
.el-tag--success {
  &.is-light {
    background-color: #f0f9ff;
    border-color: #c6f6d5;
    color: #22c55e;
  }
}

.el-tag--warning {
  &.is-light {
    background-color: #fffbeb;
    border-color: #fed7aa;
    color: #f59e0b;
  }
}

.el-tag--danger {
  &.is-light {
    background-color: #fef2f2;
    border-color: #fecaca;
    color: #ef4444;
  }
}

.el-tag--info {
  &.is-light {
    background-color: #f8fafc;
    border-color: #cbd5e1;
    color: #64748b;
  }
}

.el-tag--primary {
  &.is-light {
    background-color: #eff6ff;
    border-color: #bfdbfe;
    color: #3b82f6;
  }
}

// 动画效果
.el-tag {
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
}

// 圆角样式
.el-tag.is-round {
  border-radius: 12px;
}

// 大小变体
.el-tag--large {
  padding: 8px 12px;
  font-size: 14px;
  
  .status-icon {
    font-size: 14px;
  }
}

.el-tag--small {
  padding: 2px 6px;
  font-size: 11px;
  
  .status-icon {
    font-size: 10px;
  }
  
  .status-dot {
    font-size: 6px;
  }
}

// 特殊效果
.el-tag.is-hit {
  border: 1px solid currentColor;
}

// 可关闭标签
.el-tag.is-closable {
  padding-right: 20px;
}

// 禁用过渡效果
.el-tag.is-disable-transitions {
  transition: none;
  
  &:hover {
    transform: none;
    box-shadow: none;
  }
}
</style>
