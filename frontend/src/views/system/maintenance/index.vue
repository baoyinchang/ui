<template>
  <div class="systemmaintenance-container">
    <div class="page-header">
      <h1 class="page-title">系统维护</h1>
      <div class="page-actions">
        <el-button type="primary" @click="handleRefresh">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>
    
    <div class="page-content">
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>系统维护概览</span>
              </div>
            </template>
            <div class="overview-content">
              <el-empty description="系统维护功能模块">
                <el-button type="primary" @click="handleAction">查看详情</el-button>
              </el-empty>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 子功能模块 -->
      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="24">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>功能模块</span>
              </div>
            </template>
            <div class="modules-content">
              <p>包含日志审计、更新管理和备份恢复功能</p>
              <el-alert
                title="提示"
                type="info"
                description="请使用左侧菜单导航到具体的功能模块"
                show-icon
                :closable="false">
              </el-alert>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

// 页面状态
const loading = ref(false)

// 刷新页面数据
const handleRefresh = () => {
  ElMessage.success('刷新成功')
}

// 处理操作
const handleAction = () => {
  ElMessage.info('请使用左侧菜单导航到具体功能')
}

// 组件挂载
onMounted(() => {
  console.log('SystemMaintenance 页面已加载')
})
</script>

<style scoped>
.systemmaintenance-container {
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

.page-actions {
  display: flex;
  gap: 12px;
}

.page-content {
  min-height: 400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.overview-content,
.modules-content {
  padding: 20px 0;
}
</style>