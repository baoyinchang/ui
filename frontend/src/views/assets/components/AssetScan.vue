<template>
  <div class="asset-scan">
    <el-card>
      <el-tabs v-model="activeTab" type="border-card">
        <el-tab-pane label="快速扫描" name="quick">
          <el-form :model="quickScanForm" label-width="120px">
            <el-form-item label="IP范围" prop="ipRange">
              <el-input 
                v-model="quickScanForm.ipRange" 
                placeholder="例如: 192.168.1.1-100 或 192.168.1.0/24"
              />
            </el-form-item>
            <el-form-item label="扫描端口" prop="ports">
              <el-input 
                v-model="quickScanForm.ports" 
                placeholder="例如: 1-1000 或 80,443,3306"
              />
              <el-text type="info" size="small">
                留空将扫描常用端口
              </el-text>
            </el-form-item>
            <el-form-item label="扫描速度">
              <el-slider 
                v-model="quickScanForm.speed" 
                :min="1" 
                :max="5" 
                :marks="{1: '慢', 3: '中', 5: '快'}"
                show-stops
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="高级扫描" name="advanced">
          <el-form :model="advancedScanForm" label-width="120px">
            <el-form-item label="扫描目标" prop="targets">
              <el-input 
                v-model="advancedScanForm.targets" 
                type="textarea" 
                rows="3"
                placeholder="每行一个IP地址或域名"
              />
            </el-form-item>
            <el-form-item label="扫描类型">
              <el-checkbox-group v-model="advancedScanForm.scanTypes">
                <el-checkbox label="port" border>端口扫描</el-checkbox>
                <el-checkbox label="service" border>服务识别</el-checkbox>
                <el-checkbox label="vuln" border>漏洞检测</el-checkbox>
                <el-checkbox label="os" border>操作系统识别</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="扫描深度">
              <el-radio-group v-model="advancedScanForm.depth">
                <el-radio label="light">轻量 (快速)</el-radio>
                <el-radio label="normal">常规 (平衡)</el-radio>
                <el-radio label="deep">深度 (全面)</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="扫描时间">
              <el-time-picker
                v-model="advancedScanForm.scheduleTime"
                placeholder="选择扫描时间"
                format="HH:mm"
                value-format="HH:mm"
              />
              <el-checkbox v-model="advancedScanForm.isScheduled">
                定时扫描
              </el-checkbox>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <div class="scan-actions">
      <el-button @click="$emit('cancel')">取消</el-button>
      <el-button type="primary" @click="handleStartScan">开始扫描</el-button>
    </div>

    <!-- 扫描进度 -->
    <el-card v-if="showProgress" class="progress-card">
      <div class="progress-info">
        <h4>扫描进度: {{ progressPercent }}%</h4>
        <el-progress :percentage="progressPercent" />
        <p class="progress-status">{{ progressStatus }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import { assetsApi } from '@/api'

// 扫描配置
const activeTab = ref('quick')
const showProgress = ref(false)
const progressPercent = ref(0)
const progressStatus = ref('准备中...')

// 快速扫描表单
const quickScanForm = reactive({
  ipRange: '',
  ports: '',
  speed: 3
})

// 高级扫描表单
const advancedScanForm = reactive({
  targets: '',
  scanTypes: ['port', 'service'],
  depth: 'normal',
  isScheduled: false,
  scheduleTime: ''
})

// 开始扫描
const handleStartScan = async () => {
  // 验证表单
  if (activeTab.value === 'quick' && !quickScanForm.ipRange) {
    ElMessage.error('请输入IP范围')
    return
  }
  
  if (activeTab.value === 'advanced' && !advancedScanForm.targets) {
    ElMessage.error('请输入扫描目标')
    return
  }

  const loading = ElLoading.service({
    lock: true,
    text: '正在启动扫描任务...',
    background: 'rgba(0, 0, 0, 0.7)'
  })

  try {
    // 构建扫描参数
    const scanParams = activeTab.value === 'quick' 
      ? {
          type: 'quick',
          ip_range: quickScanForm.ipRange,
          ports: quickScanForm.ports,
          speed: quickScanForm.speed
        }
      : {
          type: 'advanced',
          targets: advancedScanForm.targets,
          scan_types: advancedScanForm.scanTypes.join(','),
          depth: advancedScanForm.depth,
          scheduled: advancedScanForm.isScheduled,
          schedule_time: advancedScanForm.scheduleTime
        }

    // 启动扫描
    const { data } = await assetsApi.startScan(scanParams)
    loading.close()
    
    // 显示进度
    showProgress.value = true
    progressPercent.value = 0
    progressStatus.value = '扫描任务已启动'
    
    // 模拟进度更新 (实际项目中应该通过WebSocket或定时轮询获取真实进度)
    simulateProgress()
    
  } catch (error) {
    console.error('扫描启动失败:', error)
    ElMessage.error('扫描启动失败')
    loading.close()
  }
}

// 模拟进度更新
const simulateProgress = () => {
  const timer = setInterval(() => {
    progressPercent.value += Math.floor(Math.random() * 10)
    if (progressPercent.value >= 30) {
      progressStatus.value = '正在检测端口和服务...'
    }
    if (progressPercent.value >= 70) {
      progressStatus.value = '正在分析扫描结果...'
    }
    if (progressPercent.value >= 100) {
      progressPercent.value = 100
      progressStatus.value = '扫描完成'
      clearInterval(timer)
      // 通知父组件扫描完成
      setTimeout(() => {
        $emit('success')
      }, 1000)
    }
  }, 1000)
}
</script>

<style scoped>
.asset-scan {
  padding: 10px 0;
}

.el-tabs {
  margin-bottom: 20px;
}

.scan-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-bottom: 20px;
}

.progress-card {
  margin-top: 20px;
}

.progress-info {
  padding: 10px 0;
}

.progress-status {
  margin-top: 10px;
  color: #666;
}
</style>