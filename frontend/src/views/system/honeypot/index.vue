<template>
  <div class="honeypotcenter-container">
    <div class="page-header">
      <h1 class="page-title">蜜罐策略中心</h1>
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
                <span>蜜罐策略中心概览</span>
              </div>
            </template>
            <div class="overview-content">
              <el-empty description="蜜罐策略中心功能模块">
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
              <p>包含蜜罐探针管理和策略配置功能</p>
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
    
    <div class="content-wrapper">
      <router-view />
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
  console.log('HoneypotCenter 页面已加载')
})
</script>

<style scoped>
.honeypotcenter-container {
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